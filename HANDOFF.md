# CallWhisper-8k Handoff

This file is the working handoff for the next session. Read this before coding.

## One-Line Project Goal

CallWhisper-8k is becoming a reproducible benchmark suite for Indian telephone-style Hindi ASR, focused on Whisper-family and Indic ASR models, telephony preprocessing, WER/CER, and honest error analysis.

## Updated Positioning

Do not claim this project is the first to use Whisper or Whisper-derived models on Hindi or GramVaani.

Prior work already includes:

- GramVaani / SLR118 Hindi telephone ASR challenge.
- IndicWhisper / Vistaar evaluations on GramVaani.
- Hindi Whisper fine-tunes from Vasista, ARTPARK-IISc, Collabora, and others.
- Production-style Indian call-center Whisper efforts from companies.

The useful remaining gap is narrower:

> A clean, open, reproducible benchmark that studies Whisper/Indic ASR on Indian telephone-style Hindi under controlled preprocessing conditions, with fixed manifests, WER/CER, error analysis, and later multi-model comparison.

Best public framing:

> CallWhisper-8k is an open evaluation harness for Indian telephone-style ASR. It compares Whisper-family and Indic ASR models on fixed Hindi telephony slices and measures whether preprocessing choices such as WAV conversion, volume normalization, bandpass filtering, and 8 kHz roundtrip help or hurt.

## What Has Been Built

Core eval:

- `src/callwhisper/eval/loader.py`: CSV manifest loader.
- `src/callwhisper/eval/runner.py`: Whisper runner with WER/CER output.
- `src/callwhisper/eval/wer.py`: WER wrapper.
- `src/callwhisper/eval/cer.py`: CER wrapper.
- `src/callwhisper/eval/normalizer.py`: conservative text normalization.

Dataset tooling:

- `src/callwhisper/datasets/build_gramvaani_manifest.py`: builds GramVaani manifests from `mp3.scp` and `text`.
- `datasets/manifests/gramvaani_dev_10.csv`: first smoke-test manifest.
- `datasets/manifests/gramvaani_dev_50.csv`: current fixed benchmark slice.

Audio preprocessing:

- `src/callwhisper/audio/telephony.py`: single-file preprocessing methods.
- `src/callwhisper/audio/preprocess_manifest.py`: batch preprocessing from a manifest.

Current preprocessing methods:

- `whisper_wav`: mono 16 kHz WAV conversion.
- `normalize`: loudness normalization + mono 16 kHz WAV.
- `bandpass`: telephone-style bandpass + mono 16 kHz WAV.
- `roundtrip_8k`: 8 kHz downsample then 16 kHz upsample.

Eval runner improvements:

- Added `--language-mode` with `manifest`, `auto`, and `hi`.
- Added `--seed` for more reproducible decoding.

## Current Data Location

Raw local data is under:

```text
datasets/GV_Dev_5h/
datasets/Metadata/
```

These folders are ignored by git. Do not commit raw audio.

Generated processed audio is under:

```text
results/raw/audio/
```

This is also ignored by git. Do not commit generated WAVs.

## Current Benchmark Results

Baseline on GramVaani GV Dev:

| Model | Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_10 | raw MP3 | 10 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | raw MP3 | 10 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | raw MP3 | 10 | 0.8109 | 0.4963 |
| Whisper small | gramvaani_dev_50 | raw MP3 | 50 | 0.8434 | 0.5598 |

Preprocessing on GramVaani 50 files with Whisper `small`:

| Condition | WER | CER | Meaning |
|---|---:|---:|---|
| raw MP3 | 0.8434 | 0.5598 | baseline |
| mono 16 kHz WAV | 0.8327 | 0.5240 | helped slightly |
| volume normalized WAV | 0.8223 | 0.5087 | best so far |
| telephone bandpass WAV | 0.8452 | 0.5709 | worse |
| 8 kHz roundtrip WAV | 0.8468 | 0.5457 | WER worse, CER better |

Language-mode check on 10 files with Whisper `small`, seed `0`:

| Language Mode | WER | CER |
|---|---:|---:|
| manifest Hindi hint | 0.8278 | 0.4906 |
| auto-detect | 0.8001 | 0.5544 |

Interpretation: auto language detection slightly improves WER but worsens CER. Keep `manifest` as default for now.

Sample-rate split on the same 50-file raw MP3 Whisper `small` result:

| Slice | Files | Source Sample Rate | WER | CER |
|---|---:|---|---:|---:|
| gramvaani_dev_50_8khz | 32 | 8 kHz | 0.9239 | 0.6528 |
| gramvaani_dev_50_highrate | 18 | 44.1/48 kHz | 0.7003 | 0.3946 |

Interpretation: the true 8 kHz subset is harder on this slice, but do not attribute the gap to sample rate alone without manual listening and clean-control comparison.

## Compute Policy

Do not optimize the project around the MacBook.

Use the MacBook for:

- code edits,
- manifest building,
- quick 10/50-file smoke tests,
- debugging,
- result/documentation updates.

Use Colab/GPU for:

- Whisper `medium`, and possibly controlled `large-v3` checks,
- Hindi-tuned Whisper models,
- IndicWhisper / ARTPARK / Vasista / Collabora comparisons,
- larger fixed slices,
- LoRA or other domain-adaptation experiments.

