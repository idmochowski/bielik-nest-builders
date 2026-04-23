/* ═══════════════════════════════════════════════
   Agent Architectures — Slide Engine
   Navigation, fragments, speaker notes, animations
   Works with both HTTP server and file:// protocol
   ═══════════════════════════════════════════════ */

const SLIDES = [
  'slide-00-title.html',
  'slide-01-overview.html',
  'slide-02-react.html',
  'slide-03-tool-calling.html',
  'slide-04-rewod.html',
  'slide-05-plan-execute.html',
  'slide-06-reflexion.html',
  'slide-07-lats.html',
  'slide-08-multi-agent.html',
  'slide-09-comparison.html',
  'slide-10-takeaway.html',
];

let currentSlide = 0;
let isTransitioning = false;
let currentFragment = -1;
let totalFragments = 0;
let notesVisible = false;
let useEmbeddedSlides = false;

// Embedded slide content for file:// protocol support
const EMBEDDED_SLIDES = {};

// ─── DOM references ──────────────────────────

const container = document.getElementById('slide-container');
const progressBar = document.getElementById('progress-bar');
const counterEl = document.getElementById('slide-counter');
const gotoOverlay = document.getElementById('goto-overlay');
const gotoInput = document.getElementById('goto-input');
const overviewOverlay = document.getElementById('overview-overlay');
const overviewGrid = document.getElementById('overview-grid');
const speakerNotes = document.getElementById('speaker-notes');
const speakerNotesContent = document.getElementById('speaker-notes-content');
const fragmentIndicator = document.getElementById('fragment-indicator');
const fragmentDots = document.getElementById('fragment-dots');

// ─── Initialize ──────────────────────────────

document.addEventListener('DOMContentLoaded', async () => {
  // Try fetching first slide to detect if we need embedded mode
  try {
    const resp = await fetch(SLIDES[0]);
    if (!resp.ok) throw new Error('fetch failed');
    useEmbeddedSlides = false;
  } catch (e) {
    // file:// protocol — use embedded slides
    useEmbeddedSlides = true;
    loadEmbeddedSlides();
  }

  loadSlide(0);
  buildOverviewGrid();
  setupTouchSupport();
});

// ─── Embedded slides loader ──────────────────
// Populated by serve.py or the inline script in index.html

function loadEmbeddedSlides() {
  // Look for embedded slide data in the document
  const embeddedData = document.getElementById('embedded-slides-data');
  if (embeddedData) {
    try {
      const data = JSON.parse(embeddedData.textContent);
      Object.assign(EMBEDDED_SLIDES, data);
    } catch (e) {
      console.warn('Failed to parse embedded slides data');
    }
  }
}

// ─── Slide loading ───────────────────────────

