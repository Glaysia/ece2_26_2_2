"""Validate relative PDF links and package the current LAB1 handouts."""
from pathlib import Path
import json
import tempfile
from urllib.parse import unquote
import zipfile

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, DictionaryObject, NameObject, TextStringObject

SLIDES = Path(__file__).resolve().parents[1]
BASE = SLIDES / 'weekly-slides/LAB1_FPGA_0914'
ARCHIVE = BASE / '04.LAB1_0910_PDF.zip'
PACKAGE_ROOT = '04.LAB1_0910_PDF'
PDFS = [
    '04.LAB1_00_CONTENTS.pdf',
    '04.LAB1_01_LOGIC_GATES_LEGACY.pdf',
    '01.vivado_2026_1_설치_매뉴얼.pdf',
    '02.vscode_verilog_환경설정_매뉴얼.pdf',
]

README = '''# LAB1 실습 자료 — 2026-09-10 작성

## 열기

1. ZIP 전체를 압축 해제합니다.
2. `04.LAB1_00_CONTENTS.pdf`를 먼저 엽니다.
3. 논리 게이트 또는 레거시 실습 링크를 누르면 실습 01 PDF로 이동합니다.
4. 각 PDF 좌하단의 ‘목차’를 누르면 같은 PDF의 목차로 돌아갑니다. 레거시 01의 실습 목차는 2쪽입니다.
5. ‘전체 목차 PDF’는 별도 파일로 이동하는 링크입니다. 외부 링크를 지원하지 않는 뷰어에서는 같은 폴더의 파일을 직접 여세요.

PDF를 같은 폴더에 두고 파일명을 유지하세요. 외부 PDF 링크의 동작은 뷰어에 따라 다릅니다. 데스크톱 Acrobat Reader에서 열어 사용하고, 링크가 동작하지 않는 뷰어에서는 아래 파일을 직접 여세요.

## 포함 자료

- [목차·공통 안내](04.LAB1_00_CONTENTS.pdf): 5쪽
- [01 AND·OR·XOR — 레거시 Vivado](04.LAB1_01_LOGIC_GATES_LEGACY.pdf): 69쪽
- [Vivado 2026.1 설치](01.vivado_2026_1_설치_매뉴얼.pdf): 기존 보조 자료
- [VS Code Verilog 환경설정](02.vscode_verilog_환경설정_매뉴얼.pdf): 기존 보조 자료

이 묶음에는 현재 작성된 레거시 01만 포함됩니다. 나머지 회로·최신 Vivado·통합 프로젝트·CLI 자료는 이후 추가합니다. VS Code 사전 시뮬레이션을 실험 전 레포트에 자세히 기록하고, Vivado 시뮬레이션·실제 보드 기록·사진·영상·GitHub 자료를 실험 후 레포트에 정리합니다.

## 원자료와 검증 범위

레거시 01은 서울시립대학교 박동욱 교수의 「논리 게이트 구현」 PDF p.3–52를 재구성했습니다. 원본 문구와 GUI·코드 이미지를 보존하고 긴 설명과 복수 이미지를 나누었습니다. 원본의 `LVCMOSS33` 표기는 별도 보충 페이지에서 `LVCMOS33`으로 설명합니다.

원본 화면은 이번 제작 과정에서 새로 실행한 Vivado·보드 검증 증빙이 아닙니다. PDF는 제작 PC에서 빌드했으며 이 ZIP은 PDF 열람용입니다. TeX·PNG는 포함하지 않습니다.

PDF 간 링크 안내: https://helpx.adobe.com/acrobat/using/links-attachments-pdfs.html
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
                expected = 'legacy-01-contents' if 'LEGACY' in name else 'lab1-contents'
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
            for path in sorted(package.iterdir()):
                archive.write(path, f'{PACKAGE_ROOT}/{path.name}')
        extracted = staging/'extracted'
        with zipfile.ZipFile(ARCHIVE) as archive:
            assert archive.testzip() is None
            archive.extractall(extracted)
        assert validate(extracted/PACKAGE_ROOT) == stats
    print(json.dumps({'archive':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,**stats},ensure_ascii=False))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
