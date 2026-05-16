# CallWhisper-8k

Reproducible benchmark and inference pipeline for 8 kHz telephony-style ASR, focused on Hindi and Indian narrowband speech.

## Results Snapshot

First smoke-test benchmark on 10 Gramvaani GV Dev files. This is not a final result yet.

| Model | Dataset Slice | Condition | WER | CER |
|---|---|---|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | telephone_mp3 | 0.8109 | 0.4963 |

## Problem

Whisper expects 16 kHz audio, while telephone audio is commonly narrowband 8 kHz. Feeding telephony audio incorrectly or assuming preprocessing helps can produce misleading results. This project measures Whisper behavior on real 8 kHz Hindi audio where possible, then compares it with synthetic telephony degradation on cleaner speech.

## What This Project Shows

- Baseline WER/CER for Whisper on narrowband or telephony-style Hindi speech.
- Whether simple telephony preprocessing changes WER/CER on the chosen slice.
- Controlled adaptation experiments, only after a working baseline exists.
- A reproducible CLI/API artifact rather than a fine-tuning-first claim.

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
- Common Voice synthetic telephony experiments are useful controls, not evidence of real telephone performance.
- This project reports slice-specific WER/CER deltas. It does not claim to fix Whisper for telephony.

## Future Work

See [FUTURE_WORK.md](FUTURE_WORK.md). New ideas go there unless they directly support the current weekly deliverable.
