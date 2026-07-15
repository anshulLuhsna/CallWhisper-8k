# CallWhisper-8k Tracking

## Current Week

Week: benchmark expansion and error diagnostics
Tag target: v0.4-benchmark
This week's non-negotiable deliverable: validate the expanded 100-file comparison, then diagnose the strongest model's remaining native-8-kHz failures.

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

### 2026-05-20

- Planned: Add a clean Hindi control slice.
- Done: Created and evaluated a 50-file FLEURS Hindi clean-control slice. Added `results/clean_control_v1.md`: Whisper `large-v3` WER is 0.3112 on FLEURS clean Hindi versus 0.5616 on GramVaani mixed and 0.6511 on GramVaani 8 kHz; ARTPARK WER is 0.1326 on FLEURS versus 0.2597 on GramVaani mixed and 0.2900 on GramVaani 8 kHz.
- Blocked: Raw FLEURS clean-control JSON outputs are not yet copied into the local repo; current clean-control summary is based on the Colab table.
- Next action: Copy FLEURS JSON outputs into `results/results/` or `results/results/results/`, then begin Week 4 packaging: CLI polish, FastAPI, Docker, and final README.

### 2026-05-20 edge fine-tuning direction

- Planned: Capture the new ambition to fine-tune compact Whisper models for edge Hindi telephony ASR.
- Done: Added `EDGE_FINE_TUNING_PLAN.md` to define the compact adaptation track, success levels, leakage rules, and comparison targets. Added `notebooks/05_whisper_small_lora_edge_smoke.ipynb` as the first Whisper-small LoRA smoke-test notebook.
- Blocked: Full GramVaani training audio is not confirmed locally; serious fine-tuning should use `GV_Train_100h` or another train split, not the frozen held-out 50-file benchmark slice.
- Next action: Run the LoRA smoke notebook on Colab, confirm one adapter checkpoint can be saved to Drive, then switch the training source to real GramVaani train data.

### 2026-05-20 Kaggle LoRA pilot upgrade

- Planned: Make the Kaggle LoRA notebook a credible pilot experiment instead of only a smoke test.
- Done: Upgraded notebook 05 with `smoke` / `pilot` / `serious` run profiles, safe GramVaani archive download/copy/extract, dataset validation, 1-30 second duration filtering, saved train/internal-eval splits, saved run config and package versions, and same-pipeline base HF Whisper-small versus LoRA evaluation on frozen GramVaani manifests with both macro and corpus WER/CER.
- Blocked: Notebook has not yet been executed on Kaggle GPU.
- Next action: Run notebook 05 with default `RUN_PROFILE = "pilot"` on Kaggle, then copy the generated comparison Markdown/JSON back into `results/`.

### 2026-05-20 Kaggle split progress fix

- Planned: Make the deterministic split cell observable and faster on Kaggle.
- Done: Added progress bars for transcript/SCP indexing and `ffprobe` duration probing. Changed pilot/serious duration filtering to stop after enough valid clips plus a buffer instead of probing the full 100h corpus.
- Blocked: Not yet re-run on Kaggle after the notebook update.
- Next action: Re-run from the deterministic split cell; verify it reaches the training cell with `RUN_PROFILE = "pilot"`.

### 2026-05-20 Kaggle eval import hardening

- Planned: Make the frozen-manifest evaluation cell robust after long Kaggle runs or partial notebook reruns.
- Done: Added explicit imports for `csv`, `json`, `Path`, `torch`, and `WhisperForConditionalGeneration`; inserted the cloned repo `src` path before importing `callwhisper`; added local metric/normalization fallbacks if `callwhisper.eval.*` is not importable.
- Blocked: Not yet re-run on Kaggle after the notebook update.
- Next action: Re-run the eval cell after training finishes and confirm base-vs-LoRA JSON/Markdown files are written.

### 2026-05-21 LoRA pilot results

- Planned: Bring the Kaggle Whisper-small LoRA pilot outputs back into the repo.
- Done: Added the final LoRA adapter and processor under `models/whisper-small-lora-gramvaani-pilot-seed0/`, copied detailed run artifacts to `results/lora_pilot_seed0/`, and wrote `results/lora_pilot_v1.md`. Same-pipeline beam-5 WER improved from `1.0303` to `0.7532` on `gramvaani_dev_50`, from `1.1595` to `0.8946` on the 8 kHz subset, and from `0.8006` to `0.5018` on the high-rate subset.
- Done: Added `callwhisper-lora-eval`, a repo-native adapter reload/eval runner that evaluates base HF Whisper-small and the committed LoRA adapter on fixed manifests and writes per-sample JSON plus Markdown comparison tables.
- Done: Re-ran the committed adapter in Colab with `notebooks/06_lora_reload_eval_colab_report.ipynb`, including GramVaani fixed slices and the FLEURS clean-control slice. Added `results/lora_reload_eval_colab_v1.md` plus CSV exports under `results/lora_reload_eval_colab/`.
- Next action: Design the next ambitious experiment: LoRA-domain-adapt `ARTPARK-IISc/whisper-medium-vaani-hindi` on GramVaani Train 100h and evaluate against the public ARTPARK checkpoint on the same frozen slices.

