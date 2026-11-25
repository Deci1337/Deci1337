"""Generates every static SVG in assets/ (dark + light). Run: python scripts/build_assets.py"""
import math

from svgtext import sans, mono, text, wrap, svg, write_pair

W = 840
MW = 420


def card(x, y, w, h, t, r=14):
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{r}" '
            f'fill="{t["surface"]}" stroke="{t["line"]}"/>')


def check(cond, msg):
    if not cond:
        raise SystemExit(f"layout overflow: {msg}")


# ---------- header ----------
AGENTS = ["spec", "code", "review", "test", "ship"]


def agent_graph(t, cx, cy, R, labels=True):
    b = []
    nodes = []
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        nodes.append((cx + R * math.cos(a), cy + R * math.sin(a), math.cos(a), math.sin(a)))

    # dashed orbit, very slow rotation
    b.append(f'<g><circle cx="{cx}" cy="{cy}" r="{R * 1.34:.1f}" fill="none" stroke="{t["line"]}" '
             f'stroke-dasharray="2 7"/><animateTransform attributeName="transform" type="rotate" '
             f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="60s" repeatCount="indefinite"/></g>')
    # pentagon + spokes
    ring = " ".join(f"{x:.1f},{y:.1f}" for x, y, *_ in nodes)
    b.append(f'<polygon points="{ring}" fill="none" stroke="{t["line"]}" stroke-dasharray="3 5"/>')
    for x, y, *_ in nodes:
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["line"]}" stroke-width="1.2"/>')

    cycle = "8s"
    for i, (x, y, ca, sa) in enumerate(nodes):
        t0 = round(i * 0.18 + 0.02, 3)
        t1 = round(t0 + 0.12, 3)
        # edge highlight while the signal travels
        b.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["accent"]}" '
                 f'stroke-width="1.2" opacity="0"><animate attributeName="opacity" values="0;0;.55;.55;0;0" '
                 f'keyTimes="0;{t0};{t0 + .02:.3f};{t1};{t1 + .06:.3f};1" dur="{cycle}" repeatCount="indefinite"/></line>')
        # travelling signal
        b.append(f'<circle r="3" fill="{t["accent"]}" opacity="0">'
                 f'<animateMotion path="M{cx},{cy} L{x:.1f},{y:.1f}" keyPoints="0;0;1;1" '
                 f'keyTimes="0;{t0};{t1};1" calcMode="linear" dur="{cycle}" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{t0};{t0 + .005:.3f};{t1};{t1 + .005:.3f};1" dur="{cycle}" repeatCount="indefinite"/>'
                 f'</circle>')
        # node, flashes when the signal arrives
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{t["surface"]}" stroke="{t["bordeaux"]}" '
                 f'stroke-width="1.6"><animate attributeName="stroke" '
                 f'values="{t["bordeaux"]};{t["bordeaux"]};{t["accent"]};{t["accent"]};{t["bordeaux"]};{t["bordeaux"]}" '
                 f'keyTimes="0;{t1};{t1 + .01:.3f};{t1 + .05:.3f};{t1 + .12:.3f};1" dur="{cycle}" '
                 f'repeatCount="indefinite"/></circle>')
        lx, ly = cx + (R + 20) * ca, cy + (R + 20) * sa + 4
        anchor = "middle" if abs(ca) < 0.3 else ("start" if ca > 0 else "end")
        if labels:
            b.append(text(mono(500), AGENTS[i], lx, ly, 11, t["muted"], ls=0.5, anchor=anchor))

    # orchestrator
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R * .16:.1f}" fill="{t["surface"]}" stroke="{t["accent"]}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{max(3, R * .045):.1f}" fill="{t["accent"]}"/>')
    return "".join(b)


def header(t):
    H = 280
    b = [card(0, 0, W, H, t, 20)]
    b.append(f'<line x1="48" y1="66" x2="70" y2="66" stroke="{t["accent"]}" stroke-width="1.5"/>')
    b.append(text(mono(500), "Deci1337", 82, 70, 13, t["accent"], ls=0.4))
    b.append(text(sans(600), "Arseniy", 46, 146, 68, t["text"], ls=-1.5))
    lead = "Fullstack developer · AI agents · agent orchestration"
    check(sans(400).width(lead, 18) < 520, "header lead")
    b.append(text(sans(400), lead, 48, 186, 18, t["text"]))
    b.append(text(mono(500), "Moscow · NUST MISIS · Information Systems", 48, 230, 12, t["muted"], ls=0.2))
    b.append(agent_graph(t, 680, 140, 88))
    return svg(W, H, "".join(b), "Arseniy (Deci1337): fullstack developer, AI agents, agent orchestration")


