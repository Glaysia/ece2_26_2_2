# 보고서용 실험 16~21

카운터·분주기·스텝모터·피에조·피아노·시계를 선택하는 통합 소스.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/clock_divider.v](src/clock_divider.v) | 설계 |
| [src/counter.v](src/counter.v) | 설계 |
| [src/piano.v](src/piano.v) | 설계 |
| [src/stepper.v](src/stepper.v) | 설계 |
| [src/tone.v](src/tone.v) | 설계 |
| [src/top_main.v](src/top_main.v) | 설계 |
| [src/watch.v](src/watch.v) | 설계 |
| [sim/tb_top_main.sv](sim/tb_top_main.sv) | 테스트벤치·모델 |

이 자료에 별도 핀 제약 파일은 포함되어 있지 않다.

## 출처

기존 `example/reports/simulation/exp16`~`exp21`의 중복 소스를 하나로 모았다.

`src/top_main.v`의 `EXPERIMENT` 값을 16~21 중 하나로 선택한다. 기본값은 16이다.

| 값 | 실험 |
|---:|---|
| 16 | 카운터 |
| 17 | 클록 분주 |
| 18 | 스텝모터 |
| 19 | 피에조 |
| 20 | 피아노 |
| 21 | 분·초 시계 |
