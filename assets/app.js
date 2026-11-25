(() => {
  "use strict";
  const DATA = window.SKILL_DATA || { areas: [], skills: [] };
  const RECIPES = window.RECIPES || [];
  const AREA = Object.fromEntries(DATA.areas.map(a => [a.id, a]));
  const BY_ID = Object.fromEntries(DATA.skills.map(s => [s.id, s]));
  const SOURCES = ["전체", "공식", "Anthropic", "커뮤니티", "내 스킬", "모음집"];
  const $ = s => document.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // A. 첫 화면 빠른 버튼 — 분야(area) 또는 한국어 업무(ko)
  const QUICK = [
    { id: "marketing", label: "광고·마케팅", icon: "📣" },
    { id: "script", label: "대본·기획", icon: "🎙️" },
    { id: "writing", label: "작문", icon: "✍️" },
    { id: "video", label: "영상", icon: "🎬" },
    { id: "ko", label: "한국어 업무", icon: "🇰🇷" }
  ];
  const TAGS = ["쇼츠 훅", "SEO", "한국어 교정", "HWP", "썸네일", "랜딩 카피", "논문", "엑셀"];

  let favs = new Set();
  try { favs = new Set(JSON.parse(localStorage.getItem("sab-favs") || "[]")); } catch (e) {}
  const saveFavs = () => { try { localStorage.setItem("sab-favs", JSON.stringify([...favs])); } catch (e) {} };

  const state = { q: "", area: null, ko: false, source: "전체", installed: false, fav: false };
  const quiz = { out: null, env: null, pay: null };

  const ALIAS = {
    쇼츠: "video", 영상: "video", 유튜브: "video", 동영상: "video", 음성: "video", 더빙: "video", 자막: "video",
    대본: "script", 스크립트: "script", 기획: "script", 팟캐스트: "script", 훅: "script",
    글: "writing", 작문: "writing", 블로그: "writing", 자소서: "writing", 이력서: "writing", 교정: "writing", 윤문: "writing",
    조사: "research", 자료: "research", 논문: "research", 리서치: "research",
    광고: "marketing", 마케팅: "marketing", 홍보: "marketing", 썸네일: "marketing", sns: "marketing", 카피: "marketing", seo: "marketing", 랜딩: "marketing",
    코딩: "code", 개발: "code", 코드: "code", 테스트: "code", 버그: "code",
    엑셀: "docs", 워드: "docs", ppt: "docs", 발표: "docs", 한글: "docs", hwp: "docs", 보고서: "docs",
    디자인: "design", 포스터: "design", 이미지: "design",
    데이터: "data", 차트: "data", 분석: "data", 공부: "learn", 시험: "learn",
    보안: "security", 자동화: "automation", 스킬만들기: "meta", 플러그인: "meta"
  };

  const srcClass = s => (s.source === "공식" || s.source === "Anthropic") ? "src-official" : s.source === "내 스킬" ? "src-mine" : "";
  const needsKey = s => /API 키|키 필요|유료|비용|계정 및/.test(s.note || "");

  function textMatch(s, q) {
    if (!q) return true;
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    const hay = [s.name, s.author, s.purpose, s.example, s.group, s.note, ...s.areas.map(a => AREA[a]?.name)].join(" ").toLowerCase();
    return terms.every(t => hay.includes(t) || (ALIAS[t] && s.areas.includes(ALIAS[t])));
  }
  function matches(s) {
    if (state.area && !s.areas.includes(state.area)) return false;
    if (state.ko && !s.korean) return false;
    if (state.source !== "전체" && s.source !== state.source) return false;
    if (state.installed && !s.installed) return false;
    if (state.fav && !favs.has(s.id)) return false;
    return textMatch(s, state.q);
  }

  function badges(s) {
    return `<span class="badge ${srcClass(s)}">${esc(s.source)}</span>
      ${s.installed ? `<span class="badge inst">✓ 설치됨</span>` : ""}
      ${s.korean ? `<span class="badge ko">한국어 친화</span>` : ""}
      ${s.lowstar ? `<span class="badge low">별 적음</span>` : ""}
      ${s.origin === "gemini" ? `<span class="badge gem">제미나이 수집</span>` : ""}`;
  }

  // B. 간단한 카드 — 이름 · 한 줄 설명 · 분야 2개
  function card(s) {
    return `<article class="card" data-id="${s.id}">
      <button class="fav ${favs.has(s.id) ? "is-on" : ""}" data-fav="${s.id}" aria-label="즐겨찾기">${favs.has(s.id) ? "★" : "☆"}</button>
      <div class="card-top">${badges(s)}</div>
      <h3>${esc(s.name)}</h3>
      <p>${esc(s.purpose)}</p>
      <div class="tags">${s.areas.slice(0, 2).map(a => `<span>#${esc(AREA[a]?.name || a)}</span>`).join("")}</div>
      <div class="row">
        <button class="btn primary" data-open="${s.id}">사용법·설치</button>
        <button class="btn" data-copy="${esc(s.example)}">예시 복사</button>
      </div>
    </article>`;
  }
  const rank = s => (s.installed ? 0 : 2) + (srcClass(s) === "src-official" ? 0 : 1);
  const sortSkills = list => list.sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name));

  function renderQuick() {
    const n = id => id === "ko" ? DATA.skills.filter(s => s.korean).length : DATA.skills.filter(s => s.areas.includes(id)).length;
    $("#quick").innerHTML = QUICK.map(q => {
      const on = q.id === "ko" ? state.ko : state.area === q.id;
      return `<button class="qbtn ${on ? "is-on" : ""}" data-quick="${q.id}">${q.icon} ${esc(q.label)} <small>${n(q.id)}</small></button>`;
    }).join("");
    $("#tags").innerHTML = TAGS.map(t => `<button data-tag="${esc(t)}">#${esc(t)}</button>`).join("");
  }
  function renderAreas() {
    const counts = {};
    DATA.skills.forEach(s => s.areas.forEach(a => counts[a] = (counts[a] || 0) + 1));
    $("#areas").innerHTML =
      `<button class="area ${state.area || state.ko ? "" : "is-on"}" data-area="">전체 <span class="n">${DATA.skills.length}</span></button>` +
      DATA.areas.map(a => `<button class="area ${state.area === a.id ? "is-on" : ""}" data-area="${a.id}">${a.icon} ${esc(a.name)} <span class="n">${counts[a.id] || 0}</span></button>`).join("");
  }
  function renderSources() {
    $("#sources").innerHTML = SOURCES.map(s => `<button class="${state.source === s ? "is-on" : ""}" data-src="${esc(s)}">${esc(s)}</button>`).join("");
  }

  // F. 결과가 적으면 레시피 제안
  function recipesFor(areas, q) {
    const ql = (q || "").toLowerCase();
    const score = r => {
      let n = 0;
      if (ql && (r.title + r.desc).toLowerCase().includes(ql)) n += 5;
      r.steps.forEach(st => { const s = BY_ID[st.skill]; if (s) n += s.areas.filter(a => areas.includes(a)).length; });
      return n;
    };
    return RECIPES.map(r => [r, score(r)]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).map(x => x[0]);
  }
  function renderGrid() {
    const list = sortSkills(DATA.skills.filter(matches));
    $("#grid").innerHTML = list.map(card).join("");
    $("#empty").hidden = list.length > 0;
    $("#count").textContent = `${list.length}개 표시`;
    const filtered = state.q || state.area || state.ko;
    let areas = state.area ? [state.area] : state.ko ? ["writing", "docs"] : [];
    if (!areas.length && state.q) state.q.toLowerCase().split(/\s+/).forEach(t => ALIAS[t] && areas.push(ALIAS[t]));
    let recs = filtered && list.length <= 2 ? recipesFor(areas, state.q).slice(0, 3) : [];
    if (filtered && !list.length && !recs.length) recs = RECIPES.slice(0, 3);
    $("#suggest").hidden = !recs.length;
    $("#suggest").innerHTML = recs.length ? `<b>${list.length ? "결과가 적어요." : ""} 이런 레시피는 어때요?</b>` +
      recs.map(r => `<button data-recipe="${r.id}">${r.icon} ${esc(r.title)} →</button>`).join("") : "";
  }

  function recipesUsing(id) { return RECIPES.filter(r => r.steps.some(st => st.skill === id)); }

  // C. 설치 방법 탭
  function installHtml(s) {
    const ins = s.install || { steps: [], commands: [] };
    const cmds = c => c.map(x => `<div class="cmd"><code>${esc(x)}</code><button class="copy" data-copy="${esc(x)}">복사</button></div>`).join("");
    if (!ins.tabs || !ins.tabs.length) {
      return `<ol class="steps">${(ins.steps || []).map(t => `<li>${esc(t)}</li>`).join("")}</ol>${cmds(ins.commands || [])}`;
    }
    let pref = "app";
    try { pref = localStorage.getItem("sab-itab") || "app"; } catch (e) {}
    if (!ins.tabs.some(t => t.id === pref)) pref = ins.tabs[0].id;
    return `<div class="itabs" role="tablist">${ins.tabs.map(t => `<button data-itab="${t.id}" class="${t.id === pref ? "is-on" : ""}">${esc(t.label)}</button>`).join("")}</div>` +
      ins.tabs.map(t => `<div class="ipane ${t.id === pref ? "is-on" : ""}" data-pane="${t.id}"><ol class="steps">${t.steps.map(x => `<li>${esc(x)}</li>`).join("")}</ol>${cmds(t.commands)}</div>`).join("");
  }

  function openDetail(id, push = true) {
    const s = BY_ID[id];
    if (!s) return;
    const used = recipesUsing(id);
    $("#detail").innerHTML = `
      <div class="d-head">
        <div class="card-top">${badges(s)}<span class="badge">${esc(s.install?.label || "")}</span></div>
        <h2 id="d-name">${esc(s.name)}</h2>
        <div class="by">만든 이 · ${esc(s.author)}${s.group ? " · " + esc(s.group) : ""}</div>
      </div>
      <div class="d-sec"><h4>용도</h4><p>${esc(s.purpose)}</p></div>
      <div class="d-sec"><h4>분야</h4><div class="chips">${s.areas.map(a => `<span>${AREA[a]?.icon || ""} ${esc(AREA[a]?.name || a)}</span>`).join("")}</div></div>
      <div class="d-sec"><h4>사용 방법 — 이렇게 말해 보세요</h4>
        <div class="say-box"><q>${esc(s.example)}</q>
          <button class="btn" data-copy="${esc(s.example)}">문장 복사</button>
          <button class="btn" data-copy="${esc(s.name + " 스킬을 써서 " + s.example)}">스킬 이름 넣어 복사</button>
        </div>
        <p class="hint">스킬은 켜져 있으면 Claude가 알아서 고릅니다. 확실히 쓰게 하려면 문장에 스킬 이름을 넣으세요.</p>
      </div>
      <div class="d-sec"><h4>설치 방법</h4>${installHtml(s)}</div>
      ${s.note ? `<div class="d-sec"><h4>참고 · 주의</h4><div class="note-box">${esc(s.note)}</div></div>` : ""}
      ${used.length ? `<div class="d-sec in-recipes"><h4>이 스킬이 들어간 레시피</h4>${used.map(r => `<button data-recipe="${r.id}">${r.icon} ${esc(r.title)}</button>`).join("")}</div>` : ""}
      <div class="d-links">
        ${s.url ? `<a class="btn primary" href="${esc(s.url)}" target="_blank" rel="noopener">GitHub에서 보기 ↗</a>` : ""}
        <button class="btn" data-fav="${s.id}">${favs.has(s.id) ? "★ 즐겨찾기 해제" : "☆ 즐겨찾기"}</button>
        <button class="btn" data-copy="${esc(location.href.split("#")[0] + "#skill=" + s.id)}">링크 복사</button>
      </div>`;
    $("#sheet").hidden = false;
    document.body.style.overflow = "hidden";
    if (push) history.replaceState(null, "", "#skill=" + s.id);
  }
  function closeDetail() {
    $("#sheet").hidden = true;
    document.body.style.overflow = "";
    if (location.hash.startsWith("#skill=")) history.replaceState(null, "", location.pathname + location.search);
  }

  function renderRecipes() {
    $("#recipes").innerHTML = RECIPES.map(r => `
      <article class="recipe" id="recipe-${r.id}">
        <h3>${r.icon} ${esc(r.title)}</h3>
        <div class="d">${esc(r.desc)}</div>
        <ol>${r.steps.map(st => {
          const s = BY_ID[st.skill];
          return `<li><button data-open="${st.skill}">${esc(s ? s.name : st.skill)}</button>${s && s.installed ? `<span class="inst-mark">✓ 설치됨</span>` : ""}<span class="say">${esc(st.say)}</span></li>`;
        }).join("")}</ol>
      </article>`).join("");
  }

  // D. 질문 3개 추천
  const OUT_AREAS = { writing: ["writing", "marketing"], script: ["script"], video: ["video", "design"], code: ["code", "automation"], research: ["research", "data"], docs: ["docs"] };
  function renderQuiz() {
    document.querySelectorAll(".opts").forEach(g => g.querySelectorAll("button").forEach(b => b.classList.toggle("is-on", quiz[g.dataset.q] === b.dataset.v)));
    const box = $("#quiz-result");
    if (!quiz.out) { box.innerHTML = `<p class="hint">1번부터 골라 보세요. 2·3번은 건너뛰어도 돼요.</p>`; return; }
    const want = OUT_AREAS[quiz.out];
    let list = DATA.skills.filter(s => s.areas.some(a => want.includes(a)) && s.install?.type !== "list");
    if (quiz.pay === "free") list = list.filter(s => !needsKey(s));
    const score = s => {
      let n = s.areas.filter(a => want.includes(a)).length * 3 + (s.areas[0] === want[0] ? 3 : 0);
      if (s.installed) n += 2;
      if (quiz.env === "app" && ["builtin", "mine", "official", "folder"].includes(s.install?.type)) n += 2;
      if (quiz.env === "code" && ["repo", "folder", "official"].includes(s.install?.type)) n += 2;
      if (quiz.env === "ko" && s.korean) n += 6;
      if (s.areas.includes("meta")) n -= 3;
      return n;
    };
    list = list.map(s => [s, score(s)]).sort((a, b) => b[1] - a[1] || a[0].name.localeCompare(b[0].name)).slice(0, 5).map(x => x[0]);
    const rec = recipesFor(want, "")[0];
    box.innerHTML = `<h3>추천 스킬 ${list.length}개</h3><div class="grid">${list.map(card).join("")}</div>` +
      (rec ? `<div class="rec-box">이어서 쓰면 좋은 레시피 · <button data-recipe="${rec.id}">${rec.icon} ${esc(rec.title)} →</button></div>` : "");
  }

  // E. 새로 들어온 스킬 (회차별)
  function renderBatches() {
    const groups = {};
    DATA.skills.filter(s => s.batch).forEach(s => (groups[s.batch] = groups[s.batch] || []).push(s));
    const keys = Object.keys(groups).sort().reverse();
    $("#batches").innerHTML = keys.length ? keys.map(k => {
      const list = sortSkills(groups[k]);
      const cnt = {};
      list.forEach(s => cnt[s.areas[0]] = (cnt[s.areas[0]] || 0) + 1);
      const by = Object.entries(cnt).sort((a, b) => b[1] - a[1]).map(([a, n]) => `${AREA[a]?.name || a} ${n}`).join(" · ");
      const s0 = list[0];
      const rm = k.match(/^\d{4}-\d{2}-\d{2}-(\d+)$/);
      const title = rm ? `${s0.batch_date || k.slice(0, 10)} · ${+rm[1]}회차` : `${s0.batch_date || ""} · 카톡 메모에서`;
      return `<section class="batch"><div class="batch-head"><h3>${esc(title)}</h3><span>${list.length}개 · ${esc(by)}${s0.batch_by ? " · " + esc(s0.batch_by) : ""}</span></div>
        <div class="grid">${list.map(card).join("")}</div></section>`;
    }).join("") : `<p class="empty">아직 수집 회차가 없어요.</p>`;
  }

  function setView(v) {
    document.querySelectorAll(".tab").forEach(t => t.classList.toggle("is-on", t.dataset.view === v));
    document.querySelectorAll(".view").forEach(el => el.classList.toggle("is-on", el.id === "view-" + v));
    window.scrollTo({ top: 0 });
  }

  let toastT;
  function toast(msg) {
    const t = $("#toast"); t.textContent = msg; t.classList.add("show");
    clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("show"), 1600);
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); }
    catch (e) {
      const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta);
      ta.select(); try { document.execCommand("copy"); } catch (_) {} ta.remove();
    }
    toast("복사했어요");
  }
  const refresh = () => { renderQuick(); renderAreas(); renderGrid(); };

  document.addEventListener("click", e => {
    const el = e.target.closest("[data-copy],[data-open],[data-fav],[data-area],[data-src],[data-view],[data-close],[data-recipe],[data-quick],[data-tag],[data-itab],.opts button");
    if (!el) { const c = e.target.closest(".card"); if (c) openDetail(c.dataset.id); return; }
    const d = el.dataset;
    if (d.copy !== undefined) { e.stopPropagation(); copy(d.copy); return; }
    if (d.fav) {
      e.stopPropagation();
      favs.has(d.fav) ? favs.delete(d.fav) : favs.add(d.fav); saveFavs();
      renderGrid(); if (!$("#sheet").hidden) openDetail(d.fav, false); return;
    }
    if (d.itab) {
      const panel = el.closest(".d-sec");
      panel.querySelectorAll("[data-itab]").forEach(b => b.classList.toggle("is-on", b === el));
      panel.querySelectorAll("[data-pane]").forEach(p => p.classList.toggle("is-on", p.dataset.pane === d.itab));
      try { localStorage.setItem("sab-itab", d.itab); } catch (_) {}
      return;
    }
    if (el.closest(".opts")) { const q = el.closest(".opts").dataset.q; quiz[q] = quiz[q] === d.v ? null : d.v; renderQuiz(); return; }
    if (d.open) { openDetail(d.open); return; }
    if (d.quick) {
      if (d.quick === "ko") { state.ko = !state.ko; state.area = null; }
      else { state.area = state.area === d.quick ? null : d.quick; state.ko = false; }
      refresh(); $("#areas").scrollIntoView({ behavior: "smooth", block: "start" }); return;
    }
    if (d.tag) { state.q = d.tag; $("#q").value = d.tag; state.area = null; state.ko = false; refresh(); return; }
    if (d.area !== undefined) { state.area = d.area || null; state.ko = false; refresh(); return; }
    if (d.src) { state.source = d.src; renderSources(); renderGrid(); return; }
    if (d.view) { setView(d.view); return; }
    if (d.recipe) { closeDetail(); setView("recipes"); setTimeout(() => document.getElementById("recipe-" + d.recipe)?.scrollIntoView({ behavior: "smooth", block: "start" }), 30); return; }
    if (d.close !== undefined) closeDetail();
  });
  $("#q").addEventListener("input", e => { state.q = e.target.value.trim(); renderGrid(); });
  $("#only-installed").addEventListener("change", e => { state.installed = e.target.checked; renderGrid(); });
  $("#only-fav").addEventListener("change", e => { state.fav = e.target.checked; renderGrid(); });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !$("#sheet").hidden) closeDetail();
    if (e.key === "/" && document.activeElement !== $("#q")) { e.preventDefault(); setView("browse"); $("#q").focus(); }
  });

  $("#stat-total").textContent = DATA.skills.length;
  renderQuick(); renderAreas(); renderSources(); renderGrid(); renderRecipes(); renderQuiz(); renderBatches();
  const m = location.hash.match(/^#skill=(.+)$/);
  if (m) openDetail(decodeURIComponent(m[1]), false);
})();
