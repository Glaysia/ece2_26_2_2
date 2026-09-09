# VS Code 사전 시뮬레이션 캡처

2026-09-10 제작 PC의 VS Code 새 창에서 캡처했다. 원본 스크린샷 PNG는 로컬 빌드 자료이며 Git에서 무시한다. 코드는 LAB1/common의 실제 파일과 일치한다.

검증: XSim 2026.1에서 00 → 10 → 01 → 11, 각 200ns, 800ns 종료 및 네 조합 PASS. 시뮬레이션 스크립트는 명령 실행 도구로 실행했으며, VS Code에서는 workspace·작업 선택 메뉴·실행 로그·VaporView 파형을 확인했다. GUI 작업 버튼으로 실행했다는 증빙은 아니다.

공식 안내: [workspace](https://code.visualstudio.com/docs/editing/workspaces/workspaces), [Tasks](https://code.visualstudio.com/docs/debugtest/tasks), [VaporView](https://github.com/Lramseyer/vaporview).

추가 검증: 공백을 포함한 다른 경로에서 정상 실행, AND를 OR로 바꾼 임시 사본의 실패 검출, 실패 시 이전 공개 VCD 제거를 확인했다.
