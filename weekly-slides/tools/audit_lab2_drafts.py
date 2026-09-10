"""Audit built drafts without treating layout/link checks as visual approval."""
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'weekly-slides/weekly-slides/LAB2_FPGA_0921'
OUT = ROOT / 'tmp/lab2-build'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def obj(value):
    return value.get_object() if hasattr(value, 'get_object') else value


def main():
    inventory = json.loads((BASE / 'series-inventory.json').read_text(encoding='utf-8'))
    builds = json.loads((OUT / 'build-results.json').read_text(encoding='utf-8'))
    stems = {row['file'] for row in inventory} | {'05.LAB2_00_START', '05.LAB2_00_CONTENTS'}
    assert len(stems) == 20 and {row['file'] for row in builds} == stems
    assert all(row['overfull'] == row['missing_characters'] == 0 for row in builds)
    readers = {stem + '.pdf': PdfReader(OUT / (stem + '.pdf')) for stem in stems}
    expected_pages = {row['file'] + '.pdf': row['pages'] for row in inventory}
    expected_notices = {row['file'] + '.pdf': row['missing_code_captures'] for row in inventory}
    results = []
    for name, reader in sorted(readers.items()):
        tex = (BASE / name).with_suffix('.tex')
        pdf = OUT / name
        assert pdf.stat().st_mtime >= tex.stat().st_mtime, (name, 'stale PDF')
        if name in expected_pages:
            assert len(reader.pages) == expected_pages[name], name
        assert reader.get_destination_page_number(reader.named_destinations['lab2-contents']) == 1
        internal = remote = notices = 0
        for number, page in enumerate(reader.pages, 1):
            assert abs(float(page.mediabox.width) / float(page.mediabox.height) - 4 / 3) < .001
            footer = 0
            for ref in obj(page.get('/Annots', [])):
                item = obj(ref)
                action = obj(item.get('/A', {}))
                target = action.get('/D') if action.get('/S') == '/GoTo' else item.get('/Dest')
                if isinstance(target, str):
                    assert target in reader.named_destinations, (name, number, target)
                    internal += 1
                    footer += target == 'lab2-contents'
                if action.get('/S') == '/GoToR':
                    file = obj(action['/F'])
                    if isinstance(file, dict):
                        file = file.get('/UF', file.get('/F'))
                    file = str(file)
                    assert file in readers, (name, number, file)
                    dest = obj(action['/D'])
                    if isinstance(dest, str):
                        assert dest in readers[file].named_destinations, (name, file, dest)
                    else:
                        assert isinstance(dest, list) and isinstance(dest[0], int), (name, dest)
                        assert 0 <= dest[0] < len(readers[file].pages), (name, file, dest)
                    remote += 1
            assert footer == 1, (name, number, 'contents footer')
            notices += '제작 중: 이 구간' in (page.extract_text() or '')
        assert notices == expected_notices.get(name, 0), (name, 'capture notice inventory mismatch')
        results.append(dict(file=name, pages=len(reader.pages), internal_links=internal,
                            relative_pdf_links=remote, draft_notice_pages=notices,
                            pdf_sha256=sha(pdf), tex_sha256=sha(tex)))
    captures = json.loads((BASE / 'required-code-captures.json').read_text(encoding='utf-8'))
    missing = []
    for row in captures:
        for source in row['sources']:
            assert sha(ROOT / source) == row['sha256'], source
        if not (BASE / row['image']).is_file():
            missing.append(row['image'])
    report = dict(status='DRAFT_STRUCTURE_PASS_NOT_RELEASE_APPROVAL',
                  gui_performed=False, all_pages_visually_reviewed=False,
                  missing_unique_images=len(missing), missing_images=missing,
                  pdfs=results)
    (BASE / 'draft-structure-validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(results)} drafts, {sum(x["pages"] for x in results)} pages; '
          f'links and geometry valid; {len(missing)} real captures missing')


if __name__ == '__main__':
    main()
