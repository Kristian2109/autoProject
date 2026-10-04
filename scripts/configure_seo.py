#!/usr/bin/env python3
"""Add deployment-specific URLs to the static site: python3 scripts/configure_seo.py https://your-domain.bg"""
import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def configure(base_url, root=ROOT):
    parts = urlsplit(base_url)
    if parts.scheme not in ('http', 'https') or not parts.hostname or parts.query or parts.fragment or parts.username or parts.password:
        raise ValueError('Use an http(s) website URL without credentials, query parameters or a fragment.')
    base_url = base_url.rstrip('/')
    namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', namespace)
    sitemap = ET.Element(f'{{{namespace}}}urlset')
    for path in sorted(root.glob('*.html')):
        url = f'{base_url}/' if path.name == 'index.html' else f'{base_url}/{path.name}'
        content = path.read_text(encoding='utf-8')
        # Replace previous generated URLs when running again or changing domain.
        content = re.sub(r'\s*<(?:link rel="canonical"|meta property="og:(?:url|image)")[^>]*>', '', content)
        tags = (
            f' <link rel="canonical" href="{escape(url, quote=True)}">\n'
            f' <meta property="og:url" content="{escape(url, quote=True)}">\n'
            f' <meta property="og:image" content="{escape(base_url, quote=True)}/assets/images/project-08.jpg">\n'
        )
        content = content.replace('</head>', tags + '</head>')
        if path.name == 'index.html':
            pattern = r'(<script type="application/ld\+json">)(.*?)(</script>)'
            def update_schema(match):
                schema = json.loads(match.group(2))
                schema['url'] = base_url + '/'
                schema['image'] = base_url + '/assets/images/project-08.jpg'
                return match.group(1) + json.dumps(schema, ensure_ascii=False) + match.group(3)
            content = re.sub(pattern, update_schema, content, flags=re.S)
        path.write_text(content, encoding='utf-8')
        entry = ET.SubElement(sitemap, f'{{{namespace}}}url')
        ET.SubElement(entry, f'{{{namespace}}}loc').text = url
    ET.indent(sitemap, space='  ')
    ET.ElementTree(sitemap).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (root / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base_url', help='Public website URL, including a subdirectory if needed')
    args = parser.parse_args()
    try:
        configure(args.base_url)
    except ValueError as error:
        parser.error(str(error))
    print('Canonical URLs, Open Graph URLs, sitemap.xml and robots.txt are ready.')
