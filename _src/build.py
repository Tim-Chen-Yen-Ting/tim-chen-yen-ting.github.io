"""Generates ../index.html with English + Traditional Chinese side by side.

Run:  python _src/build.py
Every visible string is written once as (English, 中文) so the two never drift apart.
"""
from pathlib import Path


def T(en, zh):
    return f'<span lang="en">{en}</span><span lang="zh-Hant">{zh}</span>'


def P(en, zh, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c} lang="en">{en}</p>\n<p{c} lang="zh-Hant">{zh}</p>'


def H3(n, en, zh):
    return f'<h3><span class="num">{n}</span>{T(en, zh)}</h3>'


def chips(items):
    return '<p class="chips">' + "".join(f"<span>{i}</span>" for i in items) + "</p>"


def btn(href, en, zh, ghost=False):
    cls = "button ghost" if ghost else "button"
    return f'<a class="{cls}" href="{href}">{T(en, zh)}</a>'


def tile(key, thumb, title, q, a, extra_class=""):
    return f"""
        <button class="tile" data-open="d-{key}">
          {thumb}
          <span class="tile-body">
            <span class="tile-title">{title}</span>
            <span class="tile-q">{q}</span>
            <span class="tile-a">{a}</span>
            <span class="tile-more">{T("Open →", "展開 →")}</span>
          </span>
        </button>"""


def img_thumb(src, alt, cls=""):
    return f'<span class="thumb {cls}"><img src="assets/img/{src}" alt="{alt}" loading="lazy"></span>'


def dialog(key, emoji_title, hook, img, sections, links_html=None, note=None, diagram=None, demo=False):
    out = [f'  <dialog class="modal" id="d-{key}" aria-labelledby="t-{key}">',
           '    <form method="dialog"><button class="close" aria-label="Close">×</button></form>']
    if img:
        cls = "modal-img portrait" if img[0] == "lana.png" else "modal-img"
        out.append(f'    <img class="{cls}" src="assets/img/{img[0]}" alt="{img[1]}" loading="lazy">')
    out.append(f'    <h2 id="t-{key}">{emoji_title}</h2>')
    out.append("    " + hook)
    for i, (en_title, zh_title, body) in enumerate(sections, 1):
        out.append("    " + H3(i, en_title, zh_title))
        out.append(body)
        if diagram and i == 2:
            out.append(diagram)
    if links_html:
        if demo:
            out.append("    " + H3(len(sections) + 1, "Demo &amp; code", "Demo 與原始碼"))
        else:
            out.append("    " + H3(len(sections) + 1, "Code", "原始碼"))
        out.append(f'    <p class="links">{links_html}</p>')
    if note:
        out.append("    " + note)
    out.append("  </dialog>")
    return "\n".join(out)


def hook(en, zh):
    return P(en, zh, "hook")


# ============================================================ PAGE ==========
head = f"""<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Yen-Ting (Tim) Chen</title>
  <meta name="description" content="Yen-Ting (Tim) Chen: UCLA Statistics &amp; Data Science. I build AI systems, then try very hard to prove they work.">
  <meta name="color-scheme" content="dark">
  <script>document.documentElement.classList.add("js");</script>
  <link rel="stylesheet" href="style.css">
</head>
<body data-tab="home">
  <!-- Masthead: only shown on the About (home) tab. The tab bar below it sticks to the top on scroll. -->
  <div class="masthead">
    <div class="hero">
      <img class="headshot" src="assets/img/headshot.jpg" alt="Photo of Tim Chen" width="140" height="140">
      <div>
        <p class="eyebrow">{T("Yen-Ting (Tim) Chen", "陳彥廷 (Tim)")}</p>
        <h1>{T("I build AI systems, then try very hard to prove they work.", "我打造 AI 系統，然後拚命證明它們真的有用。")}</h1>
        {P("Mostly agent simulations, LLM evals, and a chess variant whose rules can't leak your secrets.",
           "主要是多代理人模擬、LLM 評測，還有一款規則不會洩漏你秘密的西洋棋變體。", "tagline")}
        <p class="hero-meta">{T("UCLA · Statistics &amp; Data Science · March 2027", "UCLA · 統計與資料科學 · 2027 年 3 月")}</p>
        <p class="links">
          {btn("#projects", "See what I've built", "看看我做了什麼")}
          {btn("assets/resumes/YenTing_Tim_Chen_CV.pdf", "Résumé", "履歷", True)}
          {btn("https://github.com/Tim-Chen-Yen-Ting", "GitHub", "GitHub", True)}
          {btn("https://www.linkedin.com/in/yen-ting-tim-chen-303276329", "LinkedIn", "LinkedIn", True)}
        </p>
      </div>
    </div>
  </div>

  <div class="tabbar">
    <div class="tabbar-inner">
      <a class="logo" href="#home">{T("Tim Chen", "陳彥廷 (Tim)")}</a>
      <nav id="tabs" aria-label="Sections">
        <a href="#home">{T("Home", "首頁")}</a>
        <a href="#projects">{T("Projects", "專案")}</a>
        <a href="#personal">{T("Personal", "個人")}</a>
        <a href="#contact">{T("Contact", "聯絡")}</a>
      </nav>
      <div class="lang-toggle" role="group" aria-label="Language">
        <button type="button" data-set-lang="en">EN</button>
        <button type="button" data-set-lang="zh-Hant">中文</button>
      </div>
    </div>
  </div>

  <main>
"""

about = f"""
    <!-- ===================== 1. ABOUT ===================== -->
    <section class="panel" id="panel-home" aria-label="Home">
      <div class="block selected">
        <h2>{T("Selected work", "精選作品")}</h2>
        {P("Two things worth a look if you only have a minute.", "如果你只有一分鐘，看這兩樣就夠了。", "meta")}
        <div class="selected-lead clickable" role="button" tabindex="0" data-open="d-civilizism">
          <img src="assets/img/civilizism.png" alt="Civilizism replay viewer" loading="lazy">
          <div>
            <h3>🏠 Civilizism</h3>
            {hook("What if you simulated one person really well, then simulated a lot of them?", "如果你把一個人模擬得夠好，再模擬很多個，會怎樣？")}
            {P("A social simulation where nobody scripts the outcome. The model proposes actions, and a personality engine decides which one happens.", "一個沒人編劇本的社會模擬。模型負責提議行動，由人格引擎決定哪一個真的發生。")}
            <p class="links">{btn("https://civilizism.vercel.app/viewer", "Watch a replay", "觀看回放")} <button type="button" class="button ghost" data-open="d-civilizism">{T("Full story", "完整故事")}</button></p>
          </div>
        </div>
        <div class="selected-work-job clickable" role="button" tabindex="0" data-open="d-phygtl">
          <div class="job-copy">
            <div class="job-head">
              <h3>🧪 {T("Phygtl · Agentic Systems Engineering Intern", "Phygtl · Agentic Systems Engineering 實習生")}</h3>
              <span class="date">{T("Summer 2026", "2026 夏季")}</span>
            </div>
            {hook("Nobody had built evaluation for Lana, so I did. The entire eval codebase is mine.", "沒有人替 Lana 建過評測，所以我來建。整個 eval 程式碼庫都是我的。")}
            <ul class="two-lines">
              <li>{T("Every night, six simulated AI users hold <strong>192 conversations</strong> with Lana (6 personas × 32 seeds), part of <strong>five evaluation pipelines</strong> I built.", "每晚，六個 AI 模擬使用者會跟 Lana 進行 <strong>192 場對話</strong>（6 個人格 × 32 個種子），這是我建立的<strong>五條評測管線</strong>的一部分。")}</li>
              <li>{T("A CI gate blocks any deploy that makes Lana worse (a <strong>regression above 5%</strong> on any axis, or any new hard failure), and I cut its per-PR cost <strong>69%</strong> without losing signal.", "CI 閘門會擋下任何讓 Lana 變差的部署（任一指標<strong>退步超過 5%</strong>，或出現任何新的硬性失敗），而且我在不損失訊號的情況下，把每次 PR 的成本<strong>降低了 69%</strong>。")}</li>
              <li>{T("An intent consolidation, tested on <strong>1,547 utterances</strong>, adopted by the CEO and AI lead.", "一項意圖合併方案，用 <strong>1,547 句</strong>測試集驗證，獲 CEO 與 AI 負責人採納。")}</li>
            </ul>
            <p class="links"><button type="button" class="button ghost" data-open="d-phygtl">{T("Read the full story", "閱讀完整故事")}</button></p>
          </div>
          <img class="job-img" src="assets/img/lana.png" alt="Lana, Phygtl's AI concierge" loading="lazy">
        </div>
      </div>

      <div class="two-col">
        <div class="block">
          <h2>{T("Overview", "概覽")}</h2>
          {P("I'm a stats student who keeps ending up building things nobody asked for. The common thread: I like putting guardrails on unpredictable systems, like language models that drift, simulated people who stop acting like themselves, and game rules that accidentally give away a hidden piece. (Yes, I've noticed the pattern. I've chosen to lean in.)",
             "我是個統計系學生，老是在做一些沒人拜託我做的東西。共通點是：我喜歡替不可預測的系統套上護欄，例如會漂移的語言模型、演著演著就不像自己的模擬人物，還有不小心洩漏暗棋的遊戲規則。（對，我注意到這個規律了，而且我決定擁抱它。）")}
          {P("I split my time between Los Angeles and Taiwan, and I'm looking for software, AI engineering, or data roles. I'm happy to talk about any of the three.",
             "我的時間分在洛杉磯和台灣之間，正在找軟體工程、AI 工程或資料相關的工作，三種都很樂意聊。")}
        </div>
        <div class="block">
          <h2>{T("Education", "學歷")}</h2>
          <p class="edu-school">UCLA</p>
          {P("B.S. Statistics &amp; Data Science, minor in Data Science Engineering", "統計與資料科學學士，輔修資料科學工程")}
          <p class="edu-dates">{T("Sept 2024 – Mar 2027", "2024 年 9 月 – 2027 年 3 月")}</p>
          {P("That's two and a half years. I'm calling it efficiency, not a cry for help.", "兩年半。我稱之為效率，不是求救訊號。")}
          {chips([T("Major GPA 3.96", "主修 GPA 3.96"), T("Latin Honors candidate", "拉丁榮譽候選"), T("Dean's Honors List", "院長榮譽榜")])}
        </div>
      </div>
"""


