"""Generator regression checks: python -m unittest discover -s tools -p 'test_*.py'."""
import contextlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urljoin

import i18n


class PageBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in [page + 'index.html' for page in i18n.PAGES] + ['site.js']:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text((Path(i18n.ROOT) / name).read_text(encoding='utf-8'), encoding='utf-8')
        self.root_patch = patch.object(i18n, 'ROOT', str(self.root))
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            i18n.main()

    def change_about(self, before, after):
        path = self.root / 'about/index.html'
        path.write_text(path.read_text(encoding='utf-8').replace(before, after), encoding='utf-8')

    def test_nested_pages_keep_language_routes_and_shared_assets(self):
        self.build()
        for lang in i18n.LANGS:
            html = (self.root / lang / 'about/index.html').read_text(encoding='utf-8')
            for reference in ('href="../#trial"', ('href="../parents/"' if 'parents/' in i18n.PAGES else 'href="../#parents"'),
                              'src="../site.js"', 'href="../../site.css"',
                              'href="../../about/"', f'href="{i18n.SITE}{lang}/about/"'):
                self.assertIn(reference, html)
            self.assertNotIn('id="trial-form"', html)
            self.assertIn('id="trial-form"', (self.root / lang / 'index.html').read_text(encoding='utf-8'))

    def test_all_five_menu_items_target_same_language_pages(self):
        self.build()
        for lang in i18n.LANGS:
            expected = [f'{i18n.SITE}{lang}/{path}' for path in
                        ('#home', 'about/', 'parents/', 'stretching/', 'contact/')]
            for page in i18n.PAGES:
                html = (self.root / lang / page / 'index.html').read_text(encoding='utf-8')
                header_nav = re.search(r'<nav id="navigation".*?</nav>', html, re.S).group()
                hrefs = re.findall(r'<a href="([^"]+)"', header_nav)[:5]
                base = f'{i18n.SITE}{lang}/{page}'
                self.assertEqual([urljoin(base, href) for href in hrefs], expected)
                self.assertEqual(header_nav.count('aria-current="page"'), 2)  # page + language
                for code in ('en', 'ru', 'uk'):
                    prefix = '' if code == 'en' else code + '/'
                    self.assertIn(f'hreflang="{code}" href="{i18n.SITE}{prefix}{page}"', html)

    def test_header_and_footer_drift_are_rejected(self):
        for before, after in (('aria-label="Menu"', 'aria-label="Different menu"'),
                              ('class="footer-contact"', 'class="different-footer"')):
            with self.subTest(before=before):
                self.change_about(before, after)
                with self.assertRaisesRegex(ValueError, 'shared (header|footer) differs'):
                    self.build()
                self.change_about(after, before)

    def test_contact_post_stays_on_current_locale_and_api_actions_stay_absolute(self):
        self.build()
        for lang in i18n.LANGS:
            html = (self.root / lang / 'contact/index.html').read_text(encoding='utf-8')
            action = re.search(r'<form id="contact-form"[^>]*action="([^"]+)"', html)[1]
            base = f'{i18n.SITE}{lang}/contact/'
            self.assertEqual(urljoin(base, action), base + '#contact-form')
            self.assertEqual(i18n.page_urls('<form action="/api/trial">', lang, 'contact/'),
                             '<form action="/api/trial">')

    def test_untranslated_copy_does_not_overwrite_generated_pages(self):
        self.build()
        target = self.root / 'ru/about/index.html'
        previous = target.read_bytes()
        self.change_about('</main>', '<p>Untranslated new paragraph</p></main>')
        with self.assertRaisesRegex(SystemExit, 'English left'):
            self.build()
        self.assertEqual(previous, target.read_bytes())

    def test_stale_rows_and_language_menu_drift_are_rejected(self):
        with patch.object(i18n, 'ABOUT_HTML', i18n.ABOUT_HTML + [('Removed copy', 'Текст', 'Текст')]):
            with self.assertRaisesRegex(SystemExit, 'source not found'):
                self.build()
        self.change_about('href="../ru/about/"', 'href="../ru/"')
        with self.assertRaises(AssertionError):
            self.build()

    def test_coach_json_is_checked_for_english(self):
        self.change_about('id="team-data">[]', 'id="team-data">[{"name":"Untranslated coach"}]')
        with self.assertRaisesRegex(SystemExit, 'Untranslated coach'):
            self.build()

    def test_coach_translation_uses_real_nonbreaking_spaces(self):
        self.change_about('id="team-data">[]', 'id="team-data">[{"bio":"Coaching biography"}]')
        row = ('Coaching biography', 'Биография~тренера', 'Біографія~тренера')
        with patch.object(i18n, 'ABOUT_HTML', i18n.ABOUT_HTML + [row]):
            self.build()
        html = (self.root / 'ru/about/index.html').read_text(encoding='utf-8')
        data = json.loads(re.search(r'id="team-data">(.*?)</script>', html).group(1))
        self.assertEqual(data[0]['bio'], 'Биография\u00a0тренера')


if __name__ == '__main__':
    unittest.main()
