from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape

OUT = Path(__file__).resolve().parent
NAME = '图1.2代表性交互式数学教学方法分类-配色统一版'
W, H = 1280, 790
NAVY = '#112642'
PALE_BLUE, BLUE = '#CFE7FC', '#1595E5'
PALE_GREEN, GREEN = '#C7F0E9', '#10AF9E'
PALE_ORANGE, ORANGE = '#FFE6D1', '#FF893C'

# Text and classification follow the user's current edited diagram.
nodes = [
    ('root', 28, 341, 240, 106, ['交互式数学', '教学方法'], '#CDE8F5', '#94B3C6', 'root'),
    ('demo', 375, 126, 230, 80, ['示范学习'], PALE_BLUE, BLUE, 'category'),
    ('control', 375, 354, 230, 80, ['流程控制'], PALE_GREEN, GREEN, 'category'),
    ('feedback', 375, 582, 230, 80, ['交互反馈优化'], PALE_ORANGE, ORANGE, 'category'),
    ('mathdial', 725, 35, 510, 118, ['MathDial', '人类教师示范', '监督微调'], PALE_BLUE, BLUE, 'method'),
    ('socratic', 725, 179, 510, 118, ['SocraticLM', '多智能体生成教学示范', '教学能力微调'], PALE_BLUE, BLUE, 'method'),
    ('stratl', 725, 335, 510, 118, ['StratL', '识别学生状态', '控制教学意图与提示'], PALE_GREEN, GREEN, 'method'),
    ('pedagogical', 725, 491, 510, 118, ['PedagogicalRL', '多轮 GRPO', '终局解题与教学评价'], PALE_ORANGE, ORANGE, 'method'),
    ('mhpo', 725, 635, 510, 118, ['MHPO', '迭代 DPO', '单轮教学评价＋长程收益'], PALE_ORANGE, ORANGE, 'method'),
]
node_map = {n[0]: n for n in nodes}
edges = [
    ('root', 'demo', '#9AAABB', [(320, 394), (320, 166)]),
    ('root', 'control', '#9AAABB', []),
    ('root', 'feedback', '#9AAABB', [(320, 394), (320, 622)]),
    ('demo', 'mathdial', BLUE, [(665, 166), (665, 94)]),
    ('demo', 'socratic', BLUE, [(665, 166), (665, 238)]),
    ('control', 'stratl', GREEN, []),
    ('feedback', 'pedagogical', ORANGE, [(665, 622), (665, 550)]),
    ('feedback', 'mhpo', ORANGE, [(665, 622), (665, 694)]),
]

mxfile = ET.Element('mxfile', host='app.diagrams.net', version='29.0.3')
diagram = ET.SubElement(mxfile, 'diagram', name='代表性交互式数学教学方法分类', id='teaching-methods-color')
model = ET.SubElement(diagram, 'mxGraphModel', dx=str(W), dy=str(H), grid='1', gridSize='10', guides='1',
                      tooltips='1', connect='1', arrows='1', fold='1', page='1', pageScale='1',
                      pageWidth=str(W), pageHeight=str(H), math='0', shadow='0', background='#FFFFFF')
root = ET.SubElement(model, 'root')
ET.SubElement(root, 'mxCell', id='0')
ET.SubElement(root, 'mxCell', id='1', parent='0')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">代表性交互式数学教学方法分类</title>',
       '<desc id="desc">交互式数学教学方法分为示范学习、流程控制和交互反馈优化，分别采用浅蓝、青绿和浅橙配色。</desc>',
       '<defs><linearGradient id="rootFill" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#CFE7FC"/><stop offset="1" stop-color="#C7F0E9"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']

for i, (source, target, color, waypoints) in enumerate(edges):
    cell = ET.SubElement(root, 'mxCell', id=f'edge-{i}', value='', source=source, target=target, edge='1', parent='1',
        style=f'edgeStyle=orthogonalEdgeStyle;rounded=1;arcSize=12;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor={color};strokeWidth=2.4;exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
    geo = ET.SubElement(cell, 'mxGeometry', relative='1', **{'as': 'geometry'})
    if waypoints:
        arr = ET.SubElement(geo, 'Array', **{'as': 'points'})
        for x, y in waypoints:
            ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))

# Render shared tree trunks once to avoid overlapping strokes in the preview.
paths = [
    ('M 268 394 H 320 M 320 166 V 622 M 320 166 H 375 M 320 394 H 375 M 320 622 H 375', '#9AAABB'),
    ('M 605 166 H 665 M 665 94 V 238 M 665 94 H 725 M 665 238 H 725', BLUE),
    ('M 605 394 H 725', GREEN),
    ('M 605 622 H 665 M 665 550 V 694 M 665 550 H 725 M 665 694 H 725', ORANGE),
]
for d, color in paths:
    svg.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')

for ident, x, y, w, h, lines, fill, stroke, kind in nodes:
    if kind == 'method':
        value = '<div style="font-size:28px;font-weight:bold;line-height:1.2">' + escape(lines[0]) + '</div>'
        value += '<div style="font-size:23px;line-height:1.35">' + '<br>'.join(escape(s) for s in lines[1:]) + '</div>'
        font_size, font_style = 23, 0
    else:
        value = '<br>'.join(lines)
        font_size, font_style = 27, 1
    gradient = f'gradientColor={PALE_GREEN};gradientDirection=east;' if kind == 'root' else ''
    cell = ET.SubElement(root, 'mxCell', id=ident, value=value, vertex='1', parent='1',
        style=f'rounded=1;absoluteArcSize=1;arcSize=20;whiteSpace=wrap;html=1;fillColor={fill};{gradient}strokeColor={stroke};strokeWidth=2.2;fontFamily=Arial,PingFang SC,Hiragino Sans GB;fontSize={font_size};fontStyle={font_style};fontColor={NAVY};align=center;verticalAlign=middle;spacing=8;shadow=0;')
    ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
    svg_fill = 'url(#rootFill)' if kind == 'root' else fill
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{svg_fill}" stroke="{stroke}" stroke-width="2.2"/>')
    cx, cy = x+w/2, y+h/2
    if kind == 'method':
        label_specs = [(lines[0], 28, 700, cy-30), (lines[1], 23, 400, cy+3), (lines[2], 23, 400, cy+34)]
    elif len(lines) == 2:
        label_specs = [(lines[0], 27, 700, cy-17), (lines[1], 27, 700, cy+20)]
    else:
        label_specs = [(lines[0], 27, 700, cy+2)]
    for txt, size, weight, ty in label_specs:
        svg.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" dominant-baseline="middle" font-family="Arial, PingFang SC, Hiragino Sans GB, sans-serif" font-size="{size}" font-weight="{weight}" fill="{NAVY}">{escape(txt)}</text>')

svg.append('</svg>')
ET.indent(mxfile, space='  ')
ET.ElementTree(mxfile).write(OUT / f'{NAME}.drawio', encoding='utf-8', xml_declaration=True)
(OUT / f'{NAME}.svg').write_text('\n'.join(svg), encoding='utf-8')
print(OUT / f'{NAME}.drawio')
print(OUT / f'{NAME}.svg')