def glance_item(key, emoji, title, en, zh, badges):
    return f"""
        <button class="glance-item" data-open="d-{key}">
          <span class="glance-emoji" aria-hidden="true">{emoji}</span>
          <span class="glance-main">
            <span class="glance-title">{title}</span>
            <span class="glance-text">{T(en, zh)}</span>
            <span class="glance-badges">{"".join(f"<i>{b}</i>" for b in badges)}</span>
          </span>
        </button>"""


glance_items = [
    glance_item("civilizism", "🏠", "Civilizism",
                "Multi-agent social simulation where personality is enforced by code, not by prompts.",
                "多代理人社會模擬：人格由程式碼強制執行，而不是靠 prompt。",
                ["Python", "React", T("Live replay", "線上回放")]),
    glance_item("stratego", "♟️", T("Stratego-Chess", "行軍西洋棋"),
                "An original hidden-information game with a belief-tracking bot and a plain-URL interface for LLMs.",
                "原創的暗棋遊戲，有追蹤信念的機器人，以及讓 LLM 用純網址對戰的介面。",
                ["TypeScript", T("Playable", "可試玩")]),
    glance_item("whenwhere", "⏰", "WhenWhere",
                "A timezone-correct meeting planner on a live day/night map.",
                "在即時日夜地圖上、時區正確的會議時間規劃工具。",
                ["Python", "FastAPI", T("Live demo", "線上展示")]),
    glance_item("statuscard", "🔔", "Claude Code Status Card",
                "An always-on-top widget that shows which Claude Code session needs you.",
                "置頂小工具，告訴你哪個 Claude Code session 在等你。",
                ["Electron", "Node.js"]),
    glance_item("steme", "🧠", "STEME &amp; BLOC",
                "Semantic scoring and belief-clustering engines: 0.79–0.91 F1 and 0.70 ARI on their benchmarks.",
                "語意評分與信念分群引擎：基準測試 F1 為 0.79–0.91，ARI 為 0.70。",
                ["Python", "NLP"]),
    glance_item("coldemail", "📬", "Cold Email Automator",
                "An end-to-end outreach pipeline that researches, drafts, sends and tracks.",
                "端到端的開發信流程：研究、撰寫、寄出、追蹤。",
                ["Python", "Gmail API"]),
    glance_item("messages", "💬", "Past Messages Analyzer",
                "Privacy-first analysis of how a friendship's tone drifts over time.",
                "以隱私為先，分析一段友情的語氣如何隨時間漂移。",
                ["Python", "NLP"]),
    glance_item("pkb", "📚", T("Personal Knowledge Base", "個人知識庫"),
                "Upload documents, ask across them, and audit your knowledge gaps.",
                "上傳文件、跨文件提問，並審計你的知識缺口。",
                ["Python", "Supabase"]),
]

about += f"""
      <div class="block">
        <h2>{T("Projects at a glance", "專案一覽")}</h2>
        {P("The short version, for people skimming. Click any row for the whole story.", "給快速瀏覽的人看的精簡版。點任何一列看完整故事。", "meta")}
        <div class="glance">{"".join(glance_items)}
        </div>
      </div>

      <div class="block">
        <h2>{T("Toolbox", "工具箱")}</h2>
        <div class="toolbox">
          <p class="tool-label">{T("Languages", "程式語言")}</p>
          {chips(["Python", "TypeScript / JavaScript", "R", "SQL", "HTML / CSS"])}
          <p class="tool-label">{T("AI &amp; data", "AI 與資料")}</p>
          {chips([T("LLM APIs (Claude, GPT, Gemini)", "LLM API（Claude、GPT、Gemini）"), "sentence-transformers", "scikit-learn", "XGBoost", "pandas", "NumPy", "Pydantic"])}
          <p class="tool-label">{T("Backend &amp; infrastructure", "後端與基礎設施")}</p>
          {chips(["FastAPI", "Node.js / Fastify", "PostgreSQL", "SQLite", "Supabase", "pytest", "GitHub Actions"])}
          <p class="tool-label">{T("Frontend &amp; deployment", "前端與部署")}</p>
          {chips(["React", "Electron", "Streamlit", "Vercel", "Render"])}
        </div>
      </div>
    </section>
"""

tiles = [
    tile("civilizism", img_thumb("civilizism.png", "Civilizism replay viewer"),
         "🏠 Civilizism",
         T("What if you simulated one person really well, then simulated a lot of them?", "如果你把一個人模擬得夠好，再模擬很多個，會怎樣？"),
         T("A social simulation where nobody scripts the outcome. Beliefs and relationships are just a side effect.", "一個沒人編劇本的社會模擬。信念與關係只是副作用。")),
    tile("stratego", img_thumb("stratego.png", "Stratego-Chess game screenshot"),
         T("♟️ Stratego-Chess", "♟️ 行軍西洋棋 Stratego-Chess"),
         T("What if chess no longer has a 100% capture rate?", "如果西洋棋的吃子不再是 100% 成功呢？"),
         T("The child of Chess and Stratego. Pieces move like chess, but secret ranks decide who wins the fight.", "西洋棋和行軍棋的孩子。棋子走法像西洋棋，但暗藏的階級決定誰贏。")),
    tile("whenwhere", img_thumb("whenwhere.png", "WhenWhere world map"),
         "⏰ WhenWhere",
         T("What if you need to find some time to meet a friend on the other side of the globe?", "如果你要跟地球另一端的朋友找時間見面呢？"),
         T("A day/night map that shows when everyone overlaps, and who else could still join.", "在日夜地圖上看大家的空檔何時重疊，還有哪些城市也能加入。")),
    tile("statuscard", img_thumb("statuscard.png", "Claude Code Status Card", "contain"),
         "🔔 Claude Code Status Card",
         T("What if you could tell which Claude Code session needs you without alt-tabbing through all of them?", "如果你不用切視窗，就知道哪個 Claude Code session 在等你呢？"),
         T("A tiny always-on-top card per session: blue is working, red is &quot;come here&quot;, green is done.", "每個 session 一張置頂小卡：藍色是工作中，紅色是「快過來」，綠色是完成。")),
    tile("steme", img_thumb("steme_bloc.png", "STEME and BLOC benchmark results", "contain"),
         "🧠 STEME &amp; BLOC",
         T("What if you could turn &quot;sincerity&quot; into a number without calling an LLM every time?", "如果不用每次呼叫 LLM，就能把「真誠」變成數字呢？"),
         T("Two research engines under Civilizism: semantic scoring and incremental belief clustering.", "Civilizism 底下的兩個研究引擎：語意評分與增量式信念分群。")),
    tile("coldemail", img_thumb("coldemail.png", "Cold Email Automator pipeline diagram"),
         "📬 Cold Email Automator",
         T("What if the job hunt did its own legwork?", "如果求職的跑腿工作能自己做完呢？"),
         T("Researches who to contact, drafts a note around something specific, sends it, tracks replies.", "研究該聯絡誰、圍繞一個具體切入點寫信、寄出、追蹤回覆。")),
    tile("messages", img_thumb("messages.png", "Past Messages Analyzer pipeline diagram"),
         "💬 Past Messages Analyzer",
         T("What if you could watch a friendship's tone drift over time?", "如果你能看見一段友情的語氣如何隨時間漂移呢？"),
         T("Turns old Messenger and Instagram exports into a database and tracks the drift. Weirdly emotional for stats.", "把舊的 Messenger 與 Instagram 紀錄變成資料庫並追蹤漂移。對統計專題來說情緒過於豐富。")),
    tile("pkb", img_thumb("pkb.png", "Personal Knowledge Base chat screen"),
         "📚 Personal Knowledge Base",
         T("What if your notes could tell you what you're missing?", "如果你的筆記能告訴你還缺什麼呢？"),
         T("Drop in documents, ask questions across them, and get an audit of where the gaps are.", "丟進文件、跨文件提問，還有知識缺口審計。")),
]

