# skillallabout · 스킬 올어바웃

코딩, 영상제작, 작문, 대본, 자료수집, 광고까지 — **Claude 스킬을 작업별로 찾고, 쓰는 법과 설치법을 바로 복사**하는 사이트.

- 🔎 **스킬 찾기**: 검색 + 14개 작업 분야 + 출처·설치됨·즐겨찾기 필터
- 📋 **상세 패널**: 용도 / "이렇게 말해 보세요" 예시 문장 / 설치 단계와 명령 복사 / GitHub 링크
- 🧭 **작업 레시피**: 쇼츠 만들기, 대본, 블로그, 조사 보고서, 광고 소재, 코딩 등을 스킬 순서로
- 🛠 **설치 가이드**: claude.ai 업로드 / Claude Code 플러그인 마켓 / 폴더 복사

## 바로 보기
`index.html` 더블클릭, 또는 `python -m http.server 8000` 후 http://localhost:8000

## 스킬 추가하기
1. 구글 시트에 행 추가 후 CSV로 내보내 `data/skills_source.csv` 교체, 또는
2. 제미나이 수집 결과를 `data/gemini/` 에 JSON으로 저장 (형식: `docs/GEMINI_TASK.md`)
3. `python tools/build_skills.py`

계획과 역할 분담은 [docs/PLAN.md](docs/PLAN.md).
