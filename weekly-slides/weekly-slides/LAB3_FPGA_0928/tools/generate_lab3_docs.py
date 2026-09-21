from __future__ import annotations

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
DOC = HERE.parent
REPO = DOC.parents[2]
PROJECT_ROOT = REPO / "example" / "fpga_projects_hdl" / "LAB3" / "vivado_2026_1"
CODE_PREFIX = "../../../example/fpga_projects_hdl/LAB3/vivado_2026_1"


EXPERIMENTS = [
    dict(
        index=1, number=19, slug="LED_PWM", folder="01_led_pwm",
        title="PWM LED 밝기", top="lab3_led_pwm", tb="tb_led_pwm",
        pass_marker="LAB3_LED_PWM_PASS checks=4",
        purpose="버튼 한 번마다 duty를 10%씩 바꾸고 8개 LED에 같은 PWM을 출력한다.",
        concepts="50 MHz 단일 클록, 2단 동기화, 20 ms 디바운스, 한 클록 펄스, PWM duty",
        interface="clk_50mhz B6 · rst_p K4 · 밝기 버튼 N8 · LED[7:0] N5/M1/M3/M7/N7/M2/M4/L4",
        tests="0%, 30%, 100%, 100% 다음 0% 순환에서 한 주기의 HIGH 클록 수를 검사한다.",
        board="버튼을 한 번씩 눌러 단계가 하나씩 이동하는지, 0%와 100% 및 중간 밝기를 관찰한다.",
        modification="LEVELS를 10에서 5로 바꾸어 단계 수와 파형의 HIGH 폭을 비교한 뒤 복구한다.",
    ),
    dict(
        index=2, number=20, slug="RGB_PWM", folder="02_rgb_pwm",
        title="RGB LED PWM", top="lab3_rgb_pwm", tb="tb_rgb_pwm",
        pass_marker="LAB3_RGB_PWM_PASS checks=2",
        purpose="R·G·B 버튼으로 세 PWM duty를 독립적으로 바꾸고 네 개 RGB LED에 출력한다.",
        concepts="독립 PWM 채널, 공통 주기, 색 혼합, 입력 원펄스",
        interface="clk_50mhz B6 · rst_p K4 · R/G/B 버튼 N8/N4/N1 · RGB LED 12개 핀",
        tests="R=20%, G=50%, B=80%의 HIGH 폭과 R 채널만 한 단계 증가하는 조건을 검사한다.",
        board="각 버튼이 해당 색만 바꾸는지 확인하고 세 색의 조합 및 밝기 변화를 기록한다.",
        modification="한 색의 초기 duty만 바꾸어 혼합색과 세 파형의 차이를 비교한 뒤 복구한다.",
    ),
    dict(
        index=3, number=21, slug="PIEZO", folder="03_piezo",
        title="피에조 단일 음", top="lab3_piezo", tb="tb_piezo",
        pass_marker="LAB3_PIEZO_PASS edges=5",
        purpose="50 MHz를 분주하여 피에조에 294 Hz 사각파를 출력한다.",
        concepts="주파수 분주, 반주기 계산, 파라미터 기반 시뮬레이션",
        interface="clk_50mhz B6 · rst_p K4 · piezo Y21",
        tests="가속 파라미터에서 출력 반전 사이가 정확히 다섯 클록인지 연속 다섯 번 검사한다.",
        board="출력 주파수를 계산하고 실제 음 높이와 음량을 관찰한다.",
        modification="TONE_HZ를 다른 음의 주파수로 바꾸어 분주값과 소리 변화를 비교한 뒤 복구한다.",
    ),
    dict(
        index=4, number=22, slug="STEPPER", folder="04_stepper",
        title="스텝모터 위상 제어", top="lab3_stepper", tb="tb_stepper",
        pass_marker="LAB3_STEPPER_PASS checks=8",
        purpose="clock-enable마다 4상 코일 패턴을 이동하여 정·역회전과 정지를 제어한다.",
        concepts="clock-enable, 입력 동기화, 4상 시퀀스, 방향 전환",
        interface="clk_50mhz B6 · rst_p K4 · enable N8 · direction N4 · phase[3:0] Y20/Y22/AA20/AA21",
        tests="정방향 한 주기, 역방향 두 단계, enable=0 유지 조건을 가속된 step rate로 검사한다.",
        board="드라이버 결선 후 회전 방향·단계 속도·정지 유지와 모터 발열을 관찰한다.",
        modification="STEPS_PER_SEC를 절반으로 바꾸어 단계 간격을 계산하고 회전 속도를 비교한 뒤 복구한다.",
    ),
    dict(
        index=5, number=23, slug="MMSS_CLOCK", folder="05_mmss_clock",
        title="MM:SS 시계", top="lab3_mmss_clock", tb="tb_mmss_counter",
        pass_marker="LAB3_MMSS_PASS checks=7",
        purpose="1초 enable로 00:00부터 59:59까지 계수하고 4자리 7세그먼트를 스캔한다.",
        concepts="BCD 자리올림, 1초 enable, 4자리 동적 스캔, 세그먼트 디코딩",
        interface="clk_50mhz B6 · rst_p K4 · digit[3:0] · seg[7:0], decimal point로 분·초 구분",
        tests="00:09→00:10, 00:59→01:00, 59:59→00:00과 전체 3,600초 순환 및 디코더를 검사한다.",
        board="자리 순서와 극성, 분·초 구분점, 1초 간격과 59:59 순환을 확인한다.",
        modification="시뮬레이션에서 TICKS_PER_SECOND를 바꾸어 자리올림 시점이 어떻게 달라지는지 확인한 뒤 복구한다.",
    ),
    dict(
        index=6, number=24, slug="CHARACTER_LCD", folder="06_character_lcd",
        title="문자 LCD 제어", top="lab3_character_lcd", tb="tb_character_lcd",
        pass_marker="LAB3_LCD_PASS bytes=40",
        purpose="HD44780 호환 LCD를 8비트 write-only 방식으로 초기화하고 두 줄 문자열을 표시한다.",
        concepts="초기화 명령, Enable setup/high/hold, DDRAM 주소, ASCII, 명령별 대기",
        interface="clk_50mhz B6 · rst_p K4 · lcd_e A6 · lcd_rs G6 · lcd_rw D6 · lcd_data[7:0] A4/B2/C3/D4/A2/C5/C1/D1",
        tests="Enable 하강 에지에서 초기화 명령과 두 줄 데이터, 총 40바이트의 순서와 RS를 검사한다.",
        board="5 V/3.3 V 결선과 대비를 먼저 확인하고 FPGA LAB3 / LCD CONTROLLER 문자열을 확인한다.",
        modification="둘째 줄 문자열 한 글자를 바꾸어 ASCII 바이트와 표시 결과를 비교한 뒤 복구한다.",
    ),
    dict(
        index=7, number=25, slug="UART_ECHO", folder="07_uart_echo",
        title="PC–FPGA UART 에코", top="lab3_uart_echo", tb="tb_uart_echo",
        pass_marker="LAB3_UART_ECHO_PASS checks=3",
        purpose="9600 8N1로 받은 한 바이트를 그대로 송신하고 LED에 마지막 수신값을 표시한다.",
        concepts="비동기 입력 동기화, start 중앙 확인, LSB-first, stop 확인, TX ready/valid",
        interface="clk_50mhz B6 · rst_p K4 · uart_rxd C6 · uart_txd F6 · LED[7:0]",
        tests="독립 직렬 송수신 모델로 0x41, 0x5A, 0x0A의 에코와 LED, framing error 부재를 검사한다.",
        board="터미널을 9600 8N1·local echo off로 설정하고 문자 하나당 반환 문자 하나와 LED 값을 확인한다.",
        modification="BAUD 파라미터를 송수신 양쪽에서 같은 값으로 바꾸어 bit 시간을 비교한 뒤 복구한다.",
    ),
]


