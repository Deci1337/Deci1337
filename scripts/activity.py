"""Contribution heatmap + streak panel. Run daily by .github/workflows/activity.yml.
Needs GITHUB_TOKEN (or GH_TOKEN) in env; locally: GITHUB_TOKEN=$(gh auth token) python scripts/activity.py"""
import datetime as dt
import json
import os
import urllib.request

from svgtext import sans, mono, text, svg, write_pair

USER = os.environ.get("PROFILE_USER", "Deci1337")
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
W, H = 840, 290
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fetch():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], [d for w in cal["weeks"] for d in w["contributionDays"]]


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current, i = 0, len(counts) - 1
    if counts and counts[-1] == 0:  # today not committed yet: streak still alive
        i -= 1
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return current, longest


def level(c, peak):
    if c == 0:
        return 0
    return min(4, 1 + int(3 * (c - 1) / max(peak - 1, 1)))


def build(total, all_days, W=W):
    narrow = W < 600
    current, longest = streaks(all_days)
    peak = sorted(d["contributionCount"] for d in all_days)[int(len(all_days) * 0.97)] or 1
    days = all_days
    if narrow:  # last 26 full weeks, starting on a Sunday
        days = all_days[-(26 * 7 - 6):]
        while dt.date.fromisoformat(days[0]["date"]).weekday() != 6:
            days = days[1:]
    first = dt.date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    cell, gap = 11, 3
    weeks = (len(days) + offset + 6) // 7
    gx = (W - (weeks * (cell + gap) - gap)) / 2
    gy = 142
    if narrow:
        stats = [(f"{total:,}".replace(",", " "), "Contributions"), (f"{current}", "Current streak"),
                 (f"{longest}", "Longest streak")]
        note = f"Last 26 weeks · {dt.date.today().isoformat()}"
    else:
        stats = [(f"{total:,}".replace(",", " "), "Contributions, last 12 months"),
                 (f"{current}", "Current streak, days"), (f"{longest}", "Longest streak, days")]
        note = f"Updated {dt.date.today().isoformat()}"
    col_w = (W - 56) / 3 + (0 if narrow else 24)
    num_size = 30 if narrow else 36

    def render(t):
        b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>']
        for i, (num, lab) in enumerate(stats):
            x = 28 + i * col_w
            if i:
                b.append(f'<line x1="{x - 14 if narrow else x - 24:.1f}" y1="30" x2="{x - 14 if narrow else x - 24:.1f}" '
                         f'y2="96" stroke="{t["line"]}"/>')
            b.append(text(sans(600), num, x - 1, 70, num_size, t["text"] if i else t["accent"], ls=-0.8))
            b.append(text(mono(500), lab, x, 94, 11 if narrow else 12, t["muted"], ls=0.2))
        last_col = -9
        for k, d in enumerate(days):
            col, row = divmod(k + offset, 7)
            x, y = gx + col * (cell + gap), gy + row * (cell + gap)
            date = dt.date.fromisoformat(d["date"])
            if date.day == 1 and col - last_col >= 3 and col < weeks - 2:
                b.append(text(mono(500), MONTHS[date.month - 1], gx + col * (cell + gap), gy - 10, 10, t["faint"]))
                last_col = col
            lv = level(d["contributionCount"], peak)
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{t["heat"][lv]}"/>')
        ly = gy + 7 * (cell + gap) + 22
        b.append(text(mono(500), "Less", W - gx - 5 * (cell + 4) - 4, ly + 9, 10, t["faint"], anchor="end"))
        for i in range(5):
            b.append(f'<rect x="{W - gx - (5 - i) * (cell + 4) + 4:.1f}" y="{ly}" width="{cell}" height="{cell}" '
                     f'rx="2.5" fill="{t["heat"][i]}"/>')
        b.append(text(mono(500), note, gx, ly + 9, 10, t["faint"]))
        return svg(W, H, "".join(b), f"{total} contributions in the last year. Current streak {current} days, "
                                     f"longest {longest} days.")
    return render


if __name__ == "__main__":
    total, days = fetch()
    write_pair("activity", build(total, days))
    write_pair("activity-m", build(total, days, 420))
    print(total, streaks(days))
