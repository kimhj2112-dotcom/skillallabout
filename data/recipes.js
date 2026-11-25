// 작업별 레시피 — 어떤 일을 할 때 어떤 스킬을 어떤 순서로 쓰는지
// steps 의 skill 값은 data/skills.json 의 id 와 같아야 합니다.
window.RECIPES = [
  {
    id: "shorts", icon: "🎬", title: "쇼츠 영상 만들기",
    desc: "주제 조사부터 대본, 음성, 영상, 예약 게시까지",
    steps: [
      { skill: "youtube-full", say: "비슷한 주제의 인기 영상 자막을 모아 분석" },
      { skill: "content-research-writer", say: "자료 조사해서 60초 대본 작성" },
      { skill: "video-prompting-skill", say: "장면별 영상 생성 프롬프트 다듬기 (Higgsfield 등)" },
      { skill: "google-tts", say: "대본을 한국어 내레이션으로" },
      { skill: "remotion-motion-graphics", say: "자막·모션그래픽 넣어 렌더링" },
      { skill: "upload-post", say: "유튜브·인스타·틱톡 예약 게시" }
    ]
  },
  {
    id: "script", icon: "🎙️", title: "유튜브·팟캐스트 대본",
    desc: "아이디어를 구체화하고 사람 말투로 다듬기",
    steps: [
      { skill: "brainstorming", say: "막연한 아이디어를 질문으로 구체화" },
      { skill: "youtube-transcript", say: "참고 영상 자막 가져와 구성 분석" },
      { skill: "content-research-writer", say: "근거·인용 넣어 대본 초안" },
      { skill: "avoid-ai-writing", say: "AI 티 나는 표현 다시 쓰기" },
      { skill: "elevenlabs", say: "2인 대화형 음성으로 미리 듣기" }
    ]
  },
  {
    id: "writing", icon: "✍️", title: "블로그·에세이 글쓰기",
    desc: "자료 수집 → 초안 → 퇴고 → 제목 짓기",
    steps: [
      { skill: "article-extractor", say: "참고 기사 본문만 뽑기" },
      { skill: "doc-coauthoring", say: "질문 받으며 초안 함께 쓰기" },
      { skill: "avoid-ai-writing", say: "자연스러운 문장으로 퇴고" },
      { skill: "naming", say: "기억에 남는 제목 후보 짓기" }
    ]
  },
  {
    id: "research", icon: "🔎", title: "자료수집·조사 보고서",
    desc: "여러 출처를 모아 근거 있는 보고서로",
    steps: [
      { skill: "deep-research", say: "여러 출처 조사·비교" },
      { skill: "paper-search", say: "관련 논문 찾기" },
      { skill: "csv-data-summarizer", say: "모은 데이터 요약" },
      { skill: "dataviz", say: "차트로 시각화" },
      { skill: "docx", say: "Word 보고서로 정리" }
    ]
  },
  {
    id: "ads", icon: "📣", title: "광고·홍보 소재 만들기",
    desc: "브랜드 이름, 포스터, 썸네일, SNS 게시",
    steps: [
      { skill: "naming", say: "서비스·캠페인 이름 짓기" },
      { skill: "canvas-design", say: "홍보 포스터 PNG/PDF" },
      { skill: "imagen", say: "썸네일·배너 이미지 생성" },
      { skill: "web-asset-generator", say: "SNS 프로필·파비콘 세트" },
      { skill: "upload-post", say: "여러 SNS에 한 번에 게시" }
    ]
  },
  {
    id: "coding", icon: "💻", title: "웹사이트·앱 코딩",
    desc: "설계 → 테스트 먼저 → 디버깅 → 리뷰 → 배포",
    steps: [
      { skill: "brainstorming", say: "요구사항을 설계로 구체화" },
      { skill: "frontend-design", say: "템플릿 티 안 나는 화면 디자인" },
      { skill: "test-driven-development", say: "실패하는 테스트부터 작성" },
      { skill: "systematic-debugging", say: "버그 원인 단계적 분석" },
      { skill: "code-review-skill", say: "병합 전 리뷰" },
      { skill: "git-pushing", say: "커밋·푸시 (GitHub Pages 배포)" }
    ]
  },
  {
    id: "docs", icon: "📄", title: "업무 문서·발표자료",
    desc: "보고서, 엑셀, PPT를 한 번에",
    steps: [
      { skill: "polaris-datainsight-doc-extract", say: "한글(HWP)·오피스 파일에서 내용 추출" },
      { skill: "xlsx", say: "표·수식·차트 엑셀" },
      { skill: "docx", say: "Word 보고서" },
      { skill: "pptx", say: "발표자료" },
      { skill: "humanpen-skill", say: "문장 자연스럽게 다듬기" }
    ]
  },
  {
    id: "resale", icon: "🥕", title: "중고판매 자동화",
    desc: "사진 3장으로 시세·판매글·기록까지",
    steps: [
      { skill: "resale-listing", say: "사진 → 시세 조사 → 당근 판매글 → 옵시디언 노트 → 시트 기록" },
      { skill: "image-enhancer", say: "상품 사진 화질 개선" }
    ]
  },
  {
    id: "job", icon: "💼", title: "취업 준비",
    desc: "공고 찾기 → 이력서 맞춤 → 면접 대비",
    steps: [
      { skill: "job-application-agent", say: "공고 찾고 평가표로 정리" },
      { skill: "career-ops", say: "공고별 이력서·면접 질문" },
      { skill: "doc-coauthoring", say: "자기소개서 함께 쓰기" },
      { skill: "universal-exam-cram-coach", say: "필기·자격증 대비 문제 풀이" }
    ]
  },
  {
    id: "make-skill", icon: "🧩", title: "나만의 스킬 만들기",
    desc: "반복하는 일을 스킬로 저장",
    steps: [
      { skill: "skill-creator", say: "반복 작업을 스킬로 만들기" },
      { skill: "skill-seekers", say: "공식 문서 사이트를 스킬로 변환" },
      { skill: "skillcheck-free", say: "SKILL.md 품질 검증" },
      { skill: "review-claudemd", say: "CLAUDE.md 개선" }
    ]
  }
];