def esc(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}", "_": r"\_", "%": r"\%", "&": r"\&",
        "#": r"\#", "$": r"\$", "{": r"\{", "}": r"\}",
    }
    return "".join(replacements.get(ch, ch) for ch in value)


def code_files(exp: dict) -> list[Path]:
    root = PROJECT_ROOT / exp["folder"]
    files = [root / "simulation.json"]
    files.extend(sorted((root / "src").glob("*")))
    files.extend(sorted((root / "sim").glob("*")))
    files.extend(sorted((root / "constraints").glob("*")))
    return [path for path in files if path.is_file()]


def rel_code(path: Path) -> str:
    return f"{CODE_PREFIX}/{path.relative_to(PROJECT_ROOT).as_posix()}"


def listing_frames(exp: dict) -> str:
    frames: list[str] = []
    for path in code_files(exp):
        lines = path.read_text(encoding="utf-8").splitlines()
        chunk = 18 if path.suffix.lower() in {".v", ".sv"} else 22
        for first in range(1, len(lines) + 1, chunk):
            last = min(first + chunk - 1, len(lines))
            title = esc(f"{path.name} · {first}–{last}행")
            language = "Verilog" if path.suffix.lower() in {".v", ".sv"} else ""
            frames.append(
                "\\begin{frame}[fragile]{" + title + "}\n"
                "\\lstinputlisting[language=" + language + f",firstline={first},lastline={last},firstnumber={first}]"
                "{" + rel_code(path) + "}\n"
                "\\end{frame}\n"
            )
    return "\n".join(frames)


def capture_tex(capture_id: str, instruction: str) -> str:
    path = DOC / 'captures' / (capture_id + '.png')
    if path.is_file():
        return (
            r'\begin{center}\includegraphics[width=\textwidth,height=6.0cm,keepaspectratio]{'
            + 'captures/' + capture_id + '.png' + r'}\end{center}'
            + '\n' + r'{\tiny ' + esc(capture_id) + '}'
        )
    return r'\captureplaceholder{' + esc(capture_id) + '}{' + instruction + '}'


