# CallWhisper-8k Tracking

## Current Week

Week: 3 adaptation
Tag target: v0.2-preprocessing, then v0.3-adapted
This week's non-negotiable deliverable: complete model comparison and non-training adaptation results, then add clean Hindi control.

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
- Done: Confirmed prior work partially overlaps; updated project direction toward a reproducible telephony ASR benchmark with preprocessing, clean controls, model comparisons, and optional LoRA as final stretch. Clarified that MacBook is for local iteration only and Colab/GPU should be used for stronger models and adaptation.
- Blocked: Clean Hindi control data is not downloaded/prepared yet; manual listening review still needs human judgement.
- Next action: Write `results/manual_audio_review_v1.md`, then prepare a Colab/GPU benchmark plan for Whisper medium and one Hindi-tuned model.

### 2026-05-18 follow-up

- Planned: Fix the mixed-source-rate blind spot in the current 50-file GramVaani slice.
- Done: Added a reproducible sample-rate split tool, generated `gramvaani_dev_50_8khz.csv` and `gramvaani_dev_50_highrate.csv`, and wrote `results/sample_rate_split_v1.md`. Current raw Whisper `small` result splits into 32 true 8 kHz files at WER 0.9239 / CER 0.6528 and 18 high-rate files at WER 0.7003 / CER 0.3946. Also added `COLAB_BENCHMARK_PLAN.md` and a Hugging Face ASR runner for GPU comparison with Hindi-tuned models.
- Blocked: Manual listening still requires human audio review; clean Hindi control data still not prepared.
- Next action: Complete human listening notes in `results/manual_audio_review_v1.md`, then add a clean Hindi control slice.

### 2026-05-19

- Planned: Bring Colab/GPU model comparison and cheap adaptation results back into the repo.
- Done: Added `results/model_comparison_v1.md` showing Whisper `medium`, Whisper `large-v3`, and `ARTPARK-IISc/whisper-medium-vaani-hindi` on the fixed GramVaani 50-file slice and sample-rate splits. Added `results/adaptation_v1.md` showing Whisper `large-v3` decoding sweeps; `beam_size=5` improved WER from 0.5616 to 0.5248, while prompt biasing and auto language detection hurt.
- Blocked: Clean Hindi control slice still missing.
- Next action: Add 10-50 clean Hindi clips from FLEURS, Common Voice Hindi, or Kathbath and run the same baseline table.

## Scoreboard

- Day-2 WER number shipped: yes
- Baseline table shipped: yes
- Preprocessing ablation shipped: yes
- LoRA smoke test run: no
- Week-3 kill gate obeyed: yes, non-training adaptation was run before LoRA
- v1.0 shipped: no

## Cut List Temptations

- Custom dashboard -> moved to FUTURE_WORK.md? yes
- Full Whisper fine-tuning before benchmark quality checks -> moved to final stretch only? yes
- Claiming novelty as first Whisper-on-GramVaani project -> forbidden after prior-art review? yes
- Optimizing only for Whisper small because it runs locally -> forbidden after Colab/GPU access confirmed? yes