Whisper `small` is the fast local reference model only. It is not the final target. Any preprocessing/adaptation finding discovered on `small` should later be verified on stronger or Hindi-tuned models before final claims.

## Known Blind Spots

These are important. Do not hide them.

- The 50-file slice mixes source sample rates: 32 files at 8 kHz, 16 files at 44.1 kHz, and 2 files at 48 kHz.
- Some references contain `<incomplete>` markers.
- GramVaani transcripts are crowd-sourced and may be imperfect.
- Current benchmark has no clean Hindi control set yet.
- Current benchmark has no IndicWhisper / ARTPARK / Vasista comparison yet.
- Current preprocessing gains are small; do not overclaim them.
- Manual listening has not yet been done.

See:

```text
results/error_analysis_v1.md
prior_art.md
```

## Next Session Priorities

### Priority 1: Manual Listening Review

Listen to flagged files from `results/error_analysis_v1.md`.

Start with:

- `02-12557-02`: normalization helped a lot.
- `02-19188-01`: normalization hurt.
- `13-00240-05`: reference starts with `<incomplete>`.
- `01-02976-02`: reference ends with `<incomplete>`.
- `02-19849-01`: high WER short utterance.

Write notes in:

```text
results/manual_audio_review_v1.md
```

For each file, answer:

- Is speech human-understandable?
- Is there background noise, music, echo, or multiple speakers?
- Does the reference text look complete?
- Did Whisper fail because of audio quality or transcript quality?

### Priority 2: Clean Hindi Control Slice

Add 10-50 clean Hindi clips from Common Voice Hindi, FLEURS Hindi, or Kathbath if access is easy.

Goal:

| Dataset | Purpose |
|---|---|
| Clean Hindi | baseline Hindi ASR difficulty |
| GramVaani telephone Hindi | telephony difficulty |

This lets us say how much worse phone-style audio is compared with clean Hindi.

Expected manifest:

```text
datasets/manifests/common_voice_hi_clean_10.csv
```

Expected command:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.eval \
  --manifest datasets/manifests/common_voice_hi_clean_10.csv \
  --model small \
  --language-mode manifest \
  --seed 0 \
  --output-json results/control_common_voice_small_10_v0.json
```

### Priority 3: Split GramVaani By Source Sample Rate

Create separate manifests:

```text
datasets/manifests/gramvaani_dev_50_8khz.csv
datasets/manifests/gramvaani_dev_50_highrate.csv
```

Then evaluate Whisper `small` on both. This fixes the current sample-rate blind spot.

Status: manifests now exist, and `results/sample_rate_split_v1.md` summarizes the existing raw Whisper `small` result by split. A fresh rerun is optional for verification because the split summary was computed from `results/baseline_small_50_v0.json`.

### Priority 4: Add One Strong Hindi-Tuned Model

After clean control and sample-rate split, compare against at least one Hindi-tuned model:

- ARTPARK-IISc Whisper Vaani Hindi, if easy.
- Vasista Hindi Whisper, if easy.
- IndicWhisper, if easy.

Do not spend more than one evening fighting model installation. If it is messy, document it as blocked and move on.

Because Colab/GPU is available, do not reject larger models just because the local MacBook is slow. Instead, prepare reproducible Colab commands/scripts and keep local runs for smoke tests.

### Priority 5: Week 3 Adaptation

Before LoRA, run cheap adaptation first:

- `--language-mode auto` vs `manifest` vs `hi`.
- Prompt biasing, if implemented.
- Beam size sweep.
- Temperature sweep.
- `condition_on_previous_text=False`.

LoRA is a final stretch goal only. Use GPU/Colab, not the MacBook.

Rules for LoRA:

- Do not train on the same 50 files used for testing.
- Use GramVaani train/dev split.
- Keep a held-out fixed test manifest.
- Frame it as “domain adaptation,” not a new best Hindi model.

## Commands To Remember

Run raw eval:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.eval \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --model small \
  --language-mode manifest \
  --seed 0 \
  --output-json results/baseline_small_50_seed0.json
```

Generate normalized audio:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.audio.preprocess_manifest \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --output-audio-dir results/raw/audio/gramvaani_dev_50_normalize \
  --output-manifest datasets/manifests/gramvaani_dev_50_normalize.csv \
  --method normalize
```

Run normalized eval:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.eval \
  --manifest datasets/manifests/gramvaani_dev_50_normalize.csv \
  --model small \
  --language-mode manifest \
  --seed 0 \
  --output-json results/preprocessing_normalize_small_50_seed0.json
```

## Git Status As Of This Handoff

Recent important commits:

- `b9435d7 Add benchmark blind spot analysis`
- `1445fa1 Complete preprocessing ablation table`
- `abcee3f Record bandpass preprocessing result`
- `b8cb377 Record volume normalization result`
- `051f41b Record first preprocessing result`
- `4a49adc Add manifest preprocessing workflow`

Commit regularly with human-readable messages.

## What Makes This Stand Out

This will stand out if it becomes:

- reproducible,
- honest about prior work,
- explicit about dataset/audio problems,
- model-comparative,
- telephony-specific,
- useful to other Voice AI engineers.

The best final output is not “I trained Whisper.”

The best final output is:

> “I built a rigorous, reproducible benchmark for Indian telephone-style ASR and used it to measure model choice, preprocessing, and adaptation under realistic constraints.”
