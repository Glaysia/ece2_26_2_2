# LAB2 · 9월 21일 순차논리 실습

작성일 2026-09-10. TeX가 원본이며 PDF는 TeX에서 빌드한다.

- [공통 예습 PDF · 26쪽](05.LAB2_00_START.pdf)
- [편집용 TeX](05.LAB2_00_START.tex)
- [제작 목표와 남은 항목](../../../daily_goal/GOAL0910_LAB2.md)
- [8개 기능 예시와 시뮬레이션 결과](../../../example/fpga_projects_hdl/LAB2/README.md)
- [공통 PDF 검수 기록](intro-review.json)

공통 예습 자료에는 클록·리셋·이전 값 전달·버튼 입력, 8개 실험의 기대 동작, 시뮬레이션과 레포트 기준을 담았다. 개별 회로 전체 코드 화면과 Vivado 단계별 자료는 제작 중이며 이 PDF만으로 전체 실습 자료가 완성된 것은 아니다.

수업 저장소 루트에서 생성기와 빌드기를 실행한다.

```powershell
python weekly-slides/tools/lab2_intro.py
python weekly-slides/tools/build_lab2_series.py
```

빌드 출력은 `tmp/lab2-build/`다. 원고 폴더에 오래된 aux·nav 등을 남기면 빌드기가 중단한다. 렌더 검수 후 PDF만 이 폴더로 복사한다. 새 PNG는 기존 ignore 정책을 따른다.
