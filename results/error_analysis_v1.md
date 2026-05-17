# Error Analysis v1

This note reviews blind spots in the current CallWhisper-8k benchmark after the first baseline and preprocessing runs.

## Summary

- The 50-file Gramvaani slice is useful, but not clean enough to treat as a final benchmark.
- The slice mixes source sample rates: 32 files at 8 kHz, 16 files at 44.1 kHz, and 2 files at 48 kHz.
- Some references contain transcript-quality markers such as `<incomplete>`.
- Volume normalization is the best preprocessing method so far, but the gain is small.
- Auto language detection slightly improved WER on the 10-file slice, but worsened CER.

## Audio Slice Checks

| Check | Result |
|---|---:|
| Files | 50 |
| 8 kHz source files | 32 |
| 44.1 kHz source files | 16 |
| 48 kHz source files | 2 |
| Min duration | 1.90 s |
| Max duration | 17.57 s |
| Avg duration | 9.40 s |

Blind spot: we currently call the whole slice `telephone_mp3`, but not every source file is actually 8 kHz. Future tables should either report this mix clearly or split results by source sample rate.

## Transcript Quality Flags

These files contain explicit incomplete markers and should be reviewed before being used for strong claims:

| File | Issue |
|---|---|
| `13-00240-05` | Reference starts with `<incomplete>` |
| `01-02976-02` | Reference ends with `<incomplete>` |
| `02-19469-01` | Reference ends with `<incomplete>` |
| `01-05816-03` | Reference ends with `<incomplete>` |

Blind spot: if the reference transcript is incomplete, WER/CER can punish Whisper for words that are actually present in the audio but missing from the reference.

## Language Mode Check

Small 10-file comparison using Whisper `small` with seed `0`:

| Language Mode | Files | WER | CER |
|---|---:|---:|---:|
| Manifest Hindi hint | 10 | 0.8278 | 0.4906 |
| Auto-detect | 10 | 0.8001 | 0.5544 |

Interpretation: auto-detect slightly improved WER but worsened CER. This is not enough evidence to switch defaults, but it should be included as a Week 3 decoding/adaptation test.

## Preprocessing Behavior

The strongest preprocessing result so far is volume normalization:

| Condition | Files | WER | CER |
|---|---:|---:|---:|
| Raw MP3 | 50 | 0.8434 | 0.5598 |
| Volume normalized WAV | 50 | 0.8223 | 0.5087 |

Interpretation: normalization helped, but the change is modest. Do not claim that preprocessing solves telephony ASR.

## Helpful Example

`02-12557-02` improved strongly after normalization.

| Field | Text |
|---|---|
| Reference | शीशे की बोतल यूज़ करिये और थर्मस यूज़ करिये दोस्तों ऐसे में यह होगा कि हमारा जो वायु प्रदूषित है हमारे पर्यावरण |
| Raw hypothesis | एक स्यषokol refreshing are bhatal and thinnes floating on a... |
| Normalized hypothesis | खेशे की बोथल यूज करयें और खर्मस यूज करयें दोस्टा... |

Interpretation: normalization reduced mixed-script hallucination and moved output closer to Hindi/Devanagari.

## Regression Example

`02-19188-01` got worse after normalization.

| Field | Text |
|---|---|
| Reference | श्रोताओं मोबाईल वाणी के बेहद लोकप्रिय और खास कार्यक्रम खबरें ज़रा हटके में आपका स्वागत है... |
| Raw WER | 0.568 |
| Normalized WER | 0.676 |

Interpretation: normalization is not universally helpful. It can change decoding behavior in both directions.

## Manual Listening Needed

I cannot reliably judge audio quality by ear from the terminal alone. These files should be manually listened to before final claims:

| Purpose | Files |
|---|---|
| Worst raw WER | `02-12557-02`, `02-19849-01`, `01-06773-03`, `01-02976-02`, `01-00748-01` |
| Best normalization improvements | `02-12557-02`, `01-01598-02`, `02-19469-01`, `02-19849-01`, `01-02689-01` |
| Normalization regressions | `02-19188-01`, `01-02494-03`, `01-08315-03`, `01-05855-03`, `01-08138-03` |
| Transcript marker review | `13-00240-05`, `01-02976-02`, `02-19469-01`, `01-05816-03` |

Review questions:

- Is the speech understandable to a human?
- Is the reference transcript complete?
- Is there background noise, music, echo, or multiple speakers?
- Does Whisper fail because of audio quality or because the reference is questionable?

## Clean Control Gap

We still need a clean Hindi control slice, such as 10-50 files from Common Voice Hindi.

Why it matters:

- Without clean Hindi results, we cannot separate general Hindi ASR weakness from telephone-audio weakness.
- The current Gramvaani result should be described as real telephone-style performance, not as a complete Hindi ASR benchmark.

Next control experiment:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.eval \
  --manifest datasets/manifests/common_voice_hi_clean_10.csv \
  --model small \
  --language-mode manifest \
  --seed 0 \
  --output-json results/control_common_voice_small_10_v0.json
```

This is blocked until a clean Common Voice Hindi manifest exists locally.
