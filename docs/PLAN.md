# skillallabout 작업 프로젝트 계획

> 코딩·영상·작문·대본·자료수집·광고 등 **모든 작업에서 편하게 쓰는 Claude 스킬 백과**.
> 스킬마다 **용도 · 사용 방법(예시 문장) · 설치 방법**을 한 화면에서 보고 바로 복사한다.

> **이 문서가 있는 곳** — 원본은 저장소 `docs/PLAN.md`
> (`C:\Users\T470\OneDrive\문서\GitHub\skillallabout\docs\PLAN.md`).
> 옵시디언 볼트 `1. Project/skillallabout/`에는 카드 · 진행 절차 · 할 일이 있고, 프로젝트 대시보드는 그 폴더를 읽는다.
> 계획이 바뀌면 이 파일을 고치고, 볼트의 [[할 일]]에 체크한다.

## 1. 역할 분담

| 담당 | 하는 일 | 결과물 |
|---|---|---|
| **제미나이** | 유튜브·구글·GitHub·플러그인 마켓에서 스킬 수집, 사이트 디자인 시안 작성 | `data/gemini/*.json`, `docs/design-proposal.md` |
| **Claude** | 스킬 분류(14개 분야), 예시 문장·설치 방법 작성, 디자인 시안을 코드로 반영, 사이트 코딩·검증 | `tools/build_skills.py`, `index.html`, `assets/*` |
| **현진** | 제미나이에 지시서 전달, 결과 파일 넣기, 최종 확인, GitHub에 푸시 | 커밋 |

## 2. 데이터 흐름

```
구글 시트 '대표 Claude 스킬 정리'  ──CSV──▶  data/skills_source.csv ─┐
제미나이 수집 결과  ─────────────────────▶  data/gemini/*.json     ─┤
                                                                     ▼
                                          python tools/build_skills.py
                                          (중복 합치기 · 분야 분류 · 설치법 생성)
                                                                     ▼
                                     data/skills.json  +  data/skills.js  ──▶  index.html
```

- 같은 GitHub 주소는 한 장으로 합치고, '설치됨' 행이 있으면 ✓ 설치됨 표시.
- 설치 방법은 주소 모양으로 자동 결정: 공식 마켓 / 저장소 설치 / 폴더 복사 / 기본 제공 / 내 계정 / 주소 확인 필요.
- 예시 문장과 분야는 `tools/build_skills.py` 의 `INFO` 표에서 관리 (없으면 경고 출력).

## 3. 단계별 일정

### 1단계 — 기반 만들기 ✅ (2026-11-25 완료)
- [x] 시트 130행 → 중복 정리 후 120개 스킬, 14개 작업 분야로 분류
- [x] 스킬마다 예시 문장 + 설치 방법 작성
- [x] 사이트: 검색(한국어 별칭: 쇼츠·엑셀·대본…), 분야/출처/설치됨/즐겨찾기 필터, 상세 패널, 복사 버튼, 링크 공유(#skill=)
- [x] 작업 레시피 10개 (쇼츠, 대본, 블로그, 조사 보고서, 광고 소재, 코딩, 업무 문서, 중고판매, 취업, 스킬 만들기)
- [x] 설치 가이드 화면
- [x] 제미나이 작업 지시서 (`docs/GEMINI_TASK.md`)
- [x] 카톡 메모의 pstack 명령 목록을 제미나이 형식 예시로 추가 (주소는 미확인)

### 2단계 — 제미나이 1차 수집 (11/26 ~ 11/30)
- [ ] `docs/GEMINI_TASK.md` 를 제미나이에 전달 → 1회차 30~50개
- [ ] 결과 JSON을 `data/gemini/` 에 저장 → `python tools/build_skills.py`
- [ ] Claude가 분류 검토, 예시 문장 다듬기, `INFO` 표에 반영
- [ ] 우선 분야: 광고·마케팅(현재 9개), 대본(8개), 작문(11개) → 각 20개 이상
- [ ] pstack 저장소 주소 찾기

### 3단계 — 디자인 개선 ✅ (2026-11-25 완료, 제미나이 시안 A~G 전부 반영)
- [x] A 첫 화면 빠른 분야 버튼 5개(광고·대본·작문·영상·한국어 업무) + 추천 키워드
- [x] B 카드 간단히(분야 2개) + '한국어 친화' · '별 적음' 배지
- [x] C 상세 패널 설치 방법 탭(claude.ai 앱 / Claude Code 마켓 / 폴더 복사, 고른 탭 기억)
- [x] D '추천 받기' 탭 — 질문 3개로 스킬 5개 + 레시피 1개
- [x] E '새로 들어온' 탭 — 수집 회차별 묶음
- [x] F 검색 결과가 2개 이하면 관련 레시피 제안
- [x] G 색 다듬기(흰 카드, 초록 보조색) · 스킬 이름 JetBrains Mono

### 4단계 — 배포 (12/6 ~)
- [ ] GitHub에 푸시 → 저장소 Settings → Pages → `main` 브랜치 `/ (root)` 로 공개
- [ ] 휴대폰에서 확인 (rea비서 카톡으로 링크 받아 보기)
- [ ] 옵시디언 볼트 프로젝트 노트에 링크 연결

### 5단계 — 운영 (매주)
- [ ] 매주 1회 제미나이 수집 회차 추가 → 빌드 → 푸시
- [ ] 직접 만든 스킬(resale-listing 등)은 '내 스킬'로 시트에 추가
- [ ] 깨진 링크·오래된 스킬 정리

## 4. 폴더 구조

```
skillallabout/
├─ index.html              사이트 (GitHub Pages 시작 파일)
├─ assets/style.css        디자인
├─ assets/app.js           검색·필터·상세 패널·복사
├─ data/
│  ├─ skills_source.csv    구글 시트 원본 (여기를 고치거나 시트에서 다시 내보내기)
│  ├─ gemini/*.json        제미나이 수집 결과 (회차별 파일)
│  ├─ recipes.js           작업 레시피 (손으로 관리)
│  ├─ skills.json/.js      ← 자동 생성, 직접 고치지 말 것
├─ tools/build_skills.py   데이터 빌드
└─ docs/
   ├─ PLAN.md              이 문서
   └─ GEMINI_TASK.md       제미나이 지시서
```

## 5. 자주 쓰는 명령

```bash
python tools/build_skills.py        # 데이터 다시 만들기
python -m http.server 8000          # 내 컴퓨터에서 미리보기 → http://localhost:8000
git add . && git commit -m "스킬 추가" && git push
```

`index.html` 을 그냥 더블클릭해도 열립니다 (데이터를 .js로 넣어 둬서 서버 없이 동작).
