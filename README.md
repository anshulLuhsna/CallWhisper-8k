# CallWhisper-8k

Reproducible benchmark and inference pipeline for 8 kHz telephony-style ASR, focused on Hindi and Indian narrowband speech.

## Results Snapshot

First baseline benchmarks on Gramvaani GV Dev telephone-style Hindi speech. These are early results, not final claims.

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

Colab/GPU model comparison:

| Model | Mixed 50 WER | 8 kHz WER | High-rate WER |
|---|---:|---:|---:|
| Whisper medium | 0.7683 | 0.8108 | 0.6584 |
| Whisper large-v3 | 0.5616 | 0.6511 | 0.3984 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | 0.2597 | 0.2900 | 0.2057 |

See [results/model_comparison_v1.md](results/model_comparison_v1.md). These are fixed-slice benchmark results, not global ASR model rankings.

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

## Problem

Whisper expects 16 kHz audio, while telephone audio is commonly narrowband 8 kHz. Feeding telephony audio incorrectly or assuming preprocessing helps can produce misleading results. This project measures Whisper behavior on real 8 kHz Hindi audio where possible, then compares it with synthetic telephony degradation on cleaner speech.

## What This Project Shows

- Baseline WER/CER for Whisper on narrowband or telephony-style Hindi speech.
- Whether simple telephony preprocessing changes WER/CER on the chosen slice.
- Controlled adaptation experiments, only after a working baseline exists.
- A reproducible CLI/API artifact rather than a fine-tuning-first claim.
- An ambitious compact-model adaptation track for edge Hindi telephony ASR, kept separate from the benchmark results until it is evaluated honestly.

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
- This project reports slice-specific WER/CER deltas. It does not claim to fix Whisper for telephony.

## Future Work

See [FUTURE_WORK.md](FUTURE_WORK.md). New ideas go there unless they directly support the current weekly deliverable.
