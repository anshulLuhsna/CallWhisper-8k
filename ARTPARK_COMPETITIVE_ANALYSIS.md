# ARTPARK Competitive Analysis And Beat Plan

Last updated: 2026-07-06

This document answers one question:

> What did ARTPARK-IISc likely do for `whisper-medium-vaani-hindi`, how open is it, and what would CallWhisper-8k need to do to beat it honestly?

Short answer: beating ARTPARK means building an independent challenger whose base weights are not ARTPARK weights, then evaluating it against the public ARTPARK checkpoint on frozen held-out slices. Fine-tuning ARTPARK itself is useful as an upper-bound ablation, but it is not the main goal and it is not the win condition.

## Executive Summary

`ARTPARK-IISc/whisper-medium-vaani-hindi` is a strong Hindi-tuned Whisper-medium checkpoint. Its model card says it is based on `openai/whisper-medium`, has Apache-2.0 licensed weights, and was trained on roughly 718 hours of transcribed Hindi speech from several datasets including Vaani, GramVaani, IndicVoices, FLEURS, IndicTTS, and Common Voice.[^artpark-medium]

The model is open-weight, not fully open-recipe. As of 2026-07-06, the public Hugging Face repository is not gated and includes `model.safetensors`, tokenizer/config files, and `trainer_state.json`; it does not publish the exact training manifests, data mixture ratios, filtering rules, full training arguments, or a training script. The Vaani dataset is public/gated on Hugging Face and requires agreeing to access conditions; its dataset card says users must share contact information before accessing files.[^vaani-hf]

Our current CallWhisper-8k benchmark shows ARTPARK is still far ahead of our Whisper-small LoRA:

| Model | Slice | WER |
|---|---|---:|
| ARTPARK-IISc/whisper-medium-vaani-hindi | `gramvaani_dev_50` | 0.2597 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | `gramvaani_dev_50_8khz` | 0.2900 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | `gramvaani_dev_50_highrate` | 0.2057 |
| Our Whisper-small LoRA | `gramvaani_dev_50`, beam 5 | 0.7532 |
| Our Whisper-small LoRA | `gramvaani_dev_50_8khz`, beam 5 | 0.8946 |
| Our Whisper-small LoRA | `gramvaani_dev_50_highrate`, beam 5 | 0.5018 |

So the next serious goal is not "adapt ARTPARK and call that a win." The next serious goal is:

> Build a non-ARTPARK Whisper challenger, starting from `openai/whisper-large-v3` or `openai/whisper-medium`, train it on leakage-safe Indian telephone-style Hindi data, and beat the public ARTPARK checkpoint on the same frozen CallWhisper-8k GramVaani slices.

That would be a valid and ambitious win:

> We built a reproducible telephony-Hindi benchmark, used ARTPARK as the strongest public baseline, then trained an independent Whisper-family challenger that outperformed that public checkpoint on fixed held-out telephone-style Hindi slices.

## What ARTPARK/Vaani Did

### 1. Built a large, India-representative speech dataset

Project Vaani is an IISc + ARTPARK initiative. The Vaani site reports about 31,255 hours of speech, about 2,043 hours of transcribed audio, about 156K speakers, 109 languages, and 165 districts.[^vaani-site]

The Vaani paper describes the dataset as image-prompted spontaneous speech across 165 districts. It says the released corpus contains about 31,255 hours of spontaneous speech, 2,043 hours of manual transcriptions, and about 289K paired images from about 158K speakers.[^vaani-paper-abstract]

Why this matters for ASR:

- Vaani is not just clean read speech.
- It captures accent, district, demographic, device, and spontaneous-speech variation.
- It gives Hindi ASR models exposure to broader real-world Indian speech variation than FLEURS or Common Voice alone.

### 2. Used strict collection and quality-control structure

The Vaani paper says speech was collected using image-based prompts to elicit spontaneous responses.[^vaani-paper-abstract] The paper also documents collection requirements: spontaneous speech, 10-20 seconds per image prompt, quiet recording conditions, microphone placement guidance, balanced speaker selection, speaker metadata, and local/district language expectations.[^vaani-collection]

Its QC appendix includes checks for whether the speaker is audible, whether there is one speaker, whether the audio is understandable, whether the accent/dialect is local, whether the audio is clear, whether the sentence is complete, whether the content relates to the image, and whether personal information is present.[^vaani-qc]

This matters because ARTPARK's advantage is not only model size. It is data quality and diversity.

### 3. Fine-tuned Whisper-family models for Hindi

The `whisper-medium-vaani-hindi` model card says:

