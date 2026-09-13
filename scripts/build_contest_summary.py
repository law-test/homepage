"""Build the printable public summary from the website's anonymous entries."""
from pathlib import Path
import json
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets/downloads/self-study-2025-summary.pdf'
FONT_DIR = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Malgun', str(FONT_DIR / 'malgun.ttf')))
pdfmetrics.registerFont(TTFont('MalgunBold', str(FONT_DIR / 'malgunbd.ttf')))
NAVY = colors.HexColor('#143d65')
INK = colors.HexColor('#24384b')
MUTED = colors.HexColor('#60758a')
styles = {
    'title': ParagraphStyle('EntryTitle', fontName='MalgunBold', fontSize=14,
                            leading=21, textColor=NAVY, wordWrap='CJK'),
    'label': ParagraphStyle('Label', fontName='MalgunBold', fontSize=9.5,
                            leading=15, textColor=NAVY, wordWrap='CJK'),
    'body': ParagraphStyle('Body', fontName='Malgun', fontSize=10.5,
                           leading=17, textColor=INK, wordWrap='CJK'),
}


def entry_flowables(entry):
    result = [Paragraph(escape(entry['title']), styles['title']), Spacer(1, 10),
              Paragraph('학습법', styles['label']), Spacer(1, 4)]
    for index, text in enumerate(entry['method'], 1):
        result.extend([Paragraph(f'{index}. {escape(text)}', styles['body']), Spacer(1, 4)])
    result.extend([Spacer(1, 3), Paragraph('성과', styles['label']), Spacer(1, 4)])
    for text in entry['achievements']:
        result.extend([Paragraph(escape(text), styles['body']), Spacer(1, 3)])
    return result


def main():
    data = json.loads((ROOT / 'data/contest_entries.json').read_text(encoding='utf-8'))
    entries = data['entries']
    width, height = A4
    margin, padding = 42, 18
    card_width, card_height = width - 2 * margin, 327
    text_width = card_width - 2 * padding
    document = canvas.Canvas(str(OUTPUT), pagesize=A4)
    document.setTitle(data['title'])
    document.setAuthor('선율 법학경시대회 위원회')
    document.setSubject('제1회 공모전 수상작의 학습법과 성과')
    page_count = (len(entries) + 1) // 2
    for page in range(page_count):
        document.setFillColor(NAVY)
        document.setFont('MalgunBold', 18)
        document.drawString(margin, height - 49, '제1회 자기주도 학습법 공모전')
        document.setFillColor(MUTED)
        document.setFont('Malgun', 10)
        document.drawString(margin, height - 70, '수상작 요약  |  학습법과 성과')
        for slot, entry in enumerate(entries[page * 2:page * 2 + 2]):
            top = height - 91 - slot * (card_height + 15)
            document.setFillColor(colors.HexColor('#f5f8fc'))
            document.setStrokeColor(colors.HexColor('#dae3ed'))
            document.roundRect(margin, top - card_height, card_width, card_height,
                               8, stroke=1, fill=1)
            document.setFillColor(NAVY)
            document.setFont('MalgunBold', 10)
            document.drawString(margin + padding, top - 24,
                                f'{page * 2 + slot + 1:02}  {entry["award"]}')
            position = top - 37
            for flowable in entry_flowables(entry):
                _, flow_height = flowable.wrap(text_width, card_height)
                position -= flow_height
                if position < top - card_height + 12:
                    raise ValueError(f'Entry exceeds its page area: {entry["id"]}')
                flowable.drawOn(document, margin + padding, position)
        document.setStrokeColor(colors.HexColor('#d3dce6'))
        document.line(margin, 49, width - margin, 49)
        document.setFillColor(MUTED)
        document.setFont('Malgun', 8)
        document.drawString(margin, 32, '선율 법학경시대회 위원회  |  lawtest.or.kr')
        document.drawRightString(width - margin, 32, f'{page + 1} / {page_count}')
        document.showPage()
    document.save()
    print(f'Built {OUTPUT.name}: {page_count} pages, {len(entries)} entries')


if __name__ == '__main__':
    main()
