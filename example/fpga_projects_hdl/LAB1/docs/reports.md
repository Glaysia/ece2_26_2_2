# 실험 전·후 레포트와 GitHub 제출

[전체 프로젝트](../README.md) · [사전 양식](../reports/pre/TEMPLATE.md) · [사후 양식](../reports/post/TEMPLATE.md) · [첫 회로 사전 예시](../reports/pre/01_logic_gates.md) · [첫 회로 사후 예시](../reports/post/01_logic_gates.md)

실험 전 레포트는 VS Code에서 시뮬레이션하고 파형을 해석한 상태까지 작성합니다. 실험 후 레포트는 Vivado 시뮬레이션·합성·구현·비트스트림·실제 보드 기록·사진·영상을 포함합니다. 학생 본인의 실행 결과로 작성하고 교재 캡처를 자신의 실행 증거로 쓰지 않습니다.

## 폴더와 링크

각 학생 저장소에서 아래 구조를 권장합니다. 회로마다 번호를 붙이고 커밋 URL을 기록합니다. 템플릿의 `.gitignore`는 생성 캐시를 제외하지만 `evidence/`와 `reports/`의 사진·Markdown·검증 자료는 추적할 수 있습니다. 강의자료 제작 저장소의 PNG 무시 정책과 구분합니다.

```text
reports/pre/01_logic_gates.md
reports/post/01_logic_gates.md
evidence/01/vscode/simulation.txt
evidence/01/vscode/wave.vcd
evidence/01/vscode/wave.png
evidence/01/vivado/simulation.txt
evidence/01/vivado/wave.png
evidence/01/vivado/implementation.png
evidence/01/board/programmed.png
evidence/01/board/photos/input-11.jpg
evidence/01/board/videos/demo.mp4
```

Markdown 사진은 `![입력 11에서 AND·OR 점등](../../evidence/01/board/photos/input-11.jpg)`처럼 상대경로로 넣습니다. 영상은 `[동작 영상](../../evidence/01/board/videos/demo.mp4)`로 연결하고 레포트에 확인할 시간 구간을 적습니다. GitHub 미리보기에서 재생되지 않으면 파일 다운로드 또는 접근 가능한 영상 서비스 링크를 제공합니다. 대용량 영상은 GitHub Release 첨부나 별도 영상 링크로 관리하고 파일명·커밋·해시를 함께 기록합니다.

## VS Code에서 업로드

1. 자신의 GitHub 저장소를 만들고 clone한 폴더에서 작업합니다. 다른 사람 저장소로 push하지 않습니다.
2. Source Control 아이콘에서 Changes 목록을 열고 레포트·자신의 증빙·수정 소스를 확인합니다. 빌드 캐시가 섞이면 `.gitignore`를 정리합니다.
3. 필요한 파일 옆 `+`로 Stage Changes를 누릅니다. 메시지에 회로와 검증 내용을 쓰고 Commit.
4. Publish Branch 또는 Sync Changes를 눌러 자신의 원격 저장소에 올립니다.
5. 브라우저에서 커밋과 레포트를 열고 사진 표시, 로그 다운로드, 영상 접근을 직접 확인합니다.
6. 레포트에 소스 커밋 URL, 증빙 URL, bit SHA-256과 실험 날짜를 적습니다.

실패한 실험도 원인·수정·재실행으로 설명합니다. 아직 연결하지 않은 보드는 `미수행`으로 기록하고 시뮬레이션이나 bit 생성 결과를 실측으로 바꾸어 쓰지 않습니다.