- base model: `openai/whisper-medium`
- language: Hindi
- license: Apache-2.0
- model size: about 0.8B parameters
- training data: approximately 718 hours of transcribed Hindi speech
- datasets listed: Vaani, GramVaani, IndicVoices, FLEURS, IndicTTS, Common Voice
- public WER table includes GramVaani, FLEURS, IndicTTS, MUCS, Common Voice, Kathbath, Kathbath Noisy, Vaani, and RESPIN.[^artpark-medium]

ARTPARK also has small, tiny, and large-v3 Vaani Whisper Hindi variants. The collection page describes these as Whisper models fine-tuned using Vaani data and other datasets.[^vaani-whisper-collection]

The public model card does not fully specify:

- exact train/dev/test manifests
- exact hours per dataset
- exact text normalization
- audio filtering
- whether any evaluation-set leakage was avoided for every listed dataset
- full training arguments
- training script
- compute setup

However, the model repository exposes `trainer_state.json`. For `whisper-medium-vaani-hindi`, it indicates:

- total training reached 15,000 steps
- configured maximum steps were 15,000
- training batch size was 16
- best checkpoint was around step 13,000
- best logged eval WER was about 21.17
- eval happened every 1,000 steps
- checkpoints were saved every 1,000 steps
- training reached about 2.59 epochs
- learning rate peaked around `1e-5`

This is useful, but it is not a full reproduction recipe.

### 4. Published broader Vaani ASR experiments

The Vaani paper's appendix describes language-specific ASR fine-tuning experiments with Whisper-small. For Hindi, it reports using 331 hours of Vaani Hindi data. The paper says the training used Hugging Face Transformers, transcript normalization, max target length 448 tokens, Adam, warmup of 1,000 steps, FP16, 10 epochs, per-device batch size 16, gradient accumulation 2, and effective batch size 32.[^vaani-asr-exp]

Important caveat:

This appendix experiment is not necessarily the exact recipe for `ARTPARK-IISc/whisper-medium-vaani-hindi`, because the model card says that checkpoint is Whisper-medium trained on roughly 718 hours from multiple datasets, not just the 331-hour Vaani Hindi subset.

## Is ARTPARK Open Source?

### What is open

- Model weights for `ARTPARK-IISc/whisper-medium-vaani-hindi` are public on Hugging Face.
- The model card lists Apache-2.0 license.
- Config/tokenizer/generation config files are public.
- `trainer_state.json` is public.
- Vaani is published as a Hugging Face dataset with gated access and a CC-BY-4.0 license tag.
- The Vaani paper describes dataset scale, collection protocol, QC, and some training experiments.

### What is not fully open

- Exact training code for `whisper-medium-vaani-hindi`.
- Exact data mixture and manifests.
- Exact filtering rules.
- Exact normalization scripts.
- Exact evaluation scripts.
- Exact decoding settings for the model-card WER table.
- A leakage audit proving what GramVaani/FLEURS/Kathbath/Common Voice files were or were not included in training.

### Practical conclusion

ARTPARK is open-weight and partially documented, but not fully reproducible from public artifacts alone.

For CallWhisper-8k, that is actually useful. We do not need to clone their training exactly. We need to:

1. evaluate their public checkpoint in our fixed pipeline,
2. treat it as a strong public baseline,
3. adapt further on a carefully separated telephone-domain train split,
4. prove improvement on frozen held-out slices.

## Our Current Position Against ARTPARK

From `results/model_comparison_v1.md`, ARTPARK is currently the strongest model on our fixed GramVaani slices:

| Slice | ARTPARK WER | Whisper large-v3 WER | Our Whisper-small LoRA WER |
|---|---:|---:|---:|
| `gramvaani_dev_50` | 0.2597 | 0.5616 | 0.7532 |
| `gramvaani_dev_50_8khz` | 0.2900 | 0.6511 | 0.8946 |
| `gramvaani_dev_50_highrate` | 0.2057 | 0.3984 | 0.5018 |

The small LoRA result is still valuable because it proves our training and reload pipeline works. But it is not close to ARTPARK.

The gap to close on `gramvaani_dev_50` is:

```text
0.7532 -> 0.2597
```

That is too large for a simple small-model tweak. The path to beating ARTPARK is to adapt a model at or above ARTPARK's starting strength.

## What "Beating ARTPARK" Should Mean

Bad target:

> ARTPARK plus our LoRA beats public ARTPARK.

That is an ablation, not a challenger. It uses the opponent's weights.

Good target:

> OpenAI Whisper large-v3 plus CallWhisper telephony-domain training beats the public ARTPARK checkpoint on fixed GramVaani held-out slices.

