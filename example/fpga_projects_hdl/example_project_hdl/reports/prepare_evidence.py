"""Crop real VS Code captures for print; keep the unmodified captures beside them."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent / 'evidence'
# Keep the editor breadcrumb and the relevant source lines. No pixels are redrawn.
bottom = {16:285, 17:560, 18:410, 19:610, 20:490, 21:585}
for n in range(16, 22):
    with Image.open(root / f'exp{n}-source.png') as im:
        print(n, im.size)
        im.crop((285, 62, 1120, bottom[n])).save(root / f'exp{n}-source-print.png')
    with Image.open(root / f'exp{n}-wave.png') as im:
        im.crop((285, 62, 1835, 540)).save(root / f'exp{n}-wave-print.png')