def manual_tex(exp: dict) -> str:
    folder = exp["folder"]
    project_name = f"lab3_{exp['number']}_{folder[3:]}"
    files = code_files(exp)
    src_names = ", ".join(path.name for path in files if path.parent.name == "src")
    xdc_name = next(path.name for path in files if path.parent.name == "constraints")
    sim_name = next(path.name for path in files if path.parent.name == "sim")
    title = esc(f"LAB3-{exp['number']} · {exp['title']}")
    clone_text = esc(project_name)
    document = rf"""% !TEX program = xelatex
\input{{shared/lab3_preamble.tex}}
\hypersetup{{pdftitle={{{title}}},pdfauthor={{이해리}}}}
\begin{{document}}
\renewcommand{{\small}}{{\fontsize{{8.7}}{{10.5}}\selectfont}}
\setlength{{\leftmargini}}{{1.35em}}

\begin{{frame}}{{{title}}}
\small
전자전기컴퓨터설계실험Ⅱ · FPGA 응용 실습\par\vspace{{0.28cm}}
{esc(exp['purpose'])}\par\vspace{{0.28cm}}
Vivado 2026.1 · FPGA Part xc7s75fgga484-1\par\vspace{{0.28cm}}
작성일 2026. 09. 21. · 이해리
\end{{frame}}

\begin{{frame}}[label=lab3-contents]{{목차}}
\small
\navlink{{goal}}{{동작과 검증 목표}}\par\vspace{{0.28cm}}
\navlink{{start}}{{v2.0.2 프로젝트 시작}}\par\vspace{{0.28cm}}
\navlink{{code}}{{RTL·TB·XDC 직접 작성}}\par\vspace{{0.28cm}}
\navlink{{simulate}}{{VS Code·Icarus 시뮬레이션}}\par\vspace{{0.28cm}}
\navlink{{vivado}}{{Vivado XSim·비트스트림}}\par\vspace{{0.28cm}}
\navlink{{board}}{{보드 실험과 레포트}}
\end{{frame}}

\begin{{frame}}[label=goal]{{이번 회로의 목표}}
\small
{esc(exp['purpose'])}\par\vspace{{0.28cm}}
핵심 개념: {esc(exp['concepts'])}\par\vspace{{0.28cm}}
기능 TB: \texttt{{{esc(exp['tb'])}}}\par\vspace{{0.18cm}}
예상 PASS: \texttt{{{esc(exp['pass_marker'])}}}
\end{{frame}}

\begin{{frame}}{{입출력과 보드 연결}}
\small
{esc(exp['interface'])}\par\vspace{{0.32cm}}
모든 순차 로직은 MAIN CLOCK F의 50 MHz만 사용한다. 느린 동작은 내부 clock-enable로 만든다.\par\vspace{{0.28cm}}
XDC의 포트 이름은 top module 선언과 글자·대소문자까지 같아야 한다.
\end{{frame}}

\begin{{frame}}{{TB가 자동으로 확인하는 범위}}
\small
{esc(exp['tests'])}\par\vspace{{0.28cm}}
시뮬레이션 파라미터는 실제 동작의 순서와 경계 조건을 유지하면서 시간을 줄인다.\par\vspace{{0.28cm}}
PASS는 디지털 기능 검사 결과다. 핀 배선, 전기 규격, 실제 부품의 물리 동작은 보드 단계에서 확인한다.
\end{{frame}}

\begin{{frame}}[fragile,label=start]{{v2.0.2 템플릿을 새 이름으로 clone}}
\small
PowerShell에서 한 줄씩 실행한다.
\begin{{lstlisting}}[language={{}}]
git clone --branch v2.0.2 https://github.com/Glaysia/fpga-lab-template.git {project_name}
cd {project_name}
git switch -c main
code FPGA.code-workspace
\end{{lstlisting}}
태그 clone 직후 detached HEAD 안내는 정상이다. \texttt{{git switch -c main}}으로 자신의 이력을 시작한다.
\end{{frame}}

\begin{{frame}}{{빈 템플릿에서 만들 파일}}
\small
\begin{{center}}\renewcommand{{\arraystretch}}{{1.35}}\begin{{tabular}}{{>{{\raggedright\arraybackslash}}p{{2.25cm}}p{{7.2cm}}}}
경로 & 파일\\\hline
src/ & \texttt{{{esc(src_names)}}}\\
sim/ & \texttt{{{esc(sim_name)}}}\\
constraints/ & \texttt{{{esc(xdc_name)}}}\\
프로젝트 루트 & \texttt{{simulation.json}}\\
\end{{tabular}}\end{{center}}
기존 빈 파일은 이름을 바꾸고, 필요한 추가 RTL은 src에 새로 만든다.
\end{{frame}}

\begin{{frame}}{{simulation.json 확인}}
\small
sources에는 모든 RTL 파일을 의존 순서에 맞춰 넣는다.\par\vspace{{0.25cm}}
testbench는 \texttt{{sim/{esc(sim_name)}}}, simulation\_top은 \texttt{{{esc(exp['tb'])}}}다.\par\vspace{{0.25cm}}
설계 top \texttt{{{esc(exp['top'])}}}은 Vivado 합성에서 선택한다. TB module을 합성 top으로 선택하지 않는다.
\end{{frame}}

\begin{{frame}}[label=code]{{코드를 읽고 입력하는 기준}}
\small
다음 코드 화면은 줄 번호와 파일명이 원본 프로젝트와 연결되어 있다.\par\vspace{{0.25cm}}
RTL은 합성 가능한 회로, TB는 입력 자극과 기대값 비교, XDC는 핀과 20 ns 클록 제약을 담당한다.\par\vspace{{0.25cm}}
코드를 붙여 넣는 것으로 끝내지 말고 counter 폭, 파라미터 계산, 리셋 우선순위, 출력 시점을 설명할 수 있어야 한다.
\end{{frame}}

{listing_frames(exp)}

\begin{{frame}}[label=simulate]{{VS Code에서 Icarus 실행}}
\small
\begin{{enumerate}}
\item File → Save All.
\item Terminal → Run Task... → 01 Check tools.
\item Git·Python·iverilog·vvp 경로와 버전을 확인한다.
\item Terminal → Run Task... → 02 Simulate.
\item \texttt{{{esc(exp['pass_marker'])}}}와 종료 시각을 기록한다.
\item 03 Open waveform으로 \texttt{{build/sim/wave.vcd}}를 연다.
\end{{enumerate}}
\end{{frame}}

\begin{{frame}}{{VS Code · 프로젝트와 파일}}
\captureplaceholder{{{esc(folder + '-vscode-workspace')}}}{{FPGA.code-workspace를 연 뒤 Explorer에 src·sim·constraints·tools와 작성 파일이 보이게 캡처한다.}}
\end{{frame}}

\begin{{frame}}{{VS Code · 시뮬레이션 PASS}}
\captureplaceholder{{{esc(folder + '-vscode-pass')}}}{{02 Simulate 실행 뒤 {esc(exp['pass_marker'])}와 종료 시각이 함께 보이게 캡처한다.}}
\end{{frame}}

\begin{{frame}}{{VS Code · 파형}}
\captureplaceholder{{{esc(folder + '-vscode-wave')}}}{{TB top을 펼쳐 clk\_50mhz·rst\_p·주요 입력·내부 상태·출력을 추가하고 경계 조건이 보이게 확대한다.}}
\end{{frame}}

\begin{{frame}}{{파형에서 설명할 내용}}
\small
{esc(exp['tests'])}\par\vspace{{0.28cm}}
입력을 바꾼 시점, 유효 상승 에지, 상태 갱신 직후를 구분한다.\par\vspace{{0.28cm}}
파라미터를 줄인 TB 시간과 실제 50 MHz 보드 시간을 혼동하지 않는다.
\end{{frame}}

\begin{{frame}}{{수정 실험}}
\small
{esc(exp['modification'])}\par\vspace{{0.28cm}}
정상 PASS와 파형을 먼저 보관한 뒤 한 항목만 수정한다. 예상값, 실제 FAIL 또는 변화, 복구 PASS를 3행 표로 기록한다.\par\vspace{{0.28cm}}
TB의 기대값을 RTL 오류에 맞춰 바꾸지 않는다.
\end{{frame}}

\begin{{frame}}[label=vivado]{{Vivado 2026.1 프로젝트 생성}}
\small
\begin{{enumerate}}
\item Create Project → RTL Project → Do not specify sources at this time.
\item Part에 \texttt{{xc7s75fgga484-1}}을 정확히 선택한다.
\item Add Sources에 src의 RTL 전부, Add Simulation Sources에 TB를 추가한다.
\item Add or Create Constraints에 XDC를 추가한다.
\item Design Sources의 top을 \texttt{{{esc(exp['top'])}}}으로 설정한다.
\end{{enumerate}}
\end{{frame}}

\begin{{frame}}{{Vivado · 소스와 top}}
\captureplaceholder{{{esc(folder + '-vivado-sources')}}}{{Sources 창에서 RTL, Simulation Sources의 TB, Constraints의 XDC와 top module이 함께 보이게 캡처한다.}}
\end{{frame}}

\begin{{frame}}{{Vivado XSim}}
\small
Flow Navigator → Simulation → Run Behavioral Simulation.\par\vspace{{0.28cm}}
Tcl Console의 \texttt{{{esc(exp['pass_marker'])}}}를 확인한다. Objects/Wave에서 입력과 출력을 추가하고 Zoom Fit으로 전체 실행을 본다.\par\vspace{{0.28cm}}
Icarus와 XSim은 같은 RTL·TB를 실행해야 한다. 서로 다른 사본을 등록하지 않는다.
\end{{frame}}

\begin{{frame}}{{Vivado · XSim PASS와 파형}}
\captureplaceholder{{{esc(folder + '-xsim-pass')}}}{{Tcl Console PASS, waveform 이름, 시간축, 핵심 입출력이 한 화면에 보이게 캡처한다.}}
\end{{frame}}

\begin{{frame}}{{핀과 클록 제약 확인}}
\small
Open Elaborated Design 또는 I/O Planning에서 top port와 PACKAGE\_PIN을 대조한다.\par\vspace{{0.25cm}}
Reports → Timing → Report Clocks에서 clk\_50mhz 주기 20.000 ns를 확인한다.\par\vspace{{0.25cm}}
XDC를 저장한 뒤 Run Synthesis → Run Implementation → Generate Bitstream 순서로 실행한다.
\end{{frame}}

\begin{{frame}}{{Vivado · 구현과 bit 생성}}
\captureplaceholder{{{esc(folder + '-vivado-bit')}}}{{Implementation 완료, Timing Summary의 WNS, DRC 오류 0건, bitstream 생성 완료가 확인되는 화면을 캡처한다.}}
\end{{frame}}

\begin{{frame}}[label=board]{{보드에서 확인}}
\small
전원을 끈 상태에서 외부 부품 결선과 공통 GND를 먼저 확인한다.\par\vspace{{0.25cm}}
Hardware Manager → Open Target → Auto Connect → Program Device에서 생성한 bit를 기록한다.\par\vspace{{0.25cm}}
{esc(exp['board'])}\par\vspace{{0.25cm}}
사진에는 보드 전체와 사용 핀이, 영상에는 입력 조작과 출력 변화가 함께 보이게 한다.
\end{{frame}}

\begin{{frame}}{{실험 전 레포트}}
\small
\begin{{enumerate}}
\item 동작 원리와 핵심 파라미터 계산을 자기 말로 설명한다.
\item RTL·TB·XDC 각 파일의 역할과 top module을 적는다.
\item TB 자극과 기대 결과를 표로 정리한다.
\item Icarus PASS·파형과 수정/복구 결과를 넣고 경계 조건을 설명한다.
\item 보드에서 확인해야 할 항목과 예상 결과를 적는다.
\end{{enumerate}}
\end{{frame}}

\begin{{frame}}{{실험 후 레포트와 제출}}
\small
\begin{{enumerate}}
\item XSim PASS·파형, DRC·timing·bitstream 결과를 기록한다.
\item 실제 보드 관찰, 계산값과 실측의 차이, 원인을 설명한다.
\item 결선이 보이는 사진과 동작 영상 링크를 첨부한다.
\item 자신의 GitHub 저장소 URL과 최종 commit hash를 적는다.
\item src·sim·constraints·simulation.json만 최종 원본으로 관리하고 생성물은 제외한다.
\end{{enumerate}}
\end{{frame}}

\begin{{frame}}{{완료 체크}}
\small
\begin{{itemize}}
\item[$\square$] v2.0.2 태그에서 새 프로젝트를 만들었다.
\item[$\square$] RTL·TB·XDC를 직접 작성하고 설명할 수 있다.
\item[$\square$] Icarus와 XSim에서 같은 PASS를 확인했다.
\item[$\square$] 핀·20 ns 클록·DRC·timing을 확인하고 bit를 만들었다.
\item[$\square$] 보드 동작 사진·영상과 GitHub 링크를 정리했다.
\item[$\square$] 실험 전·후 레포트에 결과와 한계를 구분해 기록했다.
\end{{itemize}}
\end{{frame}}
\end{{document}}
"""


    return re.sub(
        r'\\captureplaceholder\{([^}]+)\}\{([^\n]*)\}',
        lambda match: capture_tex(match[1].replace(r'\_', '_'), match[2]),
        document,
    )


