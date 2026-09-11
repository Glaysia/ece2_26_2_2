# 전자전기컴퓨터설계실험Ⅱ

2026학년도 2학기 FPGA·STM32 실습 강의자료 저장소.

조건을 판단하고, 상태를 기억하고, 동작을 반복하는 시스템을 회로와 프로그램으로 구현하고 검증한다.

## 자료 찾기

- [강의자료 목록](weekly-slides/README.md): OT, 레거시 HDL 교재, 설치·환경설정 매뉴얼의 TeX와 PDF.
- [LAB1 자료](weekly-slides/weekly-slides/LAB1_FPGA_0914/README.md): 22개 매뉴얼·PDF 묶음. [프로젝트·workspace](example/fpga_projects_hdl/LAB1/README.md) · [학생용 템플릿](https://github.com/Glaysia/fpga-lab-template) · [검증 현황](example/fpga_projects_hdl/LAB1/docs/validation.md).
- [문서 관리 및 남은 작업](docs/README.md): 미반영 초안과 과거 기록.

- [LAB2 자료](weekly-slides/weekly-slides/LAB2_FPGA_0921/README.md): 순차논리 실습. [첫 카운터 완성 PDF](weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_01_COUNTER_VIVADO.pdf) · [40개 예시 소스 바로가기](example/fpga_projects_hdl/README.md).

## 원본 관리 원칙

**강의 내용의 단일 원본(SSOT)은 각 자료의 TeX다.**

- 수업 안내·실습 설명·제출 요건을 고칠 때는 해당 TeX를 수정한다.
- PDF는 TeX에서 빌드한 열람·배포본이다. PDF를 별도로 편집하지 않는다.
- README는 파일 안내, 편집·빌드 방법, 현재 상태만 관리한다. 강의 본문을 복제하지 않는다.
- Markdown 초안은 확정 자료가 아니다. 필요한 내용을 검토해 TeX에 반영한다.
- 기존 Markdown과 TeX의 내용이 다르면 TeX를 기준으로 확인한다. 초안의 미확정 정책을 임의로 확정하지 않는다.

## 디렉터리

```text
weekly-slides/
  weekly-slides/   # LAB·PROJECT별 TeX, PDF, 개별 리소스
  templates/       # 공용 발표 템플릿
  assets/          # 공용 로고·글꼴
docs/
  README.md        # 문서 분류와 남은 작업
  drafts/          # TeX 반영 검토용 초안
  archive/         # 과거 구상·작업 기록·이전 원고
legacy/            # 기존 교육자료 (원자료 보존)
example/           # LAB1 22개·LAB2 18개 예시 서브모듈·검증 증빙
```

현재의 중첩된 `weekly-slides/weekly-slides/` 경로는 TeX의 상대경로 참조를 유지하기 위해 그대로 둔다. 로컬 참고자료 `reference/`와 임시 작업 `tmp/`는 Git 제외 대상이다.

## 편집과 빌드

[강의자료 README](weekly-slides/README.md)의 빌드 안내를 따른다. 템플릿과 공용 리소스는 재사용하고, 자료별 입력 이미지도 함께 확인한다.

현재 레거시 HDL 교재는 기존 PDF를 볼 수 있지만, 코드 캡처가 있던 프로젝트 삭제로 재빌드가 막혀 있다. 자세한 상태는 [교재 편집 안내](weekly-slides/weekly-slides/LAB0_OT_0907/00.legacy_hdl.README.md)를 참고한다.
