# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])


def test_product_page_has_working_internal_navigation_and_matching_copy():
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = SiteLinks()
    parser.feed(page)

    assert all(link[1:] in parser.ids for link in parser.links if link.startswith("#"))
    assert (ROOT / "site" / "index.html").read_text(encoding="utf-8") == page
    assert "python -m pip install git+https://github.com/belentani7/xp.git" in page
    assert "Producto completo con hero shader" not in page


def test_static_page_describes_actual_features_and_accessibility():
    page = (ROOT / "index.html").read_text(encoding="utf-8")

    for text in ("xp install-hooks", "xp uninstall-hooks", "~/.xp/", "prefers-reduced-motion", "aria-live", "MIT"):
        assert text in page
