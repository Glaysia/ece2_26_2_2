# 실험 후 레포트 예시: AND·OR·XOR

작성일 2026-09-10. **Vivado GUI 시뮬레이션과 bit 생성까지 실제 수행했습니다. 보드 기록·실물 사진·영상은 미수행이므로 이 예시는 완결된 실물 실험 보고서가 아닙니다.**

[실험 전 레포트](../pre/01_logic_gates.md) · [상세 검증](../../vivado_2026_1/01_logic_gates/VALIDATION.md) · [해시·입력 기록](../../vivado_2026_1/01_logic_gates/evidence/manifest.json)

## Vivado GUI 과정과 사전 결과 비교

공개 템플릿 `740aef5`를 새로 clone한 폴더에서 Vivado 2026.1 GUI의 New Project를 사용했습니다. 부품은 `xc7s75fgga484-1`, 설계 top은 `logic_gate`, 시뮬레이션 top은 `tb_logic_gate_modern`입니다. RTL·TB·XDC를 각각 Design Sources·Simulation Sources·Constraints로 추가하고 Copy sources 옵션을 꺼 같은 원본을 참조했습니다.

Run Simulation → Run Behavioral Simulation에서 [실제 GUI 시뮬레이션 로그](../../vivado_2026_1/01_logic_gates/evidence/template-gui-simulation.log)의 `LAB1_PASS logic_gate cases=4`와 40ns 종료를 확인했습니다. 입력 00·01·10·11의 세 출력은 사전 레포트의 네 행과 같았습니다. 두 실행의 시뮬레이터는 XSim으로 같지만 VS Code 작업과 Vivado 프로젝트 GUI라는 실행 진입점이 다릅니다.

## 합성·구현·bit

Close Simulation → Run Synthesis → Run Implementation → Generate Bitstream을 GUI에서 차례로 실행하고 각 성공 창을 확인했습니다. [GUI 빌드 로그](../../vivado_2026_1/01_logic_gates/evidence/template-gui-build.log)를 보관했습니다.

생성 파일은 `vivado/logic_gate.runs/impl_1/logic_gate.bit`, 크기는 3,687,013바이트입니다. 배포 [logic_gate.bit](../../vivado_2026_1/01_logic_gates/release/logic_gate.bit)의 SHA-256은 `4fa6b520781887fa7e6452867b69e462a34064895da66aa3c74970bd16070771`입니다.

DRC 오류는 0건이며 CFGBVS-1 경고가 남아 있습니다. 구성 뱅크 전압과 CONFIG_VOLTAGE/CFGBVS 설정은 실물 보드 자료와 확인해야 합니다. 클록 없는 조합회로의 setup/hold NA는 타이밍 여유가 검증되었다는 의미가 아닙니다.

## 보드 기록·촬영 상태

Hardware Manager의 Auto Connect까지 진행한 뒤 Windows의 `hw_server.exe` 네트워크 권한 창이 나타났습니다. 이 환경에서 보드 기록을 수행하지 않았고 실제 LED 동작·사진·영상도 확보하지 않았습니다.

| 조건 | 시뮬레이션 xyz | 실측 | 사진·영상 |
|---|---|---|---|
| ab=00 | 000 | 미수행 | 미촬영 |
| ab=01 | 011 | 미수행 | 미촬영 |
| ab=10 | 011 | 미수행 | 미촬영 |
| ab=11 | 110 | 미수행 | 미촬영 |

실험실에서 연결된 xc7s75 장치를 확인하고 Program Device에 위 bit를 선택해 기록한 뒤, 입력과 LED가 같이 보이는 사진 및 4개 조건을 바꾸는 영상을 추가해야 합니다. 파일 생성·GUI 성공 창을 실제 보드 동작 증거로 대신하지 않습니다.

## 현재 결론

예상값·VS Code XSim·Vivado GUI XSim의 네 조합은 일치했고 비트스트림을 생성했습니다. 실제 보드 관찰과 GitHub 사진·영상 링크를 채우면 실험 후 레포트를 마무리할 수 있습니다.
