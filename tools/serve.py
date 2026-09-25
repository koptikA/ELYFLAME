"""Local preview at http://127.0.0.1:4173/ that tells the browser never to cache, so edits to site.css and site.js
show on a normal reload.

    python tools/serve.py
"""
import functools
import http.server
import os
import html
import re
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def contact_errors(values):
    """The local prototype validates only: no storage or message delivery."""
    limits = {'name': 100, 'email': 254, 'phone': 40, 'message': 5000}
    errors = {key for key, limit in limits.items()
              if not values.get(key, '').strip() or len(values.get(key, '').strip()) > limit}
    email = values.get('email', '').strip()
    phone = values.get('phone', '').strip()
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
        errors.add('email')
    if not re.fullmatch(r'[+\d\s().-]+', phone) or not 10 <= len(re.sub(r'\D', '', phone)) <= 15:
        errors.add('phone')
    return errors


def contact_response(source, values):
    errors = contact_errors(values)
    for key in ('name', 'email', 'phone', 'message'):
        field_id = f'contact-{key}'
        source = re.sub(rf'(<(?:input|textarea) id="{field_id}"[^>]*)(>)',
                        lambda m: m[1] + f' aria-invalid="{str(key in errors).lower()}"'
                        + (f' value="{html.escape(values.get(key, ""), quote=True)}"' if key != 'message' else '')
                        + m[2], source)
        if key == 'message':
            source = re.sub(r'(<textarea id="contact-message"[^>]*>).*?(</textarea>)',
                            lambda m: m[1] + html.escape(values.get(key, '')) + m[2], source, flags=re.S)
        if key in errors:
            source = source.replace(f'id="{field_id}-error" hidden', f'id="{field_id}-error"')
    if not errors:
        source = source.replace('id="contact-status" role="status" tabindex="-1" hidden',
                                'id="contact-status" role="status" tabindex="-1"')
    return source


class NoCache(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        path = urlsplit(self.path).path
        if path != '/api/contact':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            self.send_error(400)
            return
        if not 0 <= length <= 65536:
            self.send_error(413)
            return
        if self.headers.get_content_type() != 'application/x-www-form-urlencoded':
            self.send_error(415)
            return
        fields = parse_qs(self.rfile.read(length).decode('utf-8', errors='replace'), keep_blank_values=True)
        values = {key: fields.get(key, [''])[0] for key in ('name', 'email', 'phone', 'message')}
        language = fields.get('language', ['en'])[0]
        page_path = f'/{language}/contact/' if language in ('ru', 'uk') else '/contact/'
        if 'application/json' in self.headers.get('Accept', ''):
            body = json.dumps({'errors': sorted(contact_errors(values)), 'prototype': True}).encode('utf-8')
            content_type = 'application/json; charset=utf-8'
        else:
            source = Path(ROOT, page_path.lstrip('/'), 'index.html').read_text(encoding='utf-8')
            source = source.replace('<head>', f'<head>\n  <base href="{page_path}">', 1)
            body = contact_response(source, values).encode('utf-8')
            content_type = 'text/html; charset=utf-8'
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    http.server.ThreadingHTTPServer(('127.0.0.1', 4173), functools.partial(NoCache, directory=ROOT)).serve_forever()
