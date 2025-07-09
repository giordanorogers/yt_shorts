# Project Requirement Document

---

## 1. Project Snapshot

| Field | Entry |
|-------|-------|
| Working title | YT-Long-to-Shorts-Agent |
| One-sentence pitch | "Paste a YouTube link → get five ready-to-post 60-sec vertical shorts." |
| Primary outcome | User pastes link in a local Streamlit UI → downloads 5× (60 s, 1080 × 1920 MP4 + hard-burned captions) files. |
| Deadline / time-box | 7 calendar days (start = T0). |

---

## 2. Problem & Goal

### Problem
Manual short-form repurposing of long videos is labor-intensive; creators waste hours clipping, captioning, and formatting.

### Goal / Success KPIs

| # | Metric | Target |
|---|--------|--------|
| 1 | Throughput (end-to-end time for 60-min source) | ≤ 15 min on M-series Mac (baseline) |
| 2 | Clip coherence (LLM rubric 0–1) | Mean ≥ 0.80 |
| 3 | User touchpoints | ≤ 2 clicks from link → download |

### Non-goals / Out-of-scope
- No in-app video preview or timeline editor.
- No licensing / copyright detection.
- Only English transcripts (ISO en).

---

## 3. Users & Value

| Persona | Pain | Value delivered |
|---------|------|-----------------|
| Hobbyist YouTuber | Needs shorts but lacks editing skills | One-click pipeline auto-generates high-engagement clips |
| Pro content team | Volume demands exceed editor bandwidth | Automates routine clipping, frees editors for creative work |

---

## 4. Solution Sketch

### Flow:
1. **UI trigger**: user enters YouTube URL, clicks "Generate".
2. **Download**: yt_dlp fetches MP4 + VTT captions (en). (`download.py`)
3. **Select segments**: GPT-4o ranks transcript blocks → 5×60-sec sets. (`select.py`)
4. **Splice video**: moviepy cuts & concatenates segments. (`edit.py`)
5. **Captions burn**: auto-generated SRT → styled ASS → ffmpeg burn. (`caption.py`)
6. **Export**: ffmpeg → H.264 + AAC MP4 1080×1920 9:16. (`export.py`)
7. **UI delivery**: Streamlit shows progress bar + download links. (`ui.py`)

### Key decisions / constraints
- **Framework**: OpenAI Agents SDK orchestrating Python modules.
- **Libraries**: yt_dlp, moviepy, ffmpeg-python, openai, no closed-source deps.
- **Runtime**: local; rely on installed ffmpeg binary.
- **Max source length**: 5 h.
- **Progress UX**: Streamlit st.progress + ETA.
- **Config surface**: dropdowns → clip length (30/60/90 s), font, colour preset.

---

## 5. Vertical-Slice Roadmap

| Slice | Demo goal (E2E) | Due | Notes |
|-------|-----------------|-----|-------|
| 1 | Download + raw clip list printed | T0 + 1 day | hard-coded timestamps |
| 2 | Full cut & caption on single segment | T0 + 3 days | CLI only |
| 3 | 5-clip pipeline + tests pass | T0 + 5 days | no UI |
| 4 | Streamlit UI + progress + downloads | T0 + 7 days | launch-ready |

---

## 6. AI Guardrails & Prompt Rules

1. **Prompt preamble** (insert in every coding task):
   > "You are writing production Python for the YT-Long-to-Shorts-Agent. Follow PEP8, snake_case funcs, PascalCase classes, no global state. Think step-by-step: propose 3 options, pick the best, then output code."

2. **Forbidden**: print debugging, hard-coded paths, non-deterministic randomness.

3. **Must**: log with logging module at INFO level to `logs/app.log`.

4. **API calls**: wrap OpenAI calls in `with_backoff_retry()` util.

5. **Clip-selection prompt template** (system + user):
   - **System**: "You are an expert shorts editor optimizing engagement…"
   - **User**: includes transcript, target audience, desired #clips=5, length=60 s.

---

## 7. Quality & Testing

| Test type | Tool | Mandatory for PR merge |
|-----------|------|------------------------|
| Unit | pytest | critical funcs (download, splice, burn) |
| Audio-video sync | FFprobe + custom check | yes |
| Caption timing | compare SRT vs subtitle stream pts | yes |
| Aspect ratio | FFprobe width:height == 9:16 | yes |
| LLM coherence | GPT-4o rubric score ≥ 0.8 | yes (fail if < 0.7) |

**CI**: GitHub Actions matrix (macOS, Ubuntu).

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| yt_dlp download blocked | Med | Pipeline halt | retry w/ proxy; surface UI error |
| GPT-4o token limit on 5 h video | Med | mis-selection | chunk transcript by chapters; iterative selection |
| FFmpeg caption burn failure | Low | unusable output | fallback to open-caption via Pillow |

---

## 9. Failure & Feedback Paths

- **Download fail / no captions / no engaging segments** → Streamlit `st.error()` with actionable message.
- **Intermediate logs** streamed to UI via `st.text_area` (auto-scroll).
- **Delete cache**: "🗑 Purge Assets" button removes video + captions from `downloads/` and `output/`.

---