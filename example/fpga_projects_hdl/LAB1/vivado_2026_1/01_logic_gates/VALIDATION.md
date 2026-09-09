# 첫 회로 검증 — 2026-09-10

[설치·clone](../../docs/setup.md) · [workspace](vivado_2026_1_01_logic_gates.code-workspace) · [실습 PDF](../../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_VIVADO.pdf)

## 실행 결과

| 단계 | 결과 | 증거 |
| --- | --- | --- |
| 공개 브랜치 sparse clone | 성공, 별도 폴더에서 재검증 | 코드 기준 커밋 70c8036 |
| VS Code workspace의 XSim 실행기 | PASS, 4개 입력, 40ns 종료 | [로그](evidence/vscode-simulation.log), [VCD](evidence/vscode-wave.vcd) |
| clone 폴더에서 프로젝트 생성 | PASS | [결과](evidence/clone-create-result.json) |
| clone 폴더의 Vivado Behavioral Simulation | PASS, 같은 4개 입력, 40ns 종료 | [로그](evidence/clone-vivado-simulation.log), [결과](evidence/clone-vivado-result.json) |
| Vivado GUI Behavioral Simulation | 40ns 종료, 동일 파형 | 실습 PDF 실제 캡처 |
| 합성·구현·비트스트림 생성 | PASS / write_bitstream Complete | [결과](evidence/build-result.json), [비트스트림](release/logic_gate.bit) |

Vivado/XSim 2026.1, part xc7s75fgga484-1. 설계 top logic_gate, 시뮬레이션 top tb_logic_gate_modern.
입력 순서는 00 → 01 → 10 → 11, 각 10ns. 출력 AND/OR/XOR의 기대값과 실제값을 비교하며 미일치·검사 수 부족·watchdog은 실패 처리한다.

VS Code에 등록된 것과 동일한 Python task 실행기를 명령행에서 실행했고, 실제 VS Code 창에서 코드·작업 목록·생성 로그·VaporView를 확인했다. Vivado GUI에서도 테스트벤치 임포트·Set as Top·Run Behavioral Simulation을 실행했다.

## 보고서와 남은 장비 확인

[DRC](evidence/drc.txt)에는 오류 없이 CFGBVS-1 경고 1건이 있다. 원본 XDC에 CFGBVS / CONFIG_VOLTAGE가 없어서 구성 bank의 전압 검사를 완료할 수 없다는 내용이다. 실제 보드 회로도와 설정 전압을 확인한 뒤 값을 지정해야 하며, 임의로 3.3V로 가정하지 않았다.

[타이밍 보고서](evidence/timing_summary.txt)는 클록 없는 조합회로이므로 setup/hold 요약이 NA다. 이를 타이밍 제약 검증 완료로 해석하지 않는다.
이번 범위는 비트스트림 파일 생성까지다. 실제 장치 기록·스위치/LED 검증·사진·영상은 후속 실험에서 수행하고 실험 후 레포트에 GitHub 링크와 함께 남긴다.

비트스트림의 SHA-256과 입력 소스 해시는 [manifest](evidence/manifest.json)에 기록했다.

PDF 검수: 33쪽, 4:3, 모든 목차 버튼의 2쪽 목적지와 외부 PDF 대상 확인. 전 페이지 렌더링을 검토했으며 화면 잘림과 잘못 저장된 캡처를 수정했다. 설치·환경설정 PDF를 포함한 별도 ZIP은 압축 해제 내용과 원본 일치를 검사했다.
