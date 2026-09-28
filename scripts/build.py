#!/usr/bin/env python3
"""Render the small static site using only the Python standard library."""
import argparse
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = 'https://michaelgaozt.github.io/ZitengGao2000.github.io/'
PAGES = {
    'index': ('index.html', 'en', 'Ziteng Gao | 高紫腾',
              'Ziteng Gao is a Ph.D. student at HIT Shenzhen researching embodied AI, reinforcement learning, and autonomous driving.'),
    'cn': ('cn/index.html', 'zh-CN', '高紫腾 | Ziteng Gao',
           '高紫腾，哈尔滨工业大学（深圳）计算机科学博士生，研究方向为具身智能、强化学习与自动驾驶。'),
    'hobbies': ('hobbies/index.html', 'en', 'Beyond research | Ziteng Gao',
                'Badminton, friendship, and life beyond research with Ziteng Gao.'),
}


def render_all():
    layout = (ROOT / 'src/layout.html').read_text(encoding='utf-8')
    for key, (output, lang, title, description) in PAGES.items():
        root = './' if key == 'index' else '../'
        labels = ['About', 'Research', 'Experience', 'Hobbies', '中文']
        if lang == 'zh-CN':
            labels = ['首页', '研究', '经历', '爱好', '中文']
        targets = ['', '#research', '#experience', 'hobbies/', 'cn/']
        active = {'index': 0, 'hobbies': 3, 'cn': 4}[key]
        navigation = []
        for i, (label, target) in enumerate(zip(labels, targets)):
            current = ' aria-current="page"' if i == active else ''
            language = ' lang="zh-CN"' if i == 4 else ''
            navigation.append(f'<a href="{root}{target}"{current}{language}>{label}</a>')
        content = (ROOT / f'src/pages/{key}.html').read_text(encoding='utf-8')
        variables = {
            'lang': lang, 'title': escape(title), 'description': escape(description, quote=True),
            'canonical': SITE_URL + ('' if key == 'index' else key + '/'),
            'site_url': SITE_URL, 'root': root, 'navigation': '\n        '.join(navigation),
            'content': content.replace('{{root}}', root),
            'skip_label': '跳转到正文' if lang == 'zh-CN' else 'Skip to content',
            'nav_label': '主导航' if lang == 'zh-CN' else 'Main navigation',
            'menu_label': '菜单' if lang == 'zh-CN' else 'Menu',
            'language_alternates': (
                f'<link rel="alternate" hreflang="en" href="{SITE_URL}">\n'
                f'  <link rel="alternate" hreflang="zh-CN" href="{SITE_URL}cn/">'
            ) if key in ('index', 'cn') else '',
        }
        rendered = re.sub(r'\{\{(\w+)\}\}', lambda match: variables[match[1]], layout)
        yield output, rendered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail when committed HTML needs rebuilding')
    args = parser.parse_args()
    stale = []
    for output, content in render_all():
        path = ROOT / output
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(output)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            print(f'Built {output}')
    if stale:
        parser.exit(1, 'Run python3 scripts/build.py to update: ' + ', '.join(stale) + '\n')
    if args.check:
        print('All generated pages are up to date.')


if __name__ == '__main__':
    main()
