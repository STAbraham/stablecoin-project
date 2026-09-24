# Post-pandoc polish: direct formatting that survives both Word and Google Docs import
# (table borders + header shading, code-block boxes, title rule). Called by build_docx.py.
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BORDER = 'C9CFDA'   # light blue-gray lines
HEADER = 'EEF2F8'   # header-row fill
CODEBG = 'F4F5F7'   # code-block fill
NAVY   = '1F3850'


def _edge(tag, sz='4', color=BORDER):
    el = OxmlElement(tag)
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '0')
    el.set(qn('w:color'), color)
    return el


def _insert_in_tblPr(tblPr, el):
    # keep schema order: borders/cellMar must precede tblLook
    look = tblPr.find(qn('w:tblLook'))
    if look is not None:
        look.addprevious(el)
    else:
        tblPr.append(el)


def polish(doc):
    for tbl in doc.tables:
        tblPr = tbl._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for e in ('w:top', 'w:left', 'w:bottom', 'w:right', 'w:insideH', 'w:insideV'):
            borders.append(_edge(e))
        _insert_in_tblPr(tblPr, borders)
        mar = OxmlElement('w:tblCellMar')
        for tag, w in (('w:top', '50'), ('w:left', '90'), ('w:bottom', '50'), ('w:right', '90')):
            m = OxmlElement(tag)
            m.set(qn('w:w'), w)
            m.set(qn('w:type'), 'dxa')
            mar.append(m)
        _insert_in_tblPr(tblPr, mar)
        if tbl.rows:
            for cell in tbl.rows[0].cells:
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), HEADER)
                tcPr.append(shd)

    for para in doc.paragraphs:
        name = para.style.name
        if name == 'Source Code':
            pPr = para._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            for e in ('w:top', 'w:left', 'w:bottom', 'w:right'):
                pBdr.append(_edge(e, sz='4', color='D8DCE4'))
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), CODEBG)
            style = pPr.find(qn('w:pStyle'))
            anchor = style if style is not None else None
            if anchor is not None:
                anchor.addnext(shd)   # order ends up pStyle, pBdr, shd
                anchor.addnext(pBdr)
            else:
                pPr.insert(0, shd)
                pPr.insert(0, pBdr)
        elif name == 'Heading 1':
            pPr = para._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            bottom = _edge('w:bottom', sz='6', color=NAVY)
            bottom.set(qn('w:space'), '6')
            pBdr.append(bottom)
            style = pPr.find(qn('w:pStyle'))
            if style is not None:
                style.addnext(pBdr)
            else:
                pPr.insert(0, pBdr)
    return doc
