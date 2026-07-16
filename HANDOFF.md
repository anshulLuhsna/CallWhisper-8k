# CallWhisper-8k Handoff

This file is the working handoff for the next session. Read this before coding.

## One-Line Project Goal

CallWhisper-8k is becoming an open paired benchmark for the Hindi "telephony tax": how narrowband channels change ASR accuracy and group disparities when the same utterance, speaker, and references are held fixed, plus a compact mitigation model evaluated against ARTPARK.

## Updated Positioning

Do not claim this project is the first to use Whisper or Whisper-derived models on Hindi or GramVaani.

Prior work already includes:

- GramVaani / SLR118 Hindi telephone ASR challenge.
- IndicWhisper / Vistaar evaluations on GramVaani.
- Hindi Whisper fine-tunes from Vasista, ARTPARK-IISc, Collabora, and others.
- Production-style Indian call-center Whisper efforts from companies.

The useful remaining gap is narrower than the older positioning below:

> A clean, open, reproducible benchmark that studies Whisper/Indic ASR on Indian telephone-style Hindi under controlled preprocessing conditions, with fixed manifests, WER/CER, error analysis, and later multi-model comparison.

Best public framing:

> CallWhisper-8k is an open evaluation harness for Indian telephone-style ASR. It compares Whisper-family and Indic ASR models on fixed Hindi telephony slices and measures whether preprocessing choices such as WAV conversion, volume normalization, bandpass filtering, and 8 kHz roundtrip help or hurt.

Current primary thesis:

> Build a paired, multi-reference Hindi benchmark from Vaani Benchmark V1.0, apply predeclared telephone channels to the same utterances, measure channel-by-gender/region interactions, validate on real GramVaani telephone speech, and train a compact channel-adapted Whisper-small under a frozen ARTPARK win condition.

See `TELEPHONY_TAX_RESEARCH_PLAN.md`.

## Current State — 2026-07-14

