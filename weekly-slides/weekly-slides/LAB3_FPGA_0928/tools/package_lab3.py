"""Package the nine manuals only after final capture/PDF validation passes."""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

DOC = Path(__file__).resolve().parent.parent


def main():
    subprocess.run([sys.executable, str(DOC / 'tools/validate_lab3_pdfs.py'), '--final'], check=True)
    files = sorted(DOC.glob('06.LAB3_*.pdf')) + [DOC / 'pdf-validation.json']
    output = DOC / '06.LAB3_0928_MANUALS.zip'
    temporary = output.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.name)
    with zipfile.ZipFile(temporary) as archive:
        assert archive.testzip() is None
        assert sorted(archive.namelist()) == sorted(path.name for path in files)
        for path in files:
            assert archive.read(path.name) == path.read_bytes()
        with tempfile.TemporaryDirectory(prefix='lab3-package-') as directory:
            archive.extractall(directory)
            extracted = Path(directory)
            assert sorted(path.name for path in extracted.iterdir()) == sorted(path.name for path in files)
            for path in files:
                assert (extracted / path.name).read_bytes() == path.read_bytes()
    temporary.replace(output)
    print(f'LAB3_PACKAGE_PASS FreshExtraction=True {output}')


if __name__ == '__main__':
    main()
