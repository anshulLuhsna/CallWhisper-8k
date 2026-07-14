# CallWhisper-8k

Reproducible benchmark and inference pipeline for 8 kHz telephony-style ASR, focused on Hindi and Indian narrowband speech.

## Results Snapshot

CallWhisper-8k currently has three result tracks:

1. fixed-slice benchmarking of Whisper-family and Hindi-tuned ASR models,
2. preprocessing and decoding ablations,
3. compact Whisper-small LoRA adaptation for edge-oriented Hindi telephony ASR.

The current research direction is now more specific than another WER table or generic fine-tune: [`TELEPHONY_TAX_RESEARCH_PLAN.md`](TELEPHONY_TAX_RESEARCH_PLAN.md) defines a paired, multi-reference study of Hindi ASR under narrowband codecs, followed by a compact mitigation model evaluated against ARTPARK under a frozen win condition.

The expanded GPU benchmark evaluates the same 100 GramVaani files with every model and reports the native 8 kHz and higher-rate subsets separately:

| Model | Mixed 100 WER | Native 8 kHz WER | High-rate WER |
|---|---:|---:|---:|
| Whisper medium | 0.7182 | 0.7889 | 0.6281 |
| Whisper large-v3 | 0.5182 | 0.6083 | 0.4036 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | **0.2565** | **0.3091** | **0.1895** |

See [results/model_comparison_v2.md](results/model_comparison_v2.md). On this fixed slice, ARTPARK had the lowest WER/CER on all three views. Every model performed worse on the native 8 kHz subset than on the higher-rate subset, but source rate is not the only difference between those groups.

That caveat is now measured across all 1,885 local GramVaani dev clips. Dataset-provided gender has Cramer's V `0.543` with source-rate group: `76.3%` of male-labeled clips are native 8 kHz versus `18.1%` of female-labeled clips, an odds ratio of `14.59`. Inaudibility flags are also concentrated in the native-8-kHz group. See [results/gramvaani_source_rate_confound_audit_v1.md](results/gramvaani_source_rate_confound_audit_v1.md). The natural source-rate split is a deployment view, not a causal channel experiment.

The strongest new adaptation result is the Kaggle LoRA pilot:

| Experiment | Slice | Beams | WER Before | WER After | Change |
|---|---|---:|---:|---:|---:|
| HF Whisper-small -> Whisper-small LoRA | gramvaani_dev_50 | 5 | 1.0303 | 0.7532 | -0.2771 |
| HF Whisper-small -> Whisper-small LoRA | gramvaani_dev_50_8khz | 5 | 1.1595 | 0.8946 | -0.2649 |
| HF Whisper-small -> Whisper-small LoRA | gramvaani_dev_50_highrate | 5 | 0.8006 | 0.5018 | -0.2988 |

This is a same-pipeline base-vs-LoRA comparison from [results/lora_pilot_v1.md](results/lora_pilot_v1.md). It shows a real adaptation signal, but it is not a claim that the adapter beats the strongest Hindi-tuned public models.

Baseline benchmarks on Gramvaani GV Dev telephone-style Hindi speech:

| Model | Dataset Slice | Condition | WER | CER |
|---|---|---|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | telephone_mp3 | 0.8109 | 0.4963 |
| Whisper small | gramvaani_dev_50 | telephone_mp3 | 0.8434 | 0.5598 |
| Whisper small | gramvaani_dev_50 | mono_16khz_wav | 0.8327 | 0.5240 |
| Whisper small | gramvaani_dev_50 | volume_normalized_wav | 0.8223 | 0.5087 |
| Whisper small | gramvaani_dev_50 | telephone_bandpass_wav | 0.8452 | 0.5709 |
| Whisper small | gramvaani_dev_50 | roundtrip_8k_wav | 0.8468 | 0.5457 |
| Whisper medium | gramvaani_dev_50 | telephone_mp3 | 0.7683 | 0.4860 |
| Whisper large-v3 | gramvaani_dev_50 | telephone_mp3 | 0.5616 | 0.3057 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_50 | telephone_mp3 | 0.2597 | 0.1298 |

Sample-rate split for the same Whisper `small` raw MP3 run:

| Dataset Slice | Files | Source Sample Rate | WER | CER |
|---|---:|---|---:|---:|
| gramvaani_dev_50_8khz | 32 | 8 kHz | 0.9239 | 0.6528 |
| gramvaani_dev_50_highrate | 18 | 44.1/48 kHz | 0.7003 | 0.3946 |