- The current headline benchmark is the fixed 100-file GramVaani slice, with 56 native 8 kHz files and 44 higher-rate files.
- Whisper medium, Whisper large-v3, and ARTPARK Vaani Hindi were evaluated on the same 100 predictions using a Tesla T4.
- Mixed-slice WER: medium `0.7182`, large-v3 `0.5182`, ARTPARK `0.2565`.
- Native-8-kHz WER: medium `0.7889`, large-v3 `0.6083`, ARTPARK `0.3091`.
- The clean FLEURS Hindi control, manual 15-file audio review, decoding adaptation sweep, Whisper-small LoRA pilot, and committed-adapter reload evaluation are complete.
- Canonical v2 reports are `results/model_comparison_v2.md`, `.json`, and `.csv`; per-sample outputs and runtime metadata are under `results/benchmark_v2/`.
- Automated v2 diagnostics and an ARTPARK-vs-large-v3 15-file review queue are complete. ARTPARK had lower per-file WER on 53 of 56 native-8-kHz files, tied on 2, and higher WER on 1.
- The v2 human review is complete. Among the 15 highest-WER ARTPARK native-8-kHz files, 6 were classified as bad audio, 5 as model failures, 2 as questionable references, 1 as mixed, and 1 as uncertain. See `results/artpark_8khz_manual_review_summary_v1.md`.
- The full 1,885-file metadata audit is complete. Dataset-provided gender is strongly associated with source-rate group (Cramer's V `0.543`): `76.3%` of male-labeled clips are native 8 kHz versus `18.1%` of female-labeled clips. The male-versus-female native-rate odds ratio is `14.59`; inaudibility flags are also concentrated in the native-8-kHz group.
- Result: the existing native-8-kHz/high-rate WER gap is an observational deployment comparison, not a causal bandwidth estimate.
- Notebook 11's v1 run produced 500 speakers and 2,500 complete mono 16 kHz files with no duration or missing-file violations.
- Manual listening caught that the v1 codec-only conditions sounded closer to original than the explicit bandlimit. No model inference had started. The canonical transform now applies 300-3400 Hz bandlimiting before A-law, mu-law, and GSM-FR.
- Vaani paired pilot v2 is complete and frozen: 500 speaker-unique source utterances, 2,500 complete paired files, mono 16 kHz output, no missing files, no duration violations, and a passed manual listening check. See `results/vaani_paired_pilot_v2_validation.md`.
- The Vaani alignment-based multi-reference scorer is implemented and covered by toy cases for accepted alternatives, universal substitutions, insertions, and unanimous deletions.
- Next: run `notebooks/12_vaani_paired_artpark_adalat_smoke_colab.ipynb` on a T4. It evaluates 10 speakers across five conditions and two pinned models, checkpoints every prediction, and stops before the full run.

## What Has Been Built

Core eval:

- `src/callwhisper/eval/loader.py`: CSV manifest loader.
- `src/callwhisper/eval/runner.py`: Whisper runner with WER/CER output.
- `src/callwhisper/eval/wer.py`: WER wrapper.
- `src/callwhisper/eval/cer.py`: CER wrapper.
- `src/callwhisper/eval/normalizer.py`: conservative text normalization.

Dataset tooling:

- `src/callwhisper/datasets/build_gramvaani_manifest.py`: builds GramVaani manifests from `mp3.scp` and `text`.
- `src/callwhisper/datasets/metadata_audit.py`: quantifies source-rate associations with GramVaani gender, accent, state, and quality metadata.
- `src/callwhisper/datasets/paired_telephony.py`: deterministic speaker-stratified pilot selection, codec round trips, hashing, and audio validation for the paired benchmark.
- `datasets/manifests/gramvaani_dev_10.csv`: first smoke-test manifest.
- `datasets/manifests/gramvaani_dev_50.csv`: original fixed smoke benchmark slice.
- `datasets/manifests/gramvaani_dev_100.csv`: expanded fixed benchmark slice.
- `datasets/manifests/gramvaani_dev_100_8khz.csv`: 56-file native 8 kHz subset.
- `datasets/manifests/gramvaani_dev_100_highrate.csv`: 44-file higher-rate subset.

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

Expanded GPU comparison on the fixed GramVaani 100-file slice:

| Model | Mixed 100 WER | Native 8 kHz WER | High-rate WER |
|---|---:|---:|---:|
| Whisper medium | 0.7182 | 0.7889 | 0.6281 |
| Whisper large-v3 | 0.5182 | 0.6083 | 0.4036 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | 0.2565 | 0.3091 | 0.1895 |

These are fixed-slice results, not global model rankings. The source-rate split is observational and does not isolate sample rate from content, speaker, noise, or transcript differences.

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

- The headline 100-file slice is still small and comes from one GramVaani development set.
- The 100-file slice mixes source rates; the 56/44 split describes model behavior but does not isolate sample rate causally.
- The full-dev metadata audit proves the source-rate groups differ strongly in gender composition and quality flags.
- Some references contain `<incomplete>` markers.
- GramVaani transcripts are crowd-sourced and may be imperfect.
- FLEURS provides a clean Hindi control, but dataset/domain differences prevent a pure channel-only claim.
- ARTPARK is covered; broader non-Whisper Indic ASR coverage is still missing.
- Current preprocessing gains are small; do not overclaim them.
- Vaani Benchmark V1.0 Hub and paper releases currently report different row/hour totals; every run must pin and record the exact dataset revision.

See:

```text
results/error_analysis_v1.md
prior_art.md
```

## Next Session Priorities

1. Freeze model/dataset revisions, transform parameters, macro-region mapping, group-size threshold, and multi-reference scoring protocol.
2. Run notebook 12 with its default `smoke` profile on a T4.
3. Review its 100 predictions, completeness, scorer counts, and pooled-telephone table before changing the profile to `full`.
4. Run the full baseline before training. Then run notebook 10 and curate `GV_Train_100h` for the compact challenger.

## Completed Historical Priorities

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