def header_m(t):
    w, H = MW, 280
    b = [card(0, 0, w, H, t, 20),
         f'<line x1="28" y1="52" x2="46" y2="52" stroke="{t["accent"]}" stroke-width="1.5"/>',
         text(mono(500), "Deci1337", 56, 56, 13, t["accent"], ls=0.4),
         text(sans(600), "Arseniy", 26, 124, 58, t["text"], ls=-1.2),
         text(sans(400), "Fullstack developer", 28, 166, 19, t["text"]),
         text(sans(400), "AI agents · agent orchestration", 28, 192, 19, t["text"]),
         text(mono(500), "Moscow · NUST MISIS", 28, 232, 13, t["muted"], ls=0.2),
         text(mono(500), "Information Systems", 28, 254, 13, t["muted"], ls=0.2),
         agent_graph(t, 336, 92, 44, labels=False)]
    return svg(w, H, "".join(b), "Arseniy (Deci1337): fullstack developer, AI agents, agent orchestration")


# ---------- contact pills ----------
ICONS = {
    "telegram": "M3 11.5 20.5 4.5 17 19.5 11.5 14.5 3 11.5Z M11.5 14.5 20.5 4.5 M11.5 14.5V19l2.6-2.4",
    "channel": "M12 12.01V12 M8.5 8.5a5 5 0 0 0 0 7 M15.5 8.5a5 5 0 0 1 0 7 M5.6 5.6a9 9 0 0 0 0 12.8 M18.4 5.6a9 9 0 0 1 0 12.8",
    "email": "M3.5 6h17v12h-17z M3.5 6.5 12 13l8.5-6.5",
}


def pill(icon, label):
    def build(t):
        lw = sans(500).width(label, 15)
        w, h = int(18 + 20 + 10 + lw + 20), 44
        b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22" fill="{t["surface"]}" stroke="{t["line"]}"/>',
             f'<path d="{ICONS[icon]}" transform="translate(16 10)" fill="none" stroke="{t["accent"]}" '
             f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
             text(sans(500), label, 48, 27.5, 15, t["text"])]
        return svg(w, h, "".join(b), label)
    return build


# ---------- section divider ----------
def divider(num, title, W=W):
    def build(t):
        H = 56
        tw = sans(600).width(title, 22)
        x1 = 40 + tw + 20
        b = [text(mono(500), num, 2, 36, 13, t["accent"], ls=1),
             text(sans(600), title, 40, 37, 22, t["text"]),
             f'<line x1="{x1:.1f}" y1="30" x2="{W - 2}" y2="30" stroke="{t["line"]}"/>',
             f'<line x1="{x1:.1f}" y1="30" x2="{x1 + 24:.1f}" y2="30" stroke="{t["accent"]}" stroke-width="1.5"/>']
        return svg(W, H, "".join(b), f"{num} {title}")
    return build


# ---------- commercial work ----------
WORK = [
    ("Procurement", "Tender monitoring agent",
     "Pulls tenders from procurement platforms, reads the attached documents and scores each one for relevance."),
    ("Sales", "Telegram sales agent",
     "Handles customer chats for a retail shop end to end. It replaced the shop's sales managers."),
    ("Internal", "Knowledge-base agents",
     "Turn team chats into a daily-updated knowledge base and answer new employees' questions over it with RAG."),
    ("Manufacturing", "Multi-agent platform",
     "Seven agents for a production business on one shared knowledge layer, with OCR and CI checks."),
]


def tile(x, y, w, h, t, tag, title, body, maxl=3):
    b = [card(x, y, w, h, t),
         text(mono(500), tag, x + 28, y + 38, 12, t["accent"], ls=0.3),
         text(sans(600), title, x + 28, y + 70, 20, t["text"])]
    lines = wrap(sans(400), body, 14.5, w - 56)
    check(len(lines) <= maxl, f"tile body '{title}'")
    for k, line in enumerate(lines):
        b.append(text(sans(400), line, x + 28, y + 100 + k * 21, 14.5, t["muted"]))
    return "".join(b)


