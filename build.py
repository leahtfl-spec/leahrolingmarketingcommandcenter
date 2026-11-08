"""Build the Rep With Me Marketing Command Center.

    python3 build.py

Outputs:
  exports/command_center.html  -> uploaded to Google Drive as a Google Doc
  exports/daily_tracker.csv    -> uploaded to Google Drive as a Google Sheet
  src/data/plan.json           -> data for the Vite web app (deployed on Vercel)
"""
import csv
import json
import html
import pathlib
import sys

from command_center import brand, calendar_plan, formats, intel

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "exports"
WEB_DATA = ROOT / "src" / "data" / "plan.json"
NAVY, CREAM, GOLD = "#1B2A41", "#F7F1E6", "#B08D57"


def esc(s):
    return html.escape(s or "", quote=False).replace("\n", "<br>")


def table(headers, rows, widths=None):
    th = "".join(
        f'<td bgcolor="{CREAM}"><b>{esc(h)}</b></td>' for h in headers
    )
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f'<td>{c}</td>' for c in r) + "</tr>"
    return f'<table border="1" cellpadding="5"><tr>{th}</tr>{body}</table>'


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def fmt_date(d):
    return d.strftime("%a %b ") + str(d.day)


def validate():
    """Brand rule: no em dashes in anything that gets posted."""
    problems = []
    for date, _, _, d in calendar_plan.schedule():
        for field in ("caption", "hook_text", "hook_spoken", "title", "rep"):
            if "—" in d[field]:
                problems.append(f"{date} {field}")
        for b in d["beats"]:
            if "—" in b:
                problems.append(f"{date} beats")
    if len(calendar_plan.DAYS) != 28:
        problems.append(f"expected 28 days, got {len(calendar_plan.DAYS)}")
    for date, wd, _, _ in calendar_plan.schedule():
        if wd not in formats.SERIES:
            problems.append(f"no series for {wd}")
    if problems:
        sys.exit("Validation failed:\n  " + "\n  ".join(problems))