This split is a benchmark quality check, not a final causal claim. The 8 kHz subset is harder on this slice, but transcript quality, speakers, topics, and noise may also differ.

The earlier 50-file GPU comparison remains in [results/model_comparison_v1.md](results/model_comparison_v1.md). The 100-file v2 table above is the current headline comparison. Both are fixed-slice benchmark results, not global ASR model rankings.

Decoding adaptation on Whisper `large-v3`:

| Experiment | Slice | WER | CER |
|---|---|---:|---:|
| baseline manifest hint | gramvaani_dev_50 | 0.5616 | 0.3057 |
| beam size 5 | gramvaani_dev_50 | 0.5248 | 0.2861 |
| auto language detection | gramvaani_dev_50 | 0.6685 | 0.4654 |

See [results/adaptation_v1.md](results/adaptation_v1.md). On this slice, beam search helped, while prompt biasing and auto language detection hurt.

Clean Hindi control:

| Model | FLEURS Clean WER | GramVaani Mixed WER | GramVaani 8 kHz WER |
|---|---:|---:|---:|
| Whisper medium | 0.4363 | 0.7683 | 0.8108 |
| Whisper large-v3 | 0.3112 | 0.5616 | 0.6511 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | 0.1326 | 0.2597 | 0.2900 |

See [results/clean_control_v1.md](results/clean_control_v1.md). FLEURS and GramVaani differ in channel and domain, so this is a practical clean-control comparison rather than a claim about channel alone.

Whisper-small LoRA pilot on Kaggle:

| Slice | Beams | Base HF Whisper-small WER | LoRA Whisper-small WER | Delta |
|---|---:|---:|---:|---:|
| gramvaani_dev_50 | 5 | 1.0303 | 0.7532 | -0.2771 |
| gramvaani_dev_50_8khz | 5 | 1.1595 | 0.8946 | -0.2649 |
| gramvaani_dev_50_highrate | 5 | 0.8006 | 0.5018 | -0.2988 |

See [results/lora_pilot_v1.md](results/lora_pilot_v1.md). This is a same-pipeline base-vs-LoRA comparison, not a claim that the adapter beats the strongest Hindi-tuned public models.

Committed adapter reload evaluation on Colab:

| Slice | Beams | Base HF Whisper-small WER | LoRA Whisper-small WER | Delta |
|---|---:|---:|---:|---:|
| gramvaani_dev_50 | 1 | 1.5187 | 0.7473 | -0.7714 |
| gramvaani_dev_50 | 5 | 1.0292 | 0.7532 | -0.2760 |
| gramvaani_dev_50_8khz | 1 | 1.7725 | 0.8708 | -0.9016 |
| gramvaani_dev_50_8khz | 5 | 1.1579 | 0.8946 | -0.2633 |
| gramvaani_dev_50_highrate | 1 | 1.0675 | 0.5277 | -0.5398 |
| gramvaani_dev_50_highrate | 5 | 0.8006 | 0.5018 | -0.2988 |
| fleurs_hi_clean_50 | 1 | 0.7686 | 0.5236 | -0.2450 |
| fleurs_hi_clean_50 | 5 | 0.5667 | 0.5128 | -0.0539 |

See [results/lora_reload_eval_colab_v1.md](results/lora_reload_eval_colab_v1.md). This verifies that the committed adapter reloads and improves over base HF Whisper-small on the fixed GramVaani slices and the small FLEURS clean-control slice.

First diagnostic benchmark flags beyond WER/CER:

| Model | Slice | Beams | Hallucination Risk Rate | Repetition Rate |
|---|---|---:|---:|---:|
| HF Whisper-small base | gramvaani_dev_50 | 1 | 0.3200 | 0.3200 |
| HF Whisper-small base | gramvaani_dev_50_8khz | 1 | 0.3125 | 0.3125 |
| HF Whisper-small LoRA | gramvaani_dev_50 | 1 | 0.0800 | 0.0800 |
| HF Whisper-small LoRA | gramvaani_dev_50_8khz | 1 | 0.1250 | 0.1250 |

See [results/benchmark_diagnostics_v1.md](results/benchmark_diagnostics_v1.md). These are heuristic flags for repetition loops, length explosions, script drift, and near-empty outputs; they are meant to complement WER/CER, not replace them.

