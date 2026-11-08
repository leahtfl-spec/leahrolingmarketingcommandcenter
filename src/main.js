import plan from './data/plan.json';
import './style.css';

const $app = document.getElementById('app');
const $nav = document.getElementById('nav');

const VIEWS = [
  ['today', 'Today'],
  ['calendar', 'Calendar'],
  ['routine', 'Daily Routine'],
  ['filming', 'How to Film'],
  ['growth', 'Growth'],
  ['brand', 'Brand'],
  ['intel', 'Creator Intel'],
];

// ---------- helpers ----------
const esc = (s = '') =>
  String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const nl = (s) => esc(s).replace(/\n/g, '<br>');
const list = (items, tag = 'ul') => `<${tag}>${items.map((i) => `<li>${esc(i)}</li>`).join('')}</${tag}>`;

const store = {
  get(k, fallback) {
    try {
      const v = localStorage.getItem(k);
      return v === null ? fallback : JSON.parse(v);
    } catch {
      return fallback;
    }
  },
  set(k, v) {
    try {
      localStorage.setItem(k, JSON.stringify(v));
    } catch {
      /* storage unavailable; the page still works */
    }
  },
};
const doneSet = () => new Set(store.get('rwm-done', []));
const toggleDone = (date) => {
  const s = doneSet();
  s.has(date) ? s.delete(date) : s.add(date);
  store.set('rwm-done', [...s]);
};

const localISO = (d = new Date()) => {
  const z = new Date(d.getTime() - d.getTimezoneOffset() * 60000);
  return z.toISOString().slice(0, 10);
};
const prettyDate = (iso) =>
  new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
