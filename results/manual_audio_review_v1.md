# Manual Audio Review v1

Status: pending human listening.

This file tracks the manual listening review requested by `results/error_analysis_v1.md`. Do not mark a row as reviewed unless the audio has actually been heard by a human reviewer.

## Review Questions

- Is the speech understandable to a human?
- Is there background noise, music, echo, clipping, or multiple speakers?
- Does the reference transcript look complete?
- Did Whisper fail mainly because of audio quality, transcript quality, or model behavior?

## Priority Files

| File | Why Review | Raw WER | Raw CER | Normalized WER | Normalized CER | Listening Notes |
|---|---|---:|---:|---:|---:|---|
| `02-12557-02` | normalization helped a lot; mixed-script hallucination in raw output | 1.273 | 1.171 | 0.727 | 0.315 | pending |
| `02-19188-01` | normalization regression | 0.568 | 0.254 | 0.676 | 0.321 | pending |
| `13-00240-05` | reference starts with `<incomplete>` | 0.458 | 0.190 | 0.458 | 0.190 | pending |
| `01-02976-02` | reference ends with `<incomplete>`; high raw error | 1.000 | 0.904 | 1.000 | 0.592 | pending |
| `02-19849-01` | high WER short utterance | 1.167 | 0.765 | 1.000 | 0.676 | pending |

## Additional Flagged Files

| File | Why Review | Raw WER | Raw CER | Normalized WER | Normalized CER | Listening Notes |
|---|---|---:|---:|---:|---:|---|
| `01-06773-03` | worst raw WER; very short utterance | 1.000 | 0.684 | 1.000 | 0.684 | pending |
| `01-00748-01` | worst raw WER | 1.000 | 0.936 | 0.960 | 0.624 | pending |
| `01-01598-02` | normalization improvement | 0.964 | 0.761 | 0.714 | 0.384 | pending |
| `02-19469-01` | normalization improvement; reference ends with `<incomplete>` | 1.000 | 0.563 | 0.750 | 0.418 | pending |
| `01-02689-01` | normalization improvement; short utterance | 1.000 | 0.750 | 0.857 | 0.750 | pending |
| `01-02494-03` | normalization regression by WER | 0.909 | 0.738 | 1.000 | 0.639 | pending |
| `01-08315-03` | normalization regression by WER but CER improved | 0.500 | 0.207 | 0.571 | 0.159 | pending |
| `01-05855-03` | normalization regression | 0.862 | 0.437 | 0.931 | 0.459 | pending |
| `01-08138-03` | normalization regression | 0.800 | 0.453 | 0.867 | 0.473 | pending |
| `01-05816-03` | reference ends with `<incomplete>` | 1.000 | 0.653 | 0.909 | 0.628 | pending |

## Audio Paths

Raw audio lives under:

```text
datasets/GV_Dev_5h/Audio/
```

Generated normalized audio lives under:

```text
results/raw/audio/gramvaani_dev_50_normalize/
```
