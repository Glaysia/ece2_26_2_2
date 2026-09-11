# LAB1 설치와 시작

[LAB1 홈](../README.md) · [직접 작성하는 공통 실습](student-workflow.md) · [완성 예시 22개](examples.md)

학생 프로젝트는 [단일 빈 템플릿](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.0)에서 시작한다. Git·Python 3.10 이상·VS Code·Icarus Verilog를 먼저 설치한다. HDL 편집에는 slang, 파형에는 VaporView, 교안에는 vscode-pdf를 사용한다. workspace를 열고 Extensions에서 `@recommended`를 검색하면 세 확장이 표시된다.

Windows는 `python --version`, `git --version`, `iverilog -V`, `vvp -V`를 확인한다. Linux·macOS·WSL은 `python` 대신 `python3`를 사용한다. 설치 경로를 PATH에 등록한 뒤 VS Code를 다시 연다. [운영체제별 설치 안내](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.0)를 따른다.

```sh
git clone https://github.com/Glaysia/fpga-lab-template.git new_project_name
cd new_project_name
code LAB1.code-workspace
```

GUI에서는 File → New Window → Open Workspace from File... → 새 폴더의 LAB1.code-workspace를 선택한다. [직접 작성 순서](student-workflow.md)에 따라 RTL·TB·XDC를 입력하고 simulation.json을 수정한다. Task는 01 Check tools, 02 Simulate, 03 Open waveform 세 개다. 먼저 Icarus 파형과 실험 전 레포트를 완성한다.

Vivado 실습은 사전 작업 뒤 Vivado GUI를 열고 자신의 src·sim·constraints 파일을 가져온다. 정확한 part는 `xc7s75fgga484-1`이다. 최신 교안은 2026.1 GUI를 사용하며 레거시 원문은 원래 버전의 화면을 보존한다. 구버전 실행 여부는 [검증 기록](validation.md)을 확인한다.

CLI 통합 실습은 Vivado를 설치하거나 XSim을 실행하지 않는다. [CLI 안내](cli.md)의 오픈소스 도구·장치 DB·bit·openFPGALoader 흐름을 따른다. 정확한 S75 bit 생성·파일 검사 결과와 실제 보드 기록의 검증 범위를 해당 문서에서 구분한다.

완성 예시를 참고하려면 강의 저장소에서 `git submodule update --init --recursive`를 실행한다. 각 예시는 독립 저장소이며 해당 디렉터리의 LAB1.code-workspace만 열면 된다. 이 과정은 학생이 빈 프로젝트를 만드는 clone 명령과 구분한다.
