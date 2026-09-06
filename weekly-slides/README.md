# 주차별 발표 자료

`weekly_presentation.tex`은 `reference/Ch3.pdf`의 16:9 구성(파란 표지, 흰 본문, 파란 제목, 하단 소속/페이지 표기)을 따라 만든 XeLaTeX Beamer 템플릿이다.

컴파일 명령:

```powershell
cd weekly-slides
xelatex weekly_presentation.tex
```

발표마다 파일을 복사한 뒤, 파일 위쪽의 `\week`, `\course`, `\presenter`, `\presentationdate`와 각 슬라이드 내용을 바꾸면 된다. 그림은 `images/` 폴더를 만들어 넣고 `\includegraphics`로 삽입한다.