projects = f"""
    <!-- ===================== 2. PROJECTS ===================== -->
    <section class="panel" id="panel-projects" aria-label="Projects">
      <h2 class="panel-title">{T("Projects", "專案")}</h2>
      {P("Click anything for the full story: the problem, the fix, and the bugs that made me question my life choices.",
         "點任何一張卡片看完整故事：問題、解法，還有那些讓我懷疑人生的 bug。", "panel-sub")}

      <div class="gallery">
{"".join(tiles)}
      </div>
    </section>
"""

facts = [
    ("🏐", "Sport", "運動",
     "Volleyball. I play badly, but who can reject a sport that gives you a valid excuse to roll on the floor? Also, Haikyu is fire.",
     "排球。我打得很爛，但誰能拒絕一個讓你有正當理由在地上打滾的運動？還有，《排球少年》超神。"),
    ("🏴‍☠️", "Anime", "動漫",
     "One Piece. The only anime better than One Piece is One Piece before the time skip. After the time skip... that's hard to say... Oda, I know you can do better.",
     "《海賊王》。唯一比《海賊王》更好看的動漫，是時間跳躍前的《海賊王》。時間跳躍後嘛…這不好說…尾田老師，我知道你可以更好的。"),
    ("📚", "Light novel", "輕小說",
     "No Game No Life. Yuu Kamiya, where is the new volume? It's been ten years. Also, your books are a bit too smart for me, but that's what a battle of wits is.",
     "《遊戲人生》。榎宮祐老師，新的一集呢？已經十年了。還有，你的書對我來說有點太聰明了，但這就是鬥智。"),
    ("🎤", "Artist", "歌手",
     "The globally renowned pick: JJ Lin. The hot take: Ren Ran, no hesitation. I have a 15-hour Spotify playlist of only Ren Ran songs, and I didn't even know Spotify had that many.",
     "舉世聞名的選擇：林俊傑。冷門的看法：任然，毫不猶豫。我有一個 15 小時、全是任然的 Spotify 歌單，我甚至不知道 Spotify 上有那麼多任然的歌。"),
    ("🍜", "Food", "食物",
     "Lu wei (Taiwanese braised street snacks), no hesitation. Stir-fried noodles are a close second. In the US the closest thing is malatang, which is somehow expensive, so my US pick is Chick-fil-A. Thinking about it is making me want some right now.",
     "滷味，毫不猶豫。炒麵是第二名。在美國最接近的是麻辣燙，但它貴得莫名其妙，所以我的美國首選是 Chick-fil-A。想到這裡我現在就想吃。"),
    ("🐻", "School", "學校",
     "U! C! L! A! Fight, fight, fight! I'm convinced the eight clap is written in our DNA.",
     "U！C！L！A！Fight, fight, fight！我深信八拍掌（eight clap）已經寫進我們的 DNA 裡。"),
    ("💬", "Quote", "名言",
     "&quot;We do these things not because they are easy, but because we thought they were going to be easy.&quot; John F. Kennedy did not say this. Maciej Cegłowski did.",
     "「我們做這些事，不是因為它們容易，而是因為我們以為它們會很容易。」甘迺迪沒說過這句話，是 Maciej Cegłowski 說的。"),
    ("😴", "Spare time", "閒暇時間",
     "Sleep and reading light novels when I'm broke, whiskey tasting when I'm rich. I'm a college student, so you can guess which one wins.",
     "窮的時候睡覺、看輕小說，有錢的時候品威士忌。我是大學生，所以你可以猜猜哪個比較常發生。"),
]
fact_html = "".join(
    f'\n        <article class="fact">\n          <p class="fact-label">{e} {T(en, zh)}</p>\n          {P(ben, bzh)}\n        </article>'
    for e, en, zh, ben, bzh in facts)

personal = f"""
    <!-- ===================== 3. PERSONAL ===================== -->
    <section class="panel" id="panel-personal" aria-label="Personal">
      <h2 class="panel-title">{T("The non-work me", "工作以外的我")}</h2>
      {P("Strong opinions, held loosely. Mostly about anime and food.", "強烈的意見，鬆鬆地持有。主要關於動漫和食物。", "panel-sub")}

      <article class="block novel">
        <h3>{T("📖 The Unobserved", "📖 《未然？已然。》")}</h3>
        {hook("What if your power depended on how sharply you understood reality?", "如果你的力量取決於你對現實理解得多銳利呢？")}
        {P("An original fantasy novel · Traditional Chinese · in progress", "原創奇幻小說 · 繁體中文 · 撰寫中", "meta")}
        {P("In this world, every attack on a living opponent gets turned into a hallucination, so their body stays untouched until you break their mind first. At the center are a boy who sealed away his ability to feel, and a girl who senses every possibility, including the ones she kills by choosing.",
           "在這個世界裡，對活人的任何攻擊都會被轉化成幻覺，所以在你擊潰對方的心智之前，他的身體毫髮無傷。故事中心是一個封印了感受能力的少年，和一個能感知所有可能性、包括她因做出選擇而扼殺的那些可能性的少女。")}
        {P("Right now it's a world, a cast, and a storyboard through the first arc, planned to run past 800,000 words. The prose is the part I'm putting off. (The plan is AI help filling in between my beats, with me reviewing, and the repo says so openly.)",
           "目前它是一個世界、一群角色，以及涵蓋第一篇章的分鏡，預計寫到超過 80 萬字。正文是我在拖延的部分。（計畫是由 AI 在我的劇情節點之間補寫、我負責審稿，而且 repo 裡有公開寫明。）")}
        <p class="links">{btn("https://github.com/Tim-Chen-Yen-Ting/Design-The_Unobserved", "Read the world design", "閱讀世界設定", True)}</p>
      </article>

      <h3 class="subhead">{T("Favorites", "最愛")}</h3>
      <div class="facts">{fact_html}
      </div>
    </section>
"""

def faq(q_en, q_zh, a_en, a_zh):
    return f"""
        <details class="faq">
          <summary>{T(q_en, q_zh)}</summary>
          {P(a_en, a_zh)}
        </details>"""


def fact_row(label_en, label_zh, val_en, val_zh):
    return f'<div class="cheat-row"><dt>{T(label_en, label_zh)}</dt><dd>{T(val_en, val_zh)}</dd></div>'


cheat = "".join([
    fact_row("Name", "名字", "Yen-Ting (Tim) Chen. Tim is also on my passport as an alternative name.", "陳彥廷，但我都叫 Tim，護照上也有 Tim 這個別名。"),
    fact_row("Based in", "所在地", "Los Angeles and Taiwan", "洛杉磯與台灣"),
    fact_row("Languages", "語言", "English and Mandarin Chinese (Traditional)", "英文與中文（繁體）"),
    fact_row("Graduating", "畢業時間", "March 2027, UCLA, B.S. Statistics &amp; Data Science", "2027 年 3 月，UCLA 統計與資料科學學士"),
    fact_row("Available", "可到職時間", "From April 2027", "2027 年 4 月起"),
    fact_row("Looking for", "正在尋找", "Software, AI engineering, or data roles", "軟體、AI 工程或資料相關職位"),
    fact_row("Most recent role", "最近的職位", "Agentic Systems Engineering Intern, Phygtl (summer 2026)", "Phygtl 的 Agentic Systems Engineering 實習生（2026 夏季）"),
])

