"""Rasterize the supplied legacy teaching pages, retaining their original pixels/layout."""
from pathlib import Path
import hashlib
import json
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'weekly-slides/weekly-slides/LAB2_FPGA_0921'
OLD=ROOT/'legacy/교안 22년도'
SOURCES={
 '01_counter':('*5.1*.pdf',3,37),
 '02_clock_divider':('*5.1*.pdf',38,71),
 '03_register':('*6.2*.pdf',3,29),
 '04_shift_register':('*6.2*.pdf',30,62),
 '05_piso':('*6.2*.pdf',63,90),
 '06_moore':('*9.1*.pdf',3,15),
 '07_mealy':('*9.1*.pdf',16,29),
 '08_segment_scan':('*4.1*.pdf',115,151),
}

def main():
    records=[]
    for slug,(pattern,first,last) in SOURCES.items():
        sources=list(OLD.glob(pattern)); assert len(sources)==1
        source=sources[0]; digest=hashlib.sha256(source.read_bytes()).hexdigest()
        doc=pdfium.PdfDocument(source)
        folder=BASE/'assets'/('legacy-'+slug); folder.mkdir(parents=True,exist_ok=True)
        for number in range(first,last+1):
            image=folder/f'page-{number:03}.png'
            doc[number-1].render(scale=1.5).to_pil().save(image)
        records.append({'slug':slug,'source':source.relative_to(ROOT).as_posix(),'sha256':digest,
                        'pages':[first,last],'render_scale':1.5,'method':'PDFium rasterization; no added or altered source text'})
        doc.close()
    (BASE/'legacy-page-provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Rendered',sum(last-first+1 for _,first,last in SOURCES.values()),'original legacy pages')

if __name__=='__main__': main()
