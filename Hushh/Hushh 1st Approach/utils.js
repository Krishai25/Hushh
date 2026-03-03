// ─── CONFIG ────────────────────────────────────────────────
const CONFIG = {
  // Replace with your deployed Google Apps Script Web App URL
  // API_URL: 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec',
  // Replace with your n8n webhook URL for email nudges / automation
  // N8N_WEBHOOK: 'https://your-n8n-instance.com/webhook/kai-campus',
  // SHEET_ID: 'YOUR_GOOGLE_SHEET_ID',
};

// ─── SESSION HELPERS ───────────────────────────────────────
const Auth = {
  save(user) { localStorage.setItem('kaiUser', JSON.stringify(user)); },
  get()      { try { return JSON.parse(localStorage.getItem('kaiUser')); } catch { return null; } },
  clear()    { localStorage.removeItem('kaiUser'); },
  require()  {
    const u = Auth.get();
    if (!u) { window.location.href = 'student-login.html'; return null; }
    return u;
  },
};

// ─── API CALLS ─────────────────────────────────────────────
async function apiPost(payload) {
  const res = await fetch(CONFIG.API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const text = await res.text();
  try { return JSON.parse(text); } catch { return { status: 'raw', data: text }; }
}

// n8n webhook for automation (email nudges, streak triggers, etc.)
async function n8nTrigger(event, data) {
  try {
    await fetch(CONFIG.N8N_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event, ...data, timestamp: new Date().toISOString() }),
    });
  } catch (e) { console.warn('n8n webhook failed silently:', e); }
}

// ─── GAMIFICATION ──────────────────────────────────────────
const Gamification = {
  BADGES: [
    { id: 'newcomer',    icon: '🌱', label: 'Newcomer',    xp: 0   },
    { id: 'active',      icon: '⚡', label: 'Active',      xp: 50  },
    { id: 'explorer',    icon: '🧭', label: 'Explorer',    xp: 100 },
    { id: 'connector',   icon: '🔗', label: 'Connector',   xp: 200 },
    { id: 'champion',    icon: '🏆', label: 'Champion',    xp: 400 },
  ],
  getCurrentBadge(xp) {
    return [...this.BADGES].reverse().find(b => xp >= b.xp) || this.BADGES[0];
  },
  getNextBadge(xp) {
    return this.BADGES.find(b => xp < b.xp);
  },
  getStreakFromStorage() {
    const d = localStorage.getItem('kaiStreak');
    if (!d) return { streak: 0, lastLogin: null };
    return JSON.parse(d);
  },
  updateStreak() {
    const { streak, lastLogin } = this.getStreakFromStorage();
    const today = new Date().toDateString();
    if (lastLogin === today) return streak;
    const yesterday = new Date(Date.now() - 86400000).toDateString();
    const newStreak = lastLogin === yesterday ? streak + 1 : 1;
    localStorage.setItem('kaiStreak', JSON.stringify({ streak: newStreak, lastLogin: today }));
    return newStreak;
  },
  getXP() { return parseInt(localStorage.getItem('kaiXP') || '0'); },
  addXP(amount) {
    const current = this.getXP();
    const newXP = current + amount;
    localStorage.setItem('kaiXP', newXP);
    return newXP;
  },
};

// ─── TOAST ─────────────────────────────────────────────────
function showToast(msg, type = 'info') {
  const existing = document.querySelector('.kai-toast');
  if (existing) existing.remove();
  const t = document.createElement('div');
  t.className = 'kai-toast';
  const colors = { info: '#6c63ff', success: '#00e5a0', error: '#f87171', warning: '#ffd166' };
  t.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:9999;
    background:#1a1d28; border:1px solid ${colors[type]};
    color:#e8eaf6; padding:12px 20px; border-radius:12px;
    font-family:'DM Sans',sans-serif; font-size:0.9rem;
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
    animation:fadeUp 0.3s ease;
    max-width:320px;
  `;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ─── EVENTS MOCK DATA (fallback when sheet is empty) ───────
const MOCK_EVENTS = [
  { id:'e1', title:'Hackathon 2025', club:'Tech Club', venue:'Lab 204', time:'2025-08-15 10:00', tags:'tech,coding', joinLink:'https://chat.whatsapp.com/example' },
  { id:'e2', title:'Art Exhibition Opening', club:'Arts Society', venue:'Gallery Hall', time:'2025-08-18 16:00', tags:'art,culture', joinLink:'#' },
  { id:'e3', title:'Debate Championship', club:'Debate Club', venue:'Auditorium', time:'2025-08-20 09:00', tags:'debate,communication', joinLink:'#' },
  { id:'e4', title:'Startup Pitch Night', club:'Entrepreneurship Cell', venue:'Seminar Room', time:'2025-08-22 18:00', tags:'business,startup', joinLink:'#' },
  { id:'e5', title:'Photography Walk', club:'Photography Club', venue:'Campus Grounds', time:'2025-08-25 07:00', tags:'photography,art', joinLink:'#' },
  { id:'e6', title:'ML Workshop', club:'AI Club', venue:'Lab 101', time:'2025-08-28 14:00', tags:'tech,ml,coding', joinLink:'#' },
];

const MOCK_CLUBS = [
  { id:'c1', name:'Tech Club', description:'Build, hack and ship cool projects.', tags:'tech,coding,hardware' },
  { id:'c2', name:'Arts Society', description:'Painting, sculpture, and mixed media.', tags:'art,culture,design' },
  { id:'c3', name:'Debate Club', description:'Sharpen your rhetoric and critical thinking.', tags:'debate,communication,leadership' },
  { id:'c4', name:'Entrepreneurship Cell', description:'From ideation to launch — we fund ideas.', tags:'business,startup,finance' },
  { id:'c5', name:'Photography Club', description:'Capture moments that matter.', tags:'photography,art,travel' },
  { id:'c6', name:'AI Club', description:'Machine learning, NLP, and beyond.', tags:'tech,ml,coding,research' },
];
