# CallWhisper-8k Tracking

## Current Week

Week: 2 complete / Week 3 prep
Tag target: v0.2-preprocessing, then v0.3-adapted
This week's non-negotiable deliverable: validate benchmark quality with manual listening, add clean Hindi control, then begin cheap adaptation experiments.

## Daily Log

### 2026-05-14

- Planned: Scaffold the repository and define the smallest reproducible Week 1 eval path.
- Done:
- Blocked:
- Next action: Download or prepare a tiny 10-file evaluation slice and run Whisper `tiny` through the eval harness.

### 2026-05-16

- Planned: Run first tiny benchmark on Gramvaani GV Dev 5h.
- Done: Created 10-file and 50-file Gramvaani manifests, ran Whisper `tiny`, `base`, and `small`, saved baseline/preprocessing result files, and wrote first error analysis.
- Blocked: None.
- Next action: Manually listen to flagged files and prepare a clean Hindi control slice.

### 2026-05-18

- Planned: Reposition project after prior-art review and prepare next-session handoff.
- Done: Confirmed prior work partially overlaps; updated project direction toward a reproducible telephony ASR benchmark with preprocessing, clean controls, model comparisons, and optional LoRA as final stretch.
- Blocked: Clean Hindi control data is not downloaded/prepared yet; manual listening review still needs human judgement.
- Next action: Write `results/manual_audio_review_v1.md` by listening to flagged files from `results/error_analysis_v1.md`.

## Scoreboard

- Day-2 WER number shipped: yes
- Baseline table shipped: yes
- Preprocessing ablation shipped: yes
- LoRA smoke test run: no
- Week-3 kill gate obeyed: no
- v1.0 shipped: no

## Cut List Temptations

- Custom dashboard -> moved to FUTURE_WORK.md? yes
- Full Whisper fine-tuning before benchmark quality checks -> moved to final stretch only? yes
- Claiming novelty as first Whisper-on-GramVaani project -> forbidden after prior-art review? yes
