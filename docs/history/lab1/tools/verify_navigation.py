"""Check LAB1 local Markdown targets, section anchors and course navigation order.

Literal examples inside code blocks are excluded. Remote URLs are inventoried,
not claimed to be live. PDF action destinations use package_lab1_pdfs.py.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json, re, sys

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]
SLIDES = ROOT / 'weekly-slides/weekly-slides/LAB1_FPGA_0914'


def prose(path):
    text = path.read_text(encoding='utf-8')
    return re.sub(r'```[\s\S]*?```|`[^`]*`', '', text)


def anchors(path):
    text = prose(path)
    result = set(re.findall(r'<a\s+id=["\']([^"\']+)', text))
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        title = re.sub(r'<[^>]+>', '', title).lower().strip()
        slug = re.sub(r'[^\w\- ]', '', title).replace(' ', '-')
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug + (f'-{number}' if number else ''))
    return result


def main():
    projects = json.loads((LAB / 'projects.json').read_text(encoding='utf-8'))
    ordered = sorted(projects, key=lambda p: (
        {'vivado_2026_1': 0, 'opensource_cli': 1, 'legacy': 2}[p['edition']], p['path']))
    docs = {LAB / 'README.md', SLIDES / 'README.md', ROOT / 'daily_goal/GOAL0910.md'}
    docs.update((LAB / 'docs').glob('*.md'))
    docs.update((LAB / 'reports').rglob('*.md'))
    for p in projects:
        docs.update((LAB / p['path']).glob('*.md'))
    errors = []
    local = sections = remote = 0
    for doc in sorted(docs):
        for target in re.findall(r'\]\(([^)]+)\)', prose(doc)):
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme:
                remote += 1
                continue
            dest = (doc.parent / unquote(parsed.path)).resolve() if parsed.path else doc
            local += 1
            if not dest.exists():
                errors.append({'file': str(doc.relative_to(ROOT)), 'missing': target})
            elif parsed.fragment and dest.suffix == '.md':
                sections += 1
                if unquote(parsed.fragment) not in anchors(dest):
                    errors.append({'file': str(doc.relative_to(ROOT)), 'missing_anchor': target})
    for catalog in [LAB / 'README.md', LAB / 'docs/validation.md']:
        positions = [prose(catalog).find('[' + p['id'] + ']') for p in ordered]
        if min(positions) < 0 or positions != sorted(positions):
            errors.append({'file': str(catalog.relative_to(ROOT)), 'order': 'Expected modern, CLI, legacy'})
    for p in projects:
        doc = LAB / p['path'] / 'README.md'
        if '](../../README.md)' not in prose(doc):
            errors.append({'file': str(doc.relative_to(ROOT)), 'missing': 'Backlink to LAB1 hub'})
    report = {'status': 'FAIL' if errors else 'PASS', 'markdown_files': len(docs),
              'local_links': local, 'section_links': sections,
              'remote_urls_not_requested': remote, 'project_backlinks': len(projects),
              'catalog_order': 'Vivado 2026.1, open-source CLI, legacy', 'errors': errors}
    (LAB / 'docs/navigation-validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