def build_doc():
    c = brand.CAMPAIGN
    p = []
    p.append(f"<h1>REP WITH ME | Marketing Command Center</h1>")
    p.append(f"<p><i>The Practice by InnerBoard | The Practice Club | {brand.FOUNDER}</i></p>")
    p.append(f"<p><b>{esc(c['tagline'])}</b></p>")
    p.append(f"<p>{esc(c['promise'])}</p>")

    # --- How to use
    p.append("<h2>1. Start here: how to use this every day</h2>")
    p.append(ul([
        "<b>Open the 28-Day Calendar (section 6) and find today's date.</b> It tells you the series, the rep, the hook, the script, how to film it, and the caption.",
        "<b>The app's rep always wins.</b> Each day lists a backup rep written in the app's voice. If the app drops a different rep at 7 AM, use the app's rep with the same format and shot list.",
        "<b>Follow the Daily Routine (section 2).</b> Morning story, film for 15 minutes, post, 30-minute engagement block, evening Close the Day.",
        "<b>Tick it off in the Google Sheet tracker</b> (Rep With Me Daily Tracker) and log the day's numbers. Every Friday, update the rep counter.",
        f"<b>North star:</b> {esc(c['north_star'])}",
    ]))

    p.append("<h2>2. The daily routine</h2>")
    p.append(table(["When", "What", "How"],
                   [(esc(t), f"<b>{esc(w)}</b>", esc(h)) for t, w, h in formats.DAILY_ROUTINE]))

    # --- Campaign
    p.append("<h2>3. The big idea: Rep With Me</h2>")
    p.append("<p>Every day the Practice app gives everyone a new rep. Instead of just promoting the app, Leah does the rep <b>with</b> people, on camera, every single day, and invites them in. The content is the product working. The comments are the community forming. Nobody does their one life alone.</p>")
    p.append(ul([
        f"<b>Campaign:</b> {esc(c['name'])}",
        f"<b>Tagline:</b> {esc(c['tagline'])}",
        f"<b>Community name:</b> {esc(c['community_name'])}",
        f"<b>The ritual:</b> read the rep, react, do it, invite. Everyone joins by commenting <b>{esc(c['keyword'])}</b>.",
        f"<b>Closing line, every post:</b> Life takes reps. See you tomorrow.",
        f"<b>Hashtags:</b> {esc(' '.join(c['hashtags']))}",
        "<b>What 'make life sexy' means here:</b> alive, confident, present, a little cheeky. Golden hour, the good perfume on a Tuesday, the pause that lets someone tell the truth. Life is the sexy part.",
    ]))
    p.append("<h3>Fun rules</h3>")
    p.append(ul([esc(r) for r in formats.FUN_RULES]))
    p.append("<h3>The growth engine: how we get to thousands of people doing reps</h3>")
    p.append(table(["Lever", "How"], [(f"<b>{esc(a)}</b>", esc(b)) for a, b in formats.GROWTH_ENGINE]))

    # --- Brand recall
    p.append("<h2>4. Brand recall: what InnerBoard and The Practice stand for</h2>")
    p.append("<p><b>The Practice is what people use. The Practice Club is what people belong to. InnerBoard is the methodology behind it.</b></p>")
    p.append(table(["Brand", "Role", "What it is"], [(f"<b>{esc(a)}</b>", esc(b), esc(cc)) for a, b, cc in brand.ARCHITECTURE]))
    p.append("<h3>Core lines</h3>")
    p.append(ul([esc(x) for x in brand.CORE_LINES]))
    p.append("<h3>The app's daily rhythm (build content around it)</h3>")
    p.append(table(["When", "Moment", "What the app says"], [(esc(a), f"<b>{esc(b)}</b>", esc(cc)) for a, b, cc in brand.APP_RHYTHM]))
    p.append("<h3>Real reps the app has sent</h3>")
    p.append(table(["Date", "Rep"], [(esc(a), esc(b)) for a, b in brand.REAL_REPS]))
    p.append("<h3>Audience lanes</h3>")
    p.append(table(["Who", "What they're thinking"], [(f"<b>{esc(a)}</b>", f"<i>{esc(b)}</i>") for a, b in brand.AUDIENCE_LANES]))
    p.append("<h3>Look and feel</h3>")
    p.append(ul([f"<b>{esc(k.title())}:</b> {esc(v)}" for k, v in brand.VISUAL.items()]))
    p.append("<h3>Guardrails</h3>")
    p.append(ul([esc(g) for g in brand.GUARDRAILS]))

    # --- Weekly series
    p.append("<h2>5. The weekly series</h2>")
    p.append(table(["Day", "Series", "Format", "Post time", "Setup", "Why"],
                   [(k, f"<b>{esc(s['name'])}</b>", esc(s['fmt']), esc(s['time']), esc(s['setup']), esc(s['why']))
                    for k, s in formats.SERIES.items()]))
    p.append("<p><i>Post times are a starting point in your local time. After two weeks, check Instagram Insights for when your followers are most active and adjust.</i></p>")

    # --- Calendar
    p.append("<h2>6. The 28-day calendar: Nov 9 to Dec 6, 2026</h2>")
    for wi, (wk, theme, desc) in enumerate(calendar_plan.WEEKS):
        p.append(f"<h2>{esc(wk)}: {esc(theme)}</h2>")
        p.append(f"<p><i>{esc(desc)}</i></p>")
        for date, wd, w, d in calendar_plan.schedule():
            if w != wi:
                continue
            s = formats.SERIES[wd]
            setup_names = ", ".join(f"{k} ({formats.SETUPS[k][0]})" for k in s["setup"].replace(" ", "").split("+"))
            p.append(f"<h3>{fmt_date(date)} | {esc(s['name'])} | {esc(d['title'])}</h3>")
            rep_label = "Rep (a real one from the app's archive; today's app rep wins)" if d["real"] else "Backup rep (the app's rep wins)"
            p.append(f"<p><b>{rep_label}:</b> {esc(d['rep'])}<br>"
                     f"<b>Area:</b> {esc(d['area'])} | <b>Format:</b> {esc(s['fmt'])} | <b>Post:</b> {esc(s['time'])}<br>"
                     f"<b>Hook on screen:</b> {esc(d['hook_text'])}"
                     + (f"<br><b>Say:</b> <i>\"{esc(d['hook_spoken'])}\"</i>" if d["hook_spoken"] else "") + "</p>")
            p.append("<p><b>Script</b></p><ol>" + "".join(f"<li>{esc(x)}</li>" for x in d["beats"]) + "</ol>")
            p.append(f"<p><b>How to film:</b> Setup {esc(setup_names)}</p>" + ul([esc(x) for x in d["shots"]]))
            p.append(f"<p><b>Caption:</b><br>{esc(d['caption'])}</p>")
            if d["extras"]:
                p.append(f"<p><b>Extra:</b> {esc(d['extras'])}</p>")

    # --- Filming
    p.append("<h2>7. Filming playbook</h2>")
    p.append("<p><b>Kit:</b> your phone, a small tripod, a clip-on wireless mic, a window. Optional: a dash mount and a second phone for Facebook Live. Edit in Instagram's Edits app or CapCut, captions on every video (most people watch on mute).</p>")
    for k, (name, tips) in formats.SETUPS.items():
        p.append(f"<h3>Setup {k}: {esc(name)}</h3>")
        p.append(ul([esc(t) for t in tips]))
    p.append("<p><b>Every video:</b> hook in the first second (spoken + on screen), captions burned in, end card with 'Today's rep' and 'Comment IN', closing line 'Life takes reps. See you tomorrow.'</p>")

    # --- Intel
    p.append("<h2>8. Creator intel: who's winning in this space and what to take</h2>")
    p.append("<p><i>Format patterns from well-known creators. This build did not have logged-in access to Instagram or Facebook, so check current follower counts and recent top posts before quoting numbers.</i></p>")
    p.append(table(["Account", "Lane", "What works for them", "What we take"],
                   [(f"<b>{esc(a)}</b>", esc(b), esc(cc), esc(dd)) for a, b, cc, dd in intel.CREATORS]))
    p.append("<h3>Platform playbook (Instagram + Facebook, late 2026)</h3>")
    p.append(table(["Principle", "What to do"], [(f"<b>{esc(a)}</b>", esc(b)) for a, b in intel.PLATFORM_PLAYBOOK]))

    # --- KPIs
    p.append("<h2>9. Scoreboard: what to track every week</h2>")
    p.append(table(["Metric", "Why it matters", "Where to find it"], [
        ("Reps done together (running total)", "The north star. IN comments + story tags + Add Yours entries + app completions.", "Comments, Stories, app dashboard"),
        ("Sends per post", "Instagram's strongest reach signal. Carousels and duets should lead.", "Insights > post > Shares"),
        ("Average watch time / 3-second hold", "Tells you which hooks work.", "Insights > Reel"),
        ("Saves", "Shows which reps people want to keep.", "Insights > post"),
        ("New followers (IG + FB)", "Growth.", "Professional dashboard"),
        ("Facebook Group members and daily thread comments", "Community depth.", "Group admin tools"),
        ("Link clicks to the app and new app sign-ups", "Business result.", "Link-in-bio tool + app analytics"),
    ]))

    # --- Sources & maintenance
    p.append("<h2>10. Sources</h2>")
    p.append("<p>Brand content: THE PRACTICE CLUB brand brief, THE PRACTICE AI Ads playbook, INNERBOARD SUITE build brief, The Practice Club Master Video Scripts, InnerBoard Academy courses, and Practice app reminder emails, all from Leah's Drive and inbox.</p>")
    p.append(ul([f'<a href="{u}">{esc(t)}</a>' for t, u in intel.SOURCES]))
    p.append("<h2>11. How this is built</h2>")
    p.append("<p>This document is generated from code in the GitHub repo <b>leahtfl-spec/leahrolingmarketingcommandcenter</b>. To change the plan, edit the files in <b>command_center/</b> (calendar_plan.py holds the days) and run <b>python3 build.py</b>.</p>")

    return "<html><head><meta charset='utf-8'><title>Rep With Me | Marketing Command Center</title></head><body>" + "\n".join(p) + "</body></html>"


