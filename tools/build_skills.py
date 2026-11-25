# -*- coding: utf-8 -*-
"""data/skills_source.csv (+ data/gemini/*.json) -> data/skills.js

사용법:  python tools/build_skills.py
- CSV 원본(구글 시트 '대표 Claude 스킬 정리' 내보내기)을 읽고
- 같은 스킬(GitHub 주소 또는 이름 기준)은 한 장으로 합치며 '설치됨' 표시
- 작업 분야(areas)·예시 프롬프트·설치 방법을 붙여
- 사이트가 바로 읽는 data/skills.js 와 data/skills.json 을 만든다.
"""
import csv, json, re, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "skills_source.csv")

# ── 작업 분야 정의 ─────────────────────────────────────────────
AREAS = [
    ("code", "코딩·개발", "💻"),
    ("video", "영상·미디어", "🎬"),
    ("writing", "작문·글쓰기", "✍️"),
    ("script", "대본·기획", "🎙️"),
    ("research", "자료수집·조사", "🔎"),
    ("marketing", "광고·마케팅", "📣"),
    ("docs", "문서·오피스", "📄"),
    ("design", "디자인", "🎨"),
    ("data", "데이터·분석", "📊"),
    ("learn", "학습·지식관리", "🧠"),
    ("collab", "협업·업무", "🤝"),
    ("security", "보안", "🛡️"),
    ("automation", "자동화", "⚙️"),
    ("meta", "스킬·플러그인 만들기", "🧩"),
]