faqs = "".join([
    faq("Are you authorized to work in the US? Do you need sponsorship?", "你有在美國工作的許可嗎？需要簽證擔保嗎？",
        "Yes, I'm authorized to work in the US through F-1 OPT and STEM OPT, and I don't need visa sponsorship. Happy to talk through the details in an interview.",
        "有，我透過 F-1 OPT 與 STEM OPT 取得在美國工作的授權，而且不需要簽證擔保。細節很樂意在面試時聊。"),
    faq("Which resume should I read?", "我該看哪一份履歷？",
        "Hiring for software? Grab the software one. Forward-deployed or customer-facing engineering? The forward-deployed one. Stats or data science? The last one. Can't decide? The full CV has all of it, and I won't be offended by the length.",
        "找軟體工程師？看軟體那份。Forward-deployed 或貼近客戶的工程？看 forward-deployed 那份。統計或資料科學？看最後一份。下不了決定？完整 CV 什麼都有，我不會介意它很長。"),
    faq("Is Tim your real name?", "Tim 是你的本名嗎？",
        "My legal name is Yen-Ting Chen. I go by Tim, and Tim is also listed on my passport as an alternative name, so both are real and both work. Use whichever you like.",
        "我的本名是陳彥廷，但我習慣被叫 Tim，而 Tim 也登記在我的護照上作為別名，所以兩個都是真的、都通用。你喜歡哪個就叫哪個。"),
    faq("Can I see the private Civilizism code?", "我可以看 Civilizism 的私有程式碼嗎？",
        "Yes, on request. The public repo has the architecture, devlogs, research engines and sample outputs. The core simulation lives in a private repo, and I'm happy to walk someone through it.",
        "可以，歡迎提出。公開 repo 有架構文件、開發日誌、研究引擎與範例輸出。核心模擬放在私有 repo 裡，我很樂意帶人走一遍。"),
    faq("Why is there so much humor on this site?", "為什麼這個網站這麼多玩笑？",
        "Because my READMEs, devlogs and commit messages are like this too. You'd have found out eventually, and I'd rather you find out before the interview.",
        "因為我的 README、開發日誌和 commit 訊息也都是這樣。你遲早會發現，我寧可你在面試前就發現。"),
    faq("Good reasons to email me", "寄信給我的好理由",
        "You're hiring for software, AI or data roles. You want to see the private Civilizism code. You found a bug in WhenWhere, or you beat my Stratego-Chess bot. You want to settle the One Piece post-timeskip debate. Or you are Yuu Kamiya, and you have news about No Game No Life.",
        "你在招軟體、AI 或資料相關職位。你想看 Civilizism 的私有程式碼。你在 WhenWhere 找到 bug，或者打贏了我的行軍西洋棋機器人。你想來裁決《海賊王》時間跳躍後的爭議。或者你就是榎宮祐老師，而且帶來了《遊戲人生》的消息。"),
])

contact = f"""
    <!-- ===================== 4. CONTACT ===================== -->
    <section class="panel" id="panel-contact" aria-label="Contact">
      <h2 class="panel-title">{T("Say hi", "打聲招呼")}</h2>
      {P("Email is the fastest way to reach me. I split my time between the US and Taiwan, so phone reception is a coin flip.",
         "最快的聯絡方式是電子郵件。我的時間分在美國和台灣之間，所以手機訊號是擲硬幣。", "panel-sub")}

      <p class="links">
        {btn("mailto:timchen56789@gmail.com", "Email", "寄信")}
        {btn("https://www.linkedin.com/in/yen-ting-tim-chen-303276329", "LinkedIn", "LinkedIn", True)}
        {btn("https://github.com/Tim-Chen-Yen-Ting", "GitHub", "GitHub", True)}
      </p>

      <h3 class="subhead">{T("Resumes", "履歷")}</h3>
      {P("Same person, three framings. Grab whichever fits the role.", "同一個人，三種包裝。挑適合該職缺的那份。", "panel-sub")}
      <div class="downloads">
        <a class="download" href="assets/resumes/YenTing_Tim_Chen_Resume_SWE.pdf"><strong>{T("Software engineering", "軟體工程")}</strong><span>PDF</span></a>
        <a class="download" href="assets/resumes/YenTing_Tim_Chen_Resume_FDE.pdf"><strong>{T("Forward-deployed engineering", "Forward-deployed 工程")}</strong><span>PDF</span></a>
        <a class="download" href="assets/resumes/YenTing_Tim_Chen_Resume_StatsDS.pdf"><strong>{T("Statistics &amp; data science", "統計與資料科學")}</strong><span>PDF</span></a>
        <a class="download" href="assets/resumes/YenTing_Tim_Chen_CV.pdf"><strong>{T("Full CV", "完整 CV")}</strong><span>{T("PDF · everything, all of it", "PDF · 全部，一個不漏")}</span></a>
      </div>

      <div class="two-col">
        <div class="block">
          <h2>{T("The recruiter cheat sheet", "招募人員速查表")}</h2>
          <dl class="cheat">{cheat}</dl>
        </div>
        <div class="block clocks">
          <h2>{T("Where &amp; when", "在哪、幾點")}</h2>
          <div class="clock-row"><span class="clock-city">{T("Los Angeles", "洛杉磯")}</span><span class="clock-time" id="clock-la">--:--</span></div>
          <div class="clock-row"><span class="clock-city">{T("Taipei", "台北")}</span><span class="clock-time" id="clock-tpe">--:--</span></div>
          {P("Those are the live local times. Only one of the two does daylight saving, so the gap is 15 or 16 hours depending on the season. If you're scheduling an interview and want an overlap, my WhenWhere project will gladly do the math.",
             "以上是即時的當地時間。兩地只有一邊實施日光節約時間，所以時差依季節是 15 或 16 小時。如果你要排面試、想找重疊時段，我的 WhenWhere 專案很樂意幫你算。", "note")}
        </div>
      </div>

      <h3 class="subhead">{T("Questions you might have", "你可能想問的")}</h3>
      <div class="faqs">{faqs}
      </div>
    </section>

  </main>

  <footer>
    <p>&copy; <span id="year"></span> {T("Yen-Ting (Tim) Chen", "陳彥廷 (Tim)")}&nbsp;·&nbsp;{T("UCLA, B.S. Statistics &amp; Data Science, 2027", "UCLA 統計與資料科學學士，2027")}</p>
  </footer>
"""

# ============================================================ DIALOGS =======
dialogs = []

