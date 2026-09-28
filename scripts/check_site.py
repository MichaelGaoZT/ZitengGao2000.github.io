#!/usr/bin/env python3
"""Check local site links, anchor targets, and essential document metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / 'index.html', ROOT / 'cn/index.html', ROOT / 'hobbies/index.html']


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.ids = set()
        self.links = []
        self.errors = []
        self.h1_count = 0
        self.lang = None
        self.viewport = False
        self.feed(content)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f'Duplicate id: {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'meta' and attrs.get('name') == 'viewport':
            self.viewport = True
        if tag == 'img' and not attrs.get('alt'):
            self.errors.append('Image is missing descriptive alt text')
        for attr in ('href', 'src'):
            if attr in attrs:
                self.links.append(attrs[attr])


def main():
    errors = []
    documents = {p: Document(p.read_text(encoding='utf-8')) for p in PAGES}
    checked = 0
    for path, doc in documents.items():
        name = str(path.relative_to(ROOT))
        errors.extend(f'{name}: {e}' for e in doc.errors)
        if not doc.lang or not doc.viewport or doc.h1_count != 1:
            errors.append(f'{name}: expected language, viewport, and exactly one h1')
        if '{{' in path.read_text(encoding='utf-8'):
            errors.append(f'{name}: unresolved template placeholder')
        for link in doc.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith('/'):
                errors.append(f'{name}: root-relative URL breaks project Pages hosting: {link}')
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f'{name}: missing local target: {link}')
            elif parsed.fragment and target in documents and unquote(parsed.fragment) not in documents[target].ids:
                errors.append(f'{name}: missing anchor: {link}')
            checked += 1
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {len(PAGES)} pages and {checked} local links/assets: OK')


if __name__ == '__main__':
    main()
