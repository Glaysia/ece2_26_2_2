# LAB3 · 9월 28일 FPGA 응용회로 실습

작성일: 2026-09-21. 필수 범위는 개별 실험 7개다. 통합판과 명령줄 Vivado 구현은 자동으로 추가하지 않는다.

[전체 목차](06.LAB3_00_CONTENTS.pdf) · [공통 예습](06.LAB3_00_START.pdf)

## 매뉴얼

| 번호 | 자료 | 원고 | 기능 시뮬레이션 기준 |
|---:|---|---|---|
| 19 | [PWM LED 밝기](06.LAB3_01_LED_PWM_VIVADO.pdf) | [06.LAB3_01_LED_PWM_VIVADO.tex](06.LAB3_01_LED_PWM_VIVADO.tex) | `LAB3_LED_PWM_PASS checks=4` |
| 20 | [RGB LED PWM](06.LAB3_02_RGB_PWM_VIVADO.pdf) | [06.LAB3_02_RGB_PWM_VIVADO.tex](06.LAB3_02_RGB_PWM_VIVADO.tex) | `LAB3_RGB_PWM_PASS checks=2` |
| 21 | [피에조 단일 음](06.LAB3_03_PIEZO_VIVADO.pdf) | [06.LAB3_03_PIEZO_VIVADO.tex](06.LAB3_03_PIEZO_VIVADO.tex) | `LAB3_PIEZO_PASS edges=5` |
| 22 | [스텝모터 위상 제어](06.LAB3_04_STEPPER_VIVADO.pdf) | [06.LAB3_04_STEPPER_VIVADO.tex](06.LAB3_04_STEPPER_VIVADO.tex) | `LAB3_STEPPER_PASS checks=8` |
| 23 | [MM:SS 시계](06.LAB3_05_MMSS_CLOCK_VIVADO.pdf) | [06.LAB3_05_MMSS_CLOCK_VIVADO.tex](06.LAB3_05_MMSS_CLOCK_VIVADO.tex) | `LAB3_MMSS_PASS checks=7` |
| 24 | [문자 LCD 제어](06.LAB3_06_CHARACTER_LCD_VIVADO.pdf) | [06.LAB3_06_CHARACTER_LCD_VIVADO.tex](06.LAB3_06_CHARACTER_LCD_VIVADO.tex) | `LAB3_LCD_PASS bytes=40` |
| 25 | [PC–FPGA UART 에코](06.LAB3_07_UART_ECHO_VIVADO.pdf) | [06.LAB3_07_UART_ECHO_VIVADO.tex](06.LAB3_07_UART_ECHO_VIVADO.tex) | `LAB3_UART_ECHO_PASS checks=3` |

학생은 [`fpga-lab-template` v2.0.2](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.2)를 실험별 새 폴더로 clone하고, 매뉴얼을 보며 RTL·TB·XDC·`simulation.json`을 직접 작성한다. VS Code에서는 Icarus, Vivado에서는 같은 원본과 TB로 XSim을 실행한다. 구현 뒤 실제 보드 사진·영상·GitHub 링크를 실험 후 레포트에 넣는다.

현재 원고에는 코드 전체, 핀, 검증 절차, 보드 절차, 실험 전후 레포트 기준이 들어 있다. GUI 화면은 `required-captures.json`의 ID와 같은 자리표시자로 남겨 두었으며 다음 화면 촬영 단계에서 실제 캡처로 교체한다.

## 빌드

`LAB3_FPGA_0928` 폴더에서 XeLaTeX로 각 원고를 두 번 빌드한다. 생성 PDF는 같은 폴더에 둔다.

```powershell
python tools/generate_lab3_docs.py
Get-ChildItem 06.LAB3_*.tex | ForEach-Object { xelatex -interaction=nonstopmode -halt-on-error $_.Name }
```

## 검증 기준

- 4:3 PDF, 내부 목차 이동, 전체 목차의 PDF 간 링크.
- Icarus와 XSim 모두 7개 TB의 PASS marker 확인.
- Vivado 2026.1에서 xc7s75fgga484-1 대상으로 합성·구현·DRC·timing·bitstream 확인.
- 실제 보드 동작은 학생 실험 단계이며 자동 시뮬레이션 결과와 구분한다.