Expanded 100-file diagnostics:

| Model | Slice | Hallucination Risk Rate | Empty/Near-Empty Rate |
|---|---|---:|---:|
| ARTPARK Vaani Hindi | gramvaani_dev_100_8khz | 0.0000 | 0.0000 |
| Whisper large-v3 | gramvaani_dev_100_8khz | 0.0000 | 0.0179 |
| Whisper medium | gramvaani_dev_100_8khz | 0.0000 | 0.0893 |

See [results/benchmark_diagnostics_v2.md](results/benchmark_diagnostics_v2.md). These heuristic rates do not mean ARTPARK made no transcription errors; its native-8-kHz WER was `0.3091`. In per-file comparison, ARTPARK had lower WER than large-v3 on 53 of 56 native-8-kHz files, tied on 2, and had higher WER on 1. The 15 highest-ARTPARK-WER files are prepared in [results/artpark_8khz_error_review_v1.md](results/artpark_8khz_error_review_v1.md) for human listening.

That listening review is now complete. Of the 15 deliberately difficult files, 6 were classified primarily as bad audio, 5 as model failures, 2 as questionable references, 1 as mixed, and 1 as uncertain. Four references were marked wrong or incomplete, with one more uncertain. See [results/artpark_8khz_manual_review_summary_v1.md](results/artpark_8khz_manual_review_summary_v1.md). These selected-tail counts diagnose error types; they are not estimates for the full benchmark.

## Problem

Whisper expects 16 kHz audio, while telephone audio is commonly narrowband 8 kHz. Feeding telephony audio incorrectly or assuming preprocessing helps can produce misleading results. This project measures Whisper behavior on real 8 kHz Hindi audio where possible, then compares it with synthetic telephony degradation on cleaner speech.

## What This Project Shows

- Baseline WER/CER for Whisper on narrowband or telephony-style Hindi speech.
- Whether simple telephony preprocessing changes WER/CER on the chosen slice.
- Controlled adaptation experiments, only after a working baseline exists.
- A reproducible CLI/API artifact rather than a fine-tuning-first claim.
- An ambitious compact-model adaptation track for edge Hindi telephony ASR, kept separate from the benchmark results until it is evaluated honestly.
- A broader benchmark direction beyond WER/CER: channel robustness, transcript trust, hallucination/repetition flags, entity preservation, and deployability tradeoffs for Indian telephony ASR.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The Week 1 target command is:

```bash
python -m callwhisper.eval --manifest datasets/manifests/example.csv --model tiny
```

For GPU model comparison, use the Colab notebooks in [notebooks](notebooks/README.md).

For the compact fine-tuning direction, see [EDGE_FINE_TUNING_PLAN.md](EDGE_FINE_TUNING_PLAN.md).

For the expanded benchmark scope before the next fine-tuning push, see [BENCHMARK_EXPANSION_PLAN.md](BENCHMARK_EXPANSION_PLAN.md).

For the current article-level thesis, paired benchmark protocol, predeclared ARTPARK win condition, and compact-model plan, see [TELEPHONY_TAX_RESEARCH_PLAN.md](TELEPHONY_TAX_RESEARCH_PLAN.md).

For the current expanded diagnostics and human-review queue, see [results/benchmark_diagnostics_v2.md](results/benchmark_diagnostics_v2.md) and [results/artpark_8khz_error_review_v1.md](results/artpark_8khz_error_review_v1.md).

For a first public update draft about the benchmark track, see [SOCIAL_POST_01_BENCHMARK.md](SOCIAL_POST_01_BENCHMARK.md).

For the posting checklist, platform-specific launch copy, and visual asset, see [SOCIAL_POSTING_CHECKLIST.md](SOCIAL_POSTING_CHECKLIST.md), [SOCIAL_LAUNCH_PACKET.md](SOCIAL_LAUNCH_PACKET.md), [social_assets/benchmark_part1_card.png](social_assets/benchmark_part1_card.png), and [social_assets/benchmark_part1_card.svg](social_assets/benchmark_part1_card.svg).

For the ARTPARK/Vaani competitive analysis and the next "beat ARTPARK honestly" experiment plan, see [ARTPARK_COMPETITIVE_ANALYSIS.md](ARTPARK_COMPETITIVE_ANALYSIS.md).

