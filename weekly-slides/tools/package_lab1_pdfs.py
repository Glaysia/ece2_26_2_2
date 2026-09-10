"""Validate relative PDF links and package the current LAB1 handouts."""
from pathlib import Path
import json
import re
import hashlib
import tempfile
from urllib.parse import unquote
import zipfile

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, DictionaryObject, NameObject, TextStringObject

SLIDES = Path(__file__).resolve().parents[1]
BASE = SLIDES / 'weekly-slides/LAB1_FPGA_0914'
ARCHIVE = BASE / '04.LAB1_0910_PDF.zip'
PACKAGE_ROOT = '04.LAB1_0910_PDF'
PDFS = ['04.LAB1_00_CONTENTS.pdf'] + ['04.LAB1_01_LOGIC_GATES_VIVADO.pdf'] + [p['file']+'.pdf' for p in json.loads((BASE/'series-inventory.json').read_text(encoding='utf-8'))] + ['01.vivado_2026_1_설치_매뉴얼.pdf','02.vscode_verilog_환경설정_매뉴얼.pdf']
PDFS[:23] = sorted(PDFS[:23], key=lambda name:(int(re.match(r'04\.LAB1_(\d+)',name)[1]), re.match(r'04\.LAB1_\d+([AB]?)_',name)[1]))
README = '''# LAB1 실습 자료 · 2026-09-10 작성

ZIP을 전부 푼 뒤 04.LAB1_00_CONTENTS.pdf를 여세요. 22개 실습 PDF와 설치·VS Code 보조 자료를 같은 폴더에 둡니다. 각 실습 좌하단 목차는 같은 PDF 2쪽으로 이동합니다. PDF 간 링크가 열리지 않는 뷰어에서는 해당 파일을 직접 여세요.

순서: 최신 Vivado 01–10 → 최신 통합 10A → CLI 통합 10B → 레거시 11–20. 모든 실습은 VS Code 사전 시뮬레이션과 실험 전 레포트부터 시작합니다. Vivado 과정은 GUI 메뉴로 진행합니다.

학생 템플릿: https://github.com/Glaysia/fpga-lab-template
검증 현황: https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/example/fpga_projects_hdl/LAB1/docs/validation.md

원본 레거시 이미지와 새 제작자의 실행 결과를 구분합니다. 실제 보드 기록·사진·영상은 아직 미수행이며 레포트 예시에도 그 상태를 명시했습니다. 새 PNG는 제작 PC의 빌드 자료이고 배포물에는 PDF를 넣습니다.
'''


def filename(spec):
    if hasattr(spec, 'get_object'):
        spec = spec.get_object()
    if isinstance(spec, dict):
        spec = spec.get('/UF', spec.get('/F', ''))
    return unquote(str(spec))


def normalize_unicode_file_specs(path):
    """XeTeX emits UTF-8 /F bytes; provide a Unicode /UF for PDF viewers."""
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    changed = False
    for page in writer.pages:
        for reference in page.get('/Annots', []):
            annotation = reference.get_object()
            action = annotation.get('/A')
            if not action:
                continue
            action = action.get_object()
            if action.get('/S') not in ('/GoToR', '/Launch'):
                continue
            spec = action.get('/F')
            if not isinstance(spec, TextStringObject):
                continue
            try:
                raw = spec.original_bytes
                decoded = raw.decode('utf-8')
            except Exception:
                # Unavailable original bytes or a non-UTF-8 file specification.
                continue
            if decoded == str(spec) or not (path.parent/decoded).is_file():
                continue
            action[NameObject('/F')] = DictionaryObject({
                NameObject('/Type'): NameObject('/Filespec'),
                NameObject('/F'): ByteStringObject(raw),
                NameObject('/UF'): TextStringObject(decoded),
            })
            changed = True
    if changed:
        with tempfile.NamedTemporaryFile(suffix='.pdf', dir=path.parent, delete=False) as temporary:
            temporary_path = Path(temporary.name)
            writer.write(temporary)
        temporary_path.replace(path)


