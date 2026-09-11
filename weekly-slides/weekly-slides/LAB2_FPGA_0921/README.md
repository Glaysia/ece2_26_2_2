# LAB2 · 9월 21일 순차논리 실습

작성일 2026-09-10. TeX가 원본이며 PDF는 TeX에서 빌드한다.

- [공통 예습 PDF · 26쪽](05.LAB2_00_START.pdf)
- [편집용 TeX](05.LAB2_00_START.tex)
- [제작 목표와 남은 항목](../../../daily_goal/GOAL0910_LAB2.md)
- [18개 공개 예시와 검증 결과](../../../example/fpga_projects_hdl/LAB2/README.md)
- [공통 PDF 검수 기록](intro-review.json)

공통 예습 자료에는 클록·리셋·이전 값 전달·버튼 입력, 8개 실험의 기대 동작, 시뮬레이션과 레포트 기준을 담았다. 개별 회로 전체 코드 화면과 Vivado 단계별 자료는 제작 중이며 이 PDF만으로 전체 실습 자료가 완성된 것은 아니다.

수업 저장소 루트에서 생성기와 빌드기를 실행한다.

```powershell
python weekly-slides/tools/lab2_intro.py
python weekly-slides/tools/build_lab2_series.py
```

빌드 출력은 `tmp/lab2-build/`다. 원고 폴더에 오래된 aux·nav 등을 남기면 빌드기가 중단한다. 렌더 검수 후 PDF만 이 폴더로 복사한다. 새 PNG는 기존 ignore 정책을 따른다.

## 첫 카운터 완성본 · 2026-09-11

- [VS Code → Vivado 2026.1 · 75쪽 PDF](05.LAB2_01_COUNTER_VIVADO.pdf) · [TeX](05.LAB2_01_COUNTER_VIVADO.tex)
- 20쪽 언어 서버 정상 상태 재촬영, RTL·TB·XDC 입력 화면과 GUI 구현 절차 포함.
- VS Code·Vivado 각 36개 검사, 356 ns 종료와 실제 비트스트림 생성을 확인했다. 물리 보드 기록·촬영은 학생 실험 절차로 구분했다.
- 첫 매뉴얼 생성기는 `weekly-slides/tools/lab2_counter_complete.py`다. 전체 생성기로 덮어쓰지 않는다.

## 나머지 개별 매뉴얼 제작 상태

18개 TeX 원고(최신 8·레거시 8·통합 2)는 총 1,113쪽이다. 레거시 원본 221쪽과 기존 실제 GUI 화면을 출처 차이와 함께 연결했다. 첫 카운터용 실제 코드 캡처 12개는 확보·검수했다. 나머지 매뉴얼의 코드 캡처와 최종 검수는 남아 있다. 초안 PDF를 완성 배포본으로 복사하지 않는다.

- [전체 목차 원고](05.LAB2_00_CONTENTS.tex)
- [원고별 페이지·미완료 상태](series-inventory.json)
- [필요한 코드 캡처·행 범위·소스 해시](required-code-captures.json)
- [레거시 페이지 출처](legacy-page-provenance.json)

실제 캡처를 넣은 뒤 전체를 다시 빌드하고 모든 페이지를 시각 검수한다. `final-visual-review.json`에 각 PDF와 TeX 해시 및 전체 페이지 검수 기록을 남긴 후 `python weekly-slides/tools/package_lab2_pdfs.py`를 실행한다. 이 도구는 미완료 표시·누락 캡처·검수 기록·4:3·목차·상대 링크를 확인하고 ZIP을 새로 풀어 다시 검사한다.

초안 구조 검사는 전체 빌드 후 `python weekly-slides/tools/audit_lab2_drafts.py`로 실행한다. 각 PDF의 실제 페이지 수·4:3·페이지별 목차·다른 PDF의 목적지·누락 표시 수·소스 해시를 확인한다. 이 결과는 전체 페이지 시각 검수나 배포 승인이 아니다.
