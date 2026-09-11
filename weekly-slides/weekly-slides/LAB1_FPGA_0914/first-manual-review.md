# 첫 번째 매뉴얼 검토판 — 2026-09-10

[PDF 열기](04.LAB1_01_LOGIC_GATES_VIVADO.pdf) · [작업 목표](../../../daily_goal/GOAL0910_2.md#12-목표-변경--첫-번째-매뉴얼-완성-후-사용자-검토)

이번 완료 범위는 논리 게이트 최신 Vivado 매뉴얼 하나다. 나머지 21개는 사용자 검토 후 확장한다.

## 피드백 반영

| PDF 쪽 | 반영 내용 |
|---|---|
| 3–4 | 검정 배경·흰 글씨·7pt 명령어. `git clone --branch v2.0.0`과 작업 브랜치 생성 |
| 13–14 | 실제 VS Code 테스트벤치 1–22행. 긴 14행도 화면 줄바꿈으로 전체 표시 |
| 24 | 실제 VS Code XDC 전체 1–12행. 다섯 핀 및 전기 규격 지정 |
| 10 | 직접 작성할 simulation.json 전체 7행 화면 |
| 18–21 | 실제 VS Code 작업 PASS·40ns 종료·새 VCD 파형과 실행 오류 해결 |

소스 코드는 이미지로 유지한다. 새 PNG는 사용자 지시대로 Git ignore를 유지하며, 최종 PDF에 포함한다. 기존 Vivado 메뉴·파일 선택·합성·구현·bit 화면을 재사용하며, 본문의 파일 경로는 학생 자신의 src·sim·constraints로 수정했다. 과거 화면의 사용자 경로는 그대로 입력하지 않도록 안내한다.

## 검증 범위

- 템플릿 `v2.0.0` 원격 태그 존재 확인. 학생 clone에서 RTL·TB·XDC 파일명을 바꾸고 내용을 작성했다.
- Windows Icarus 13.0과 Python 3.12.10으로 새 학생 폴더의 실행기를 실행했다. 정상 4개 PASS, XOR→OR 변경 시 `vector=3 expected=6 actual=7` 실패, 복구 후 4개 PASS를 확인했다. 정상 종료는 40000ps(40ns)다.
- 후속 GUI 재검증을 완료했다. Python 3.12.10의 설치 경로를 세 작업의 windows.command에 지정한 뒤 VS Code에서 Ctrl+Shift+B로 02 Simulate를 실행하여 cases=4·40000ps 종료를 확인했다. Task 메뉴에서 03 Open waveform을 실행해 같은 새 VCD를 열었다. VaporView를 해당 workspace에서 활성화하고 a·b·x·y·z 추가, Zoom to Fit, ns 선택, 35.004ns의 입력 11과 출력 110을 확인·촬영했다. Python 경로와 비활성화된 확장 문제의 해결 순서를 교안에 반영했다.
- Vivado 시뮬레이션·bit 생성 화면은 같은 회로의 기존 GUI 검증 자료다. 이번 피드백 수정 중에 Vivado 전체 GUI 과정을 새로 수행한 것은 아니다.
- 65쪽 4:3 PDF를 렌더링 검수했다. 목차 목적지 `modern01-contents`는 2쪽이며 각 절의 내부 링크 목적지를 확인했다. 새 코드 이미지의 오른쪽 끝·마지막 행과 명령어 상자의 줄 끝을 확인했다.
- 실제 FPGA 기록·보드 사진·영상은 제작 환경에서 수행하지 않았다. 교안은 학생의 실험 후 기록·제출 절차를 안내한다.

## 새 학생 프로젝트 실행 기록

```json
[
  {
    "case": "baseline",
    "exit_code": 0,
    "status": "SIMULATED",
    "input_sha256": {
      "simulation.json": "701e521940e34e7fc2c3c5c5d670b4da48d16dd3ac12306ad7e6cd0fcfee751c",
      "src/logic_gate.v": "e3cbd3a7219ecd100f49ced79059e76f89d0670d03ecc442f82e2bc732494a3b",
      "sim/tb_logic_gate_modern.sv": "8815d26ae87ee452a7cec9e99d54cab62ab72d35ec1e090e3af6afc154ffb232"
    }
  },
  {
    "case": "xor_to_or",
    "exit_code": 1,
    "status": "FAILED",
    "input_sha256": {
      "simulation.json": "701e521940e34e7fc2c3c5c5d670b4da48d16dd3ac12306ad7e6cd0fcfee751c",
      "src/logic_gate.v": "9440c3221ad2ffba44b95740107926cfaca27f68962d61d4239407749123d891",
      "sim/tb_logic_gate_modern.sv": "8815d26ae87ee452a7cec9e99d54cab62ab72d35ec1e090e3af6afc154ffb232"
    }
  },
  {
    "case": "restored",
    "exit_code": 0,
    "status": "SIMULATED",
    "input_sha256": {
      "simulation.json": "701e521940e34e7fc2c3c5c5d670b4da48d16dd3ac12306ad7e6cd0fcfee751c",
      "src/logic_gate.v": "e3cbd3a7219ecd100f49ced79059e76f89d0670d03ecc442f82e2bc732494a3b",
      "sim/tb_logic_gate_modern.sv": "8815d26ae87ee452a7cec9e99d54cab62ab72d35ec1e090e3af6afc154ffb232"
    }
  }
]
```

최종 GUI 실행 기록: `run-5ac9e121616d4f9ea40144798a1dd2d8`. 최종 파형 화면은 이 실행에서 생성한 build/sim/wave.vcd를 사용한다.

## 22개 확장 후 보강 — 문법 오류와 수정 실험

- 20–21쪽: 실제 VS Code의 세미콜론 누락 오류 → Problems 두 번 클릭으로 해당 행 이동 → 복구·저장·재실행 화면.
- 24쪽: XOR를 OR로 바꾸고 a=b=1에서 실패를 확인한 뒤 복구하는 학생 과제.
- XDC 전체 화면은 새 페이지 추가로 27쪽에 있다. 기존 RTL·TB 화면은 그대로 유지했다.
- 문법 오류 복구 실행은 `run-d90579a60b9848b28e32826a814d335a`이며 RTL·TB 입력 해시는 앞의 정상 학생 실행과 같다.
- 회로별 수정 실험은 제작 검사기에서 11개 회로 × 정상·변경·복구 3회로 검증했다.

최종 보강본은 68쪽이다. 문법 오류·수정 과제의 새 페이지를 실제 렌더링으로 확인했고, 목차 버튼은 계속 2쪽으로 돌아간다.