def start_tex() -> str:
    rows = "\n".join(
        rf"{exp['number']} & {esc(exp['title'])} & \texttt{{{esc(exp['top'])}}}\\"
        for exp in EXPERIMENTS
    )
    return rf"""% !TEX program = xelatex
\input{{shared/lab3_preamble.tex}}
\hypersetup{{pdftitle={{LAB3 응용회로 공통 예습}},pdfauthor={{이해리}}}}
\begin{{document}}
\renewcommand{{\small}}{{\fontsize{{8.7}}{{10.6}}\selectfont}}
\setlength{{\leftmargini}}{{1.35em}}
\begin{{frame}}{{LAB 3 · FPGA 응용회로 공통 예습}}
\small
전자전기컴퓨터설계실험Ⅱ\par\vspace{{0.28cm}}
PWM·구동기·표시장치·직렬통신을 50 MHz 단일 클록으로 구현한다.\par\vspace{{0.28cm}}
9월 28일 실습을 위한 공통 안내\par\vspace{{0.28cm}}작성일 2026. 09. 21. · 이해리
\end{{frame}}
\begin{{frame}}[label=lab3-contents]{{목차}}
\small
\navlink{{scope}}{{01 · 7개 실험과 공통 규칙}}\par\vspace{{0.3cm}}
\navlink{{timing}}{{02 · 단일 클록·clock-enable·비동기 입력}}\par\vspace{{0.3cm}}
\navlink{{verification}}{{03 · Icarus와 XSim 검증}}\par\vspace{{0.3cm}}
\navlink{{hardware}}{{04 · Vivado 구현과 보드 안전}}\par\vspace{{0.3cm}}
\navlink{{reports}}{{05 · 실험 전후 레포트와 제출}}
\end{{frame}}
\begin{{frame}}[label=scope]{{LAB3 필수 실험}}
\small
\begin{{center}}\renewcommand{{\arraystretch}}{{1.25}}\begin{{tabular}}{{cll}}
번호 & 실험 & 설계 top\\\hline
{rows}
\end{{tabular}}\end{{center}}
7개를 개별 프로젝트로 진행한다. 통합판과 명령줄 Vivado 구현은 이번 필수 범위에 포함하지 않는다.
\end{{frame}}
\begin{{frame}}{{한 실험을 끝내는 순서}}
\small
\begin{{enumerate}}
\item v2.0.2 빈 템플릿 clone → 자신의 main 브랜치 생성.
\item RTL·TB·XDC·simulation.json 직접 작성.
\item VS Code에서 01 Check tools → 02 Simulate → 03 Open waveform.
\item 실험 전 레포트에 원리·예상값·PASS·파형·수정 실험 정리.
\item Vivado GUI에서 같은 원본으로 XSim → 합성 → 구현 → bit 생성.
\item 보드 기록 → 사진·영상·관찰 → GitHub·실험 후 레포트 제출.
\end{{enumerate}}
\end{{frame}}
\begin{{frame}}[fragile]{{공통 시작 명령}}
\small
실험마다 마지막 폴더 이름만 바꾼다.
\begin{{lstlisting}}[language={{}}]
git clone --branch v2.0.2 https://github.com/Glaysia/fpga-lab-template.git lab3_19_led_pwm
cd lab3_19_led_pwm
git switch -c main
code FPGA.code-workspace
\end{{lstlisting}}
완성 예시 저장소를 clone하는 절차가 아니다. 빈 템플릿에 교안의 원본을 직접 작성한다.
\end{{frame}}
\begin{{frame}}[label=timing]{{50 MHz 단일 클록}}
\small
최상위 입력 clk\_50mhz는 MAIN CLOCK F, 50 MHz다. 클록 주기는 20 ns다.\par\vspace{{0.28cm}}
LED PWM, 모터 step, 1초 tick, LCD tick, UART bit timing은 counter가 만드는 clock-enable로 제어한다.\par\vspace{{0.28cm}}
주파수를 parameter로 받는 하위 모듈은 일반 이름 clk를 쓸 수 있다. 분주한 일반 신호는 다른 always 블록의 clk로 사용하지 않는다.
\end{{frame}}
\begin{{frame}}{{파라미터 계산}}
\small
\begin{{center}}\renewcommand{{\arraystretch}}{{1.35}}\begin{{tabular}}{{ll}}
기능 & 기준 계산\\\hline
PWM 주기 & CLK\_HZ / PWM\_HZ\\
피에조 반주기 & CLK\_HZ / (2·TONE\_HZ)\\
모터 step 간격 & CLK\_HZ / STEPS\_PER\_SEC\\
1초 tick & CLK\_HZ 클록마다 1회\\
UART bit & 반올림한 CLK\_HZ / BAUD\\
\end{{tabular}}\end{{center}}
나눗셈 결과와 counter 범위를 계산한 뒤 parameter가 0이 되는 조건을 피한다.
\end{{frame}}
\begin{{frame}}{{비동기 입력 처리}}
\small
버튼·UART RX는 FPGA clk와 무관한 시점에 바뀐다. 첫 두 플립플롭으로 동기화한다.\par\vspace{{0.28cm}}
기계식 버튼은 동기화 뒤 안정 시간을 확인하고 눌림당 한 클록 펄스를 만든다.\par\vspace{{0.28cm}}
방향·enable 같은 레벨 입력도 두 단계 동기화를 거친다. 시뮬레이션은 메타안정성 자체가 아니라 동기화 이후의 디지털 순서를 검사한다.
\end{{frame}}
\begin{{frame}}[label=verification]{{Icarus 기능 시뮬레이션}}
\small
TB는 실제 시간 상수를 작은 parameter로 덮어써 빠르게 실행한다.\par\vspace{{0.25cm}}
정상 경로만 보지 말고 0%/100%, 자리올림, 순환, 정지, stop bit 같은 경계를 검사한다.\par\vspace{{0.25cm}}
PASS 문자열·검사 수·종료 시각과 파형을 함께 보관한다. XDC는 Icarus가 읽지 않으므로 핀 검증과 구분한다.
\end{{frame}}
\begin{{frame}}{{Vivado XSim 교차 확인}}
\small
Vivado Simulation Sources에 Icarus에서 사용한 같은 TB를 등록한다.\par\vspace{{0.25cm}}
Run Behavioral Simulation 뒤 같은 PASS marker가 나오는지 확인한다.\par\vspace{{0.25cm}}
파형에서 clk\_50mhz·rst\_p·입력·내부 counter 또는 state·출력을 함께 보고 유효 에지 전후를 설명한다.
\end{{frame}}
\begin{{frame}}{{기능 PASS의 한계}}
\small
기능 시뮬레이션은 RTL의 디지털 동작을 검증한다. 실제 핀 번호·IOSTANDARD·배선·전원·부품 특성은 포함하지 않는다.\par\vspace{{0.28cm}}
합성·구현·DRC·timing·bitstream 성공은 보드 관찰을 대신하지 않는다.\par\vspace{{0.28cm}}
레포트에서 자동검사 결과, 구현 결과, 실제 관찰을 서로 구분한다.
\end{{frame}}
\begin{{frame}}[label=hardware]{{Vivado 구현 체크}}
\small
\begin{{enumerate}}
\item Part: xc7s75fgga484-1.
\item Design top과 Simulation top을 구분한다.
\item 모든 top port에 PACKAGE\_PIN과 LVCMOS33을 적용한다.
\item clk\_50mhz에 20.000 ns create\_clock이 적용되었는지 확인한다.
\item DRC 오류 0, timing WNS 0 이상, bitstream 완료를 기록한다.
\end{{enumerate}}
\end{{frame}}
\begin{{frame}}{{외부 부품을 연결할 때}}
\small
전원을 끄고 회로와 공통 GND를 먼저 연결한다. 모터는 FPGA 핀에서 직접 구동하지 않고 드라이버와 별도 전원을 사용한다.\par\vspace{{0.28cm}}
LCD 전원·논리 전압·대비 연결을 확인한다. UART는 TX↔RX를 교차하고 전압 레벨과 GND를 확인한다.\par\vspace{{0.28cm}}
피에조·LED·7세그먼트의 극성과 보드 회로도를 확인한다.
\end{{frame}}
\begin{{frame}}[label=reports]{{실험 전 레포트}}
\small
회로 목적, 블록 흐름, 파라미터 계산, 상태 또는 타이밍 표를 적는다.\par\vspace{{0.25cm}}
RTL·TB·XDC의 역할을 설명하고 TB 자극과 기대 결과를 표로 만든다.\par\vspace{{0.25cm}}
Icarus PASS와 파형, 한 항목 수정 실험과 복구 결과를 넣는다. 실제 보드에서 확인할 항목을 미리 적는다.
\end{{frame}}
\begin{{frame}}{{실험 후 레포트와 GitHub}}
\small
XSim PASS·파형, 핀·DRC·timing·bitstream 결과를 기록한다.\par\vspace{{0.25cm}}
실제 보드 사진과 입력부터 출력까지 보이는 영상, 관찰값과 예상값의 차이를 설명한다.\par\vspace{{0.25cm}}
GitHub URL과 최종 commit hash를 넣는다. 생성된 build·Vivado 파일을 소스처럼 commit하지 않는다.
\end{{frame}}
\end{{document}}
"""