Best target:

> A non-ARTPARK model improves GramVaani WER by at least 5-10% relative over public ARTPARK while preserving FLEURS clean-control performance within a small regression budget.

Example win gate:

| Slice | Public ARTPARK WER | Target WER |
|---|---:|---:|
| `gramvaani_dev_50` | 0.2597 | <= 0.2467 for 5% relative improvement |
| `gramvaani_dev_50_8khz` | 0.2900 | <= 0.2755 for 5% relative improvement |
| `gramvaani_dev_50_highrate` | 0.2057 | <= 0.1954 for 5% relative improvement |

If the adapter improves only one slice, the most meaningful slice is the 8 kHz subset, because that is closest to the project's telephony focus.

## What We Need To Beat ARTPARK

### 1. Stronger starting checkpoint

Use one of these, in order:

1. `openai/whisper-large-v3` with Hindi/telephone adaptation
2. `openai/whisper-medium` with a stronger recipe if large-v3 compute is unavailable
3. `openai/whisper-small` only for edge-model experiments, not the primary ARTPARK-beating run

Disallowed for the main challenger:

- `ARTPARK-IISc/whisper-medium-vaani-hindi` as the training base
- `ARTPARK-IISc/whisper-large-v3-vaani-hindi` as the training base
- distilling labels from ARTPARK outputs and claiming an independent win

Those can be measured as side ablations, but they do not satisfy the main goal.

First recommended experiment:

```text
Base: openai/whisper-large-v3
Method: LoRA
Train: GV_Train_100h
Eval: frozen GramVaani 50 / 8 kHz / high-rate + FLEURS clean
```

### 2. Better train data curation

We should not just throw all files into training. We need a curated training manifest:

- exclude all frozen eval IDs
- keep duration between 1 and 30 seconds initially
- remove empty, incomplete, or clearly mismatched transcripts
- mark noisy / clipped / multi-speaker samples
- deduplicate by utterance ID
- preserve speaker/source diversity
- track source sample rate

For ARTPARK-beating work, data quality is likely more important than an exotic optimizer.

### 3. Clean-control replay

If we only train on GramVaani telephone speech, the model may over-specialize and get worse on clean Hindi. We need a small replay/control mixture:

- GramVaani train: main domain
- FLEURS Hindi: clean read-speech replay
- optionally Kathbath or Common Voice Hindi: broader clean Hindi replay

The evaluation must always include FLEURS clean control.

### 4. Correct training setup

Recommended pilot:

| Setting | Value |
|---|---|
| Base model | `openai/whisper-large-v3` |
| Method | LoRA |
| Target modules | start with `q_proj`, `v_proj`; second run test `q_proj`, `k_proj`, `v_proj`, `out_proj` |
| LoRA rank | 16 first, then 32 if stable |
| LoRA alpha | 32 or 64 |
| LoRA dropout | 0.05 |
| Learning rate | `1e-5` to `3e-5` for large-v3 |
| Effective batch size | 8-32 depending on GPU |
| Warmup | 5-10% of steps |
| Max steps | smoke 100, pilot 1,000-2,000, serious 5,000-10,000 |
| Eval metric | eval loss during training; WER/CER after checkpoints |
| Decoding | beam 1 and beam 5 |

Why large-v3 first:

ARTPARK already beat vanilla Whisper large-v3 by a wide margin on our slice. To beat ARTPARK without using ARTPARK weights, we need both a strong base model and domain-specific telephone training. Whisper-small LoRA proved the pipeline, but it is too far behind to be the first serious challenger.

### 5. Evaluation discipline

Every independent challenger run must compare:

- public ARTPARK baseline
- our non-ARTPARK adapted model
- optional Whisper large-v3 context

On:

- `gramvaani_dev_50`
- `gramvaani_dev_50_8khz`
- `gramvaani_dev_50_highrate`
- `fleurs_hi_clean_50`

And report:

- macro WER/CER
- corpus WER/CER
- deltas versus public ARTPARK
- per-sample errors
- best and worst changed examples

Add bootstrap confidence intervals if possible. On only 50 files, a small WER change may be noise.

### 6. Stronger compute

T4 can probably run a LoRA pilot, but serious medium/large experiments will be slow and fragile.

Preferred:

- A100 40GB/80GB
- L4/A10G for medium LoRA if A100 is unavailable
- Kaggle/Colab for smoke, paid GPU for serious runs

## Proposed Notebook 07

Create:

```text
notebooks/07_whisper_large_v3_challenger.ipynb
```

