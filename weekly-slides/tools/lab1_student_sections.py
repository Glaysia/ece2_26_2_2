"""Shared student-authored setup sections, including the detailed first manual."""
from lab1_series import BASE, Deck, PROJECTS, student_setup, student_constraints, para, items, esc


def terminal(*commands):
    return '\\terminalbox{'+r'\\'.join(esc(line) for line in commands)+'}\n'


def main():
    p=PROJECTS[0]
    d=Deck('modern01','논리 게이트 직접 작성')
    student_setup(d,p)
    d.pages=[page.replace('lab1\\_vivado\\_2026\\_1\\_01\\_logic\\_gates','lab1\\_01\\_logic\\_gates') for page in d.pages]
    replacement=Deck('modern01','시작')
    replacement.frame('시뮬레이션 도구 확인',para('Git·Python 3.10 이상·VS Code·Icarus Verilog를 설치한다. Windows PowerShell에서 한 줄씩 실행한다.')+terminal('git --version','python --version','iverilog -V','vvp -V')+para('설치 경로를 PATH에 추가했다면 VS Code를 다시 연다. Linux·macOS·WSL은 python 대신 python3를 사용한다.'),'modern01-setup')
    replacement.frame('v2.0.0 템플릿을 새 이름으로 clone',para('아래는 Windows PowerShell 명령이다. 첫 줄 끝의 백틱(backtick)은 명령을 다음 줄로 이어 준다.')+terminal('git clone --branch v2.0.0 `','  https://github.com/Glaysia/fpga-lab-template.git lab1_01_logic_gates','cd lab1_01_logic_gates','git switch -c main','code LAB1.code-workspace')+para('태그로 같은 시작 파일을 받는다. git switch는 태그에서 학생 작업용 main 브랜치를 만든다. 다음 회로는 목적지 폴더 이름을 바꾼다.'))
    d.pages[:2]=replacement.pages
    (BASE/'sections/modern01_student_setup.tex').write_text('\n'.join(d.pages),encoding='utf-8')
    d=Deck('modern01','직접 수정하고 검증')
    d.frame('XOR를 바꾸고 실패를 확인한다',items([
        'src/logic_gate.v에서 XOR 연산자 ^를 OR 연산자 |로 바꾼다.',
        '어떤 입력에서 결과가 달라질지 진리표에 먼저 표시한다.',
        'File → Save All → Terminal → Run Task... → 02 Simulate.',
        '실패 로그에서 입력 벡터·expected·actual을 읽고 예상한 오류인지 설명한다.',
        '연산자를 ^로 복구하고 저장한 뒤 02를 다시 실행한다.',
        'cases=4 통과와 새 파형을 확인하고 실패·복구 증빙을 남긴다.'
    ])+para('TB의 예상값은 함께 바꾸지 않는다. 설계만 바꿨을 때 검사가 오류를 찾아야 한다.'))
    student_constraints(d,p)
    d.frame('XDC 전체 내용 · 1--12행',para('constraints/logic_gate.xdc를 열고 아래 내용을 직접 입력한다.')+r'\shot{xdc-student}'+para('a=K4, b=N8, x=L4, y=M4, z=M2이며 다섯 포트 모두 LVCMOS33이다.','마지막 a 핀 지정까지 입력하고 Save All. Icarus는 이 파일을 읽지 않으므로 Vivado에서 핀도 확인한다.'))
    (BASE/'sections/modern01_student_edit.tex').write_text('\n'.join(d.pages),encoding='utf-8')


if __name__=='__main__':main()
