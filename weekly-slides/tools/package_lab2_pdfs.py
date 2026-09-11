"""Package reviewed LAB2 PDFs; refuse manuscripts with missing real code captures."""
from pathlib import Path
import hashlib
import json
import tempfile
import zipfile
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'weekly-slides/weekly-slides/LAB2_FPGA_0921'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect(folder,names):
    results=[]
    for name in names:
        reader=PdfReader(folder/name)
        home=reader.named_destinations.get('lab2-contents')
        assert home and reader.get_destination_page_number(home)==1,(name,'contents destination')
        internal=external=0
        for number,page in enumerate(reader.pages,1):
            assert abs(float(page.mediabox.width)/float(page.mediabox.height)-4/3)<0.001
            annotations=page.get('/Annots',[])
            if hasattr(annotations,'get_object'): annotations=annotations.get_object()
            footer=0
            for ref in annotations:
                item=ref.get_object(); action=item.get('/A',{})
                if hasattr(action,'get_object'): action=action.get_object()
                target=action.get('/D') if action.get('/S')=='/GoTo' else item.get('/Dest')
                if isinstance(target,str):
                    assert target in reader.named_destinations,(name,number,target)
                    internal+=1
                    if target=='lab2-contents': footer+=1
                if action.get('/S')=='/GoToR':
                    file=action['/F']
                    if hasattr(file,'get_object'): file=file.get_object()
                    if isinstance(file,dict): file=file.get('/UF',file.get('/F'))
                    assert str(file) in names,(name,number,file)
                    external+=1
                if action.get('/S')=='/URI' and str(action.get('/URI','')).lower().endswith('.pdf'):
                    uri=str(action['/URI'])
                    if not uri.startswith(('https://','http://')):
                        assert uri in names,(name,number,uri)
            assert footer==1,(name,number,'footer missing or duplicated')
            assert '제작 중: 이 구간' not in (page.extract_text() or '')
        results.append({'file':name,'pages':len(reader.pages),'internal_links':internal,'relative_pdf_links':external,'sha256':digest(folder/name)})
    return results

def main():
    inventory=json.loads((BASE/'series-inventory.json').read_text(encoding='utf-8'))
    assert len(inventory)==18
    missing=sum(x['missing_code_captures'] for x in inventory)
    if missing: raise RuntimeError(f'Not a release: {missing} code-image occurrences still need actual captures')
    captures=json.loads((BASE/'required-code-captures.json').read_text(encoding='utf-8'))
    for capture in captures:
        image=BASE/capture['image']
        proof=json.loads(image.with_suffix('.json').read_text(encoding='utf-8'))
        assert proof.get('actual_vscode_capture') is True,image
        assert proof.get('source_sha256')==capture['sha256'],image
        assert proof.get('lines')==capture['lines'],image
        assert proof.get('image_sha256')==digest(image),image
        for source in capture['sources']:
            assert digest(ROOT/source)==capture['sha256'],source
    names=[x['file']+'.pdf' for x in inventory]+['05.LAB2_00_START.pdf','05.LAB2_00_CONTENTS.pdf']
    assert len(set(names))==20
    reviews=json.loads((BASE/'final-visual-review.json').read_text(encoding='utf-8'))
    for name in names:
        proof=reviews[name]
        assert proof['all_pages_visually_reviewed'] is True and proof['pdf_sha256']==digest(BASE/name),name
        assert proof['tex_sha256']==digest((BASE/name).with_suffix('.tex')),name
    results=inspect(BASE,names)
    target=BASE/'05.LAB2_0910_PDF.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names: archive.write(BASE/name,arcname=name)
    with tempfile.TemporaryDirectory(prefix='lab2-pdf-unzip-') as temporary:
        with zipfile.ZipFile(target) as archive:
            assert set(archive.namelist())==set(names)
            archive.extractall(temporary)
        assert inspect(Path(temporary),names)==results
    (BASE/'pdf-package-validation.json').write_text(json.dumps({'status':'PASS','zip':target.name,
        'zip_sha256':digest(target),'pdfs':results,'fresh_extraction_checked':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)

if __name__=='__main__': main()
