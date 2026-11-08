# Rep With Me | Marketing Command Center

Leah Roling's daily marketing command center for **The Practice by InnerBoard** and **The Practice Club**.
It tells you exactly what to post every day on Instagram and Facebook, built around doing the app's
**rep of the day** together with the community.

## Live files (Google Drive, folder "REP WITH ME | Marketing Command Center")
- **Rep With Me | Marketing Command Center** (Google Doc): the strategy and the 28-day calendar with hooks, scripts, shot lists and captions.
- **Rep With Me Daily Tracker** (Google Sheet): one row per day, with a Done box and columns for the day's numbers.

## The website (Vite, deploys on Vercel)
Open it every morning: it lands on **today's post** (rep, hook, script, how to film, caption with a Copy button)
and has views for the full calendar, daily routine, filming setups, growth plan, brand and creator intel.
"Posted" checkmarks are saved in your browser.

Run it locally:
```bash
npm install
npm run dev
```

### Deploy on Vercel
1. Go to https://vercel.com/new and import `leahtfl-spec/leahrolingmarketingcommandcenter`.
2. Vercel detects Vite from `vercel.json`: build command `npm run build`, output folder `dist`. Leave the defaults and click **Deploy**.
3. Every push to the branch you deploy redeploys the site automatically.

## How it's organized
| File | What's in it |
|---|---|
| `command_center/brand.py` | Brand facts: InnerBoard architecture, core lines, the app's daily rhythm, real reps, audiences, look and feel, guardrails, the Rep With Me campaign |
| `command_center/formats.py` | Weekly series (Mon-Sun), filming setups A-H, the daily routine, fun rules, growth engine |
| `command_center/calendar_plan.py` | The 28-day sprint (Nov 9 - Dec 6, 2026): rep, hook, script, shots, caption for every day |
| `command_center/intel.py` | Creator intel and the Instagram/Facebook platform playbook, with sources |
| `build.py` | Checks the plan (28 days, no em dashes in posted copy) and writes the outputs below |
| `src/data/plan.json` | The plan as data for the website (generated, committed so Vercel needs no Python) |
| `src/main.js`, `src/style.css`, `index.html` | The Vite website |
| `exports/command_center.html` | Uploaded to Drive as the Google Doc |
| `exports/daily_tracker.csv` | Uploaded to Drive as the Google Sheet |

## Update the plan
1. Edit the files in `command_center/` (add month two by appending days to `DAYS` and moving `START`).
2. Run `python3 build.py` (or `npm run plan`). This refreshes `src/data/plan.json` and `exports/`.
3. Commit and push; Vercel redeploys the website. Upload the new `exports/` files to the Drive folder if you want the Doc and Sheet refreshed too.

## The one rule
The app's rep of the day always wins. Each day lists a backup rep; if the app sends a different one,
use it with the same series format and shot list.
