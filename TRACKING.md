# CallWhisper-8k Tracking

## Current Week

Week: 1
Tag target: v0.1-baseline
This week's non-negotiable deliverable: first WER/CER benchmark on a small real or fallback synthetic audio slice.

## Daily Log

### 2026-05-14

- Planned: Scaffold the repository and define the smallest reproducible Week 1 eval path.
- Done:
- Blocked:
- Next action: Download or prepare a tiny 10-file evaluation slice and run Whisper `tiny` through the eval harness.

### 2026-05-16

- Planned: Run first tiny benchmark on Gramvaani GV Dev 5h.
- Done: Created `datasets/manifests/gramvaani_dev_10.csv`, ran Whisper `tiny`, `base`, and `small`, and saved baseline result files.
- Blocked: None.
- Next action: Expand the slice or start Week 2 preprocessing ablations using `small` as the local reference model.

## Scoreboard

- Day-2 WER number shipped: yes
- Baseline table shipped: yes
- Preprocessing ablation shipped: no
- LoRA smoke test run: no
- Week-3 kill gate obeyed: no
- v1.0 shipped: no

## Cut List Temptations

- Custom dashboard -> moved to FUTURE_WORK.md? yes
