import sys, cairosvg, pypdfium2 as p
from pypdf import PdfWriter
d, sp = sys.argv[1], sys.argv[2]
fs=['trang1-mat-bang-tong-the.svg','trang2-chi-tiet-block-mat-cat.svg']
w=PdfWriter()
for i,f in enumerate(fs):
    cairosvg.svg2pdf(url=f'{d}/{f}', write_to=f'{sp}/p{i}.pdf'); w.append(f'{sp}/p{i}.pdf')
w.write(f'{d}/ban-ve-lang-mo-ho-vo-A3.pdf')
doc=p.PdfDocument(f'{d}/ban-ve-lang-mo-ho-vo-A3.pdf')
for i in range(2): doc[i].render(scale=200/72).to_pil().save(f'{d}/trang{i+1}.png')
