# AGENTS.md — CallWhisper-8k AI Context

This file is for AI coding agents working on **CallWhisper-8k**.

Read this before writing code. The goal is to preserve the decision made by the council and prevent scope creep.

---

## What This Project Is

**CallWhisper-8k** is a 4-week flagship Voice AI project.

It is a reproducible benchmark and inference system for **8 kHz telephony-style ASR**, especially Hindi / Indian / Hindi-English code-switching speech.

The project investigates how Whisper behaves on narrowband telephone-style audio and whether preprocessing or lightweight adaptation can improve or better characterize transcription performance.

The project is **not** primarily a fine-tuned model project.

The correct framing is:

> CallWhisper-8k is a reproducible ASR benchmark and deployable inference pipeline for 8 kHz Indian/telephony-style speech, using real narrowband Hindi data where available and synthetic telephony degradation where necessary.

The final repo should prove:

- Anshul can build real Voice AI systems
- Anshul understands ASR evaluation, WER/CER, telephony audio constraints, and dataset limitations
- Anshul can ship a clean benchmark + CLI + FastAPI + Docker artifact
- Anshul can be honest about limitations instead of overclaiming

---

## Who This Is For

The project is built by Anshul, a final-year computer engineering student in Pune, India.

Current strengths:

- STT/TTS pipeline integration
- Voice agent workflows
- FastAPI
- Docker
- Cloud deployment
- GCP / Azure / Vertex AI
- Voice RAG systems

Current gaps this project should build:

- WER/CER evaluation
- Dataset handling for speech tasks
- Telephony audio processing
- Whisper inference behavior under degraded audio
- Basic ML adaptation / fine-tuning exposure
- Honest benchmark reporting

Career goal:

- Become employable as a strong Voice AI engineer
- Build one serious flagship GitHub repo
- Become credible to Indian Voice AI / AI startups such as SarvamAI, Krutrim, Gnani, Skit, Slang Labs, etc.

---

## The Locked Decision

The council selected:

**Path 2 — Locked Operator roadmap: A -> D -> Adaptation -> C**

Meaning:

1. **Week 1:** Evaluation baseline
2. **Week 2:** Telephony preprocessing
3. **Week 3:** Gated adaptation experiments
4. **Week 4:** Productization: CLI, FastAPI, Docker, simple demo, final README

Do not reinterpret the project as:

- fine-tuning-first
- API-wrapper-first
- research-paper-first
- dashboard-first
- real-time streaming product
- full ASR training project

The project must ship in 4 weeks.

---

## Core Product Promise

The final repo should let someone run commands like:

```bash
callwhisper bench --config configs/full.yaml
```

and regenerate benchmark results such as:

| Model | Dataset Slice | Condition | WER | CER |
|---|---|---|---:|---:|
| Whisper tiny | SLR103 | raw 8 kHz | ... | ... |
| Whisper tiny | SLR103 | preprocessed | ... | ... |
| Whisper small | synthetic telephony | raw | ... | ... |
| Whisper small | synthetic telephony | preprocessed | ... | ... |

The repo should also expose:

- CLI benchmark runner
- FastAPI transcription/evaluation API
- Docker setup
- simple Streamlit or static demo
- results files in Markdown + JSON
- honest limitations

---

## What We Are Looking For

The project should answer these questions:

1. How does Whisper perform on 8 kHz / narrowband / telephony-style speech?
2. Does telephony degradation measurably affect WER/CER?
3. Do preprocessing steps help, hurt, or do nothing?
4. Can adaptation strategies improve or characterize performance?
5. Can this be packaged as a clean, reproducible Voice AI engineering artifact?

Good answers are measured, not claimed.

Correct language:

> On this dataset slice, preprocessing method X changed WER from A to B.

Incorrect language:

> This fixes Whisper for telephony.

---

## Research Required First

Before building too much, research and validate the dataset path.

Primary research questions:

- Which datasets are actually usable for v1.0?
- Which datasets are 8 kHz or narrowband?
- Which datasets have transcripts?
- Which datasets allow public GitHub use?
- Which datasets can be downloaded/scripted without payment or manual approval?
- Which datasets are Hindi, Indian English, or Hindi-English code-switching?
- Which datasets must not be redistributed?

Expected starting candidates:

### 1. OpenSLR SLR103 — Hindi 8 kHz / MUCS