### 2026-07-06 ARTPARK beat-plan refresh

- Planned: Research what ARTPARK/Vaani did, whether their Hindi Whisper model is fully open source, and what CallWhisper-8k would need to beat it honestly.
- Done: Corrected the beat-ARTPARK direction. Public ARTPARK is the opponent baseline, not the training base. The main challenger must not use ARTPARK weights.
- Done: Updated `ARTPARK_COMPETITIVE_ANALYSIS.md` to recommend an independent `openai/whisper-large-v3` LoRA challenger on `GV_Train_100h`, evaluated against public ARTPARK on frozen GramVaani 50/8 kHz/high-rate and FLEURS clean-control slices.
- Done: Replaced the derivative ARTPARK-LoRA notebook with `notebooks/07_whisper_large_v3_challenger.ipynb`, a Kaggle-first non-ARTPARK large-v3 LoRA notebook with leakage-safe split construction and public-ARTPARK-vs-independent-challenger evaluation.
- Blocked: No independent challenger training run has been started yet; this needs GPU time, ideally A100/L4/A10G rather than relying on a T4 for large-v3.
- Next action: Run notebook 07 with `RUN_PROFILE = "smoke"` first. If large-v3 OOMs on T4, move to a larger GPU rather than changing the win condition to ARTPARK fine-tuning.

### 2026-07-07 benchmark expansion refresh

- Planned: Re-scope the benchmark into something credible before the next fine-tuning/model push.
- Done: Added `BENCHMARK_EXPANSION_PLAN.md`, which reframes CallWhisper-8k as a deployment-oriented Indian telephony ASR benchmark rather than only a WER/CER table. The expanded scope now includes channel robustness, transcript trust, hallucination/repetition safety, entity/actionability metrics, and deployability tradeoffs.
- Done: Added `SOCIAL_POST_01_BENCHMARK.md` as a first public-update draft that can be posted before Part 2 fine-tuning.
- Done: Added `callwhisper-diagnostics` / `python -m callwhisper.eval.diagnostics`, then generated `results/benchmark_diagnostics_v1.md` and `.json` from existing per-sample predictions. The first diagnostics cover repetition flags, length-ratio outliers, script drift, empty-output flags, and slice-level diagnostic summaries.
- Next action: Extend diagnostics to ARTPARK and Whisper large-v3 per-sample outputs, then add entity/number preservation on a manually labeled subset.

### 2026-07-08 GramVaani 100 expansion

- Planned: Expand the fixed GramVaani benchmark slice beyond the original 50-file sample while keeping source-rate caveats explicit.
- Done: Built `datasets/manifests/gramvaani_dev_100.csv` and source-rate splits: `gramvaani_dev_100_8khz.csv` with 56 native 8 kHz files and `gramvaani_dev_100_highrate.csv` with 44 higher-rate files. Documented the slice in `results/benchmark_slice_v2.md`.
- Done: Added `COLAB_BENCHMARK_V2_RUNBOOK.md` so the 100-file mixed/8 kHz/high-rate slices can be evaluated on GPU with Whisper medium, Whisper large-v3, and ARTPARK Vaani Hindi using one reproducible Colab flow.
- Done: Ran local CPU Whisper tiny sanity checks on all three v2 manifests. Results are saved under `results/benchmark_v2/` and summarized in `results/local_tiny_sanity_v2.md`. These are wiring checks only, not headline benchmark claims.
- Blocked: Final model comparison still needs a GPU run using the v2 runbook.
- Next action: Run `COLAB_BENCHMARK_V2_RUNBOOK.md`, copy back `results/model_comparison_v2.md` and `.json`, then run diagnostics on the stronger model per-sample outputs.

### 2026-07-13 GramVaani 100 GPU comparison

- Planned: Run the expanded fixed benchmark on a hosted GPU and verify whether the original 50-file model ordering holds on a larger slice.
- Done: Evaluated Whisper `medium`, Whisper `large-v3`, and `ARTPARK-IISc/whisper-medium-vaani-hindi` on the same 100 GramVaani files using a Tesla T4. The source-rate views were derived from the same per-file predictions: 56 native 8 kHz files and 44 higher-rate files.
- Done: Added nine per-model/slice JSON outputs under `results/benchmark_v2/`, report tables in `results/model_comparison_v2.md`, `.json`, and `.csv`, and exact runtime metadata in `results/benchmark_v2/model_comparison_v2_run_metadata.json`.
- Result: On the mixed 100-file slice, WER was `0.7182` for Whisper medium, `0.5182` for Whisper large-v3, and `0.2565` for ARTPARK. On the native 8 kHz subset, WER was `0.7889`, `0.6083`, and `0.3091`, respectively.
- Done: Added JSON support to `callwhisper-diagnostics`, generated `results/benchmark_diagnostics_v2.md` and `.json`, and created a reproducible ARTPARK-vs-large-v3 error-review command and 15-file review sheet. ARTPARK had lower per-file WER on 53 of 56 native-8-kHz files, tied on 2, and had higher WER on 1.
- Caveat: The native 8 kHz subset is harder for all three models, but the split is observational; source rate, speakers, topics, noise, and transcript quality are not independently controlled.
- Next action: Complete the 15-file listening review in `results/artpark_8khz_error_review_v1.md`, then group genuine model failures into a targeted training-data plan.