dialogs.append(dialog(
    "phygtl", "🧪 Phygtl · " + T("Agentic Systems Engineering Intern", "Agentic Systems Engineering 實習生"),
    hook("How do we know whether Lana is doing what she's supposed to do?", "我們怎麼知道 Lana 有沒有在做她該做的事？"),
    ("lana.png", "Lana, Phygtl's AI concierge"),
    [
        ("The problem", "問題",
         P("Lana is Phygtl's AI concierge: a sheep in a bellhop uniform who helps people find something nearby or share something with their neighbors. She's live in production. When I got there, &quot;is Lana better or worse after this change?&quot; was answered mostly by hope, and quality meant someone chatting with her by hand. (Totally normal for a young product. Also how you get surprised later.) Nobody had built evaluation for her, so the whole eval codebase is mine.",
           "Lana 是 Phygtl 的 AI 管家：一隻穿著飯店服務生制服的小羊，幫人找附近的東西，或和鄰居分享東西。她已經在正式環境上線。我到職時，「這次改動讓 Lana 變好還是變差？」主要靠希望來回答，品質檢查就是有人手動跟她聊天。（對年輕產品來說很正常，也是日後會嚇到你的原因。）沒有人替她建過評測，所以整個 eval 程式碼庫都是我的。")),
        ("My solution", "我的解法",
         P("My first task was going from manual QA to a simulation environment. Six AI mock users with deliberately different personas hold <strong>192 conversations</strong> with Lana <em>every night</em> (6 personas × 32 seeds across 7 buckets, each seed testing one specific behavior), like a performance review she can't skip. Then <strong>five evaluation pipelines</strong> read those conversations: core conversational evaluation, claim extraction and personal-data checks, a matcher and unlock flow, conversational policy and safety, and automated triage of whatever the others flagged.",
           "我的第一個任務，是從手動 QA 走向模擬環境。六個人格刻意各異的 AI 模擬使用者，<em>每天晚上</em>都會和 Lana 進行 <strong>192 場對話</strong>（6 個人格 × 7 個類別共 32 個種子，每個種子只測一種特定行為），像一場她逃不掉的績效考核。接著由<strong>五條評測管線</strong>讀這些對話：核心對話評測、資訊擷取與個資檢查、配對與解鎖流程、對話政策與安全，以及自動分流其他管線標出的問題。") + "\n" +
         P("On top of that came regression checks and CI/CD that answer the real question: are we making Lana better or worse? A pull-request gate blocks a deploy on any regression above 5% on an axis, or any new hard failure.",
           "再往上疊的是回歸檢查與 CI/CD，用來回答真正的問題：我們是讓 Lana 變好還是變差？Pull request 閘門會在任何指標退步超過 5%、或出現任何新的硬性失敗時擋下部署。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("Before I trusted any of it, I read the first few dozen conversation histories by hand, counting false negatives and false positives, and used that to tune both the mock users and the checks. Unglamorous, and the reason the rest could be trusted. Later, a measured audit found my own mock user breaking character in 13 of 102 conversations (12.7%), and I fixed that so a failure would mean something about Lana, not about my simulator.",
           "在我信任這一切之前，我親手讀了最初的幾十筆對話紀錄，數出漏報和誤報有多少，並用它來調整模擬使用者和各項檢查。一點也不光鮮，但後面的一切能被信任就是靠它。後來一次量化審查發現，我自己的模擬使用者在 102 場對話中有 13 場（12.7%）出戲，我把它修好，讓失敗代表的是 Lana 的問題，而不是我模擬器的問題。") + "\n" +
         P("The core idea is to split every check by <em>how it can fail</em>. If the right answer is known by construction (a banned word, a planted piece of personal data), plain code checks it, because a flaky check poisons a deploy gate. Only the truly subjective questions, like &quot;warm, but not sycophantic?&quot;, go to an LLM judge. And every check ships with a test that feeds it a deliberate violation, because a green run means nothing if the check can't fail. (Yes, I wrote tests for my tests. No, I don't feel bad about it.)",
           "核心想法是依「失敗方式」拆分每一項檢查。如果正確答案在設計上就已知（禁用詞、刻意埋進去的個資），就用純程式碼檢查，因為不穩定的檢查會毒害部署閘門。只有真正主觀的問題，例如「溫暖但不諂媚嗎？」，才交給 LLM 評審。而且每項檢查都附帶一個故意塞入違規的測試，因為如果檢查不可能失敗，全綠的結果就毫無意義。（對，我替我的測試寫了測試，而且我一點都不愧疚。）") + "\n" +
         P("I kept the judge model off the product's own model family, so it never grades its own kind. And the triage tool collapsed a 729-row human-review queue by re-deriving evidence from stored transcripts instead of asking a second LLM, then measured itself against 51 human-labeled rows rather than just asserting it was right.",
           "我讓評審模型和產品使用的模型家族分開，這樣它就不會替自己人打分數。而分流工具把 729 筆待人工審核的佇列收斂掉，靠的是從儲存的對話紀錄重新推導證據、而不是再問一個 LLM，並且拿 51 筆人工標註的資料來衡量自己，而不是光說自己是對的。") + "\n" +
         P("The PR gate originally ran 6 personas × 18 seeds = 108 cases on every pull request. I cut it to 3 × 11 = 33, a 69% reduction, based on measured evidence. One seed from the most expensive bucket stayed because it was the only place hallucination ever fired, and I picked personas for contrast, not for failure count, since a gate that overfits to known bugs misses the next one. Nothing was deleted, only deferred to the nightly 192.",
           "PR 閘門原本每次 pull request 都跑 6 個人格 × 18 個種子 = 108 個案例。我根據量測到的證據，把它縮減成 3 × 11 = 33 個，減少了 69%。最昂貴的類別裡留下了一個種子，因為那是唯一曾經觸發幻覺的地方；人格則是依「差異性」挑選，而不是依失敗次數，因為只針對已知 bug 調整的閘門會漏掉下一個。沒有任何東西被刪除，只是延後到每晚的 192 個案例裡跑。") + "\n" +
         P("The part I'm proudest of: I argued that a pile of overlapping intents in the product should be merged. I wrote the proposal down in a dated document before testing it, then checked it on a 1,547-utterance set I built for the purpose, which broke a 39.9% baseline pass rate into three distinct root causes. The CEO approved it and the AI lead adopted it. Turns out &quot;I have a test set&quot; is a very persuasive sentence.",
           "我最自豪的是：我主張把產品裡一堆重疊的意圖（intent）合併。我先把提案寫進一份標註日期的文件，再用我為此建的 1,547 句測試集驗證，把 39.9% 的基準通過率拆解成三個不同的根本原因。CEO 核准了，AI 負責人採納了。事實證明「我有測試集」是非常有說服力的一句話。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "pytest", "GitHub Actions", "LLM-as-judge", "Simulated users", "Protocol-typed ports"]) + "\n" +
         P("This is where my vibe coding went from projects to commercial level: code that ran every night, gated real deploys, and that other engineers depended on. That raised the bar for everything: checks that can fail, a judge calibrated against something outside itself, tests for the tests.",
           "這是我的 vibe coding 從個人專案升級到商用等級的地方：程式碼每晚都在跑、把關真正的部署，而且有其他工程師依賴它。這讓一切標準都被拉高：會失敗的檢查、用自身以外的東西校準的評審、替測試寫的測試。") + "\n" +
         P("It also meant writing the conventions for a codebase that had none, so I wrote the agent-facing conventions doc and a README for every harness. My role was evaluation only, so when I found real product defects, I wrote each one up for the engineer who owned it.",
           "這也代表要替一個沒有任何慣例的程式碼庫訂慣例，所以我寫了給 agent 看的慣例文件，以及每個測試框架的 README。我的角色只負責評測，所以當我發現真正的產品缺陷時，我會把每一個都寫成交接給負責它的工程師。")),
    ],
))

dialogs.append(dialog(
    "civilizism", "🏠 Civilizism",
    hook("What if you simulated one person really well, then simulated a lot of them?", "如果你把一個人模擬得夠好，再模擬很多個，會怎樣？"),
    ("civilizism.png", "Civilizism replay viewer"),
    [
        ("The problem", "問題",
         P("Most social simulations hardcode the outcome: the rules say how groups behave, and, surprise, they behave that way. I wanted the opposite. Build one believable individual, then see whether groups, beliefs and norms show up on their own.",
           "大多數社會模擬會把結果寫死：規則規定群體怎麼行為，然後，驚喜，它們真的就那樣行為了。我想要相反的做法：先打造一個可信的個體，再看看群體、信念與規範會不會自己長出來。")),
        ("My solution", "我的解法",
         P("Agents that perceive, remember, reflect and plan, with memory as the hub of everything. Whatever beliefs and relationships form are a side effect and the surprise my product gives me in return. The model only <em>proposes</em> actions; a deterministic utility engine called SHAPE scores each one against 43 personality coefficients (Schwartz values plus HEXACO traits) and decides which actually happens. Character is enforced by code, not by prompting: a wild horse is only a good ride if you put a mathematical rein on it.",
           "代理人會感知、記憶、反思與規劃，記憶是一切的核心。形成什麼信念和關係，都只是副作用，也是我的產品回饋我的驚喜。模型只負責<em>提議</em>行動；一個叫 SHAPE 的確定性效用引擎，會根據 43 個人格係數（Schwartz 價值觀加 HEXACO 特質）替每個提議打分，並決定真正發生哪一個。性格由程式碼強制執行，而不是靠 prompt：野馬要給它套上一條數學韁繩，才騎得好。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("LLM agents drift based on vibes. My first four housemates snacked all day, paced between the kitchen and the living room, and once tried to blend smoothies from ingredients that didn't exist. (I'm told this is relatable.) Then they started hiding their sadness behind cheerful small talk, and I had to ask whether that was a bug or a personality trait. Humans do it constantly, so I refused to hardcode a fix and put the control in code instead.",
           "LLM 代理人會憑感覺漂移。我最早的四個室友整天吃零食、在廚房和客廳之間來回踱步，還有一次試圖用根本不存在的食材打果昔。（聽說這很有共鳴。）後來他們開始用開朗的閒聊掩飾悲傷，我只好自問：這是 bug 還是人格特質？人類天天這樣做，所以我拒絕寫死修正，改把控制放進程式碼。") + "\n" +
         P("The validation story is the nerdy one: I'm checking the whole thing against Milgram, Asch, Robbers Cave and the Stanford Prison Experiment, with predictions written down before any run so I can't cheat. The Stanford case is built so that a <em>null</em> result agrees with the modern reading of that study. The harness is done; the scored runs are still pending...waiting on the day I feel like letting my laptop run through an entire night and hopefully not burning down while I sleep through it.",
           "驗證的部分最書呆子：我拿整個系統去對照 Milgram、Asch、Robbers Cave 和史丹佛監獄實驗，而且預測在任何一次跑之前就先寫下，所以我沒辦法作弊。史丹佛那一組的設計，讓<em>虛無</em>結果也符合學界對該研究的現代解讀。測試框架完成了，正式計分的跑次還在等…等我哪天願意讓筆電整晚開著跑，並祈禱它在我睡著時不會燒起來。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "NumPy", "sentence-transformers", "LiteLLM + Instructor", "Pydantic", "React"]) + "\n" +
         P("Pydantic saved my life when parsing LLM output with regex was a living hell. This was also my first real step into vibe coding. And modelling humans, drawing on psychology and biology and turning it all into functions and memories, was a living hell of its own kind.",
           "當用 regex 解析 LLM 輸出簡直是人間煉獄時，Pydantic 救了我一命。這也是我踏進 vibe coding 的第一步。而要模仿人類——從心理學和生物學出發，再把一切變成函式和記憶——本身又是另一種煉獄。")),
    ],
    btn("https://civilizism.vercel.app/viewer", "Watch a replay", "觀看回放") + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/Civilizism", "Public repo", "公開 repo", True) + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/STEME", "STEME", "STEME", True) + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/BLOC", "BLOC", "BLOC", True),
    note=P("The core simulation code is private, and I'm happy to share it on request.", "核心模擬程式碼是私有的，有需要我很樂意分享。", "note"),
    diagram='    <img class="modal-diagram" src="assets/img/Civilizism_Info_Flow.png" alt="Civilizism information flow diagram" loading="lazy">',
    demo=True,
))

