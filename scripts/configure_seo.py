#!/usr/bin/env python3
"""Configure production SEO URLs: python3 scripts/configure_seo.py https://your-domain.bg"""
import argparse
from copy import deepcopy
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "public"
LABELS = {
    "about": "За нас",
    "services": "Услуги",
    "gallery": "Галерия",
    "contact": "Контакти",
    "privacy": "Поверителност",
}
SCRIPT = re.compile(
    r'<script\b(?=[^>]*\btype=[\"\']application/ld\+json[\"\'])[^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


class HeadInfo(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.tags = []
        self.noindex = False
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs, self.get_starttag_text()))
        if tag == "meta" and attrs.get("name", "").lower() in ("robots", "googlebot"):
            directives = re.split(r"[,\s]+", attrs.get("content", "").lower())
            self.noindex |= "noindex" in directives or "none" in directives


def production_url(value):
    parts = urlsplit(value)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username is not None
        or parts.password is not None
        or parts.query
        or parts.fragment
        or parts.port not in (None, 443)
        or re.search(r'[\s<>"\'\\]', value)
        or any(segment in (".", "..") for segment in parts.path.split("/"))
    ):
        raise ValueError("Use the final HTTPS website URL without credentials, query parameters or a fragment.")
    host = parts.hostname.encode("idna").decode("ascii").lower()
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host):
        raise ValueError("The website hostname is invalid.")
    return urlunsplit(("https", host, parts.path.rstrip("/"), "", ""))


def business_data(homepage):
    for match in SCRIPT.finditer(homepage.split("</head>", 1)[0]):
        data = json.loads(match.group(1))
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for node in nodes:
            types = node.get("@type", [])
            if isinstance(types, str):
                types = [types]
            if "AutomotiveBusiness" in types or "LocalBusiness" in types:
                return deepcopy(node)
    raise ValueError("The homepage must contain the existing business JSON-LD.")


def configure(base_url, root=ROOT):
    root = Path(root)
    base_url = production_url(base_url)
    homepage = (root / "index.html").read_text(encoding="utf-8")
    business = business_data(homepage)
    business.update({
        "@id": f"{base_url}/#business",
        "alternateName": "ANEX",
        "url": base_url + "/",
        "image": f"{base_url}/assets/images/project-08.jpg",
    })
    business.pop("@context", None)
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    sitemap = ET.Element(f"{{{namespace}}}urlset")
    updates = []
    for path in sorted(root.glob("*.html")):
        content = path.read_text(encoding="utf-8")
        head, separator, body = content.partition("</head>")
        if not separator:
            raise ValueError(f"Missing </head> in {path.name}")
        info = HeadInfo(head)
        # Error pages and intentionally non-indexable pages must not enter the sitemap.
        if path.stem == "404" or info.noindex:
            continue
        url = base_url + "/" if path.stem == "index" else f"{base_url}/{path.stem}"
        for tag, attrs, markup in info.tags:
            generated = (
                tag == "link" and "canonical" in attrs.get("rel", "").split()
            ) or (
                tag == "meta" and attrs.get("property", "") in {
                    "og:url", "og:image", "og:image:width", "og:image:height",
                    "og:image:type", "og:image:alt",
                }
            )
            if generated:
                head = head.replace(markup, "")
        # The existing pages have one SEO JSON-LD block, replaced on repeat runs.
        head = SCRIPT.sub("", head)
        nodes = []
        if path.stem in ("index", "contact"):
            nodes.append(business)
        if path.stem in LABELS:
            nodes.append({
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Начало", "item": base_url + "/"},
                    {"@type": "ListItem", "position": 2, "name": LABELS[path.stem], "item": url},
                ],
            })
        schema = {"@context": "https://schema.org", "@graph": nodes}
        encoded_schema = json.dumps(schema, ensure_ascii=False, indent=2).replace("<", "\\u003c")
        tags = (
            f'    <link rel="canonical" href="{escape(url, quote=True)}" />\n'
            f'    <meta property="og:url" content="{escape(url, quote=True)}" />\n'
            f'    <meta property="og:image" content="{escape(business["image"], quote=True)}" />\n'
            '    <meta property="og:image:width" content="555" />\n'
            '    <meta property="og:image:height" content="415" />\n'
            '    <meta property="og:image:type" content="image/jpeg" />\n'
            '    <meta property="og:image:alt" content="Две автомобилни седалки с оранжева кожена тапицерия от архива на Анекс" />\n'
            f'    <script type="application/ld+json">\n{encoded_schema}\n    </script>\n'
        )
        head = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)*", "\n", head).rstrip()
        updates.append((path, head + "\n" + tags + "  </head>" + body))
        entry = ET.SubElement(sitemap, f"{{{namespace}}}url")
        ET.SubElement(entry, f"{{{namespace}}}loc").text = url
    # Validate every page before writing the public artifacts.
    for path, content in updates:
        path.write_text(content, encoding="utf-8")
    ET.indent(sitemap, space="  ")
    ET.ElementTree(sitemap).write(root / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (root / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n", encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="Final HTTPS production URL, including a subdirectory if needed")
    args = parser.parse_args()
    try:
        configure(args.base_url)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print("Canonical URLs, business and breadcrumb data, social previews, sitemap.xml and robots.txt are ready.")