const shortDate = (iso) =>
  new Date(iso + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

function todayIndex() {
  const t = localISO();
  const days = plan.days;
  if (t < days[0].date) return { i: 0, note: `The sprint starts ${prettyDate(days[0].date)}. Here's day one so you can prep.` };
  if (t > days[days.length - 1].date)
    return { i: days.length - 1, note: 'This sprint is finished. Time to build month two (add days in command_center/calendar_plan.py).' };
  return { i: days.findIndex((d) => d.date === t), note: '' };
}

// ---------- views ----------
function dayCard(i, note = '') {
  const d = plan.days[i];
  const week = plan.weeks[d.week];
  const done = doneSet().has(d.date);
  const repLabel = d.real ? "A real rep from the app's archive" : 'Backup rep';
  const setups = d.setups
    .map((k) => {
      const s = plan.setups[k];
      return `<details class="setup"><summary>Setup ${k}: ${esc(s.name)}</summary>${list(s.tips)}</details>`;
    })
    .join('');

  return `
  ${note ? `<p class="note">${esc(note)}</p>` : ''}
  <div class="daynav">
    <button class="ghost" data-go="${i - 1}" ${i === 0 ? 'disabled' : ''}>‹ Prev</button>
    <span>Day ${i + 1} of ${plan.days.length}</span>
    <button class="ghost" data-go="${i + 1}" ${i === plan.days.length - 1 ? 'disabled' : ''}>Next ›</button>
  </div>
  <article class="day ${done ? 'is-done' : ''}">
    <div class="day-head">
      <div>
        <div class="eyebrow">${esc(prettyDate(d.date))} · ${esc(week[0])}: ${esc(week[1])}</div>
        <h1>${esc(d.title)}</h1>
        <div class="chips">
          <span class="chip gold">${esc(d.series)}</span>
          <span class="chip">${esc(d.format)}</span>
          <span class="chip">Post ${esc(d.time)}</span>
          <span class="chip">${esc(d.area)}</span>
        </div>
      </div>
      <label class="done"><input type="checkbox" data-done="${d.date}" ${done ? 'checked' : ''}/> Posted</label>
    </div>

    <section class="rep">
      <div class="eyebrow">Today's rep</div>
      <p class="rep-text">${esc(d.rep)}</p>
      <p class="small">${repLabel}. If the app sends a different rep this morning, use the app's rep. The format below works for any rep.</p>
    </section>

    <div class="grid2">
      <section class="panel">
        <h3>The hook</h3>
        <p class="hook">“${esc(d.hook_text)}”</p>
        ${d.hook_spoken ? `<p><strong>Say it:</strong> <em>${esc(d.hook_spoken)}</em></p>` : ''}
        <h3>${d.series === 'WHY THIS REP WORKS' ? 'Slides' : d.series === 'SET THE WEEK' ? 'Live run of show' : 'Script'}</h3>
        ${list(d.beats, 'ol')}
      </section>
      <section class="panel">
        <h3>How to film</h3>
        ${list(d.shots)}
        ${setups}
        ${d.extras ? `<h3>Extra</h3><p>${esc(d.extras)}</p>` : ''}
      </section>
    </div>

    <section class="panel caption">
      <div class="row"><h3>Caption</h3><button class="btn" data-copy="${i}">Copy caption</button></div>
      <p>${nl(d.caption)}</p>
    </section>
  </article>`;
}

function viewToday(param) {
  const t = todayIndex();
  const i = param !== undefined ? Math.max(0, Math.min(plan.days.length - 1, Number(param))) : t.i;
  return dayCard(i, param === undefined ? t.note : '');
}

function viewCalendar() {
  const done = doneSet();
  const today = localISO();
  return `<h1 class="page">The 28-day sprint</h1>
  <p class="lede">${done.size} of ${plan.days.length} posted. Tap any day to open it.</p>
  ${plan.weeks
    .map(
      (w, wi) => `
    <section class="week">
      <h2>${esc(w[0])}: <em>${esc(w[1])}</em></h2>
      <p class="small">${esc(w[2])}</p>
      <div class="cal">
        ${plan.days
          .map((d, i) => [d, i])
          .filter(([d]) => d.week === wi)
          .map(
            ([d, i]) => `
          <a class="cal-day ${done.has(d.date) ? 'is-done' : ''} ${d.date === today ? 'is-today' : ''}" href="#today/${i}">
            <div class="cal-date">${esc(d.weekday)} ${esc(shortDate(d.date))}</div>
            <div class="cal-series">${esc(d.series)}</div>
            <div class="cal-title">${esc(d.title)}</div>
            ${done.has(d.date) ? '<div class="tick">✓ Posted</div>' : ''}
          </a>`,
          )
          .join('')}
      </div>
    </section>`,
    )
    .join('')}`;
}

function table(headers, rows) {
  return `<div class="tablewrap"><table><thead><tr>${headers.map((h) => `<th>${esc(h)}</th>`).join('')}</tr></thead>
  <tbody>${rows.map((r) => `<tr>${r.map((c, j) => `<td>${j === 0 ? `<strong>${esc(c)}</strong>` : esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}

function viewRoutine() {
  const s = plan.series;
  return `<h1 class="page">The daily routine</h1>
  <p class="lede">About 45 minutes a day. Same rhythm as the app: Two Minutes, Today's Rep, Close the Day.</p>
  ${table(['When', 'What', 'How'], plan.routine)}
  <h2>The weekly series</h2>
  ${table(['Day', 'Series', 'Format', 'Post time', 'Why'], Object.entries(s).map(([k, v]) => [k, v.name, v.fmt, v.time, v.why]))}
  <p class="small">Post times are a starting point in your local time. After two weeks, check Instagram Insights and adjust.</p>
  <h2>Fun rules</h2>${list(plan.funRules)}`;
}

function viewFilming() {
  return `<h1 class="page">How to film</h1>
  <p class="lede">Kit: your phone, a small tripod, a clip-on wireless mic, a window. Captions on every video. Hook in the first second. End with “Comment IN” and “Life takes reps. See you tomorrow.”</p>
  <div class="cards">${Object.entries(plan.setups)
    .map(([k, s]) => `<section class="panel"><div class="eyebrow">Setup ${k}</div><h3>${esc(s.name)}</h3>${list(s.tips)}</section>`)
    .join('')}</div>`;
}

function viewGrowth() {
  const c = plan.campaign;
  return `<h1 class="page">${esc(c.name)}</h1>
  <p class="lede"><em>${esc(c.tagline)}</em></p>
  <p>${esc(c.promise)}</p>
  <div class="stat"><div class="eyebrow">North star</div><p>${esc(c.north_star)}</p></div>
  <p><strong>Community:</strong> ${esc(c.community_name)} · <strong>Join keyword:</strong> ${esc(c.keyword)} · <strong>Hashtags:</strong> ${esc(c.hashtags.join(' '))}</p>
  <h2>The growth engine</h2>${table(['Lever', 'How'], plan.growth)}`;
}

function viewBrand() {
  return `<h1 class="page">What InnerBoard stands for</h1>
  <p class="lede">The Practice is what people use. The Practice Club is what people belong to. InnerBoard is the methodology behind it.</p>
  ${table(['Brand', 'Role', 'What it is'], plan.architecture)}
  <h2>Core lines</h2>${list(plan.coreLines)}
  <h2>The app's daily rhythm</h2>${table(['When', 'Moment', 'What the app says'], plan.appRhythm)}
  <h2>Real reps the app has sent</h2>${table(['Date', 'Rep'], plan.realReps)}
  <h2>Audience lanes</h2>${table(['Who', "What they're thinking"], plan.audiences)}
  <h2>Look and feel</h2><ul>${Object.entries(plan.visual).map(([k, v]) => `<li><strong>${esc(k)}:</strong> ${esc(v)}</li>`).join('')}</ul>
  <h2>Guardrails</h2>${list(plan.guardrails)}`;
}

function viewIntel() {
  return `<h1 class="page">Creator intel</h1>
  <p class="lede">Format patterns from well-known creators in the space. Check current follower counts and recent top posts before quoting numbers.</p>
  ${table(['Account', 'Lane', 'What works for them', 'What we take'], plan.creators)}
  <h2>Instagram + Facebook playbook</h2>${table(['Principle', 'What to do'], plan.platform)}
  <h2>Sources</h2><ul>${plan.sources.map(([t, u]) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)}</a></li>`).join('')}</ul>`;
}

const RENDER = {
  today: viewToday,
  calendar: viewCalendar,
  routine: viewRoutine,
  filming: viewFilming,
  growth: viewGrowth,
  brand: viewBrand,
  intel: viewIntel,
};

// ---------- router ----------
function render() {
  const [view = 'today', param] = location.hash.replace(/^#/, '').split('/');
  const key = RENDER[view] ? view : 'today';
  $nav.innerHTML = VIEWS.map(([k, label]) => `<a href="#${k}" class="${k === key ? 'active' : ''}">${label}</a>`).join('');
  $app.innerHTML = RENDER[key](param);
  window.scrollTo(0, 0);
}

$app.addEventListener('click', async (e) => {
  const go = e.target.closest('[data-go]');
  if (go && !go.disabled) location.hash = `today/${go.dataset.go}`;
  const copy = e.target.closest('[data-copy]');
  if (copy) {
    try {
      await navigator.clipboard.writeText(plan.days[Number(copy.dataset.copy)].caption);
      copy.textContent = 'Copied ✓';
    } catch {
      copy.textContent = 'Select and copy below';
    }
    setTimeout(() => (copy.textContent = 'Copy caption'), 1800);
  }
});
$app.addEventListener('change', (e) => {
  const box = e.target.closest('[data-done]');
  if (box) {
    toggleDone(box.dataset.done);
    box.closest('.day')?.classList.toggle('is-done', box.checked);
  }
});

window.addEventListener('hashchange', render);
render();
