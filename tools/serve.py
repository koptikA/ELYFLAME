"""Local preview at http://127.0.0.1:4173/ that tells the browser never to cache, so edits to site.css and site.js
show on a normal reload.

    python tools/serve.py
"""
import functools
import http.server
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


http.server.ThreadingHTTPServer(('127.0.0.1', 4173), functools.partial(NoCache, directory=ROOT)).serve_forever()
