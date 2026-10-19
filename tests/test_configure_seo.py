"""Run with: python3 -m unittest discover -s tests -v"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

SPEC = importlib.util.spec_from_file_location(
    "configure_seo", Path(__file__).resolve().parents[1] / "scripts/configure_seo.py"
)
SEO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEO)


class ConfigureSEOTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        business = SEO.business_data((SEO.ROOT / "index.html").read_text())
        self.business = business
        for stem in ("index", *SEO.LABELS):
            schema = '<script type="application/ld+json">' + json.dumps(business) + '</script>' if stem == "index" else ""
            (self.root / f"{stem}.html").write_text(
                '<!doctype html><html lang="bg"><head><title>Анекс</title>'
                '<meta content="https://old.example.bg" property="og:url">'
                '<link href="https://old.example.bg" rel="canonical">'
                + schema + '</head><body><h1>Съществуващ текст.</h1></body></html>'
            )
        (self.root / "404.html").write_text(
            '<html><head><meta content="noindex, follow" name="robots"></head>'
            '<body>Грешка 404</body></html>'
        )

    def files(self):
        return {path.name: path.read_bytes() for path in self.root.iterdir()}

    def test_production_urls_and_original_business_details(self):
        SEO.configure("https://ANEX.example.bg/", self.root)
        sitemap = ET.parse(self.root / "sitemap.xml")
        urls = [item.text for item in sitemap.findall(".//{*}loc")]
        self.assertEqual(set(urls), {
            "https://anex.example.bg/", *(
                f"https://anex.example.bg/{stem}" for stem in SEO.LABELS
            )
        })
        for stem in ("index", *SEO.LABELS):
            markup = (self.root / f"{stem}.html").read_text()
            self.assertEqual(markup.count('rel="canonical"'), 1)
            self.assertEqual(markup.count('property="og:url"'), 1)
            self.assertNotIn("old.example.bg", markup)
            graph = json.loads(SEO.SCRIPT.search(markup).group(1))["@graph"]
            if stem in ("index", "contact"):
                business = next(node for node in graph if node.get("@type") == "AutomotiveBusiness")
                for key in ("name", "telephone", "email", "address", "foundingDate"):
                    self.assertEqual(business[key], self.business[key])
                self.assertEqual(business["@id"], "https://anex.example.bg/#business")
            if stem in SEO.LABELS:
                breadcrumb = next(node for node in graph if node["@type"] == "BreadcrumbList")
                self.assertEqual(breadcrumb["itemListElement"][1]["item"], f"https://anex.example.bg/{stem}")
        self.assertIn("Sitemap: https://anex.example.bg/sitemap.xml", (self.root / "robots.txt").read_text())

    def test_repeat_runs_domain_changes_and_body_preservation(self):
        bodies = {p.name: p.read_text().split("</head>", 1)[1] for p in self.root.glob("*.html")}
        SEO.configure("https://first.example.bg/subdirectory", self.root)
        first = self.files()
        SEO.configure("https://first.example.bg/subdirectory/", self.root)
        self.assertEqual(self.files(), first)
        SEO.configure("https://second.example.bg", self.root)
        for path in self.root.glob("*.html"):
            self.assertEqual(path.read_text().split("</head>", 1)[1], bodies[path.name])
            self.assertNotIn("first.example.bg", path.read_text())

    def test_noindex_pages_are_untouched_and_excluded(self):
        page = self.root / "private.html"
        page.write_text('<html><head><meta name="robots" content="noindex"></head><body>Текст</body></html>')
        original = page.read_bytes()
        error = (self.root / "404.html").read_bytes()
        SEO.configure("https://anex.example.bg", self.root)
        self.assertEqual(original, page.read_bytes())
        self.assertEqual(error, (self.root / "404.html").read_bytes())
        sitemap = (self.root / "sitemap.xml").read_text()
        self.assertNotIn("private", sitemap)
        self.assertNotIn("404", sitemap)

    def test_invalid_production_urls_do_not_modify_files(self):
        original = self.files()
        for url in (
            "example.bg", "http://example.bg", "https://user:pass@example.bg",
            "https://example.bg?test=1", "https://example.bg#fragment",
            "https://example.bg/../other", "https://example.bg:99999",
            "https://bad host.bg", "https://example.bg/\n",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                SEO.configure(url, self.root)
            self.assertEqual(original, self.files())

    def test_malformed_page_does_not_leave_partial_updates(self):
        (self.root / "z-broken.html").write_text("<html><head><title>Broken</title>")
        original = self.files()
        with self.assertRaisesRegex(ValueError, "Missing </head>"):
            SEO.configure("https://anex.example.bg", self.root)
        self.assertEqual(original, self.files())


if __name__ == "__main__":
    unittest.main()
