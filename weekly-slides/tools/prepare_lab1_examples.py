"""Prepare standalone instructor examples from the empty, pinned student template.

This never changes the template or replaces existing course projects. Each new
destination is a separate clone; publication and submodule migration follow QA.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'
TEMPLATE = 'https://github.com/Glaysia/fpga-lab-template.git'
COMMIT = 'a248b802aa2dec8def8caaf5175f12fc005f8f5c'


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True,
                          encoding='utf-8', errors='replace').stdout.strip()


def prepare(project, destination):
    target = destination / project['id']
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite {target}')
    run(['git', 'clone', '--branch', 'v2.0.0', TEMPLATE, str(target)], destination)
    assert run(['git', 'rev-parse', 'HEAD'], target) == COMMIT
    run(['git', 'switch', '-c', 'main'], target)
    run(['git', 'remote', 'rename', 'origin', 'template'], target)
    source_root = LAB / project['path']
    mapping = {}
    sources = []

    def copy(name, folder):
        source = (source_root / name).resolve()
        assert source.is_relative_to(LAB.resolve()), source
        relative = f'{folder}/{source.name}'
        assert relative not in mapping, relative
        shutil.copyfile(source, target / relative)
        mapping[relative] = {
            'course_source': source.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        }
        return relative

    for name in project['sources']:
        sources.append(copy(name, 'src'))
    testbench = copy(project['testbench'], 'sim')
    constraints = copy(project['constraints'], 'constraints')
    # Remove only the known comment-only template placeholders in this new clone.
    for name in ['src/design.v', 'sim/tb_design.v', 'constraints/pins.xdc']:
        if name not in mapping:
            (target / name).unlink()
    config = {'sources': sources, 'testbench': testbench,
              'simulation_top': project['simulation_top']}
    (target / 'simulation.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    evidence = target / 'evidence'
    evidence.mkdir()
    provenance = {'template_commit': COMMIT, 'course_project': project['path'],
                  'top': project['top'], 'part': project['part'],
                  'constraints': constraints, 'files': mapping}
    (evidence / 'source-provenance.json').write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    original_readme = (target / 'README.md').read_text(encoding='utf-8')
    (target / 'README.md').write_text(
        f"# {project['id']} — 완성 예시\n\n"
        '학생용 빈 템플릿과 구분되는 강사용 참고 예시입니다. '
        '실습은 아래 템플릿을 새 폴더에 clone하고 PDF를 보며 직접 작성하세요.\n\n'
        f'```sh\ngit clone {TEMPLATE} new_project_name\n```\n\n'
        f"설계 top: `{project['top']}` · TB top: `{project['simulation_top']}` · "
        f"part: `{project['part']}`. 핀 제약: `{constraints}`.\n\n"
        '이 폴더의 `LAB1.code-workspace`를 열면 공유 폴더 없이 실행됩니다. '
        '원본 파일과 해시는 `evidence/source-provenance.json`에 기록했습니다.\n\n'
        '---\n\n' + original_readme, encoding='utf-8')
    result = subprocess.run([sys.executable, '-X', 'utf8', 'tools/lab1.py', 'simulate'],
                            cwd=target, capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    (evidence / 'standalone-simulation.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'Simulation failed: {target}; inspect evidence/standalone-simulation.txt')
    sim = json.loads((target / 'build/sim/result.json').read_text(encoding='utf-8'))
    assert sim['status'] == 'SIMULATED', sim
    marker = f"LAB1_PASS {project['top']} cases={project['cases']}"
    assert marker in result.stdout, f'Missing testbench verdict: {marker}'
    shutil.copyfile(target / 'build/sim/result.json', evidence / 'standalone-simulation.json')
    return {'project': project['path'], 'folder': str(target), 'status': 'PASS',
            'testbench_verdict': marker, 'template_commit': COMMIT,
            'sources': sources, 'testbench': testbench, 'constraints': constraints}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    projects = json.loads((LAB / 'projects.json').read_text(encoding='utf-8'))
    results = []
    for project in projects:
        results.append(prepare(project, destination))
        print(project['id'], 'PASS', flush=True)
        (destination / 'preparation-results.json').write_text(
            json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert len(results) == 22


if __name__ == '__main__':
    main()