def contents_tex() -> str:
    first = EXPERIMENTS[:4]
    second = EXPERIMENTS[4:]

    def links(items: list[dict]) -> str:
        return "\n".join(
            rf"\href{{{pdf_name(exp)}}}{{{exp['number']} · {esc(exp['title'])}}}\par\vspace{{0.34cm}}"
            for exp in items
        )

    return rf"""% !TEX program = xelatex
\input{{shared/lab3_preamble.tex}}
\hypersetup{{pdftitle={{LAB3 전체 목차}},pdfauthor={{이해리}}}}
\begin{{document}}
\renewcommand{{\small}}{{\fontsize{{9}}{{11}}\selectfont}}
\begin{{frame}}{{LAB 3 · 전체 목차}}
\small
FPGA 응용회로 7개 · Vivado 2026.1\par\vspace{{0.3cm}}
작성일 2026. 09. 21. · 이해리\par\vspace{{0.3cm}}
공통 예습 → 개별 회로 → Icarus → XSim → 보드 실험 순서로 읽는다.
\end{{frame}}
\begin{{frame}}[label=lab3-contents]{{자료 사용법}}
\small
모든 PDF를 같은 폴더에 둔다. 각 PDF 좌하단 목차 버튼은 해당 PDF의 2쪽으로 이동한다.\par\vspace{{0.3cm}}
먼저 \href{{06.LAB3_00_START.pdf}}{{공통 예습}}을 읽고 자신이 맡은 실험 PDF를 연다.\par\vspace{{0.3cm}}
화면 캡처 칸의 ID는 촬영 목록과 일치한다. 화면 조작 단계에서 실제 캡처로 교체한다.
\end{{frame}}
\begin{{frame}}{{개별 매뉴얼 · 19–22}}
\small
{links(first)}
\end{{frame}}
\begin{{frame}}{{개별 매뉴얼 · 23–25}}
\small
{links(second)}
\end{{frame}}
\end{{document}}
"""


