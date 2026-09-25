"""Contact's no-JS prototype keeps errors localized and submitted text inert."""
import unittest
from pathlib import Path

from serve import ROOT, contact_errors, contact_response


class ContactTests(unittest.TestCase):
    valid = {'name': 'Test Parent', 'email': 'parent@example.com',
             'phone': '+1 (224) 555-0123', 'message': 'A question about the trial.'}

    def test_field_validation(self):
        self.assertEqual(contact_errors(self.valid), set())
        self.assertEqual(contact_errors({}), {'name', 'email', 'message'})
        self.assertEqual(contact_errors(dict(self.valid, phone='')), set())
        invalid = dict(self.valid, email='parent@', phone='abc1234567890', message='   ')
        self.assertEqual(contact_errors(invalid), {'email', 'phone', 'message'})

    def test_localized_errors_and_retained_values(self):
        for locale in ('', 'ru', 'uk'):
            source = Path(ROOT, locale, 'contact', 'index.html').read_text(encoding='utf-8')
            result = contact_response(source, dict(self.valid, email='bad'))
            self.assertIn('id="contact-email-error">', result)
            self.assertIn('value="bad"', result)
            self.assertIn('value="Test Parent"', result)
            self.assertIn('id="contact-status" role="status" tabindex="-1" hidden', result)

    def test_submitted_html_is_escaped(self):
        source = Path(ROOT, 'contact/index.html').read_text(encoding='utf-8')
        result = contact_response(source, dict(self.valid, name='" onfocus="alert(1)',
                                              message='</textarea><script>alert(1)</script>'))
        self.assertNotIn('<script>alert(1)</script>', result)
        self.assertIn('&lt;/textarea&gt;&lt;script&gt;', result)
        self.assertIn('value="&quot; onfocus=&quot;alert(1)"', result)

    def test_success_shows_the_confirmation(self):
        source = Path(ROOT, 'contact/index.html').read_text(encoding='utf-8')
        result = contact_response(source, self.valid)
        self.assertIn('id="contact-status" role="status" tabindex="-1">', result)
        self.assertIn('Your message is in!', result)


if __name__ == '__main__':
    unittest.main()