async function loadSlide(index, direction = 'forward') {
  if (index < 0 || index >= SLIDES.length || isTransitioning) return;
  isTransitioning = true;

  // Exit animation
  if (direction === 'forward') {
    container.classList.add('exit-left');
  } else {
    container.style.opacity = '0';
    container.style.transform = 'translateX(40px)';
  }

  await sleep(200);

  // Load new content
  try {
    let html;
    if (useEmbeddedSlides && EMBEDDED_SLIDES[SLIDES[index]]) {
      html = EMBEDDED_SLIDES[SLIDES[index]];
    } else {
      const resp = await fetch(SLIDES[index]);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      html = await resp.text();
    }
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div class="slide-content"><h2>Error loading slide</h2><p>${err.message}</p></div>`;
  }

  currentSlide = index;
  resetFragments();
  updateUI();
  updateSpeakerNotes();

  // Enter animation
  container.classList.remove('exit-left');
  container.classList.add('loading');

  // Force reflow
  void container.offsetHeight;

  await sleep(50);
  container.classList.remove('loading');
  container.style.transform = '';
  container.style.opacity = '';

  isTransitioning = false;

  // Auto-reveal first fragment after a beat if any exist
  if (totalFragments === 0) {
    hideFragmentIndicator();
  }
}

// ─── Fragment System ─────────────────────────

function resetFragments() {
  currentFragment = -1;
  const fragments = getFragments();
  totalFragments = fragments.length;

  // Hide all fragments
  fragments.forEach(f => f.classList.remove('revealed'));

  updateFragmentIndicator();
}

function getFragments() {
  return Array.from(container.querySelectorAll('.fragment'));
}

function revealNextFragment() {
  const fragments = getFragments();
  if (currentFragment >= totalFragments - 1) return false;

  currentFragment++;
  fragments[currentFragment].classList.add('revealed');

  // Trigger special effects based on fragment data attributes
  const frag = fragments[currentFragment];
  if (frag.dataset.qualityMeter) {
    updateQualityMeter(frag.dataset.qualityMeter);
  }
  if (frag.dataset.highlightRow) {
    highlightTableRow(frag.dataset.highlightRow);
  }

  updateFragmentIndicator();
  return true;
}

function hasUnrevealedFragments() {
  return currentFragment < totalFragments - 1;
}

function updateFragmentIndicator() {
  if (totalFragments === 0) {
    hideFragmentIndicator();
    return;
  }

  fragmentIndicator.classList.add('visible');
  let html = '';
  for (let i = 0; i < totalFragments; i++) {
    const cls = i <= currentFragment ? 'fragment-dot revealed' : 'fragment-dot';
    html += `<div class="${cls}"></div>`;
  }
  fragmentDots.innerHTML = html;
}

function hideFragmentIndicator() {
  fragmentIndicator.classList.remove('visible');
}

// ─── Quality Meter (Reflexion slide) ────────

function updateQualityMeter(value) {
  const fill = container.querySelector('.quality-fill');
  const label = container.querySelector('.quality-label');
  if (fill && label) {
    fill.style.width = value + '%';
    label.textContent = value + '%';
  }
}

// ─── Table Row Highlight (Comparison slide) ─

function highlightTableRow(index) {
  const rows = container.querySelectorAll('.comparison-table tbody tr');
  rows.forEach(r => r.classList.remove('row-revealed'));
  const target = rows[parseInt(index)];
  if (target) {
    target.classList.add('row-revealed');
  }
}

// ─── UI updates ──────────────────────────────

function updateUI() {
  const total = SLIDES.length;
  const current = currentSlide + 1;

  // Progress bar
  progressBar.style.width = `${(current / total) * 100}%`;

  // Counter
  counterEl.innerHTML = `<span class="current">${current}</span> / ${total}`;

  // Update title
  document.title = `Agent Architectures — ${current}/${total}`;
}

// ─── Speaker Notes ──────────────────────────

function updateSpeakerNotes() {
  if (!speakerNotesContent) return;

  if (typeof SPEAKER_NOTES !== 'undefined' && SPEAKER_NOTES[currentSlide]) {
    const note = SPEAKER_NOTES[currentSlide];
    speakerNotesContent.innerHTML = `
      <div class="speaker-notes-header">
        <span class="speaker-notes-label">Speaker Notes</span>
        <span class="speaker-notes-time">${note.time || ''}</span>
      </div>
      <p>${note.text}</p>
      ${note.points ? `<ul>${note.points.map(p => `<li>${p}</li>`).join('')}</ul>` : ''}
    `;
  } else {
    speakerNotesContent.innerHTML = `
      <div class="speaker-notes-header">
        <span class="speaker-notes-label">Speaker Notes</span>
      </div>
      <p>No notes for this slide.</p>
    `;
  }
}

function toggleSpeakerNotes() {
  notesVisible = !notesVisible;
  speakerNotes.classList.toggle('visible', notesVisible);
}

// ─── Navigation ──────────────────────────────

function nextSlide() {
  // First try to reveal fragments
  if (hasUnrevealedFragments()) {
    revealNextFragment();
    return;
  }
  // Then advance slide
  if (currentSlide < SLIDES.length - 1) {
    loadSlide(currentSlide + 1, 'forward');
  }
}

function prevSlide() {
  // Go to previous slide (fragments auto-reset)
  if (currentSlide > 0) {
    loadSlide(currentSlide - 1, 'backward');
  }
}

function goToSlide(index) {
  const dir = index > currentSlide ? 'forward' : 'backward';
  loadSlide(index, dir);
}

// ─── Keyboard ────────────────────────────────

document.addEventListener('keydown', (e) => {
  // Goto overlay active
  if (gotoOverlay.classList.contains('active')) {
    if (e.key === 'Escape') {
      closeGoto();
    } else if (e.key === 'Enter') {
      const num = parseInt(gotoInput.value, 10);
      if (num >= 1 && num <= SLIDES.length) {
        closeGoto();
        goToSlide(num - 1);
      }
    }
    return;
  }

  // Overview overlay active
  if (overviewOverlay.classList.contains('active')) {
    if (e.key === 'Escape' || e.key === 'o' || e.key === 'O') {
      overviewOverlay.classList.remove('active');
    }
    return;
  }

  switch (e.key) {
    case 'ArrowRight':
    case 'ArrowDown':
    case ' ':
    case 'PageDown':
      e.preventDefault();
      nextSlide();
      break;
    case 'ArrowLeft':
    case 'ArrowUp':
    case 'PageUp':
      e.preventDefault();
      prevSlide();
      break;
    case 'Home':
      e.preventDefault();
      goToSlide(0);
      break;
    case 'End':
      e.preventDefault();
      goToSlide(SLIDES.length - 1);
      break;
    case 'f':
    case 'F':
      toggleFullscreen();
      break;
    case 'g':
    case 'G':
      openGoto();
      break;
    case 'o':
    case 'O':
      toggleOverview();
      break;
    case 's':
    case 'S':
      toggleSpeakerNotes();
      break;
    case 'Escape':
      if (notesVisible) {
        toggleSpeakerNotes();
      } else if (document.fullscreenElement) {
        document.exitFullscreen();
      }
      break;
  }
});

// ─── Touch support ───────────────────────────

function setupTouchSupport() {
  let touchStartX = 0;
  let touchStartY = 0;

  document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;

    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
      if (dx < 0) nextSlide();
      else prevSlide();
    }
  }, { passive: true });
}

// ─── Fullscreen ──────────────────────────────

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {});
  } else {
    document.exitFullscreen();
  }
}

// ─── Go-to slide ─────────────────────────────

function openGoto() {
  gotoOverlay.classList.add('active');
  gotoInput.value = '';
  gotoInput.focus();
}

function closeGoto() {
  gotoOverlay.classList.remove('active');
}

// ─── Overview grid ───────────────────────────

function buildOverviewGrid() {
  const titles = [
    'Architektury Agent&oacute;w AI',
    'Dlaczego architektura ma znaczenie?',
    'ReAct (Reasoning + Acting)',
    'Tool Calling Agent',
    'ReWOO (Reasoning Without Observation)',
    'Plan-and-Execute',
    'Reflexion',
    'LATS (Language Agent Tree Search)',
    'Multi-Agent Orchestration',
    'Por&oacute;wnanie architektur',
    'Kluczowe wnioski',
  ];

  overviewGrid.innerHTML = titles.map((title, i) => `
    <div class="overview-card" onclick="goFromOverview(${i})">
      <div class="card-num">Slide ${i + 1}</div>
      <div class="card-title">${title}</div>
    </div>
  `).join('');
}

function goFromOverview(index) {
  overviewOverlay.classList.remove('active');
  goToSlide(index);
}

function toggleOverview() {
  overviewOverlay.classList.toggle('active');
}

// ─── Spectrum Click Navigation ───────────────

document.addEventListener('click', (e) => {
  const item = e.target.closest('.spectrum-item');
  if (item) {
    const slideIndex = parseInt(item.dataset.slide);
    if (!isNaN(slideIndex) && slideIndex >= 0 && slideIndex < SLIDES.length) {
      goToSlide(slideIndex);
    }
  }
});

// ─── Utility ─────────────────────────────────

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
