"""Static regression checks for generated pages, local links and shared navigation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
import re
import sys
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,html):
        super().__init__();self.ids=[];self.links=[];self.nav=[];self.nav_depth=0;self.headings=[];self.scripts=[];self.jsonld=False;self.script='';self.feed(html)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for attr in ('href','src','data-article'):
            if a.get(attr):self.links.append((tag,attr,a[attr]))
        if tag=='nav' and a.get('id')=='primary-nav':self.nav_depth=1
        elif tag=='nav' and self.nav_depth:self.nav_depth+=1
        if self.nav_depth and tag=='a':self.nav.append(a.get('href'))
        if tag=='h1':self.headings.append(tag)
        if tag=='script' and a.get('type')=='application/ld+json':self.jsonld=True;self.script=''
    def handle_endtag(self,tag):
        if tag=='nav' and self.nav_depth:self.nav_depth-=1
        if tag=='script' and self.jsonld:self.scripts.append(self.script);self.jsonld=False
    def handle_data(self,data):
        if self.jsonld:self.script+=data

def main():
    errors=[];pages={p:Page(p.read_text(encoding='utf-8')) for p in ROOT.glob('*.html') if not p.name.startswith('google')}
    expected=['/about.html','/guide.html','/samples.html','/notice.html','/records.html','/contest.html','/contact.html']
    checked=0
    for path,page in pages.items():
        html=path.read_text(encoding='utf-8')
        if page.nav!=expected:errors.append(f'{path.name}: inconsistent primary navigation')
        if len(page.headings)!=1:errors.append(f'{path.name}: expected one h1, found {len(page.headings)}')
        dup=[x for x,c in Counter(page.ids).items() if c>1]
        if dup:errors.append(f'{path.name}: duplicate IDs: {dup}')
        if '{{ ' in html:errors.append(f'{path.name}: unresolved template')
        for payload in page.scripts:
            try:json.loads(payload)
            except ValueError:errors.append(f'{path.name}: invalid JSON-LD')
        for tag,attr,url in page.links:
            parts=urlsplit(url)
            if parts.scheme or parts.netloc:continue
            target=(ROOT/unquote(parts.path.lstrip('/'))) if parts.path.startswith('/') else (path.parent/unquote(parts.path))
            if not parts.path:target=path
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(f'{path.name}: missing {url}');continue
            checked+=1
            if parts.fragment and target.suffix=='.html':
                other=pages.get(target) or Page(target.read_text(encoding='utf-8'))
                if unquote(parts.fragment) not in other.ids:errors.append(f'{path.name}: missing anchor {url}')
        if '접수는 <b>mylawtest.com</b>에서 진행 중' in html:errors.append(f'{path.name}: stale registration banner')
    for slug in ('index','about','records','notice'):
        html=(ROOT/f'{slug}.html').read_text(encoding='utf-8')
        if not all(x in html for x in ['정헌욱','김영진','69점 / 100점','67점 / 100점']):errors.append(f'{slug}: latest winner facts missing')
    if '공개를 원치 않음' in (ROOT/'voices.html').read_text(encoding='utf-8'):errors.append('voices: excluded response exposed')
    for file in ('index','records'):
        parsed=pages[ROOT/f'{file}.html']
        if any('/None' in url or '/null' in url for _,_,url in parsed.links):errors.append(f'{file}: unresolved image URL')
    entries=json.loads((ROOT/'data/contest_entries.json').read_text(encoding='utf-8'))['entries']
    public_text=json.dumps(entries,ensure_ascii=False)
    for entry in entries:
        if set(entry)!={'id','award','title','method','achievements'}:errors.append('contest entries: unexpected public fields')
        if entry['award'] not in ('대상','최우수상','우수상'):errors.append('contest entries: invalid award label')
        if entry['id'] not in pages[ROOT/'contest-first.html'].ids:errors.append('contest entries: missing published entry')
    if re.search(r'01[016789][\s–-]*\d{3,4}[\s–-]*\d{4}|[\w.+-]+@[\w.-]+',public_text):errors.append('contest entries: contact information detected')
    if any(word in public_text for word in ('생년월일','학번','주민등록','성명:')):errors.append('contest entries: identity field detected')
    for slug in ('contest','contest-notice'):
        if '자유 양식' in (ROOT/f'{slug}.html').read_text(encoding='utf-8'):errors.append(f'{slug}: outdated free-form submission rule')
    for filename in ('2026-contest-application.hwpx','2026-contest-notice.hwpx'):
        try:
            with ZipFile(ROOT/'assets/downloads'/filename) as doc:
                if doc.testzip() or 'Contents/section0.xml' not in doc.namelist():errors.append(f'{filename}: invalid HWPX')
        except Exception as exc:errors.append(f'{filename}: {exc}')
    print(f'Checked {len(pages)} pages, {checked} local references, shared menus, anchors, headings and JSON-LD.')
    if errors:
        print('\n'.join(errors));return 1
    print('PASS');return 0
if __name__=='__main__':sys.exit(main())