def tex_name(exp: dict) -> str:
    return f"06.LAB3_{exp['index']:02d}_{exp['slug']}_VIVADO.tex"


def pdf_name(exp: dict) -> str:
    return tex_name(exp).replace(".tex", ".pdf")


def readme_text() -> str:
    rows = "\n".join(
        f"| {exp['number']} | [{exp['title']}]({pdf_name(exp)}) | [{tex_name(exp)}]({tex_name(exp)}) | `{exp['pass_marker']}` |"
        for exp in EXPERIMENTS
    )
    return f"""# LAB3 · 9월 28일 FPGA 응용회로 실습

작성일: 2026-09-21. 필수 범위는 개별 실험 7개다. 통합판과 명령줄 Vivado 구현은 자동으로 추가하지 않는다.

[전체 목차](06.LAB3_00_CONTENTS.pdf) · [공통 예습](06.LAB3_00_START.pdf)

## 매뉴얼

| 번호 | 자료 | 원고 | 기능 시뮬레이션 기준 |
|---:|---|---|---|
{rows}

학생은 [`fpga-lab-template` v2.0.2](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.2)를 실험별 새 폴더로 clone하고, 매뉴얼을 보며 RTL·TB·XDC·`simulation.json`을 직접 작성한다. VS Code에서는 Icarus, Vivado에서는 같은 원본과 TB로 XSim을 실행한다. 구현 뒤 실제 보드 사진·영상·GitHub 링크를 실험 후 레포트에 넣는다.

현재 원고에는 코드 전체, 핀, 검증 절차, 보드 절차, 실험 전후 레포트 기준이 들어 있다. GUI 화면은 `required-captures.json`의 ID와 같은 자리표시자로 남겨 두었으며 다음 화면 촬영 단계에서 실제 캡처로 교체한다.

## 빌드

`LAB3_FPGA_0928` 폴더에서 XeLaTeX로 각 원고를 두 번 빌드한다. 생성 PDF는 같은 폴더에 둔다.

```powershell
python tools/generate_lab3_docs.py
Get-ChildItem 06.LAB3_*.tex | ForEach-Object {{ xelatex -interaction=nonstopmode -halt-on-error $_.Name }}
```

## 검증 기준

- 4:3 PDF, 내부 목차 이동, 전체 목차의 PDF 간 링크.
- Icarus와 XSim 모두 7개 TB의 PASS marker 확인.
- Vivado 2026.1에서 xc7s75fgga484-1 대상으로 합성·구현·DRC·timing·bitstream 확인.
- 실제 보드 동작은 학생 실험 단계이며 자동 시뮬레이션 결과와 구분한다.
"""


