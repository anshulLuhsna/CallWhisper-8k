# Datasets

This repository does not redistribute raw datasets. Keep downloaded audio under `data/`, which is ignored by git, and commit only scripts, manifests, documentation, and derived aggregate results.

## v1.0 Dataset Plan

| Dataset | Role | Status | License / Use Notes |
|---|---|---|---|
| OpenSLR SLR103 / MUCS Hindi | Primary real 8 kHz Hindi anchor | Investigate first | OpenSLR lists Hindi train/test speech and transcripts, with 8 kHz 16-bit audio. Follow the linked license terms and do not commit raw audio. |
| Mozilla Common Voice Hindi | Clean speech for synthetic telephony degradation | Fallback / comparison slice | Mozilla Data Collective lists Hindi Common Voice releases under CC0. Confirm release version in the manifest. |
| MUSAN | Week 2 noise overlays | Optional | Commonly documented as CC BY 4.0. Attribution is required if used. |
| NOIZEUS | Tiny enhancement reference | Optional only | Do not block Week 1 or Week 2 on this. |

## Required Manifest Columns

Use CSV for the initial harness:

```csv
audio_path,reference_text,slice,condition,language
data/slr103/hindi/test/example.wav,नमस्ते दुनिया,slr103_hindi_test,raw_8khz,hi
```

Column meanings:

- `audio_path`: local path to an audio file, relative to repo root or absolute.
- `reference_text`: ground-truth transcript.
- `slice`: stable name for the dataset subset, for example `slr103_hindi_test_10`.
- `condition`: audio condition, for example `raw_8khz`, `clean_16khz`, or `synthetic_telephony`.
- `language`: BCP-47-ish language hint such as `hi` or `hi-en`.

## Source Links

- OpenSLR SLR103: https://www.openslr.org/103/
- OpenSLR SLR103 files mirror index: https://us.openslr.org/resources/103/
- Common Voice Hindi dataset page: https://prod.datacollective.mozillafoundation.org/datasets/cmflnuzw5hbe47u0fvrugjyb6
- MUSAN overview: https://audeering.github.io/datasets/datasets/musan.html

## Immediate Week 1 Decision

Start with the smallest path to one WER number:

1. Try OpenSLR SLR103 Hindi test data first because it is already 8 kHz and includes transcripts.
2. Build a 10-file manifest slice.
3. If SLR103 download or parsing stalls, use a tiny Common Voice Hindi slice and record the fallback in `TRACKING.md`.