def build_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Day", "Week theme", "Series", "Format", "Post time", "Title", "Rep (backup)",
                    "Hook (on screen)", "Filming setup", "Done?", "App rep (if different)",
                    "Views", "Sends", "Saves", "IN comments", "New followers", "Notes"])
        for date, wd, wi, d in calendar_plan.schedule():
            s = formats.SERIES[wd]
            w.writerow([date.isoformat(), wd, calendar_plan.WEEKS[wi][1], s["name"], s["fmt"], s["time"],
                        d["title"], d["rep"], d["hook_text"], s["setup"], "FALSE", "", "", "", "", "", "", ""])


def build_json():
    days = []
    for date, wd, wi, d in calendar_plan.schedule():
        s = formats.SERIES[wd]
        setups = [k for k in s["setup"].replace(" ", "").split("+")]
        days.append({**d, "date": date.isoformat(), "weekday": wd, "week": wi,
                     "series": s["name"], "format": s["fmt"], "time": s["time"], "setups": setups})
    return {
        "founder": brand.FOUNDER,
        "campaign": brand.CAMPAIGN,
        "architecture": brand.ARCHITECTURE,
        "coreLines": brand.CORE_LINES,
        "appRhythm": brand.APP_RHYTHM,
        "realReps": brand.REAL_REPS,
        "audiences": brand.AUDIENCE_LANES,
        "visual": brand.VISUAL,
        "guardrails": brand.GUARDRAILS,
        "series": formats.SERIES,
        "setups": {k: {"name": n, "tips": t} for k, (n, t) in formats.SETUPS.items()},
        "routine": formats.DAILY_ROUTINE,
        "funRules": formats.FUN_RULES,
        "growth": formats.GROWTH_ENGINE,
        "creators": intel.CREATORS,
        "platform": intel.PLATFORM_PLAYBOOK,
        "sources": intel.SOURCES,
        "weeks": calendar_plan.WEEKS,
        "days": days,
    }


def main():
    validate()
    DIST.mkdir(exist_ok=True)
    (DIST / "command_center.html").write_text(build_doc(), encoding="utf-8")
    build_csv(DIST / "daily_tracker.csv")
    WEB_DATA.parent.mkdir(parents=True, exist_ok=True)
    WEB_DATA.write_text(json.dumps(build_json(), indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{WEB_DATA.relative_to(ROOT)}: {WEB_DATA.stat().st_size:,} bytes")
    for f in sorted(DIST.iterdir()):
        print(f"{f.name}: {f.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
