# Targeted 8 kHz Challenger Plan

## Objective

Train an independent Hindi telephony ASR challenger without using ARTPARK weights, then compare it with public ARTPARK on the frozen CallWhisper-8k benchmark.

Primary stretch target:

> Beat ARTPARK's canonical WER of `0.3091` on the 56-file native-8-kHz GramVaani slice while keeping clean FLEURS Hindi regression within 5% relative.

The first success gate is more modest: improve the same-pipeline `openai/whisper-large-v3` native-8-kHz WER of `0.6083` by at least 20% relative, to `0.4866` or lower. The ARTPARK-beating gate is `0.2936` or lower for a 5% relative win.

## Model Decision

- Base: `openai/whisper-large-v3`
- Method: LoRA first; full fine-tuning only after a successful LoRA pilot
- Opponent baseline: `ARTPARK-IISc/whisper-medium-vaani-hindi`
- Training base must not use ARTPARK or other Vaani-Whisper weights
- Training source: `GV_Train_100h`, not `GV_Dev_5h`

This preserves a meaningful claim: the challenger is independently adapted from OpenAI Whisper weights.

## Frozen Evaluation Contract

Never train on any utterance ID present in:

- `datasets/manifests/gramvaani_dev_100.csv`
- `datasets/manifests/gramvaani_dev_100_8khz.csv`
- `datasets/manifests/gramvaani_dev_100_highrate.csv`
- the FLEURS clean-control manifest

Every run must evaluate the base and adapted model through the same code and decoding settings. Report macro and corpus WER/CER. Preserve the published-reference score even when a human-audited analysis is also reported.

## Step 1: Build A Training Inventory

Download or attach `GV_Train_100h` in the GPU environment. For every utterance, record:

- utterance ID and audio path;
- transcript;
- duration;
- source sample rate;
- clipping and silence ratios;
- transcript length;
- frozen-ID exclusion status.

Reject files that are missing, unreadable, shorter than 1 second, longer than 30 seconds, empty-transcript, or overlap with frozen evaluation IDs.

Output:

- `datasets/manifests/gv_train_100h_inventory.csv`
- `datasets/manifests/gv_train_100h_rejected.csv`
- a JSON summary with counts and hours by source sample rate

## Step 2: Build Quality And Target Strata

Create deterministic train/internal-eval manifests. The internal eval must use speakers or utterance IDs excluded from training.

Tag or sample these strata:

| Stratum | Purpose | Initial share |
|---|---|---:|
| Clear native 8 kHz | Core telephone Hindi recognition | 45% |
| Mildly distorted but understandable | Robustness without label corruption | 20% |
| Names, locations, institutions | Residual entity failures | 15% |
| Dates, counts, money, abbreviations | Semantically costly errors | 10% |
| Leading/trailing speech risk | Endpoint and span omissions | 10% |

The percentages are starting targets, not claims about the corpus. If metadata cannot identify a stratum reliably, create a reproducible candidate list and manually validate a small sample before training.

## Step 3: Three Gated Runs

### Wiring smoke

- 200 train clips
- 25 internal-eval clips
- 40 steps
- goal: verify dataset, LoRA, checkpoint saving, reload, and evaluation

### Data pilot

- 3,200 curated train clips
- 200 internal-eval clips
- 800 steps
- goal: demonstrate a reproducible improvement over base large-v3 on native 8 kHz

### Serious challenger

- 12,000-25,000 curated train clips
- 500-1,000 internal-eval clips
- 2,500-5,000 steps
- goal: approach or beat ARTPARK without clean-control collapse

Use early stopping or best-checkpoint selection based on internal-eval loss. The frozen benchmark is measured only after run settings are locked; it must not become the hyperparameter tuning set.

## Step 4: Evaluation Matrix

For each surviving checkpoint, produce:

| Model | Native 8 kHz | High-rate | Mixed 100 | FLEURS clean |
|---|---:|---:|---:|---:|
| Base large-v3 | fixed baseline | fixed baseline | fixed baseline | fixed baseline |
| Public ARTPARK | fixed baseline | fixed baseline | fixed baseline | fixed baseline |
| Independent challenger | new result | new result | new result | new result |

Decode with beam 1 first. Run beam 5 only after the checkpoint is selected, and report both rather than silently choosing the better test result.

## Decision Gates

1. **Pipeline gate:** smoke run trains, saves, reloads, and evaluates.
2. **Signal gate:** pilot improves native-8-kHz WER over base large-v3 by at least 10% relative.
3. **Serious-run gate:** curated-data pilot beats an equally sized uncurated-data control.
4. **ARTPARK gate:** challenger WER is below `0.3091`; a strong claim requires `0.2936` or lower and uncertainty analysis.
5. **Robustness gate:** FLEURS WER does not regress more than 5% relative.

If the model improves only native 8 kHz, report exactly that. That is still a valuable domain-specific result.

## Immediate Next Run

Run `notebooks/10_gv_train_100h_inventory_colab.ipynb`. It downloads or reuses the archive, excludes all 100 frozen IDs, probes audio with visible progress, writes the inventory/rejection manifests to Drive, and stops before training so the selected data can be inspected first.