def validate(folder):
    readers = {name: PdfReader(folder/name) for name in PDFS}
    stats = {'pdfs': {}, 'remote_links': 0, 'local_links': 0}
    for name, reader in readers.items():
        stats['pdfs'][name] = len(reader.pages)
        if name.startswith('04.'):
            box = reader.pages[0].mediabox
            assert abs(float(box.width)/float(box.height)-4/3) < .001
        for page_index, page in enumerate(reader.pages):
            if name.startswith('04.') and (page_index > 0 or 'LEGACY' in name):
                if name=='04.LAB1_00_CONTENTS.pdf':expected='lab1-contents'
                elif name=='04.LAB1_01_LOGIC_GATES_VIVADO.pdf':expected='modern01-contents'
                elif '_10A_' in name:expected='integrated-vivado-contents'
                elif '_10B_' in name:expected='integrated-cli-contents'
                else:
                    number=int(name.split('_')[1]);expected=('legacy-'+str(number-10).zfill(2) if 'LEGACY' in name else 'modern-'+str(number).zfill(2))+'-contents'
                footer = [ref.get_object() for ref in page.get('/Annots', [])
                          if float(ref.get_object().get('/Rect', [999,999])[0]) < 60
                          and float(ref.get_object().get('/Rect', [999,999])[1]) < 22]
                assert len(footer) == 1, (name, page_index, 'Missing/ambiguous contents button')
                action = footer[0]['/A'].get_object()
                assert action.get('/S') == '/GoTo' and action.get('/D') == expected, (name, page_index, action)
                assert reader.get_destination_page_number(reader.named_destinations[expected]) == 1
            for reference in page.get('/Annots', []):
                link = reference.get_object()
                if link.get('/Subtype') != '/Link':
                    continue
                action = link.get('/A')
                dest = link.get('/Dest')
                if action:
                    action = action.get_object()
                    kind = action.get('/S')
                    if kind == '/GoToR':
                        target = filename(action.get('/F'))
                        assert not Path(target).is_absolute(), (name, target)
                        assert (folder/target).is_file(), (name, target)
                        target_reader = readers.get(target) or PdfReader(folder/target)
                        destination = action.get('/D')
                        if isinstance(destination, str):
                            assert destination in target_reader.named_destinations, (name,target,destination)
                        else:
                            assert 0 <= int(destination[0]) < len(target_reader.pages)
                        stats['remote_links'] += 1
                    elif kind == '/Launch':
                        target = filename(action.get('/F'))
                        assert (folder/target).is_file(), (name,target)
                    elif kind == '/GoTo':
                        dest = action.get('/D')
                if isinstance(dest, str):
                    assert dest in reader.named_destinations, (name,dest)
                    stats['local_links'] += 1
    assert stats['remote_links'] >= 2, 'Expected links in both directions.'
    return stats


def main():
    for name in PDFS:
        normalize_unicode_file_specs(BASE/name)
    # Check the complete archive in an unrelated temporary extraction directory.
    with tempfile.TemporaryDirectory(prefix='lab1-pdf-package-') as staging:
        staging = Path(staging)
        package = staging/PACKAGE_ROOT
        package.mkdir()
        for name in PDFS:
            (package/name).write_bytes((BASE/name).read_bytes())
        (package/'README.md').write_text(README, encoding='utf-8')
        stats = validate(package)
        with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in [package/name for name in [*PDFS,'README.md']]:
                archive.write(path, f'{PACKAGE_ROOT}/{path.name}')
        extracted = staging/'extracted'
        with zipfile.ZipFile(ARCHIVE) as archive:
            assert archive.testzip() is None
            archive.extractall(extracted)
        assert validate(extracted/PACKAGE_ROOT) == stats
    manual_pages=sum(pages for name,pages in stats['pdfs'].items() if name.startswith('04.LAB1_') and name!='04.LAB1_00_CONTENTS.pdf')
    record={**stats,'archive':ARCHIVE.name,'bytes':ARCHIVE.stat().st_size,'sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),'checks':['4:3 manuals','all local contents to page 2','internal and relative PDF destinations','fresh ZIP extraction'],'visual_review':f'22 manuals ({manual_pages} pages); revised manuals fully rendered, unchanged page bodies matched against the prior reviewed PDFs and all distinct changed pages inspected. See code-page-validation.json. Previously reviewed first manual, contents and setup PDFs included unchanged.'}
    (BASE/'pdf-package-validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'archive':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,**stats},ensure_ascii=False))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