It should:

1. mount Drive or use Kaggle input
2. clone/pull repo
3. install pinned training deps
4. download or locate `GV_Train_100h`
5. build a filtered training split excluding frozen eval IDs
6. optionally build a small clean replay split
7. run public ARTPARK baseline eval first
8. train `openai/whisper-large-v3` LoRA
9. evaluate the adapted large-v3 model on frozen slices
10. save adapter, config, train/eval splits, JSON, Markdown, and Excel/CSV tables

Output path:

```text
results/whisper_large_v3_challenger_v1/
results/whisper_large_v3_challenger_v1.md
```

## Experiment Ladder

### Stage 0: Baseline Reconfirmation

Re-run public ARTPARK through our latest `callwhisper-lora-eval` style pipeline.

Goal:

```text
public ARTPARK numbers match or nearly match current repo numbers
```

### Stage 1: Smoke

Train on 200-500 filtered GramVaani train clips.

Goal:

```text
training/eval/save/reload path works
```

No claims.

### Stage 2: Pilot

Train on 3,000-5,000 filtered clips.

Goal:

```text
adapted openai/whisper-large-v3 closes meaningful distance to public ARTPARK
```

### Stage 3: Serious

Train on most/all usable `GV_Train_100h`, with clean replay and multiple seeds if compute allows.

Goal:

```text
beat public ARTPARK on GramVaani 8 kHz or mixed slice
no major FLEURS regression
```

### Stage 4: Strong Claim Candidate

Run:

- multiple seeds
- confidence intervals
- manual error analysis
- clean-control report
- maybe compare with ARTPARK large-v3 public model as an external reference

Only after this stage can we make a polished claim.

## Risks And How To Handle Them

### Risk: ARTPARK already trained on GramVaani

The model card lists GramVaani in training data. That means public ARTPARK may already have strong domain exposure. We are not starting from a naive baseline.

Mitigation:

- Use leakage-safe GramVaani Train 100h and add a larger held-out slice if possible.
- Keep held-out IDs excluded from our training.
- Report the result as a fixed-slice challenger result, not universal superiority.

### Risk: leakage uncertainty in public ARTPARK

The public model card does not publish exact training manifests. We cannot verify whether their training data overlapped with our fixed dev slice.

Mitigation:

- Compare against public ARTPARK as an external black-box baseline.
- Clearly state that we control leakage only for our training.
- Add a new held-out slice if possible.

### Risk: 50-file eval is small

A few hard files can swing WER.

Mitigation:

- Add a 200-500 file held-out GramVaani dev/eval slice if licensing and compute allow.
- Add bootstrap confidence intervals.
- Preserve per-sample outputs.

### Risk: clean Hindi regression

Domain adaptation can improve telephone audio while hurting clean speech.

Mitigation:

- Evaluate FLEURS after every run.
- Add clean replay during training.
- Use early stopping based on combined GramVaani + clean-control score.

## Final Recommendation

Do this next:

```text
Build Notebook 07: openai/whisper-large-v3 challenger LoRA.
```

Do not spend the next sprint fine-tuning ARTPARK and calling it "beating ARTPARK." Our small adapter proved the pipeline works. The ambitious, technically sound move is to start from a non-ARTPARK base, preferably `openai/whisper-large-v3`, and train a stronger telephone-Hindi challenger.

That is how we turn ambition into a real competitor instead of a derivative ARTPARK checkpoint.

## Sources

[^artpark-medium]: ARTPARK-IISc, `whisper-medium-vaani-hindi` model card, Hugging Face. https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi
[^vaani-hf]: ARTPARK-IISc, `Vaani` dataset card, Hugging Face. https://huggingface.co/datasets/ARTPARK-IISc/Vaani
[^vaani-whisper-collection]: ARTPARK-IISc Vaani-Whisper collection, Hugging Face. https://huggingface.co/collections/ARTPARK-IISc/vaani-whisper
[^vaani-site]: Project Vaani website. https://vaani.iisc.ac.in/
[^vaani-paper-abstract]: Pulikodan et al., "VAANI: Capturing the language landscape for an inclusive digital India", arXiv:2603.28714v3. https://arxiv.org/html/2603.28714v3
[^vaani-collection]: VAANI paper, collection guidelines appendix. https://arxiv.org/html/2603.28714v3
[^vaani-qc]: VAANI paper, QC appendix. https://arxiv.org/html/2603.28714v3
[^vaani-asr-exp]: VAANI paper, Appendix A.1/A.2 ASR fine-tuning experiments. https://arxiv.org/html/2603.28714v3