def work(t):
    tw, th, g = 410, 160, 20
    b = [tile((i % 2) * (tw + g), (i // 2) * (th + g), tw, th, t, *wk) for i, wk in enumerate(WORK)]
    return svg(W, 2 * th + g, "".join(b), "Commercial work: " + "; ".join(f"{w[1]}: {w[2]}" for w in WORK))


# ---------- hackathons ----------
TOP = [
    ("Nuclear IT Hack · MEPhI", "4th place", "Offline P2P messenger", "PM, frontend · 03.2026"),
    ("TenderHack Moscow", "Top 5", "Personalized procurement search", "Fullstack, ML · 04.2026"),
]
ROWS = [
    ("10.2026", "TenderHack Kazan", "Spec auto-fill from the KTRU catalog", "Architecture, backend"),
    ("05.2026", "TenderHack SPb", "Price aggregator for procurement", "PM, frontend"),
    ("05.2026", "AI Business SPb", "RAG service-desk bot", "PM, backend"),
    ("12.2025", "HSE Vibeathon", "AI personal finance app", "PM, mobile"),
    ("11.2025", "MAI × PSB", "Business email generator", "Frontend"),
    ("10.2025", "2GIS Hackathon", "Help map for volunteers", "Fullstack"),
]


def hackathons(t):
    tw, th, g, rh = 410, 150, 20, 44
    b = []
    for i, (tag, big, proj, role) in enumerate(TOP):
        x = i * (tw + g)
        b += [card(x, 0, tw, th, t),
              text(mono(500), tag, x + 28, 38, 12, t["accent"], ls=0.3),
              text(sans(600), big, x + 27, 84, 36, t["text"], ls=-0.8),
              text(sans(400), proj, x + 28, 112, 16, t["text"]),
              text(mono(500), role, x + 28, 134, 12, t["muted"], ls=0.2)]
    y0 = th + g
    lh = len(ROWS) * rh + 12
    b.append(card(0, y0, W, lh, t))
    for k, (date, ev, proj, role) in enumerate(ROWS):
        y = y0 + 6 + k * rh
        base = y + rh / 2 + 5
        if k:
            b.append(f'<line x1="28" y1="{y}" x2="{W - 28}" y2="{y}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        rw = mono(500).width(role, 12, 0.2)
        check(380 + sans(400).width(proj, 14) < W - 28 - rw - 20, f"row {ev}")
        b += [text(mono(500), date, 28, base, 12, t["muted"]),
              text(sans(500), ev, 128, base, 15, t["text"]),
              text(sans(400), proj, 380, base, 14, t["muted"]),
              text(mono(500), role, W - 28, base, 12, t["accent"], ls=0.2, anchor="end")]
    label = "Hackathons: Nuclear IT Hack (MEPhI) 4th place; TenderHack Moscow top 5; " + \
        "; ".join(f"{r[1]} ({r[0]}): {r[2]}, {r[3]}" for r in ROWS)
    return svg(W, y0 + lh, "".join(b), label)


# ---------- project cards ----------
PROJECTS = {
    "tenderhack-moscow": ("TenderHack Moscow · top 5", "Smart procurement search",
                          "Personalized product search for a public procurement portal: semantic retrieval, "
                          "learning-to-rank, and an explanation for every position.",
                          ["FastAPI", "React", "PostgreSQL", "CatBoost"]),
    "mephi-hack": ("Nuclear IT Hack · 4th place", "Offline P2P messenger",
                   "Messages, files and voice calls with no internet and no servers. Peer discovery, "
                   "multi-hop routing, AES-256-GCM.",
                   ["C#", ".NET 9", "MAUI", "UDP"]),
    "tenderhack-spb": ("TenderHack SPb", "Price aggregator",
                       "Searches marketplaces and the open web in parallel to set a contract's starting price. "
                       "A local LLM normalizes the queries.",
                       ["FastAPI", "React", "Playwright", "Qwen3"]),
    "service-desk": ("AI Business SPb", "RAG service-desk bot",
                     "Answers support requests from past tickets and knowledge-base articles. Telegram bots "
                     "for users and admins, plus a dashboard.",
                     ["YandexGPT", "ChromaDB", "FastAPI", "Docker"]),
    "finance-assistant": ("HSE Vibeathon", "AI finance assistant",
                          "Cross-platform app for personal spending: expense tracking, a spending forecast "
                          "and voice input for transactions.",
                          ["MAUI", "FastAPI", "GigaChat", "SQLite"]),
    "tg-lead-parser": ("Tool", "Telegram lead finder",
                       "Reads target chats, filters by keywords, drops ads and noise with an LLM and exports "
                       "leads to Excel for follow-up.",
                       ["Python", "OpenAI API", "Excel"]),
}


def project(tag, title, body, chips):
    def build(t):
        w, h = 410, 230
        b = [card(0, 0, w, h, t), text(mono(500), tag, 28, 40, 12, t["accent"], ls=0.3),
             f'<path d="M0 10 10 0M3 0h7v7" transform="translate(372 30)" fill="none" stroke="{t["muted"]}" '
             f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
             text(sans(600), title, 28, 78, 22, t["text"])]
        lines = wrap(sans(400), body, 14.5, w - 56)
        check(len(lines) <= 3, f"card {title}")
        for k, line in enumerate(lines):
            b.append(text(sans(400), line, 28, 108 + k * 21, 14.5, t["muted"]))
        x = 28
        for c in chips:
            cw = mono(500).width(c, 11) + 18
            b += [f'<rect x="{x + .5:.1f}" y="176.5" width="{cw - 1:.1f}" height="25" rx="6" fill="none" '
                  f'stroke="{t["line"]}"/>', text(mono(500), c, x + 9, 193, 11, t["text"])]
            x += cw + 8
        check(x < w - 20, f"chips {title}")
        return svg(w, h, "".join(b), f"{title}: {body}")
    return build


# ---------- stack ----------
STACK = [
    ("AI and agents", [("Oa", "OpenAI API"), ("Cl", "Claude"), ("Ya", "YandexGPT"), ("Gc", "GigaChat"),
                     ("Rg", "RAG"), ("Ch", "ChromaDB"), ("Mc", "MCP"), ("Sk", "Spec Kit"), ("Sa", "Subagents")]),
    ("Backend", [("Py", "Python"), ("Fa", "FastAPI"), ("Ce", "Celery"), ("Pg", "PostgreSQL"), ("Rd", "Redis"),
                 ("Sq", "SQLAlchemy"), ("Al", "Alembic"), ("Ag", "aiogram")]),
    ("Frontend", [("Ts", "TypeScript"), ("Re", "React"), ("Nx", "Next.js"), ("Vi", "Vite"), ("Tw", "Tailwind")]),
    ("Mobile", [("C#", "C#"), ("Ma", ".NET MAUI")]),
    ("Infra", [("Dk", "Docker"), ("Ng", "nginx"), ("Cd", "Caddy"), ("Ga", "GitHub Actions"), ("Lx", "Linux")]),
]


def stack(t, W=W):
    narrow = W < 600
    x0, x_end, th, gap = (28 if narrow else 176), W - 28, 34, 8
    groups, y = [], 24
    for label, items in STACK:
        lift = 34 if narrow else 0
        rows, x, ry = [], x0, lift
        for mono_s, name in items:
            tw = 36 + sans(500).width(name, 14) + 14
            if x + tw > x_end:
                x, ry = x0, ry + th + gap
            rows.append((x, y + ry, tw, mono_s, name))
            x += tw + gap
        groups.append((label, y, rows))
        y += ry + th + 28
    H = y - 4
    b = [card(0, 0, W, H, t, 16)]
    for gi, (label, gy, rows) in enumerate(groups):
        if gi:
            b.append(f'<line x1="28" y1="{gy - 14}" x2="{W - 28}" y2="{gy - 14}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        b.append(text(mono(500), label, 28, gy + 22, 12, t["accent"], ls=0.3))
        for x, ty, tw, ms, name in rows:
            b += [f'<rect x="{x + .5:.1f}" y="{ty + .5}" width="{tw - 1:.1f}" height="{th - 1}" rx="9" fill="none" stroke="{t["line"]}"/>',
                  f'<rect x="{x + 6.5:.1f}" y="{ty + 6.5}" width="21" height="21" rx="5" fill="{t["wine"]}" '
                  f'fill-opacity=".22" stroke="{t["bordeaux"]}"/>',
                  text(mono(600), ms, x + 17, ty + 21, 10, t["text"], anchor="middle"),
                  text(sans(500), name, x + 36, ty + 22, 14, t["text"])]
    label = "Stack. " + ". ".join(f"{g[0]}: {', '.join(n for _, n in g[1])}" for g in STACK)
    return svg(W, H, "".join(b), label)


# ---------- footer ----------
def footer(t, W=W):
    H = 110
    b = [f'<line x1="0" y1="1" x2="{W}" y2="1" stroke="{t["line"]}"/>',
         text(mono(500), "Open to remote fullstack and AI-engineering roles", W / 2, 54, 13, t["accent"],
              ls=0.3, anchor="middle"),
         text(sans(400), "Telegram  @Deci1337", W / 2, 84, 15, t["muted"], anchor="middle")]
    return svg(W, H, "".join(b), "Open to remote fullstack and AI-engineering roles. Telegram @Deci1337")


# ---------- mobile variants (420 wide, shown under 600px) ----------
def work_m(t):
    th, g = 170, 16
    b = []
    for i, (tag, title, body) in enumerate(WORK):
        y = i * (th + g)
        b += [card(0, y, MW, th, t), text(mono(500), tag, 24, y + 38, 13, t["accent"], ls=0.3),
              text(sans(600), title, 24, y + 70, 21, t["text"])]
        lines = wrap(sans(400), body, 15.5, MW - 48)
        check(len(lines) <= 3, f"work_m {title}")
        for k, line in enumerate(lines):
            b.append(text(sans(400), line, 24, y + 100 + k * 22, 15.5, t["muted"]))
    return svg(MW, 4 * th + 3 * g, "".join(b), "Commercial work: " + "; ".join(f"{w[1]}: {w[2]}" for w in WORK))


def hackathons_m(t):
    th, g, rh = 150, 16, 86
    b = []
    for i, (tag, big, proj, role) in enumerate(TOP):
        y = i * (th + g)
        b += [card(0, y, MW, th, t), text(mono(500), tag, 24, y + 38, 13, t["accent"], ls=0.3),
              text(sans(600), big, 23, y + 84, 36, t["text"], ls=-0.8),
              text(sans(400), proj, 24, y + 112, 17, t["text"]),
              text(mono(500), role, 24, y + 134, 13, t["muted"], ls=0.2)]
    y0 = 2 * (th + g)
    lh = len(ROWS) * rh + 8
    b.append(card(0, y0, MW, lh, t))
    for k, (date, ev, proj, role) in enumerate(ROWS):
        y = y0 + 4 + k * rh
        if k:
            b.append(f'<line x1="24" y1="{y}" x2="{MW - 24}" y2="{y}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        b += [text(sans(500), ev, 24, y + 30, 17, t["text"]),
              text(mono(500), date, MW - 24, y + 30, 13, t["muted"], anchor="end"),
              text(sans(400), proj, 24, y + 54, 15, t["muted"]),
              text(mono(500), role, 24, y + 74, 13, t["accent"], ls=0.2)]
    label = "Hackathons: Nuclear IT Hack (MEPhI) 4th place; TenderHack Moscow top 5; " +         "; ".join(f"{r[1]} ({r[0]}): {r[2]}, {r[3]}" for r in ROWS)
    return svg(MW, y0 + lh, "".join(b), label)


def project_m(tag, title, body, chips):
    """Same 410x230 frame as the desktop card (img width is fixed at 49%), but only tag + title, set large."""
    def build(t):
        w, h = 410, 230
        b = [card(0, 0, w, h, t, 18), text(mono(500), tag.split(" · ")[0], 28, 62, 24, t["accent"]),
             f'<path d="M0 22 22 0M6 0h16v16" transform="translate(352 34)" fill="none" stroke="{t["muted"]}" '
             f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>']
        lines = wrap(sans(600), title, 40, w - 56)
        check(len(lines) <= 2, f"card_m {title}")
        for k, line in enumerate(lines):
            b.append(text(sans(600), line, 27, 140 + k * 48, 40, t["text"], ls=-0.6))
        return svg(w, h, "".join(b), f"{title}: {body}")
    return build


def footer_m(t):
    H = 120
    b = [f'<line x1="0" y1="1" x2="{MW}" y2="1" stroke="{t["line"]}"/>',
         text(mono(500), "Open to remote fullstack", MW / 2, 46, 14, t["accent"], anchor="middle"),
         text(mono(500), "and AI-engineering roles", MW / 2, 70, 14, t["accent"], anchor="middle"),
         text(sans(400), "Telegram  @Deci1337", MW / 2, 100, 16, t["muted"], anchor="middle")]
    return svg(MW, H, "".join(b), "Open to remote fullstack and AI-engineering roles. Telegram @Deci1337")


if __name__ == "__main__":
    write_pair("header", header)
    write_pair("contact-telegram", pill("telegram", "Telegram"))
    write_pair("contact-channel", pill("channel", "Channel"))
    write_pair("contact-email", pill("email", "Email"))
    for num, slug, title in [("01", "work", "Commercial work"), ("02", "hackathons", "Hackathons"),
                             ("03", "projects", "Selected projects"), ("04", "stack", "Stack"),
                             ("05", "activity", "Activity")]:
        write_pair(f"divider-{slug}", divider(num, title))
        write_pair(f"divider-{slug}-m", divider(num, title, MW))
    write_pair("work", work)
    write_pair("hackathons", hackathons)
    for slug, data in PROJECTS.items():
        write_pair(f"card-{slug}", project(*data))
        write_pair(f"card-{slug}-m", project_m(*data))
    write_pair("stack", stack)
    write_pair("footer", footer)
    write_pair("header-m", header_m)
    write_pair("work-m", work_m)
    write_pair("hackathons-m", hackathons_m)
    write_pair("stack-m", lambda t: stack(t, MW))
    write_pair("footer-m", footer_m)
    print("ok")
