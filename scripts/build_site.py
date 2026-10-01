"""Build static GitHub Pages files using Python's standard library only.

Edit content/*.html and data/site.json, then run: python scripts/build_site.py
Root HTML files are generated, remain committed, and need no server-side runtime.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from datetime import date
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = json.loads((ROOT / 'data/site.json').read_text(encoding='utf-8'))
PAGES = {
    'index': ('법학경시대회 공식 홈페이지', '제9회 법학경시대회 2026.09.21.–11.30. 접수·응시, 제2회 전국 자기주도 학습법 공모전 09.14.–09.26. 접수. 포스터와 참가 안내를 확인하세요.'),
    'about': ('대회 안내', '법학경시대회의 목적, 출범 배경, 주최와 시상 체계를 안내합니다.'),
    'guide': ('응시 안내', '참가 자격, 응시 절차, 준비물, 허용 자료와 시험 운영 규정을 안내합니다.'),
    'samples': ('예시 문제·자료', '헌법·민법의 출제 유형별 예시 4문항과 해설, 회차별 시행 자료를 확인하세요.'),
    'notice': ('공지사항', '제9회 법학경시대회 접수·응시 기간 2026.09.21.–11.30., 시험과 시상 안내, 공식 포스터 및 회차별 공지 기록입니다.'),
    'records': ('대회 기록', '제1회부터 제8회까지 시상식과 대상 수상 기록, 참가자 통계, 수상자 활동을 확인하세요.'),
    'universities': ('참가자·성적 통계', '회차별 대상 점수와 참가자의 소속·출신 학교를 소개합니다.'),
    'achievements': ('수상자 활동', '법학경시대회 수상자의 논문, 도서, 학습법 공모전과 연구 활동을 소개합니다.'),
    'voices': ('축하 메시지·참가 후기', '법조계·학계의 축하 메시지와 참가자의 대회 경험을 소개합니다.'),
    'media': ('언론보도', '법학경시대회에 관한 신문기사와 대학 공식 보도, 회차별 개최·시상 기록입니다.'),
    'faq': ('자주 묻는 질문', '제9회 일정, 참가 자격, 시험 방식, 오픈북 규정과 수상 후 활동에 관한 질문입니다.'),
    'contest': ('2026 제2회 전국 자기주도 학습법 공모전', '2026년 9월 26일 접수 마감. 제2회 공모전의 공고 기록과 제1회 수상작의 학습법·성과를 확인하세요.'),
    'contest-notice': ('자기주도 학습법 공모전 공고', '2026년 9월 26일 접수 마감. 제2회 공모전 당시 공고와 참고용 양식을 보관합니다.'),
    'contest-first': ('제1회 공모전 수상작', '자기주도 학습법 공모전 수상작의 학습 방법과 성과를 소개합니다.'),
    'contact': ('문의하기', '대회 운영, 참가 접수, 수상 기록과 개인정보 관련 전화·문자·이메일 문의 창구입니다.'),
    'privacy': ('개인정보처리방침', '대회 운영과 접수, 시험 감독, 시상 과정의 개인정보 처리 및 권리 행사 안내입니다.'),
    'terms': ('이용약관', '법학경시대회 홈페이지와 참가 접수, 응시 및 게시 자료 이용에 관한 약관입니다.'),
    '404': ('페이지를 찾을 수 없습니다', '요청한 페이지를 찾을 수 없습니다. 홈페이지나 공지사항으로 이동하세요.')
}
NAV = [('about','대회 안내'),('guide','응시 안내'),('samples','예시 문제·자료'),('notice','공지사항'),('records','대회 기록'),('contest','학습법 공모전'),('contact','문의')]
RECORD_PAGES = {'records','universities','achievements','voices','media'}

def e(value):
    return escape(str(value), quote=True)

def number(value):
    return '<span class="empty-value" aria-label="미공개">—</span>' if value is None else e(value)

def winners():
    cards = []
    for item in SITE['round8']['winners']:
        score = '' if item['score'] is None else f'<p class="score">총점 {e(item["score"])}점 / 100점</p>'
        cards.append(f'<article class="winner-card"><div class="award-title">{e(item["award"])} · {e(item["organization"])}</div><h3>{e(item["name"])}</h3><p>{e(item["affiliation"])}</p>{score}</article>')
    return '<div class="winner-grid">' + ''.join(cards) + '</div>'

def photo():
    item = SITE['round8']
    if not item['photo']:
        return '<figure class="ceremony-photo"><div class="photo-slot" role="img" aria-label="제8회 시상식 사진 미등록"></div><figcaption class="photo-caption">제8회 시상식 · 2026년 9월 12일</figcaption></figure>'
    path = item['photo'].lstrip('/')
    if not path.startswith('assets/images/') or not (ROOT / path).is_file():
        raise ValueError('round8.photo must identify an existing image under assets/images/')
    return f'<figure class="ceremony-photo" data-lightbox data-lb-title="제8회 법학경시대회 시상식"><img src="/{e(path)}" alt="{e(item["photo_alt"])}"><figcaption class="photo-caption">제8회 시상식 · 2026년 9월 12일</figcaption></figure>'

def rows():
    parts = []
    for round_no in range(8, 0, -1):
        if round_no == 8:
            items = SITE['round8']['winners']
            ceremony = SITE['round8']['ceremony_date']
            source = '<a class="text-link" href="/notice.html#notice-8">결과 공지</a>'
        else:
            items = [x for x in SITE['archive'] if x['round'] == round_no]
            ceremony = items[0]['ceremony']
            source = f'<a class="text-link" href="{e(items[0]["source"])}" target="_blank" rel="noopener noreferrer">기사 확인<span class="sr-only"> (새 창)</span></a>'
        group = []
        span = len(items)
        for index, item in enumerate(items):
            shared = '' if index else f'<th scope="rowgroup" rowspan="{span}" class="round-col">제{round_no}회</th><td rowspan="{span}" class="ceremony-col">{e(ceremony.replace("-", "."))}</td>'
            award = item.get('organization') or item.get('award', '').removeprefix('대상 · ')
            award_text = f'<br><small>{e(award)}</small>' if award else ''
            source_cell = '' if index else f'<td rowspan="{span}" class="source-col">{source}</td>'
            group.append(f'<tr>{shared}<td class="name-col">{e(item["name"])}{award_text}</td><td class="score-col">{number(item["score"])}</td>{source_cell}</tr>')
        parts.append('<tbody>'+''.join(group)+'</tbody>')
    return '<div class="table-scroll" tabindex="0" role="region" aria-label="회차별 대상 점수 표"><table class="data-table round-score-table"><thead><tr><th scope="col">회차</th><th scope="col">시상식</th><th scope="col">대상 수상자</th><th scope="col">점수</th><th scope="col">출처</th></tr></thead>'+''.join(parts)+'</table></div><p class="source-note">100점 만점 · — 미공개</p>'

def archives():
    parts = []
    photo_sizes = {1: (3751, 2813), 2: (748, 555), 3: (900, 516), 4: (900, 675), 5: (900, 675), 6: (900, 675), 7: (4032, 3024), 8: (1381, 758)}
    for round_no in range(8, 0, -1):
        if round_no == 8:
            info = SITE['round8']
            items = info['winners']
            ceremony = info['ceremony_date']
            image_path = info['photo']
            source = '/notice.html#notice-8'
            details = f'<p class="record-event-details">시상식: {e(info["ceremony_time"])} · {e(info["ceremony_place"])}<br>시험: {e(info["exam_date"].replace("-", "."))}</p>'
            links = '<a href="/notice.html#notice-8">제8회 결과 공지</a><a href="/media.html#round-8-news">제8회 시상식 보도</a><a href="/voices.html#reviews">참가 후기</a>'
        else:
            items = [x for x in SITE['archive'] if x['round'] == round_no]
            ceremony = items[0]['ceremony']
            image_path = f'photos/r{round_no}_group.jpg'
            source = items[0]['source']
            details = ''
            links = f'<a href="{e(source)}" target="_blank" rel="noopener noreferrer">시상식 보도 (새 창)</a><a href="/notice.html#notice-{round_no}">해당 회차 공지</a>'
        people = []
        for item in items:
            award = f'{item["award"]} · {item["organization"]}' if round_no == 8 else item.get('award', '대상')
            score = '' if item['score'] is None else f'<span class="record-winner-score">{e(item["score"])}점 / 100점</span>'
            people.append(f'<li><p class="record-award">{e(award)}</p><p class="record-winner-name"><strong>{e(item["name"])}</strong>{score}</p><p class="record-affiliation">{e(item["affiliation"])}</p></li>')
        picture = ''
        if image_path:
            if not (ROOT / image_path).is_file():
                raise ValueError(f'Missing ceremony photo: {image_path}')
            width, height = photo_sizes[round_no]
            picture = f'<figure class="record-photo" data-lightbox data-lb-title="제{round_no}회 법학경시대회 시상식" data-article="{e(source)}"><img src="/{e(image_path)}" alt="제{round_no}회 시상식 단체사진" width="{width}" height="{height}" loading="lazy" decoding="async"><figcaption>사진 크게 보기 <span aria-hidden="true">↗</span></figcaption></figure>'
        layout = 'record-layout' + ('' if picture else ' record-layout-text')
        parts.append(f'<article class="ceremony-record" id="round-{round_no}"><header class="record-heading"><h3>제{round_no}회 법학경시대회</h3><p>시상식 <time datetime="{e(ceremony)}">{e(ceremony.replace("-", "."))}</time></p></header><div class="{layout}">{picture}<div class="record-details">{details}<ul class="record-winners">'+''.join(people)+f'</ul><div class="record-links">{links}</div></div></div></article>')
    return ''.join(parts)

def notice_archives():
    parts = []
    for round_no in range(7,0,-1):
        items = [x for x in SITE['archive'] if x['round'] == round_no]
        first = items[0]
        parts.append(f'<article class="notice-entry" id="notice-{round_no}"><span class="status-chip">지난 대회</span><h2>제{round_no}회 법학경시대회 시상식 결과</h2><p class="meta">기사 게시일 {e(first["published"])}</p><p>제{round_no}회 시상식은 {e(first["ceremony"].replace("-","."))}에 열렸습니다.</p><ul>'+''.join(f'<li>{e(x.get("award","대상"))}: {e(x["name"])} · {e(x["affiliation"])}'+('' if x['score'] is None else f' · {x["score"]}점')+'</li>' for x in items)+f'</ul><div class="record-links"><a href="{e(first["source"])}" target="_blank" rel="noopener noreferrer">기사 원문 (새 창)</a><a href="/records.html#round-{round_no}">회차별 기록</a></div></article>')
    return ''.join(parts)

def publications():
    items=json.loads((ROOT/'data/publications.json').read_text(encoding='utf-8'))
    def cards(category):
        return ''.join(f'<article class="record-block"><span class="status-chip">{e(x["status"])}</span><h3>{e(x["title"])}</h3><p>{e(x["subtitle"])}</p><p><strong>{e(x["authors"])}</strong><br>{e(x["journal"])} {e(x["issue"])} · {e(x["date"])} · {e(x["pages"])}쪽</p><div class="record-links"><a href="{e(x["url"])}" target="_blank" rel="noopener noreferrer">KCI 논문 보기 (새 창)</a><a href="https://doi.org/{e(x["doi"])}" target="_blank" rel="noopener noreferrer">DOI 원문 연결 (새 창)</a></div></article>' for x in items if x['category']==category)
    count=sum(x['category'] in ('recipient','student_collaboration') for x in items)
    return f'<section class="content-section" id="papers"><div class="container"><h2>학생 공동연구·수상자 학술 논문 · {count}편</h2><p class="section-intro">김민규 변호사와 학생들의 공동연구 및 수상자의 학술 활동을 소개합니다. 저자와 학술지 정보는 각 논문의 KCI 기록에서 확인할 수 있습니다.</p>'+cards('student_collaboration')+cards('recipient')+'</div></section>'


def latest_publications():
    items=json.loads((ROOT/'data/publications.json').read_text(encoding='utf-8'))
    return '<div class="quick-grid publication-preview">'+''.join(f'<article class="quick-card"><span class="status-chip">{e(x["date"])} · 학술 논문</span><h3>{e(x["title"])}</h3><p>{e(x["subtitle"])}</p><p class="publication-byline">{e(x["authors"])}<br>{e(x["journal"])} · {e(x["issue"])}</p><a class="text-link" href="{e(x["url"])}" target="_blank" rel="noopener noreferrer">KCI 논문 보기 (새 창)</a></article>' for x in items if x['category']=='student_collaboration')+'</div>'


def latest_press():
    content=(ROOT/'content/media.html').read_text(encoding='utf-8')
    section=re.search(r'<section\b[^>]*id="recent-news".*?</section>', content, re.S)
    if not section:
        raise ValueError('Missing recent news section')
    cards=re.findall(r'<a\b[^>]*class="quick-card".*?</a>', section.group(), re.S)
    if not cards:
        raise ValueError('Missing recent press cards')
    return '<div class="quick-grid">'+''.join(cards)+'</div>'


def page_body(slug):
    """Reuse the maintained page content without its standalone page heading."""
    content=(ROOT/f'content/{slug}.html').read_text(encoding='utf-8')
    return re.sub(r'^\s*<section class="page-header">.*?</section>', '', content, count=1, flags=re.S)


def record_sections():
    groups=[('universities','participants','02','참가자·성적 통계'),
            ('achievements','activities','03','수상자 활동·학생 공동연구'),
            ('voices','voices','04','축하 메시지·참가 후기'),
            ('media','press','05','언론보도')]
    parts=[]
    for slug,anchor,number,title in groups:
        content=page_body(slug)
        if slug=='media':
            content=re.sub(r'id="round-(\d+)"', r'id="press-round-\1"', content)
            content=re.sub(r'href="#round-(\d+)"', r'href="#press-round-\1"', content)
        parts.append(f'<section class="records-group" id="{anchor}" aria-labelledby="{anchor}-title"><header class="record-section-heading"><div class="container"><span class="eyebrow">{number} / 대회 기록</span><h2 id="{anchor}-title">{title}</h2></div></header>'+content+'<div class="container section-return"><a href="#records-top">대회 기록 목차로 ↑</a></div></section>')
    return '\n'.join(parts)


def visible_disclosures(content):
    """Publish full answers as ordinary HTML, including when JavaScript is off."""
    def expand(match):
        attrs,body=match.groups()
        attrs=re.sub(r'\s+data-(?:open|close)-label="[^"]*"', '', attrs)
        attrs=re.sub(r'\s+open(?:="[^"]*")?', '', attrs)
        if 'class="' in attrs:
            attrs=attrs.replace('class="', 'class="expanded-content ', 1)
        else:
            attrs+=' class="expanded-content"'
        def heading(summary):
            label=re.sub(r'<[^>]+>', '', summary.group(1)).strip()
            label=re.sub(r'\s*[＋+]\s*$', '', label).strip()
            label=re.sub(r'\s+(?:보기|닫기)$', '', label)
            return '<h3 class="expanded-heading">'+label+'</h3>'
        body=re.sub(r'<summary\b[^>]*>(.*?)</summary>', heading, body, flags=re.S)
        return '<article'+attrs+'>'+body+'</article>'
    return re.sub(r'<details\b([^>]*)>(.*?)</details>', expand, content, flags=re.S)

class FAQParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.questions=[]; self.in_summary=False; self.in_detail=False; self.q=''; self.a=''
    def handle_starttag(self,tag,attrs):
        if tag=='details': self.in_detail=True; self.q=''; self.a=''
        if tag=='summary': self.in_summary=True
    def handle_endtag(self,tag):
        if tag=='summary': self.in_summary=False
        if tag=='details':
            self.questions.append({'@type':'Question','name':' '.join(self.q.split()),'acceptedAnswer':{'@type':'Answer','text':' '.join(self.a.split())}});self.in_detail=False
    def handle_data(self,data):
        if self.in_summary:self.q += data+' '
        elif self.in_detail:self.a += data+' '


def contest_notice():
    data=json.loads((ROOT/'data/contest_notice.json').read_text(encoding='utf-8'))
    def paragraph(text):
        if text.startswith('양식 받는 곳:'):
            return '<p><strong>양식 받는 곳:</strong> <a class="text-link" href="/index.html">lawtest.or.kr</a> → <a class="text-link" href="/contest.html">학습법 공모전</a> → <a class="text-link" href="/assets/downloads/2026-contest-application.hwpx" download>참가 양식 HWPX 다운로드</a></p>'
        return f'<p>{e(text)}</p>'
    return ''.join(f'<section class="contest-notice-section"><h2>{i}. {e(x["heading"])}</h2>'+''.join(paragraph(t) for t in x['paragraphs'])+'</section>' for i,x in enumerate(data['sections'],1))

def contest_entries():
    entries=json.loads((ROOT/'data/contest_entries.json').read_text(encoding='utf-8'))['entries']
    sections=[]
    for award,anchor in [('대상','grand'),('최우수상','excellence'),('우수상','merit')]:
        cards=[]
        for i,x in enumerate(entries,1):
            if x['award']!=award:continue
            cards.append(f'<article class="study-entry" id="{e(x["id"])}"><span class="study-number">{i:02}</span><h3>{e(x["title"])}</h3><h4>학습법</h4><ul>'+''.join(f'<li>{e(t)}</li>' for t in x['method'])+'</ul><div class="study-achievements"><h4>성과</h4><ul>'+''.join(f'<li>{e(t)}</li>' for t in x['achievements'])+'</ul></div></article>')
        sections.append(f'<section class="study-award-section" id="{anchor}"><h2>{award}</h2><div class="study-entry-grid">'+''.join(cards)+'</div></section>')
    return ''.join(sections)


def contest_banner(slug):
    return '<div class="notice-bar"><div class="container events-notice-bar current-event-only"><a href="/guide.html#application"><strong>제9회 법학경시대회</strong><span>09.21. – 11.30. 접수·응시</span><span aria-hidden="true">→</span></a></div></div>'

def floating_cta(slug):
    return '<a class="floating-apply" href="/guide.html#application">제9회 접수·응시 안내 <span aria-hidden="true">→</span></a>'

def main():
    layout=(ROOT/'templates/layout.html').read_text(encoding='utf-8')
    for slug,(title,description) in PAGES.items():
        content=(ROOT/f'content/{slug}.html').read_text(encoding='utf-8')
        content=content.replace('{{ record_sections }}',record_sections())
        if slug=='guide':
            faq=page_body('faq')
            faq=re.sub(r'id="([^"]+)"',r'id="faq-\1"',faq)
            content+='<section id="faq" class="guide-faq"><header class="record-section-heading"><div class="container"><h2>자주 묻는 질문</h2><p>접수부터 응시·시상까지, 질문과 답변을 한눈에 확인하세요.</p></div></header>'+faq+'</section>'
        replacements={'round8_winners':winners(),'round8_photo':photo(),'score_table':rows(),'archive_records':archives(),'archive_notices':notice_archives(),'publications':publications(),'latest_publications':latest_publications(),'latest_press':latest_press(),'updated':e(SITE['updated']),'contest_notice':contest_notice(),'contest_entries':contest_entries()}
        for key,val in replacements.items():content=content.replace('{{ '+key+' }}',val)
        if slug=='records':
            for source,anchor in [('records','photos'),('universities','participants'),('achievements','activities'),('voices','voices'),('media','press')]:
                content=content.replace(f'href="/{source}.html"',f'href="#{anchor}"')
                if source=='media':
                    content=re.sub(r'href="/media.html#round-(\d+)"',r'href="#press-round-\1"',content)
                content=content.replace(f'href="/{source}.html#','href="#')
        canonical='https://lawtest.or.kr/'+('' if slug=='index' else slug+'.html')
        active='records' if slug in RECORD_PAGES else ('guide' if slug=='faq' else ('contest' if slug.startswith('contest') else slug))
        navigation=''.join(f'<li><a href="/{key}.html"'+(' class="active" aria-current="'+('page' if slug==key else 'location')+'"' if key==active else '')+f'>{label}</a></li>' for key,label in NAV)
        schema={'@context':'https://schema.org','@type':'WebPage','name':title,'url':canonical,'description':description,'dateModified':SITE['updated'],'publisher':{'@type':'Organization','name':SITE['organizer'],'url':'https://lawtest.or.kr/'}}
        structured='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>'
        if slug=='faq':
            parser=FAQParser();parser.feed(content)
            structured+='\n<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':parser.questions},ensure_ascii=False)+'</script>'
        content=visible_disclosures(content)
        social_image = 'self-study-contest-2026-hwpx.png' if slug.startswith('contest') else 'round9-poster-20260920-100min.jpg'
        social_alt = '2026 제2회 전국 자기주도 학습법 공모전 포스터' if slug.startswith('contest') else '제9회 법학경시대회 포스터'
        values={'title':e(title),'description':e(description),'canonical':e(canonical),'content':content,'updated':e(SITE['updated']),'asset_version':e(SITE.get('asset_version',SITE['updated'])),'navigation':navigation,'structured_data':structured,'notice_banner':contest_banner(slug),'floating_cta':floating_cta(slug),'social_image':e(social_image),'social_alt':e(social_alt),'extra_head':'<meta name="robots" content="noindex, follow">' if slug=='404' else ''}
        output=layout
        for key,val in values.items():output=output.replace('{{ '+key+' }}',val)
        if re.search(r'\{\{\s*\w+\s*\}\}',output):raise ValueError(f'Unresolved template marker: {slug}')
        output = '\n'.join(line.rstrip() for line in output.splitlines()) + '\n'
        (ROOT/f'{slug}.html').write_text(output,encoding='utf-8',newline='\n')
    urls=''.join(f'<url><loc>https://lawtest.or.kr/{"" if slug=="index" else slug+".html"}</loc><lastmod>{SITE["updated"]}</lastmod></url>\n' for slug in PAGES if slug!='404')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n',encoding='utf-8')
    print(f'Built {len(PAGES)} static pages from shared layout and verified content.')

if __name__=='__main__':main()
