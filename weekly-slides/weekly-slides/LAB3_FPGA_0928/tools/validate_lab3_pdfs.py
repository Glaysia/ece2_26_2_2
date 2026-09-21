from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path

from pypdf import PdfReader

from generate_lab3_docs import EXPERIMENTS, pdf_name


DOC = Path(__file__).resolve().parent.parent
EXPECTED = ["06.LAB3_00_CONTENTS.pdf", "06.LAB3_00_START.pdf"] + [
    pdf_name(exp) for exp in EXPERIMENTS
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def uri_links(reader: PdfReader) -> list[str]:
    links: list[str] = []
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            action = annotation.get("/A")
            if action and action.get("/URI"):
                links.append(str(action["/URI"]))
    return links


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--final', action='store_true', help='Require all 42 real captures and no PDF placeholders')
    args = parser.parse_args()
    actual = sorted(path.name for path in DOC.glob("06.LAB3_*.pdf"))
    assert actual == sorted(EXPECTED), (actual, EXPECTED)

    capture_manifest = json.loads((DOC / "required-captures.json").read_text(encoding="utf-8"))
    assert capture_manifest["count"] == 42
    assert len({item["id"] for item in capture_manifest["captures"]}) == 42
    capture_files = {item['id']: DOC / 'captures' / (item['id'] + '.png')
                     for item in capture_manifest['captures']}
    missing = [key for key, path in capture_files.items() if not path.is_file()]
    if args.final and missing:
        raise SystemExit(f'FINAL_INCOMPLETE missing_captures={len(missing)}: ' + ', '.join(missing))

    results: list[dict] = []
    for name in EXPECTED:
        path = DOC / name
        reader = PdfReader(path)
        assert reader.pages, name
        texts = [(page.extract_text() or "") for page in reader.pages]
        joined = "\n".join(texts)

        sizes = []
        for page in reader.pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            ratio = width / height
            assert abs(ratio - 4 / 3) < 0.01, (name, width, height)
            sizes.append([round(width, 3), round(height, 3)])

        links = uri_links(reader)
        for link in links:
            if link.lower().endswith(".pdf") and "://" not in link:
                assert (DOC / link).exists(), (name, link)

        is_manual = "_VIVADO.pdf" in name
        if is_manual:
            exp = next(exp for exp in EXPERIMENTS if pdf_name(exp) == name)
            assert len(reader.pages) >= 25, name
            assert exp["pass_marker"] in joined, (name, exp["pass_marker"])
            expected_missing = sum(key.startswith(exp['folder'] + '-') for key in missing)
            assert joined.count("실제 화면 캡처 자리") == expected_missing, name
            if args.final:
                assert joined.count('실제 화면 캡처 자리') == 0, name
                for key, image in capture_files.items():
                    if key.startswith(exp['folder'] + '-'):
                        assert key in joined, (name, key)
                        assert path.stat().st_mtime >= image.stat().st_mtime, (name, 'PDF predates capture')
            assert "v2.0.2" in joined, name
            assert "xc7s75fgga484-1" in joined, name
            assert "clk_50mhz" in joined, name
            assert "rst_p" in joined, name
            assert "완료 체크" in joined, name

        results.append(
            {
                "file": name,
                "pages": len(reader.pages),
                "media_box_points": sizes[0],
                "sha256": sha256(path),
                "capture_placeholders": joined.count("실제 화면 캡처 자리"),
                "uri_links": sorted(set(links)),
            }
        )

    output = {
        "version": 1,
        "pdf_count": len(results),
        "capture_count": capture_manifest["count"],
        "missing_captures": missing,
        "final": args.final,
        "checks": [
            "all expected PDFs exist",
            "every page is 4:3",
            "all local PDF URI targets exist",
            "each manual contains its PASS marker and the expected remaining capture placeholders",
            "each manual contains v2.0.2, FPGA part, and completion checklist",
        ],
        "pdfs": results,
    }
    (DOC / "pdf-validation.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"LAB3_PDF_VALIDATION_PASS pdfs={len(results)} captures={capture_manifest['count']}")


if __name__ == "__main__":
    main()