# ── 스킬별 분류 + 예시 프롬프트 (이름 기준) ──────────────────────
# (분야 목록, "이렇게 말해 보세요" 예시)
INFO = {
 "docx": (["docs"], "첨부한 회의록을 표와 머리글이 있는 Word 보고서(.docx)로 만들어 줘"),
 "pdf": (["docs"], "이 PDF 3개를 하나로 합치고 2쪽 표를 엑셀로 뽑아 줘"),
 "pptx": (["docs", "marketing"], "이 기획안으로 10장짜리 PowerPoint(.pptx) 발표자료 만들어 줘"),
 "xlsx": (["docs", "data"], "가계부 엑셀 만들어 줘. 월별 합계 수식이랑 차트도 넣어서"),
 "doc-coauthoring": (["writing", "docs"], "자기소개서 같이 쓰자. 먼저 나한테 필요한 질문부터 해 줘"),
 "algorithmic-art": (["design"], "p5.js로 파도가 흐르는 듯한 생성 예술 만들어 줘"),
 "canvas-design": (["design", "marketing"], "광주 청년 취업박람회 홍보 포스터를 PNG로 만들어 줘"),
 "frontend-design": (["design", "code"], "이 랜딩페이지를 템플릿 티 안 나게 다시 디자인해 줘"),
 "theme-factory": (["design", "docs"], "이 발표자료에 차분한 네이비 테마 적용해 줘"),
 "slack-gif-creator": (["design", "video"], "팀 슬랙에 올릴 '배포 완료' 축하 GIF 만들어 줘"),
 "web-artifacts-builder": (["code", "design"], "React랑 Tailwind로 할 일 관리 앱 아티팩트 만들어 줘"),
 "mcp-builder": (["code", "meta"], "공공데이터포털 API를 쓰는 MCP 서버를 Python으로 만들어 줘"),
 "webapp-testing": (["code"], "localhost:3000 로그인 화면을 Playwright로 테스트하고 스크린샷 찍어 줘"),
 "brand-guidelines": (["design", "marketing"], "우리 브랜드 색상·서체 규칙을 이 문서에 적용해 줘"),
 "internal-comms": (["writing", "collab"], "이번 주 업무 진행 상황을 팀장님께 보낼 상태 보고로 써 줘"),
 "skill-creator": (["meta"], "내가 매주 하는 '광주 참여프로그램 정리'를 스킬로 만들어 줘"),
 "template-skill": (["meta"], "새 스킬 뼈대(SKILL.md) 하나 만들어 줘. 이름은 shorts-script"),
 "superpowers": (["code"], "brainstorming부터 시작해서 이 기능을 계획→TDD 순서로 만들어 줘"),
 "karpathy-guidelines": (["code"], "Karpathy 지침대로, 불필요한 코드 추가 없이 이 버그만 고쳐 줘"),
 "get-shit-done": (["code", "automation"], "/gsd 로 이 기능 스펙부터 잡고 단계별로 진행해 줘"),
 "playwright-skill": (["code", "automation"], "이 사이트에 접속해서 공지사항 제목 10개 긁어 와 줘"),
 "ios-simulator-skill": (["code"], "iOS 시뮬레이터에서 앱 빌드하고 회원가입 흐름 테스트해 줘"),
 "Expo Skills": (["code"], "Expo로 사진 찍어서 저장하는 앱 화면 만들어 줘"),
 "Trail of Bits Security Skills": (["security", "code"], "이 저장소를 정적 분석해서 취약점 찾아 줘"),
 "ffuf-web-fuzzing": (["security"], "내 테스트 서버(staging)에 ffuf로 숨은 경로 찾는 법 안내해 줘"),
 "claude-d3js-skill": (["data", "design"], "이 CSV로 d3.js 인터랙티브 막대그래프 만들어 줘"),
 "claude-scientific-skills": (["research", "data"], "이 유전자 목록으로 관련 논문·데이터베이스 찾아 정리해 줘"),
 "frontend-slides": (["design", "docs"], "애니메이션 들어간 HTML 발표자료 만들고 PPT로도 뽑아 줘"),
 "web-asset-generator": (["design", "marketing"], "내 로고로 파비콘이랑 인스타 프로필 이미지 만들어 줘"),
 "Skill_Seekers": (["meta", "research"], "Remotion 공식 문서 사이트를 Claude 스킬로 바꿔 줘"),
 "polaris-datainsight-doc-extract": (["docs", "data"], "이 한글(HWP) 공문에서 표 내용만 뽑아 엑셀로 정리해 줘"),
 "revealjs-skill": (["docs", "design"], "Reveal.js로 졸업 프로젝트 발표 슬라이드 만들어 줘"),
 "humanpen-skill": (["writing", "docs"], "이 PPT 문장들 AI 티 안 나게 자연스럽게 고쳐 줘"),
 "docx-cli": (["docs"], "이 Word 파일 댓글 다 반영하고 표 서식 맞춰 줘"),
 "brainstorming": (["code", "script"], "유튜브 채널 아이디어가 막연한데, 질문하면서 구체화해 줘"),
 "test-driven-development": (["code"], "이 함수 고치기 전에 실패하는 테스트부터 써 줘"),
 "systematic-debugging": (["code"], "테스트가 가끔 실패해. 원인을 단계적으로 찾아 줘"),
 "using-git-worktrees": (["code"], "이 실험용 기능은 별도 worktree에서 작업해 줘"),
 "finishing-a-development-branch": (["code"], "이 브랜치 마무리하고 병합 방식 골라 줘"),
 "pypict-claude-skill": (["code"], "회원가입 폼 입력값 조합 테스트 케이스를 PICT로 만들어 줘"),
 "aws-skills": (["code"], "이 Lambda 구성을 AWS CDK 모범 사례대로 바꾸고 비용도 줄여 줘"),
 "hashicorp-agent-skills": (["code"], "이 인프라를 Terraform 코드로 작성해 줘"),
 "azure-devops": (["code", "collab"], "Azure DevOps에서 이번 스프린트 작업 항목 정리해 줘"),
 "jules": (["code", "automation"], "이 리팩터링 작업을 Jules에게 맡겨 줘"),
 "claude-skills (jeffallan)": (["code"], "Next.js + Prisma 풀스택 게시판 만들어 줘"),
 "debug-skill": (["code"], "이 파이썬 스크립트에 중단점 걸고 변수 값 확인해 줘"),
 "plugin-authoring": (["meta", "code"], "내 작업용 Claude Code 플러그인 만들어 줘"),
 "code-review-skill": (["code"], "이번 변경사항 병합해도 되는지 리뷰해 줘"),
 "git-pushing": (["code", "automation"], "변경사항 정리해서 커밋하고 푸시해 줘"),
 "test-fixing": (["code"], "실패한 테스트 찾아서 고쳐 줘"),
 "Superdesign": (["design", "code"], "내 코드베이스에서 디자인 시스템 뽑고 설정 화면 시안 3개 만들어 줘"),
 "Design Auditor": (["design"], "이 화면을 디자인 원칙 17가지로 점수 매겨 줘"),
 "csv-data-summarizer": (["data"], "이 CSV 파일 요약해 줘. 결측치랑 상관관계도"),
 "postgres": (["data", "code"], "우리 DB에서 지난달 가입자 수 조회해 줘 (읽기 전용)"),
 "kaggle-skill": (["data", "learn"], "타이타닉 대회 데이터 받아서 기본 노트북 만들어 줘"),
 "notebooklm": (["research", "learn"], "내 NotebookLM 노트북 목록 보여 주고 요약해 줘"),
 "gh-star-history": (["data", "research"], "이 세 저장소 GitHub 별 추이를 차트로 비교해 줘"),
 "claude-ecom": (["data", "marketing"], "주문 CSV로 이번 분기 매출 분석 보고서 써 줘"),
 "deep-research": (["research"], "2026년 광주 청년 일자리 정책을 여러 출처로 조사해 보고서로 써 줘"),
 "paper-search": (["research", "learn"], "'LLM 에이전트 평가' 관련 최근 논문 10편 찾아 줘"),
 "article-extractor": (["research", "writing"], "이 기사 링크에서 본문이랑 작성일만 뽑아 줘"),
 "content-research-writer": (["writing", "research", "script"], "'시니어 스마트폰 사기 예방' 블로그 글을 자료 조사·인용 넣어서 써 줘"),
 "avoid-ai-writing": (["writing"], "이 글에서 AI 같은 표현 찾아서 다시 써 줘"),
 "naming": (["writing", "marketing"], "중고거래 자동화 서비스 이름 후보 10개 지어 줘"),
 "karpathy-llm-wiki": (["learn"], "이 강의 자료들로 개인 마크다운 위키 만들어 줘"),
 "llm-wiki": (["learn"], "내 메모들을 검색 가능한 지식베이스로 정리해 줘"),
 "learn-this": (["learn", "research"], "이 유튜브 강의 내용을 실천 계획으로 정리해 줘"),
 "ship-learn-next": (["learn"], "이번 프로젝트 피드백 보고 다음에 뭘 만들지 정해 줘"),
 "universal-exam-cram-coach": (["learn"], "내 통계학 노트로 기말고사 대비 문제 내 줘"),
 "understanding-ladder": (["learn"], "베이즈 정리를 나한테 맞는 형식으로 설명해 줘"),
 "youtube-transcript": (["video", "research", "script"], "이 유튜브 영상 자막 가져와서 요약해 줘"),
 "youtube-full": (["video", "research"], "'AI 자동매매' 유튜브 검색해서 조회수 높은 영상 자막 모아 줘"),
 "video-downloader": (["video"], "이 영상(내가 권리 있는 것) 다운로드해 줘"),
 "image-enhancer": (["design", "video"], "이 스크린샷 화질 선명하게 개선해 줘"),
 "imagen": (["design", "video", "marketing"], "쇼츠 썸네일용 배경 이미지 3장 만들어 줘"),
 "elevenlabs": (["video", "script"], "이 대본으로 2인 팟캐스트 음성 만들어 줘"),
 "google-tts": (["video", "script"], "이 쇼츠 대본을 한국어 내레이션 음성으로 만들어 줘"),
 "claude-epub-skill": (["docs", "writing"], "이 원고를 킨들용 EPUB으로 바꿔 줘"),
 "video-prompting-skill": (["video", "script"], "Higgsfield에 넣을 8초짜리 영상 프롬프트 다듬어 줘"),
 "Claude Code Video Toolkit": (["video", "code"], "Remotion이랑 ElevenLabs로 1분짜리 설명 영상 만들어 줘"),
 "VideoDB Skills": (["video"], "내 영상들에서 '자막에 할인 나오는 장면'만 찾아 잘라 줘"),
 "upload-post": (["marketing", "video", "automation"], "이 쇼츠를 유튜브·인스타·틱톡에 내일 저녁 7시 예약 게시해 줘"),
 "kanban-skill": (["collab"], "이 프로젝트 할 일을 칸반 보드 파일로 만들어 줘"),
 "linear-claude-skill": (["collab"], "Linear에 이번 주 이슈 정리해서 올려 줘"),
 "meeting-insights-analyzer": (["collab", "writing"], "이 회의 녹취록에서 누가 말을 많이 했는지, 결정사항 뭔지 분석해 줘"),
 "google-workspace-skills": (["collab", "automation"], "Gmail에서 이번 주 면접 메일 찾아서 캘린더에 넣어 줘"),
 "pm-skills": (["collab", "script"], "이 앱 아이디어로 PRD(제품 요구사항 문서) 써 줘"),
 "VibeSec-Skill": (["security", "code"], "이 로그인 코드 보안 취약점 없게 다시 짜 줘"),
 "owasp-security": (["security", "code"], "OWASP 체크리스트로 이 API 점검해 줘"),
 "varlock-claude-skill": (["security", "code"], ".env 비밀키가 커밋·로그에 안 새게 설정해 줘"),
 "file-organizer": (["automation"], "다운로드 폴더 파일들 종류별로 정리해 줘"),
 "invoice-organizer": (["automation", "docs"], "이 영수증 사진들 연말정산용으로 정리해 줘"),
 "review-claudemd": (["meta", "automation"], "지난 대화들 보고 CLAUDE.md 개선점 찾아 줘"),
 "SkillCheck-Free": (["meta"], "내가 만든 SKILL.md 검증해 줘"),
 "job-application-agent": (["automation", "research"], "광주 데이터분석 신입 공고 찾아서 평가표로 정리해 줘"),
 "career-ops": (["writing", "automation"], "이 공고에 맞춰 이력서 고치고 예상 면접 질문 뽑아 줘"),
 "awesome-claude-skills (travisvn)": (["meta"], "이 목록에서 영상 제작에 쓸 만한 스킬 골라 줘"),
 "awesome-claude-skills (ComposioHQ)": (["meta", "automation"], "Gmail·Slack 연동 스킬 중 내 업무에 맞는 거 추천해 줘"),
 "awesome-claude-skills (BehiSecc)": (["meta"], "문서·미디어 분야 스킬만 추려 줘"),
 "awesome-agent-skills (VoltAgent)": (["meta"], "공식 개발팀 스킬 중 마케팅용만 골라 줘"),
 "resale-listing": (["automation", "marketing"], "(사진 3장 첨부) 이거 당근에 팔 거야"),
 "artifact-emulator": (["design", "meta"], "방금 만든 페이지 실제로 어떻게 보이는지 확인해 줘"),
 "built-in-browser": (["automation"], "내장 브라우저로 이 사이트 들어가서 공지 읽어 줘"),
 "chrome-browser": (["automation"], "내 크롬에서 이 쇼핑몰 장바구니 확인해 줘"),
 "computer-use": (["automation"], "내 컴퓨터에서 메모장 열고 오늘 할 일 적어 줘"),
 "docs": (["docs", "writing"], "이번 프로젝트 계획서를 문서로 만들어 줘"),
 "google-workspace": (["docs", "collab"], "구글 시트 '중고판매 기록'에 오늘 판매 한 줄 추가해 줘"),
 "import-memory": (["meta"], "ChatGPT 메모리 내보낸 거 가져와 줘"),
 "morning": (["collab", "automation"], "/morning 아침 브리핑 보여 줘"),
 "remotion-motion-graphics": (["video", "code"], "채널 인트로 5초짜리 로고 애니메이션 만들어 줘"),
 "video-making": (["video", "script"], "시니어 대상 '보이스피싱 예방' 1분 쇼츠 만들어 줘"),
 "dataviz": (["data", "design"], "이 매출 데이터로 대시보드 만들어 줘"),
 "cowork-plugin": (["meta"], "우리 팀용 플러그인 만들어 줘"),
 "explain-usage": (["meta"], "이번 대화 토큰 어디에 많이 썼어?"),
 "setup-claude": (["meta"], "Claude 처음 설정 도와줘"),
 "file-reading": (["docs"], "(파일 첨부) 이 파일 내용 읽어 줘"),
 "pdf-reading": (["docs", "research"], "이 스캔 PDF에서 표만 뽑아 줘"),
 "product-self-knowledge": (["meta"], "Claude Pro랑 Max 요금제 차이 알려 줘"),
}

