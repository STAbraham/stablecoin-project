import subprocess, os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".build/reference.docx")
os.makedirs(os.path.dirname(REF), exist_ok=True)
raw = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                     capture_output=True).stdout
open(REF, "wb").write(raw)

d = Document(REF)
NAVY = RGBColor(0x1F, 0x38, 0x50)

def strip_theme_fonts(style):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is not None:
        for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]

def set_font(name, family, size, bold=None, italic=None, color=None):
    try:
        st = d.styles[name]
    except KeyError:
        print("missing style:", name); return
    f = st.font
    if family: f.name = family
    if size: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    if color is not None: f.color.rgb = color
    strip_theme_fonts(st)

set_font('Normal',       'Arial', 11)
set_font('Title',        'Arial', 24, bold=True,  color=NAVY)
set_font('Subtitle',     'Arial', 13, bold=False, color=RGBColor(0x44,0x44,0x44))
set_font('Heading 1',    'Arial', 22, bold=True,  color=NAVY)
set_font('Heading 2',    'Arial', 16, bold=True,  color=NAVY)
set_font('Heading 3',    'Arial', 13, bold=True,  color=NAVY)
set_font('Heading 4',    'Arial', 11.5, bold=True, italic=False, color=NAVY)
set_font('Source Code',  'Consolas', 9)
set_font('Verbatim Char','Consolas', 9.5)

# keep heading spacing sensible: a bit of air above, little below
from docx.enum.style import WD_STYLE_TYPE
for nm, before, after in [('Heading 1', 18, 6), ('Heading 2', 14, 4), ('Heading 3', 10, 3), ('Heading 4', 8, 2)]:
    pf = d.styles[nm].paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)

d.save(REF)
print("wrote", REF, os.path.getsize(REF))