### 2026-07-14 ARTPARK native-8-kHz manual review

- Done: Completed the 15-file human review of ARTPARK's highest-WER native-8-kHz cases and saved a structured parse to `results/artpark_8khz_manual_review_v1.json`.
- Result: 6 cases were classified as `bad_audio`, 5 as `model_failure`, 2 as `questionable_reference`, 1 as `mixed`, and 1 as `uncertain`. Four references were marked wrong or incomplete and one more uncertain.
- Interpretation: The review set is deliberately the worst-scoring tail, so the counts diagnose failure modes rather than estimate prevalence. Residual model themes include short function-word confusion, leading-phrase deletion, tail/span omission, and local-entity errors.
- Done: Added `results/artpark_8khz_manual_review_summary_v1.md` and `TARGETED_8KHZ_CHALLENGER_PLAN.md`.
- Done: Added `notebooks/10_gv_train_100h_inventory_colab.ipynb` and the tested `callwhisper-gramvaani-inventory` CLI. The CLI probes audio concurrently, preserves portable relative paths, records duration/sample rate/channels/transcript flags, and writes accepted/rejected inventories plus a JSON summary.
- Next action: Run notebook 10 on Colab CPU, inspect the saved inventory artifacts, then create deterministic curated train/internal-eval splits before the independent large-v3 LoRA smoke experiment.

### 2026-07-14 paired telephony research direction

- Planned: Find a defensible contribution beyond generic Hindi Whisper fine-tuning or another small WER table.
- Done: Re-audited recent primary work. Generic Hindi fine-tuning, Hindi codec ablations, broad Indian telephony benchmarking, and generic fairness-under-degradation are already covered by recent work including Vividh-ASR, Voice of India, Vaani Benchmark V1.0, Basu et al. (2026), Ginjala et al. (2026), and Altwlkany et al. (2025).
- Decision: The new thesis is a paired, multi-reference Hindi telephony audit plus compact mitigation model. The same Vaani utterances will be evaluated under original, bandwidth-only 8 kHz, G.711 A-law, G.711 mu-law, and GSM-FR conditions, followed by real GramVaani validation.
- Done: Added `TELEPHONY_TAX_RESEARCH_PLAN.md` with the novelty boundary, research questions, evaluation contract, data-leakage rules, model ablations, and a predeclared definition of beating ARTPARK.
- Done: Added tested `callwhisper-metadata-audit` tooling and generated `results/gramvaani_source_rate_confound_audit_v1.md`, `.json`, and `_rows.csv` across all 1,885 local GramVaani dev files.
- Finding: Dataset-provided gender and source-rate group have Cramer's V `0.543`. Native-8-kHz share is `76.3%` for male-labeled clips and `18.1%` for female-labeled clips; male-versus-female native-rate odds ratio is `14.59`. `inaudible` flags occur in 340 native-8-kHz clips versus 72 higher-rate clips.
- Interpretation: The old source-rate WER split is useful operationally but cannot identify the causal bandwidth penalty. The paired Vaani design exists to hold speaker, utterance, and references fixed.
- Done: Added `notebooks/11_vaani_paired_telephony_benchmark_colab.ipynb` and tested `paired_telephony.py` utilities. The CPU Colab run pins dataset revision `1bf019521d12d742178acc32bf2a42f81cf7c8ef`, selects one clip per speaker, generates five channel conditions, validates hashes/audio metadata, and checkpoints restartable archives to Drive.
- Next action: Accept Vaani access, add `HF_TOKEN` to Colab Secrets, run notebook 11, and bring its schema, pilot manifest, and validation summary back to the repo before model inference.

## Scoreboard

- Day-2 WER number shipped: yes
- Baseline table shipped: yes
- Preprocessing ablation shipped: yes
- LoRA smoke test run: yes
- Week-3 kill gate obeyed: yes, non-training adaptation was run before LoRA
- v1.0 shipped: no

## Cut List Temptations

- Custom dashboard -> moved to FUTURE_WORK.md? yes
- Full Whisper fine-tuning before benchmark quality checks -> moved to final stretch only? yes
- Claiming novelty as first Whisper-on-GramVaani project -> forbidden after prior-art review? yes
- Optimizing only for Whisper small because it runs locally -> forbidden after Colab/GPU access confirmed? yes