GH = re.compile(r"https://github\.com/([^/]+)/([^/]+)(?:/tree/[^/]+/(.*))?")


def install_for(name, url, source):
    """설치 방법을 단계 목록 + 복사용 명령으로 만든다."""
    if not url.startswith("http"):
        if "내 Claude 계정" in url or source == "내 스킬":
            return {"type": "mine", "label": "내 계정에 있음",
                    "steps": ["이미 내 Claude 계정 스킬에 저장되어 있어요.",
                              "설정 → 기능(Capabilities) → 스킬에서 켜져 있는지 확인하세요.",
                              "다른 컴퓨터의 Claude Code에서 쓰려면 스킬 폴더를 ~/.claude/skills/ 에 복사하세요."],
                    "commands": []}
        return {"type": "builtin", "label": "기본 제공",
                "steps": ["Claude 앱에 기본으로 들어 있어 따로 설치할 필요가 없어요.",
                          "관련된 요청을 하면 Claude가 알아서 불러 씁니다. 이름으로 불러도 돼요."],
                "commands": []}
    m = GH.match(url)
    owner, repo, sub = (m.group(1), m.group(2), (m.group(3) or "").rstrip("/")) if m else ("", "", "")
    if owner == "anthropics" and repo == "skills":
        return {"type": "official", "label": "공식 마켓",
                "steps": ["claude.ai/앱: 설정 → 기능 → 스킬에서 예시 스킬을 켜면 바로 사용 (대부분 기본 포함).",
                          "Claude Code: 아래 명령으로 공식 마켓을 추가한 뒤 플러그인을 설치합니다.",
                          "설치 후 Claude Code를 다시 시작하세요."],
                "commands": ["/plugin marketplace add anthropics/skills",
                             "/plugin install document-skills@anthropic-agent-skills",
                             "/plugin install example-skills@anthropic-agent-skills"]}
    if source == "모음집":
        return {"type": "list", "label": "모음 목록",
                "steps": ["스킬 하나가 아니라 여러 스킬을 모아 둔 목록이에요.",
                          "링크에서 원하는 스킬을 고른 뒤, 그 스킬의 설치 방법을 따르세요.",
                          "좋은 스킬을 찾으면 이 사이트의 '제안' 방법으로 추가해 주세요."],
                "commands": []}
    clone = f"git clone https://github.com/{owner}/{repo}.git"
    if sub:  # 저장소 안의 한 폴더 = 스킬 하나
        folder = sub.split("/")[-1] or name
        return {"type": "folder", "label": "폴더 복사",
                "steps": ["저장소를 내려받습니다(git clone 또는 GitHub의 Code → Download ZIP).",
                          f"'{sub}' 폴더(SKILL.md가 들어 있는 폴더)를 찾습니다.",
                          "Claude Code: 그 폴더를 ~/.claude/skills/ 아래에 복사합니다 (Windows: %USERPROFILE%\\.claude\\skills).",
                          "claude.ai/앱: 그 폴더를 ZIP으로 묶어 설정 → 기능 → 스킬 → 업로드."],
                "commands": [clone,
                             f"cp -r {repo}/{sub} ~/.claude/skills/{folder}"]}
    return {"type": "repo", "label": "저장소 설치",
            "steps": ["저장소 README의 설치 안내를 먼저 확인하세요 (플러그인 마켓을 지원하면 그 방법이 가장 쉬워요).",
                      "Claude Code 플러그인 마켓 지원 시: 아래 첫 번째 명령으로 마켓을 추가하고 /plugin 메뉴에서 설치.",
                      "아니면 저장소를 내려받아 SKILL.md가 든 폴더를 ~/.claude/skills/ 에 복사하세요.",
                      "claude.ai/앱: 스킬 폴더를 ZIP으로 묶어 설정 → 기능 → 스킬 → 업로드."],
            "commands": [f"/plugin marketplace add {owner}/{repo}", clone]}