Use as the main real narrowband Hindi anchor if it loads cleanly.

Notes:

- 8 kHz Hindi data
- useful for real narrowband behavior
- not perfect call-center speech
- likely read/story speech, not natural customer-support dialogue
- do not bundle raw audio in repo
- provide download script and license notes

### 2. MUCS Hindi-English Code-Switching Release

Investigate early.

Use only if it loads cleanly within 1-2 evenings.

Notes:

- potentially more relevant to Hindi-English code-switching
- do not let this delay Week 1 baseline
- if unclear or slow, move it to future work

### 3. Common Voice Hindi

Use as clean 16 kHz speech for synthetic telephony degradation.

Notes:

- CC0
- good for reproducible experiments
- can be degraded to 8 kHz telephony-style audio
- not real telephony

### 4. MUSAN

Use for noise overlays.

Notes:

- CC BY 4.0
- useful for SNR-controlled noise augmentation
- do not overcomplicate noise profiles

### 5. NOIZEUS

Optional only.

Use as a tiny clean/noisy enhancement-eval reference if easy.

Do not depend on it.

### Commercial datasets to avoid

Do not build v1.0 around paid/commercial/contact-us datasets:

- Shaip Hinglish call-center datasets
- Defined.ai Hindi call-center datasets
- AxonData contact-center datasets
- Macgence commercial Hinglish call-center data
- FutureBee commercial call-center data

These may be mentioned in research notes, but they cannot be project dependencies.

---

## Dataset Strategy

Use a two-layer benchmark:

### Layer A — Real Narrowband

Use a real 8 kHz / narrowband dataset such as OpenSLR SLR103.

Purpose:

- test real low-bandwidth behavior
- create credible baseline WER/CER
- avoid relying only on synthetic degradation

### Layer B — Synthetic Telephony

Take clean speech such as Common Voice Hindi and simulate telephony conditions.

Transforms:

- resample / downsample to 8 kHz
- upsample back to 16 kHz before Whisper inference
- apply telephony bandpass / IRS-like filter
- µ-law / A-law encode/decode
- MUSAN noise overlay at controlled SNRs
- optional VAD/chunking

Important Whisper rule:

Whisper expects 16 kHz input. Do not feed 8 kHz audio as if it were 16 kHz. Simulate telephony damage at 8 kHz, then resample back to 16 kHz for Whisper.

---

## Metrics

Required:

- WER
- CER

Nice to have:

- per-condition WER delta
- per-sample error analysis
- entity error notes for names, numbers, phone numbers if easy
- short vs long clip comparison if available

Avoid:

- vendor-style "accuracy" unless clearly defined
- comparing directly against unrelated public benchmarks as if they are equivalent
- claiming state-of-the-art

Use careful language:

- absolute WER/CER per slice
- delta from baseline per condition
- limitations clearly stated

---

## Week-by-Week Implementation Rules

### Week 1 — Baseline + Eval Harness

Must ship:

- dataset notes
- first manifest
- Whisper inference
- WER/CER computation
- baseline result table

Hard gate:

- by end of Day 2, produce one `wer()` number on real audio

If this does not happen, stop everything and debug minimal eval only.

### Week 2 — Telephony Preprocessing

Must ship:

- `audio/telephony.py`
- codec simulation
- resampling pipeline
- noise overlay
- VAD/chunking if easy
- ablation table

Rule:

- every preprocessing step must be measured against Week 1 baseline

### Week 3 — Adaptation Experiments

Week 3 is **not LoRA week**. It is adaptation week.

Allowed:

- LoRA only if Week 2 smoke test succeeds
- initial prompt biasing
- beam-size sweep
- temperature sweep
- condition-on-previous-text toggle
- chunk-length sweep
- lightweight rescoring only if trivial

Kill gate:

- Wednesday 10 PM
- if LoRA does not train and evaluate cleanly, kill it and switch to non-training adaptation

### Week 4 — Productize + Polish

Must ship:

- FastAPI
- Dockerfile
- docker-compose
- CLI benchmark command
- simple Streamlit or static demo
- final README
- architecture diagram
- 60-second demo video link
- final results files

Do not build custom frontend.

---

## Hard Cut List

Forbidden before v1.0:

- Whisper large / large-v3
- custom React / Next.js dashboard
- auth
- users
- multi-tenant API
- cloud deployment
- real-time streaming
- diarization
- WhisperX
- faster-whisper / CTranslate2 conversion
- second language beyond Hindi + Hindi-English code-switching
- training Whisper-medium or large
- custom KenLM training from scratch
- more than two core dataset slices
- blog post series
- refactoring Week 1 eval code during Week 3 or Week 4

If tempted, create or update `FUTURE_WORK.md`.

---

## Required Repo Structure

Recommended structure:

```text
callwhisper-8k/
  README.md
  LICENSE
  pyproject.toml
  Dockerfile
  docker-compose.yml
  configs/
    full.yaml
  datasets/
    README.md
    manifests/
  results/
    baseline_v1.md
    baseline_v1.json
    preprocessing_v1.md
    preprocessing_v1.json
    adaptation_v1.md
    adaptation_v1.json
  src/
    callwhisper/
      eval/
        loader.py
        normalizer.py
        wer.py
        cer.py
        runner.py
      datasets/
        download_slr103.py
        build_manifest.py
      audio/
        telephony.py
        noise.py
        vad.py
      adaptation/
        decoding.py
        lora_train.py
      api/
        main.py
  bench/
    cli.py
  examples/
  app.py
  FUTURE_WORK.md
  TRACKING.md
```

---

## README Requirements

The README must lead with results.

Recommended order:

1. `# CallWhisper-8k`
2. one-line elevator
3. results snapshot table
4. problem: why 8 kHz telephony ASR is hard
5. what this project shows
6. quickstart
7. architecture
8. datasets and licenses
9. evaluation methodology
10. results
11. preprocessing ablations
12. adaptation experiments
13. CLI usage
14. API usage
15. demo
16. limitations
17. future work
18. what I learned
19. license and citations

README must include:

- dataset limitations
- license notes
- how to reproduce results
- exact commands
- WER/CER tables
- what did not work
- what was intentionally excluded

---

## What Makes This Impressive

This project is impressive if it has:

- real WER/CER tables
- credible dataset notes
- reproducible benchmark command
- clear audio preprocessing pipeline
- ablation results
- honest adaptation experiments
- FastAPI and Docker as packaging, not the core trick
- limitations section
- clean final README

This project is not impressive if it has:

- a huge README with weak code
- a Whisper wrapper with no WER/CER
- "fine-tuned Whisper" claims with no baseline
- no dataset license explanation
- no reproducible command
- custom UI while eval is unfinished
- vague claims like "improved accuracy"

---

## Behavioral Rules For AI Agents

When helping Anshul build this project:

- Prefer the smallest correct implementation.
- Do not add features outside the roadmap.
- If a new idea appears, add it to `FUTURE_WORK.md`.
- Keep the benchmark reproducible.
- Do not hide limitations.
- Do not overclaim results.
- Do not turn this into an orchestration framework.
- Do not build a custom dashboard.
- Do not add cloud deployment before v1.0.
- Always ask: does this help Week 1/2/3/4 deliverable ship?

---

## First Tasks For A Coding Agent

If starting from zero, do these in order:

1. Create repo skeleton.
2. Add `TRACKING.md` and `FUTURE_WORK.md`.
3. Write `datasets/README.md` with candidate datasets and licenses.
4. Implement a tiny manifest format.
5. Run Whisper on 10 files.
6. Compute one WER number.
7. Save result to Markdown and JSON.
8. Only then improve structure.

Do not start with FastAPI.
Do not start with LoRA.
Do not start with a dashboard.

---

## Non-Negotiable Gates

| Gate | Required Evidence |
|---|---|
| Day 2 Week 1 | one WER number on real audio |
| End Week 1 | baseline WER/CER table |
| End Week 2 | preprocessing ablation table |
| End Week 2 | hello-LoRA smoke test result |
| Wednesday Week 3 | explicit LoRA continue/kill decision |
| End Week 3 | adaptation result file |
| End Week 4 | v1.0 repo with CLI/API/Docker/README/results |

If a gate fails, follow the fallback in `ROADMAP.md`.

---

## Source Documents

For the full council history, read:

- `context.md`
- `discussion.md`
- `synthesizer.md`
- `ROADMAP.md`
- `summary.html`

`ROADMAP.md` is the execution source of truth.
`synthesizer.md` is the decision source of truth.