def main() -> None:
    DOC.mkdir(parents=True, exist_ok=True)
    (DOC / "06.LAB3_00_START.tex").write_text(start_tex(), encoding="utf-8", newline="\n")
    (DOC / "06.LAB3_00_CONTENTS.tex").write_text(contents_tex(), encoding="utf-8", newline="\n")
    captures: list[dict] = []
    for exp in EXPERIMENTS:
        (DOC / tex_name(exp)).write_text(manual_tex(exp), encoding="utf-8", newline="\n")
        for kind, description in [
            ("vscode-workspace", "VS Code workspace와 작성 파일"),
            ("vscode-pass", "Icarus PASS와 종료 시각"),
            ("vscode-wave", "핵심 신호 waveform"),
            ("vivado-sources", "Vivado Sources, top, XDC"),
            ("xsim-pass", "XSim PASS와 waveform"),
            ("vivado-bit", "DRC, timing, bitstream 완료"),
        ]:
            captures.append({
                "id": f"{exp['folder']}-{kind}",
                "experiment": exp["number"],
                "project": exp["folder"],
                "description": description,
            })
    (DOC / "required-captures.json").write_text(
        json.dumps({"version": 1, "count": len(captures), "captures": captures}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (DOC / "README.md").write_text(readme_text(), encoding="utf-8", newline="\n")
    print(f"generated 2 common documents, {len(EXPERIMENTS)} manuals, {len(captures)} capture slots")


if __name__ == "__main__":
    main()
