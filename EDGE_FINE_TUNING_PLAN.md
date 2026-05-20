# Edge Fine-Tuning Plan

This is the ambitious track for CallWhisper-8k.

The benchmark track asks:

> How do Whisper-family and Hindi-tuned ASR models behave on clean Hindi, real telephone-style Hindi, preprocessing variants, decoding variants, and source-rate splits?

The edge fine-tuning track asks:

> Can a compact Whisper model be adapted for Indian telephone-style Hindi strongly enough to be useful for edge or low-resource deployment?

This track is allowed to be ambitious. It must still preserve honest evaluation.

## Target

The goal is not to claim a new best Hindi ASR model.

The goal is to build and evaluate the strongest compact Hindi telephony ASR model we can, then compare it honestly against:

- vanilla Whisper `small`
- vanilla Whisper `medium`
- vanilla Whisper `large-v3`
- `ARTPARK-IISc/whisper-medium-vaani-hindi`
- FLEURS clean-control results
- GramVaani mixed / 8 kHz / high-rate splits

Best possible story:

> A small adapted model approaches or beats larger vanilla Whisper models on Indian telephone-style Hindi while keeping lower size/latency.

## Success Levels

| Level | Result | Meaning |
|---|---|---|
| 1 | LoRA fine-tuning runs end to end and produces a checkpoint | training pipeline works |
| 2 | adapted `tiny` or `base` beats vanilla model of same size | domain adaptation signal exists |
| 3 | adapted `small` beats vanilla Whisper `large-v3` on GramVaani | strong compact-domain result |
| 4 | adapted `small` approaches ARTPARK medium on GramVaani | credible edge ASR story |
| 5 | adapted `small` beats ARTPARK medium on true 8 kHz subset | stretch result, not assumed |

Any level is useful if reported honestly.

## Non-Negotiable Evaluation Rules

- Do not train on `datasets/manifests/gramvaani_dev_50.csv`.
- Do not train on `datasets/manifests/gramvaani_dev_50_8khz.csv`.
- Do not train on `datasets/manifests/gramvaani_dev_50_highrate.csv`.
- Keep those manifests frozen as held-out tests.
- Use GramVaani train data for serious training, ideally `GV_Train_100h`.
- A smoke test may use `GV_Dev_5h` minus held-out IDs, but it cannot be reported as a final model result.
- Always evaluate the adapted model on:
  - GramVaani mixed 50
  - GramVaani 8 kHz subset
  - GramVaani high-rate subset
  - FLEURS clean Hindi 50

## First Experiment

Start with LoRA on Whisper `small`.

Why LoRA first:

- cheaper than full fine-tuning
- faster to debug
- less VRAM pressure
- good first signal for whether adaptation helps

Recommended first run:

| Setting | Value |
|---|---|
| Base model | `openai/whisper-small` |
| Method | LoRA |
| Train data | GramVaani train subset, 1-5 hours first |
| Eval data | frozen fixed manifests |
| Metric | WER/CER |
| Kaggle save path | `/kaggle/working/checkpoints/whisper-small-lora-gramvaani-*` |

Kaggle upload layout:

```text
/kaggle/input/<dataset-name>/
  GV_Dev_5h/
    Audio/*.mp3
    text
    mp3.scp
    uttids
    utt2labels
  GV_Train_100h/        # recommended for serious training
    Audio/*.mp3
    text
    mp3.scp
    uttids
    utt2labels
```

`notebooks/05_whisper_small_lora_edge_smoke.ipynb` is Kaggle-first. It symlinks uploaded data into the cloned repo, excludes frozen benchmark IDs from training, saves adapters under `/kaggle/working/checkpoints/`, and writes frozen-manifest JSON/Markdown results under `/kaggle/working/results/`.

If `GV_Train_100h` is not uploaded as a Kaggle input, the notebook can download `GV_Train_100h.tar.gz` directly from OpenSLR into `/kaggle/working/data` when Kaggle internet is enabled. Uploading it once as a Kaggle Dataset is still preferable for repeat runs.

## Comparison Table To Produce

| Model | Size Class | GramVaani Mixed WER | GramVaani 8 kHz WER | FLEURS WER | Notes |
|---|---|---:|---:|---:|---|
| Whisper small | small | 0.8697 | TBD | TBD | vanilla |
| Whisper large-v3 | large | 0.5616 | 0.6511 | 0.3112 | vanilla |
| ARTPARK medium Vaani Hindi | medium | 0.2597 | 0.2900 | 0.1326 | public Hindi-tuned |
| Our Whisper-small LoRA | small | TBD | TBD | TBD | edge-adapted |

## Risks

- Data leakage can create fake wins.
- GramVaani transcript noise can confuse training and evaluation.
- A model can improve on GramVaani while getting worse on clean Hindi.
- LoRA may not outperform a strong public Hindi model.
- A small model may still be too weak for noisy/unclear telephone speech.

None of these risks are reasons not to try. They are reasons to measure carefully.

## Reporting Language

Correct:

> Our Whisper-small LoRA improved over vanilla Whisper-small on the fixed GramVaani slice, but did not beat ARTPARK.

Correct:

> Our adapted compact model traded some clean Hindi performance for better telephone-style Hindi performance.

Incorrect:

> We built the best Hindi ASR model.

Incorrect:

> We fixed Whisper for telephony.