def make_tabs(s):
    """설치 방법을 사용하는 곳별 탭(claude.ai 앱 / Claude Code 마켓 / 폴더 복사)으로 나눈다."""
    ins, url = s["install"], s.get("url", "")
    t = ins["type"]
    if t not in ("official", "repo", "folder"):
        return []
    m = GH.match(url)
    owner, repo, sub = (m.group(1), m.group(2), (m.group(3) or "").rstrip("/")) if m else ("", "", "")
    folder = sub.split("/")[-1] if sub else repo
    clone = f"git clone https://github.com/{owner}/{repo}.git"
    if t == "official":
        return [
            {"id": "app", "label": "claude.ai 앱",
             "steps": ["설정 → 기능(Capabilities) → 스킬에서 켜기.",
                       "공식 스킬은 대부분 이미 들어 있어요. 목록에 없으면 폴더 복사 탭 방법으로 ZIP 업로드."],
             "commands": []},
            {"id": "market", "label": "Claude Code 마켓",
             "steps": ["Claude Code에서 공식 마켓을 추가하고 플러그인을 설치한 뒤 다시 시작하세요."],
             "commands": ins["commands"]},
            {"id": "copy", "label": "폴더 복사",
             "steps": ["저장소를 받아 스킬 폴더를 ~/.claude/skills/ 에 복사 (Windows: %USERPROFILE%\\.claude\\skills)."],
             "commands": [clone, f"cp -r {repo}/{sub} ~/.claude/skills/{folder}"]},
        ]
    copy_cmds = [clone, f"cp -r {repo}/{sub} ~/.claude/skills/{folder}" if sub else f"cp -r {repo} ~/.claude/skills/{folder}"]
    return [
        {"id": "app", "label": "claude.ai 앱",
         "steps": ["GitHub에서 Code → Download ZIP으로 받기.",
                   f"압축을 풀고 SKILL.md가 바로 들어 있는 폴더('{folder}')만 다시 ZIP으로 묶기.",
                   "claude.ai → 설정 → 기능(Capabilities) → 스킬 → 업로드."],
         "commands": []},
        {"id": "market", "label": "Claude Code 마켓",
         "steps": ["저장소 README에 플러그인 마켓 안내가 있을 때만 쓰는 방법이에요.",
                   "마켓을 추가한 뒤 /plugin 메뉴에서 골라 설치하고 Claude Code를 다시 시작하세요.",
                   "README에 안내가 없으면 '폴더 복사' 탭 방법을 쓰세요."],
         "commands": [f"/plugin marketplace add {owner}/{repo}", "/plugin"]},
        {"id": "copy", "label": "폴더 복사",
         "steps": ["저장소를 내려받고 SKILL.md가 든 폴더를 Claude Code 스킬 폴더로 복사합니다.",
                   "Windows는 ~/.claude/skills 대신 %USERPROFILE%\\.claude\\skills 입니다.",
                   "프로젝트에서만 쓰려면 프로젝트 안 .claude/skills/ 에 넣으세요."],
         "commands": copy_cmds},
    ]


