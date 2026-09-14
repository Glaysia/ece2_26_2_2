"""The 2026-09-21 release: eight Vivado circuits and one integrated manual."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'weekly-slides/weekly-slides/LAB2_FPGA_0921'
COUNTER = '05.LAB2_01_COUNTER_VIVADO'


def projects():
    rows = json.loads((ROOT / 'example/fpga_projects_hdl/LAB2/projects.json').read_text(encoding='utf-8'))
    selected = [p for p in rows if p['edition'] == 'vivado_2026_1']
    assert len(selected) == 9 and len({p['pdf'] for p in selected}) == 9
    return selected


def stems():
    return [p['pdf'].removesuffix('.pdf') for p in projects()] + ['05.LAB2_00_START', '05.LAB2_00_CONTENTS']
