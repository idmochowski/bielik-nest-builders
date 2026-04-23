#!/usr/bin/env python3
"""Build a self-contained presentation.html that works without a server.

Reads all slide HTML files, CSS, JS, and speaker notes,
then embeds everything into a single HTML file that works on file:// protocol.

Usage:
    python build.py          # Creates presentation.html in slides/
"""

import json
import os
import sys

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

SLIDE_FILES = [
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
]


def read_file(name):
    path = os.path.join(DIRECTORY, name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def build():
    css = read_file('styles.css')
    js = read_file('slides.js')
    notes = read_file('speaker-notes.js')

    # Read all slides into a JSON map
    slides_data = {}
    for slide_file in SLIDE_FILES:
        slides_data[slide_file] = read_file(slide_file)

    slides_json = json.dumps(slides_data, ensure_ascii=False)

    # Read index.html and extract the body structure
    index_html = read_file('index.html')

    # Build self-contained HTML
    output = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Architectures — Presentation</title>
  <meta name="description" content="Praktyczny przewodnik po wzorcach budowania agentow AI">
  <style>
{css}
  </style>
</head>
<body>

  <!-- Embedded slide data (for file:// protocol support) -->
  <script type="application/json" id="embedded-slides-data">
{slides_json}
  </script>

  <!-- Progress bar -->
  <div class="progress-bar" id="progress-bar" style="width: 0%"></div>

  <!-- Navigation bar -->
  <nav class="nav-bar">
    <div class="nav-left">
      <span class="nav-title">Architektury Agent&oacute;w AI</span>
      <span class="nav-badge">Bielik Nest Builders</span>
    </div>
    <div class="nav-center">
      <button class="nav-btn" onclick="prevSlide()" title="Previous slide">&#8592;</button>
      <span class="nav-counter" id="slide-counter"><span class="current">1</span> / 11</span>
      <button class="nav-btn" onclick="nextSlide()" title="Next slide">&#8594;</button>
    </div>
    <div class="nav-right">
      <span class="nav-shortcut"><kbd>&larr;</kbd> <kbd>&rarr;</kbd> navigate</span>
      <span class="nav-shortcut"><kbd>F</kbd> fullscreen</span>
      <span class="nav-shortcut"><kbd>O</kbd> overview</span>
      <span class="nav-shortcut"><kbd>S</kbd> notes</span>
    </div>
  </nav>

  <!-- Slide viewport -->
  <div class="slide-viewport">
    <div class="slide-container loading" id="slide-container">
      <div class="slide-content">
        <p>Loading...</p>
      </div>
    </div>
  </div>

  <!-- Fragment progress dots -->
  <div class="fragment-indicator" id="fragment-indicator">
    <div id="fragment-dots"></div>
  </div>

  <!-- Speaker notes panel -->
  <div class="speaker-notes" id="speaker-notes">
    <div id="speaker-notes-content"></div>
  </div>

  <!-- Go-to overlay -->
  <div class="goto-overlay" id="goto-overlay">
    <div class="goto-box">
      <h3>Go to slide</h3>
      <input type="number" class="goto-input" id="goto-input" min="1" max="11" placeholder="1&ndash;11">
      <p style="margin-top:12px;color:var(--text-muted);font-size:13px;">Press Enter to go, Escape to cancel</p>
    </div>
  </div>

  <!-- Overview overlay -->
  <div class="overview-overlay" id="overview-overlay">
    <div class="overview-grid" id="overview-grid"></div>
  </div>

  <script>
{notes}
  </script>
  <script>
{js}
  </script>
</body>
</html>'''

    output_path = os.path.join(DIRECTORY, 'presentation.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Built: {output_path} ({size_kb:.1f} KB)")
    print("Open this file directly in a browser — no server needed.")


if __name__ == '__main__':
    build()