The manual-review-informed training recipe is in [TARGETED_8KHZ_CHALLENGER_PLAN.md](TARGETED_8KHZ_CHALLENGER_PLAN.md).

The next executable benchmark step is `notebooks/11_vaani_paired_telephony_benchmark_colab.ipynb`, which is specified in the research plan and still needs to be built. It will pin Vaani Benchmark V1.0, create a deterministic 500-file pilot, and generate validated paired channel manifests before model evaluation. The existing [notebooks/10_gv_train_100h_inventory_colab.ipynb](notebooks/10_gv_train_100h_inventory_colab.ipynb) remains the later training-data inventory step.

The first non-ARTPARK challenger notebook is [notebooks/07_whisper_large_v3_challenger.ipynb](notebooks/07_whisper_large_v3_challenger.ipynb).

The first compact adapter artifact is committed under:

```text
models/whisper-small-lora-gramvaani-pilot-seed0/
```

That directory contains:

```text
final_adapter/   # LoRA adapter weights and config
processor/       # Whisper processor/tokenizer files used with the adapter
```

Detailed pilot outputs are under:

```text
results/lora_pilot_seed0/
results/lora_pilot_v1.md
```

To reload the committed adapter and re-run the same-pipeline base-vs-LoRA eval:

```bash
pip install -e ".[finetune]"

callwhisper-lora-eval \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --manifest datasets/manifests/gramvaani_dev_50_8khz.csv \
  --manifest datasets/manifests/gramvaani_dev_50_highrate.csv \
  --adapter-dir models/whisper-small-lora-gramvaani-pilot-seed0/final_adapter \
  --processor-dir models/whisper-small-lora-gramvaani-pilot-seed0/processor \
  --output-dir results/lora_reload_eval
```

Use a GPU runtime for this command when possible. CPU evaluation will work, but it will be slow.

## Datasets And Licenses

Raw audio is not committed to this repository. Dataset download scripts and manifests should reproduce slices locally.

- OpenSLR SLR103 / MUCS Hindi: real 8 kHz Hindi speech anchor. Use for the first narrowband benchmark if it downloads cleanly.
- Gramvaani GV Dev 5h: real spontaneous telephone-style Hindi speech used for the first smoke-test baseline. Academic use is free; commercial use requires permission from Gram Vaani.
- Mozilla Common Voice Hindi: clean Hindi speech candidate for synthetic telephony degradation.
- MUSAN: optional noise source for Week 2 SNR-controlled overlays.

See [datasets/README.md](datasets/README.md) for links, license notes, and current v1.0 dataset decisions.

## Evaluation Methodology

Each manifest row points to one local audio file and one reference transcript. The eval runner transcribes each file with Whisper, normalizes reference and hypothesis text, then computes WER and CER.

Manifest columns:

```csv
audio_path,reference_text,slice,condition,language
data/slr103/hindi/test/audio.wav,नमस्ते दुनिया,slr103_hindi_test,raw_8khz,hi
```

## Limitations

- SLR103 is real 8 kHz Hindi speech, but it is not the same as natural call-center dialogue.
- Gramvaani GV Dev is real telephone-style Hindi, but the current slice mixes 8 kHz, 44.1 kHz, and 48 kHz source files.
- The initial sample-rate split shows higher error on the 8 kHz subset, but this should not be attributed to sample rate alone without manual audio review and a clean Hindi control.
- Some Gramvaani references contain transcript-quality markers such as `<incomplete>`.
- Common Voice synthetic telephony experiments are useful controls, not evidence of real telephone performance.
- FLEURS Hindi is clean read speech, while GramVaani is spontaneous telephone-style speech. The clean-control comparison should not be treated as a pure channel-only ablation.
- The LoRA pilot should be interpreted as a same-pipeline comparison against HF Whisper-small. It should not be directly compared against earlier OpenAI Whisper CLI numbers without rerunning those baselines in the same HF evaluation path.
- The LoRA adapter improved over base HF Whisper-small on the small FLEURS clean-control slice, but that does not prove broad clean-speech robustness.
- This project reports slice-specific WER/CER deltas. It does not claim to fix Whisper for telephony.

## Future Work

See [FUTURE_WORK.md](FUTURE_WORK.md). New ideas go there unless they directly support the current weekly deliverable.
