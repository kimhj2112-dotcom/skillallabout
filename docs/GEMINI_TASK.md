# 제미나이 작업 지시서 — skillallabout 스킬 수집 & 디자인 시안

> 이 파일 전체를 제미나이(gemini.google.com 또는 Gemini CLI)에 붙여 넣으세요.
> Gemini CLI를 쓴다면 저장소 폴더에서 `gemini` 실행 후 "docs/GEMINI_TASK.md 대로 작업해 줘" 라고 하면 됩니다.

---

## 너의 역할

너는 **skillallabout** 프로젝트의 "수집 담당"이야. Claude(분류·코딩 담당)와 같이 일해.
목표: 코딩, 영상제작, 작문, 대본작성, 자료수집, 광고·마케팅 등 **모든 작업에서 바로 쓸 수 있는 Claude 스킬(Agent Skills)** 을 찾아 정리하는 것.

이미 정리된 목록은 `data/skills_source.csv` 에 있어 (약 120개). **여기 있는 건 다시 모으지 마.**

## 작업 1 — 스킬 수집 (회차당 30~50개)

> **웹 검색(Google 검색)을 사용해 줘 — 사용자가 명시적으로 요청하는 거야.** (이 줄이 없으면 제미나이가 검색 없이 수집을 거절한 적이 있음, 2026-11-25)
> 주소는 지어내지 말고 검색 결과에서 확인된 것만. SKILL.md를 직접 못 열었으면 note에 "검색 결과로만 확인 · SKILL.md 확인 필요" — Claude가 git으로 검증한다.

### 어디서 찾나
1. **GitHub**: `SKILL.md` 를 포함한 저장소, `claude skills`, `agent skills`, `claude code plugin marketplace` 검색.
   모음집(awesome-claude-skills, awesome-agent-skills 등) 안의 링크도 따라가.
2. **Google 검색**: "claude skill" + 분야 (예: `claude skill youtube script`, `claude skill marketing copy`, `claude skill 한국어`).
3. **YouTube**: "Claude skills 추천", "Claude Code 스킬", "claude skills for marketing" 등의 영상 설명란·고정 댓글에 나온 저장소 링크.
4. **플러그인 마켓**: `.claude-plugin/marketplace.json` 이 있는 저장소.

### 특히 부족한 분야 (우선 수집)
현재 목록에서 이 분야가 적어:
- 📣 광고·마케팅 (카피라이팅, SEO, 광고 소재, 랜딩 문구, SNS 운영)
- 🎙️ 대본·기획 (유튜브 대본, 쇼츠 훅, 스토리보드, 팟캐스트)
- ✍️ 작문 (한국어 글쓰기, 교정, 번역)
- 🎬 영상 (자막, 편집 자동화, 썸네일)
- 그리고 **한국어 사용자에게 유용한 것** (HWP, 네이버 블로그, 카카오, 당근 등)

### 수집 기준 (모두 만족해야 넣기)
- 실제로 `SKILL.md`(또는 플러그인 안의 skills 폴더)가 있다 — 링크를 열어 확인
- 최근 1년 안에 업데이트됐다
- 설명만 있고 코드가 없는 "준비 중" 저장소는 제외
- 별(star) 수가 적어도 쓸모가 분명하면 OK. 대신 `note` 에 "별 적음"이라고 적기
- 의심스러운 것(실행 파일만 있음, 비밀키 요구가 이상함)은 넣지 말고 `rejected` 에 이유와 함께 적기

### 결과 형식 (꼭 이 JSON 형식으로)
파일 이름: `data/gemini/YYYY-MM-DD-회차.json` (예: `data/gemini/2026-11-26-01.json`)

```json
{
  "collected_by": "Gemini",
  "collected_at": "2026-11-26",
  "skills": [
    {
      "name": "스킬 이름 (저장소의 skill name 그대로)",
      "author": "만든 사람 또는 조직",
      "url": "https://github.com/소유자/저장소/tree/main/skills/폴더  ← SKILL.md가 있는 폴더 주소",
      "source": "커뮤니티",
      "group": "커뮤니티 · 마케팅",
      "areas": ["marketing", "writing"],
      "purpose": "한 줄 기능 설명 (한국어, 40자 안팎)",
      "example": "사용자가 Claude에게 할 말 예시 (한국어, 실제 상황처럼)",
      "note": "API 키 필요 여부, 유료 여부, 주의할 점",
      "sources_found": ["어디서 발견했는지: 유튜브 영상 제목/URL, 검색어 등"]
    }
  ],
  "rejected": [
    { "name": "...", "url": "...", "reason": "SKILL.md 없음" }
  ]
}
```

`areas` 에 쓸 수 있는 값 (1~3개):
`code`(코딩·개발) `video`(영상·미디어) `writing`(작문) `script`(대본·기획) `research`(자료수집) `marketing`(광고·마케팅) `docs`(문서·오피스) `design`(디자인) `data`(데이터·분석) `learn`(학습) `collab`(협업·업무) `security`(보안) `automation`(자동화) `meta`(스킬 만들기)

> 분류는 Claude가 최종 검토해. 애매하면 너의 판단을 적고 `note` 에 "분류 확인 필요"라고 남겨.

## 작업 2 — 사이트 디자인 시안

지금 사이트(`index.html`, `assets/style.css`)는 이런 구조야:
- **스킬 찾기**: 검색창 + 분야 칩 + 출처 필터 + 카드 그리드 → 카드를 누르면 오른쪽에 상세 패널(용도 / 이렇게 말해 보세요 / 설치 방법 / GitHub 링크)
- **작업 레시피**: "쇼츠 만들기" 같은 일을 스킬 순서로 보여 주는 카드
- **설치 가이드**: claude.ai / Claude Code 마켓 / 폴더 복사 3가지 방법

이걸 보고 `docs/design-proposal.md` 에 아래를 써 줘:
1. **첫 화면 개선안** — 처음 온 사람이 3초 안에 "내 일에 맞는 스킬"을 찾게 하려면? (와이어프레임을 텍스트/ASCII로)
2. **카드·상세 패널 개선안** — 어떤 정보를 더/덜 보여 줄지
3. **새 화면 아이디어 1~2개** (예: "질문 몇 개 답하면 스킬 추천", "이번 주 새로 들어온 스킬")
4. **색·글꼴 제안** — 지금은 따뜻한 종이색 배경 + 주황 포인트 + Pretendard. 바꾸자면 이유와 함께 색상 코드로
5. 참고한 사이트가 있으면 링크

HTML 코드는 안 써도 돼. **Claude가 시안을 보고 코드로 옮겨.**

## 끝나면
- 새로 만든 JSON 파일 이름, 수집 개수, 분야별 개수, 제외한 개수를 요약해서 알려 줘.
- 저장소에 직접 쓸 수 있으면 `data/gemini/` 와 `docs/design-proposal.md` 에 저장. 못 쓰면 내용을 그대로 출력해 줘 (사용자가 복사해서 넣음).