KO = re.compile(r"한국어|한글|HWP|카카오|당근|네이버|korean|hangeul|-ko\b|\bko-|중고 물건", re.I)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "skill"


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    skills, by_key = [], {}
    for r in rows:
        name = (r.get("스킬 이름") or "").strip()
        if not name:
            continue
        group = r["구분"].strip()
        source, _, sub = group.partition("·")
        source, sub = source.strip(), sub.strip()
        url = r["GitHub 주소"].strip()
        key = url if url.startswith("http") else name
        installed = source == "설치됨"
        if key in by_key:  # 같은 스킬 → 합치기
            s = by_key[key]
            s["installed"] = s["installed"] or installed
            if len(r["기능"]) > len(s["purpose"]):
                s["purpose"] = r["기능"].strip()
            continue
        areas, example = INFO.get(name, (["meta"], f"{name} 스킬을 써서 도와줘"))
        if name not in INFO:
            print("분류 없음:", name, file=sys.stderr)
        src_label = {"공식": "공식", "커뮤니티": "커뮤니티", "모음집": "모음집",
                     "내 스킬": "내 스킬", "설치됨": "Anthropic"}.get(source, source)
        s = {
            "id": slug(name), "name": name, "author": r["제작"].strip(),
            "url": url if url.startswith("http") else "", "note": "" if url.startswith("http") else url,
            "source": src_label, "group": sub or group, "areas": areas,
            "purpose": r["기능"].strip(), "example": example,
            "installed": installed or source == "내 스킬",
            "install": install_for(name, url, source),
            "origin": "sheet",
        }
        by_key[key] = s
        skills.append(s)

    # 제미나이가 모아 온 스킬 합치기 (tools/merge_gemini.py 결과)
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "gemini", "*.json"))):
        try:
            extra = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("제미나이 파일 읽기 실패:", f, e, file=sys.stderr); continue
        stem = os.path.splitext(os.path.basename(f))[0]
        for g in extra.get("skills", []):
            g["batch"] = stem
            g["batch_date"] = extra.get("collected_at", "")
            g["batch_by"] = extra.get("collected_by", "")
            key = g.get("url") or g.get("name")
            if not key or key in by_key:
                continue
            g.setdefault("id", slug(g["name"]))
            g.setdefault("source", "커뮤니티"); g.setdefault("installed", False)
            g.setdefault("areas", ["meta"]); g.setdefault("group", "제미나이 수집")
            g.setdefault("example", f"{g['name']} 스킬을 써서 도와줘")
            if g.get("url"):
                g.setdefault("install", install_for(g["name"], g["url"], g["source"]))
            else:
                g.setdefault("install", {"type": "unknown", "label": "주소 확인 필요",
                    "steps": ["아직 저장소 주소를 확인하지 못했어요.",
                              "제미나이 수집 단계에서 주소를 찾아 data/gemini/ 파일에 url을 채우면 설치 방법이 자동으로 생깁니다."],
                    "commands": []})
            g.setdefault("author", "미확인"); g.setdefault("purpose", ""); g.setdefault("note", "")
            g["origin"] = "gemini"
            by_key[key] = g; skills.append(g)

    # 설치 탭 · 배지
    for s in skills:
        s["install"]["tabs"] = make_tabs(s)
        text = " ".join([s["name"], s.get("purpose", ""), s.get("url", ""), s.get("note", "")])
        s["korean"] = bool(KO.search(text))
        s["lowstar"] = "별 적음" in s.get("note", "")
        s.setdefault("batch", "")

    # id 중복 방지
    seen = {}
    for s in skills:
        if s["id"] in seen:
            seen[s["id"]] += 1; s["id"] = f'{s["id"]}-{seen[s["id"]]}'
        else:
            seen[s["id"]] = 1

    out = {"areas": [{"id": a, "name": n, "icon": i} for a, n, i in AREAS],
           "skills": skills}
    json.dump(out, open(os.path.join(ROOT, "data", "skills.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "data", "skills.js"), "w", encoding="utf-8") as f:
        f.write("// 자동 생성 파일 — tools/build_skills.py 로 다시 만드세요\n")
        f.write("window.SKILL_DATA = " + json.dumps(out, ensure_ascii=False) + ";\n")
    print(f"스킬 {len(skills)}개 생성 (설치됨 {sum(s['installed'] for s in skills)}개)")


if __name__ == "__main__":
    main()