dialogs.append(dialog(
    "stratego", T("♟️ Stratego-Chess", "♟️ 行軍西洋棋 Stratego-Chess"),
    hook("What if chess no longer has a 100% capture rate?", "如果西洋棋的吃子不再是 100% 成功呢？"),
    ("stratego.png", "Stratego-Chess game screenshot"),
    [
        ("The problem", "問題",
         P("Chess is perfect information: everything is on the board. Stratego is all hidden information, but its pieces just shuffle forward one square at a time. What happens if you put the secrets onto chess movement?",
           "西洋棋是完全資訊：一切都在棋盤上。行軍棋全是隱藏資訊，但它的棋子只會一格一格往前挪。如果把那些祕密放到西洋棋的走法上，會發生什麼事？")),
        ("My solution", "我的解法",
         P("Welcome to the child of Chess and Stratego. Every piece moves like a chess piece (public), but also carries a hidden rank (secret) that decides what it beats. You can see how an enemy piece moves, never what it can capture. It is not chess: there's no checkmate, the king is just a piece, and passing is always legal. If you came to castle your way to safety, welcome.",
           "歡迎來到西洋棋和行軍棋的孩子。每顆棋子都像西洋棋那樣移動（公開），同時帶著一個暗藏的階級（祕密），決定它打得贏誰。你看得到敵方棋子怎麼走，卻永遠不知道它能吃掉什麼。這不是西洋棋：沒有將死、國王只是一顆普通的棋子、而且隨時可以跳過。如果你是來靠易位保平安的，歡迎。") + "\n" +
         P("No friends? No worries. There's a bot to play against, and the game is LLM friendly: swap <code>/g/</code> with <code>/llm/</code> in the URL and a chatbot can play by fetching plain links.",
           "沒朋友？沒關係。有機器人可以陪你下，而且這個遊戲對 LLM 很友善：把網址裡的 <code>/g/</code> 換成 <code>/llm/</code>，聊天機器人就能靠抓取純連結來下棋。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("The fun problem is that information leaks everywhere. If the game announced &quot;equal rank&quot; and &quot;bomb&quot; differently, the announcement itself would reveal a hidden piece, so both read as the same mutual destruction. Engineers and the flag are both immune to bombs, because an immunity only one piece had would point right at it. If your setup timer runs out, the server deals you a random legal army, since a predictable default is a leaked army.",
           "有趣的問題在於資訊會從各處洩漏。如果遊戲對「同階」和「爆裂物」的公告不一樣，公告本身就會洩漏暗棋，所以兩者都顯示成同樣的同歸於盡。工兵和軍旗都對爆裂物免疫，因為如果只有一種棋子免疫，就等於直接指名它。如果你的佈署計時用完，伺服器會替你發一支隨機的合法軍隊，因為可預測的預設值就是洩漏的軍隊。") + "\n" +
         P("The bot is a particle filter that keeps a running probability for what each of your pieces might be, and it plays a little randomly on purpose: a deterministic bot leaks its own ranks over enough games just by which move it reliably picks.",
           "機器人是個粒子濾波器，持續維護你每顆棋子可能是什麼的機率，而且刻意帶點隨機：確定性的機器人只要下得夠多局，光靠它固定會選哪一步，就會洩漏自己的階級。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["TypeScript", "Fastify 5", "Socket.IO", "React 19", "Vite", "Zustand", "Vitest"]) + "\n" +
         P("My first step into TypeScript, and my first time seeing client/server lessons up close. As a non-CS student I learned those lessons the hard way, and thank god Claude Code exists. The biggest takeaway was to make a leak <em>structurally impossible</em>: hidden ranks leave the server through exactly one function, so there's no display filter to forget about.",
           "我踏進 TypeScript 的第一步，也是第一次近距離接觸前後端的課題。身為非資工系的學生，這些課我都學得很辛苦，感謝老天有 Claude Code。最大的收穫是讓洩漏在<em>結構上不可能發生</em>：暗棋的階級只會通過唯一一個函式離開伺服器，所以不存在會被忘記的顯示過濾器。")),
    ],
    btn("https://stratego-chess.onrender.com/", "Play it", "開始玩") + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/stratego-chess", "Code", "原始碼", True),
    note=P("It's on free hosting, so the first load after a quiet spell can take up to a minute. Go stretch.",
           "它放在免費主機上，閒置一陣子後第一次載入可能要等到一分鐘。去伸個懶腰吧。", "note"),
    demo=True,
))

dialogs.append(dialog(
    "whenwhere", "⏰ WhenWhere",
    hook("What if you need to find some time to meet a friend on the other side of the globe?", "如果你要跟地球另一端的朋友找時間見面呢？"),
    ("whenwhere.png", "WhenWhere world map"),
    [
        ("The problem", "問題",
         P("I kept doing LA-to-Taipei math in my head, and it's a worse problem than it sounds: only one of the two places does daylight saving, so the offset between them changes twice a year. And I'm lazy.",
           "我老是在腦中算洛杉磯到台北的時差，而這問題比聽起來更糟：兩地只有一邊實施日光節約時間，所以兩地的時差一年會變兩次。而且我很懶。")),
        ("My solution", "我的解法",
         P("Add cities to a day/night map, say when each person is free, and it shows when everyone overlaps. Every other city on the map turns green or red depending on whether it could still join. There's also a simple point-in-time converter. Daylight saving and half-hour timezones are handled properly, so you can trust this more than the old fashioned clock on your wall...as long as you can find your city on the map.",
           "把城市加到日夜地圖上，說出每個人的空檔，它就會顯示大家何時重疊。地圖上其他每座城市會依「還能不能加入」變成綠色或紅色。也有簡單的單一時間點換算。日光節約時間和半小時時區都處理得正確，所以你可以比牆上那個老派時鐘更信任它…只要你找得到你的城市。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("For cities far enough apart, the real overlap can land on <em>adjacent calendar days</em>, so &quot;same local window&quot; has to be treated as a recurring daily pattern, not the date you typed. And the map itself fought me: Russia, Fiji and Antarctica drew spurious bands across the whole world because their polygons cross the antimeridian and the map library doesn't wrap. I had to split the rings.",
           "對於相隔夠遠的城市，真正的重疊時段可能落在<em>相鄰的兩個日曆日</em>，所以「當地同一時段」必須當成每日重複的模式處理，而不是你輸入的那個日期。地圖本身也跟我作對：俄羅斯、斐濟和南極洲的多邊形跨越換日線，而地圖函式庫不會自動環繞，結果整個世界被畫上莫名其妙的條紋。我只好把多邊形的環切開。") + "\n" +
         P("Custom cities were another puzzle. Their timezone is inferred from the nearest known city, longitude first, since timezones are basically longitude bands, with a distance cutoff so a far-away neighbor's political quirks (looking at you, Adelaide) don't come along.",
           "自訂城市又是另一個謎題。它的時區從最近的已知城市推斷，先看經度，因為時區基本上就是經度帶，再加上距離門檻，免得遠方鄰居的政治怪癖（說的就是你，阿德雷德）被一起繼承。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "FastAPI", "pytz", "Leaflet", "Intl API", "pytest", "Render"]) + "\n" +
         P("Civilizism taught me how to build my own framework. WhenWhere taught me when <em>not</em> to, because that has another name: reinventing the wheel. Thank god pytz exists, and there are already datasets online. The timezone math also runs in the browser, mirroring a tested backend, so most interactions need no round trip.",
           "Civilizism 教我怎麼打造自己的框架，WhenWhere 則教我什麼時候<em>不該</em>這麼做，因為那有另一個名字：重新發明輪子。感謝老天有 pytz，線上也早就有現成的資料集。時區計算還會在瀏覽器裡執行，對應一個經過測試的後端，所以多數操作不需要往返伺服器。")),
    ],
    btn("https://whenwhere-65it.onrender.com/", "Try it", "試用") + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/WhenWhere", "Code", "原始碼", True),
    note=P("Free hosting again, so it may take a moment to wake up.", "又是免費主機，所以可能需要一點時間醒來。", "note"),
    demo=True,
))

dialogs.append(dialog(
    "statuscard", "🔔 Claude Code Status Card",
    hook("What if you could tell which Claude Code session needs you without alt-tabbing through all of them?", "如果你不用切視窗，就知道哪個 Claude Code session 在等你呢？"),
    ("statuscard.png", "Claude Code Status Card"),
    [
        ("The problem", "問題",
         P("With several Claude Code sessions open, I kept losing track of which one had finished and which was quietly stuck waiting on me.",
           "同時開著好幾個 Claude Code session 時，我老是搞不清楚哪個已經跑完，哪個正默默卡在那邊等我。")),
        ("My solution", "我的解法",
         P("One always-on-top card per session. Blue is working, red means &quot;come here&quot;, green is done. Click a card to jump to that repo's VS Code window, and a sound plays when something changes. Each repo gets its own animal and each session its own color, which is unnecessary and I stand by it. It's fed by global Claude Code hooks, so it doesn't care which editor you use.",
           "每個 session 一張置頂小卡。藍色是工作中，紅色代表「快過來」，綠色是完成。點一下卡片就跳到那個 repo 的 VS Code 視窗，狀態改變時還會有音效。每個 repo 有自己的動物、每個 session 有自己的顏色，這完全沒必要，而我堅持。它由全域的 Claude Code hooks 驅動，所以不在乎你用哪個編輯器。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("Favorite bug: log rotation briefly left an empty file, the widget read that as &quot;start over&quot;, and dead sessions came back to life. I was, technically, the necromancer. The fix was an atomic rename.",
           "最愛的 bug：日誌輪替時短暫留下一個空檔案，小工具把它解讀成「重新開始」，於是死掉的 session 全都復活了。嚴格來說，我是那個死靈法師。修法是原子性的改名。") + "\n" +
         P("Another: sessions started from different subfolders counted as different repos, so one real project showed up as nine entries with nine icons. Now it walks up to the project root. And on Windows, Claude Code's hook layer eats backslashes in paths, which took an embarrassing amount of time to figure out.",
           "另一個：從不同子資料夾啟動的 session 會被當成不同的 repo，於是一個真實專案變成九筆紀錄、九個圖示。現在它會往上找到專案根目錄。還有在 Windows 上，Claude Code 的 hook 層會吃掉路徑裡的反斜線，這個問題花了我尷尬的時間才搞懂。") + "\n" +
         P("Known issue: the red &quot;needs approval&quot; state is inferred rather than signalled, and it's been unreliable since Claude Code defaulted to Auto mode. Turns out the best way to fix approval prompts is to have fewer of them.",
           "已知問題：紅色的「需要核准」狀態是推測出來的，不是被通知的，而自從 Claude Code 預設改成 Auto 模式後，它就不太可靠了。看來修好核准提示的最佳方法，就是讓它們變少。", "note")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Electron", "Node.js", "Claude Code hooks", "PowerShell"]) + "\n" +
         P("SaaS cannot be done in one day. I learned how hooks work and how to tell repos apart by reading hooks alone. And grinding out improvements took weeks, as a real user of my own tool. Day one I realized I couldn't recall which session was named what. Day two the icons were inconsistent across sessions. Day three I noticed I was still keeping an eye on my monitor, just not alt-tabbing anymore, so I added sound effects on top of the state changes.",
           "SaaS 不可能一天做完。我學會了 hooks 怎麼運作，也學會只靠讀 hooks 就分辨不同的 repo。而且身為自己工具的真實使用者，打磨改進花了好幾個星期。第一天我發現我記不得哪個 session 叫什麼名字。第二天我發現各個 session 的圖示不一致。第三天我發現自己雖然不再切視窗了，卻還是一直盯著螢幕，所以我在狀態變化之外又加了音效。")),
    ],
    btn("https://github.com/Tim-Chen-Yen-Ting/claude-code-status-card", "Code", "原始碼", True),
))

dialogs.append(dialog(
    "steme", "🧠 STEME &amp; BLOC",
    hook("What if you could turn &quot;sincerity&quot; into a number without calling an LLM every time?", "如果不用每次呼叫 LLM，就能把「真誠」變成數字呢？"),
    ("steme_bloc.png", "STEME and BLOC benchmark results"),
    [
        ("The problem", "問題",
         P("Civilizism constantly has to translate between words and numbers: how sincere is this person, do these two memories express the same belief, are these two beliefs fighting each other? Doing that with an LLM call every time would be slow, expensive and inconsistent.",
           "Civilizism 不斷需要在文字和數字之間轉換：這個人有多真誠？這兩段記憶表達的是同一個信念嗎？這兩個信念彼此衝突嗎？每次都用 LLM 呼叫來做，會又慢、又貴、又不一致。")),
        ("My solution", "我的解法",
         P("<strong>STEME</strong> (Semantic Transformation &amp; Evaluation Mapping Engine) is the translation layer. It combines calibrated embedding similarity, zero-shot entailment classification, and an emotion classifier, and it can anchor abstract concepts like <em>sincerity</em> using definitions plus polar behavioral examples. <strong>BLOC</strong> (Belief &amp; Label-Oriented Clustering) groups memories into beliefs that drift as new experiences arrive, and flags opposing beliefs as internal conflict.",
           "<strong>STEME</strong>（語意轉換與評估對應引擎）是翻譯層。它結合校準過的嵌入相似度、零樣本蘊含分類，以及情緒分類器，還能用定義加上兩極的行為範例，替<em>真誠</em>這類抽象概念定錨。<strong>BLOC</strong>（信念與標籤導向分群）把記憶分成會隨新經驗漂移的信念，並把彼此對立的信念標記為內在衝突。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("Raw cosine similarity is a trap: embedding scores crowd into a narrow band, so I had to recalibrate them to get any separation. And clustering by cosine similarity makes centroids crowd together as meaning drifts, so BLOC uses entailment to decide cluster membership instead.",
           "原始的餘弦相似度是個陷阱：嵌入分數會擠在很窄的區間內，所以我得重新校準才能拉開差距。而且用餘弦相似度分群，會讓質心隨語意漂移而擠在一起，所以 BLOC 改用蘊含關係來決定群的歸屬。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "sentence-transformers", "NLI models", "scikit-learn"]) + "\n" +
         P("I thought STEME (essentially 1-NN) was a universal tool, until the emotion projection pushed everything toward the center, and I realized I needed a different classification method. The chart shows real benchmark output: STEME scores 0.79–0.91 F1 across four embedding models on a synthetic tagging set, and BLOC gets 0.70 ARI on drifting data versus 0.57 for global k-means.",
           "我本來以為 STEME（本質上就是 1-NN）是萬用工具，直到情緒投影把所有東西都推向中心，我才意識到需要另一種分類方法。圖中是真實的基準測試輸出：在一組合成的標註資料上，STEME 於四種嵌入模型的 F1 為 0.79–0.91；在漂移資料上，BLOC 的 ARI 是 0.70，全域 k-means 則是 0.57。")),
    ],
    btn("https://github.com/Tim-Chen-Yen-Ting/STEME", "STEME", "STEME", True) + " " +
    btn("https://github.com/Tim-Chen-Yen-Ting/BLOC", "BLOC", "BLOC", True),
))

dialogs.append(dialog(
    "coldemail", "📬 Cold Email Automator",
    hook("What if the job hunt did its own legwork?", "如果求職的跑腿工作能自己做完呢？"),
    ("coldemail.png", "Cold Email Automator pipeline diagram"),
    [
        ("The problem", "問題",
         P("Cold outreach works, but the middle is miserable: figuring out who to contact, finding a working address, and writing something that isn't obviously a template.",
           "陌生開發信有效，但中間的過程很痛苦：搞清楚該聯絡誰、找到能用的信箱，還要寫出一封看起來不像模板的信。")),
        ("My solution", "我的解法",
         P("A pipeline I use on my own job search. Claude researches targets with web search, an email verifier checks the addresses, a draft is written around one specific hook (a recent launch, a piece of news), and the email goes out through Gmail while a Google Sheets dashboard tracks status, bounces and replies. Yes, I automated the job hunt; someone still has to read the replies.",
           "我自己求職時用的流程。Claude 用網路搜尋研究目標，信箱驗證器檢查地址，信件圍繞一個具體的切入點（最近的產品發布、一則新聞）撰寫，再透過 Gmail 寄出，同時由 Google Sheets 儀表板追蹤狀態、退信與回覆。對，我把求職自動化了；回信還是得有人讀。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("Keeping it from researching the same companies forever (each run is told to skip the 100 most recent), and keeping it cheap: roughly a few cents per sent email depending on the provider. I also made the LLM layer provider-agnostic, so Claude, GPT-4o and Gemini are interchangeable from a config file.",
           "不讓它永遠重複研究同樣的公司（每次執行都會被告知跳過最近的 100 間），還有控制成本：依供應商不同，每封寄出的信大約幾美分。我也把 LLM 層做成與供應商無關，所以 Claude、GPT-4o 和 Gemini 只要改設定檔就能互換。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "Pydantic", "SQLite", "Gmail API", "Google Sheets API", "Claude / GPT-4o / Gemini"]) + "\n" +
         P("I learned OAuth the hard way: Gmail's credentials are not bypassable when you mass-send from scripts, no matter how clever you feel. Also, my wallet is crying from the API cost.",
           "我用最痛的方式學會了 OAuth：當你用腳本大量寄信時，Gmail 的憑證機制是繞不過去的，不管你覺得自己多聰明。另外，我的錢包正在為 API 費用哭泣。")),
    ],
    btn("https://github.com/Tim-Chen-Yen-Ting/Cold-Email-Automator", "Code", "原始碼", True),
    note=P("Feature-complete and tested. I'm deliberately holding off deploying it until the timing of my job search makes sense.",
           "功能完整且經過測試。我刻意先不部署，等到求職的時機合適再說。", "note"),
))

dialogs.append(dialog(
    "messages", "💬 Past Messages Analyzer",
    hook("What if you could watch a friendship's tone drift over time?", "如果你能看見一段友情的語氣如何隨時間漂移呢？"),
    ("messages.png", "Past Messages Analyzer pipeline diagram"),
    [
        ("The problem", "問題",
         P("Years of messages with the same people, and no real sense of how those relationships changed. Weirdly emotional for a stats project.",
           "和同一群人傳了好幾年的訊息，卻完全不知道這些關係是怎麼變的。對統計專題來說，情緒過於豐富。")),
        ("My solution", "我的解法",
         P("A pipeline that ingests Facebook Messenger and Instagram exports into a normalized SQLite database, then layers analysis on top: response latency, sentiment, and rolling drift in vocabulary and tone, with changepoint detection to flag when a relationship's style actually shifts. It reuses BLOC's incremental clustering to track relationship drift in embedding space.",
           "一條把 Facebook Messenger 和 Instagram 匯出資料灌進正規化 SQLite 資料庫的流程，再往上疊加分析：回覆延遲、情緒，以及詞彙與語氣的滾動漂移，並用變點偵測標出一段關係的風格何時真的轉變。它重用了 BLOC 的增量分群，在嵌入空間裡追蹤關係漂移。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("The real design question was privacy. They're my friends' messages, so the AI narration layer only sees summary statistics by default. A close-reading mode exists for statistically flagged anomalies, but it's opt-in and off by default, a deliberate trade of interpretability for privacy.",
           "真正的設計問題是隱私。這些是我朋友的訊息，所以 AI 的敘述層預設只看得到摘要統計。針對統計上被標記的異常有精讀模式，但它需要主動開啟、預設關閉，這是刻意拿可解釋性換隱私。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "SQLite", "pandas", "VADER", "SnowNLP", "PELT changepoints", "Jupyter"]) + "\n" +
         P("Unsurprisingly, you need two sentiment tools when your friends text in two languages. Also, welcome to the world of psychology: my stats skills get challenged by sentiment, at least according to the psych textbooks.",
           "毫不意外，當你的朋友用兩種語言傳訊息，你就需要兩套情緒分析工具。另外，歡迎來到心理學的世界：至少根據心理學教科書，我的統計能力正被情緒挑戰著。")),
    ],
    btn("https://github.com/Tim-Chen-Yen-Ting/Past-Messages-Analysis", "Code", "原始碼", True),
))

dialogs.append(dialog(
    "pkb", "📚 Personal Knowledge Base",
    hook("What if your notes could tell you what you're missing?", "如果你的筆記能告訴你還缺什麼呢？"),
    ("pkb.png", "Personal Knowledge Base chat screen"),
    [
        ("The problem", "問題",
         P("I built this for a non-technical user with a pile of documents and no way to ask questions across them, or to know what they hadn't covered yet.",
           "我替一位非技術背景的使用者做了這個：他有一大堆文件，卻沒辦法跨文件提問，也不知道自己還沒涵蓋什麼。")),
        ("My solution", "我的解法",
         P("Drop in a PDF, Word doc or text file. An LLM turns it into a tagged wiki entry, you can ask questions against the whole knowledge base (or just some topics) with sources cited, and a per-topic &quot;knowledge audit&quot; lists your strengths, gaps and what to read next. Nothing humbles you like a list of what you haven't read. Yes, the front end is ugly. It works.",
           "丟進 PDF、Word 或文字檔，LLM 會把它變成附標籤的 wiki 條目；你可以對整個知識庫（或只對某些主題）提問並附上出處，每個主題的「知識審計」會列出你的強項、缺口和接下來該讀什麼。沒有什麼比一份「你還沒讀的清單」更能讓人謙卑。對，前端很醜。但它能用。")),
        ("Challenges &amp; fun stories", "挑戰與趣事",
         P("Left alone, LLM tagging invents near-duplicates (&quot;ml&quot;, &quot;machine-learning&quot;, &quot;machine learning&quot;) until the tags are useless, so each ingest shows the model the existing tags and tells it to reuse them. I also chose to answer questions by loading the relevant entries into the prompt instead of building a vector search. At this scale it's simpler, cheaper and easier to debug, and the sources are exactly what the model saw.",
           "放著不管的話，LLM 標註會發明一堆近似重複的標籤（「ml」、「machine-learning」、「machine learning」），直到標籤毫無用處，所以每次匯入都會讓模型看到現有標籤，並要求它重複使用。我也選擇把相關條目直接放進 prompt 來回答問題，而不是做向量搜尋。在這個規模下，這樣更簡單、更便宜、更好除錯，而且出處正好就是模型看到的內容。")),
        ("Tech stack &amp; what I learned", "技術堆疊與我學到的",
         chips(["Python", "Vercel serverless", "Supabase", "Gemini API", "pdfplumber", "Chart.js"]) + "\n" +
         P("I know RAG, and this is when I learned when <em>not</em> to use RAG. Also, great minds think alike :) When I finished building the knowledge base, I realized I had built my own Gemini Notebook. Well done, past me.",
           "我懂 RAG，而這是我學到什麼時候<em>不該</em>用 RAG 的時刻。還有，英雄所見略同 :) 當我做完這個知識庫，我才發現自己造出了我的 Gemini Notebook。幹得好，過去的我。")),
    ],
    btn("https://github.com/Tim-Chen-Yen-Ting/Personal-Knowledge-DB-Manager", "Code", "原始碼", True),
))

tail = """
  <!-- ===================== PROJECT DIALOGS ===================== -->

""" + "\n\n".join(dialogs) + """

  <script src="script.js"></script>
</body>
</html>
"""

html = head + about + projects + personal + contact + tail
Path(__file__).resolve().parent.parent.joinpath("index.html").write_text(html, encoding="utf-8")
print("wrote index.html", len(html), "chars")
