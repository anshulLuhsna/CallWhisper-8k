# Who Pays the Telephony Tax?

Status: proposed primary research direction for CallWhisper-8k, July 2026.

## Decision

Do not make the next headline experiment a generic Whisper fine-tune on GramVaani.

The stronger project is:

> An open, paired, multi-reference study of how narrowband telephone channels change Hindi ASR accuracy, hallucination behavior, and between-group disparities, followed by a compact channel-adapted Whisper model evaluated against ARTPARK on a predeclared metric.

Working article title:

> **Who Pays the Telephony Tax? A Paired, Multi-Reference Audit of Hindi ASR Under Narrowband Codecs**

The benchmark is the main contribution. The model is the mitigation experiment.

## Honest Novelty Boundary

None of these ideas is new by itself:

| Idea | Why it is not enough |
|---|---|
| Fine-tune Whisper for Hindi | ARTPARK, IndicWhisper, Vasista, Collabora, and others already do this. |
| Train on harder Hindi speech | [Vividh-ASR](https://arxiv.org/abs/2605.13087) already studies complexity-tiered Hindi ASR and high-learning-rate Whisper fine-tuning. |
| Test codecs, resampling, or noise on Hindi | [Basu et al. (2026)](https://arxiv.org/abs/2606.09335) already test GSM, narrowband/wideband filtering, Opus, resampling, bit depth, and noise on Hindi ASR. |
| Measure ASR fairness under degradation | [Ginjala et al. (2026)](https://arxiv.org/abs/2604.21276) already study demographic ASR gaps under 12 synthetic degradations, though only for English read/prompted speech and not telephone codecs. |
| Show that codecs can be gender-biased | [Altwlkany et al. (Interspeech 2025)](https://www.isca-archive.org/interspeech_2025/altwlkany25_interspeech.html) already show gender differences in objective speech quality after PSTN codecs, but do not measure downstream ASR. |
| Build a broad Indian telephony benchmark | [Voice of India](https://arxiv.org/abs/2604.19151) already benchmarks 536 hours of closed, real telephonic speech across 15 languages with geographic and demographic analysis. |
| Build an inclusive Hindi benchmark | [Vaani Benchmark V1.0](https://arxiv.org/abs/2606.21408) already provides spontaneous Hindi, district/gender metadata, and three independent references. |

The defensible gap is their intersection:

1. Hindi rather than English;
2. telephone codecs rather than generic noise or masking;
3. the same utterance and speaker under every channel, rather than unrelated clean and telephone groups;
4. multi-reference scoring so orthographic variation is not mistaken for channel damage;
5. real GramVaani telephone speech as external validation;
6. a compact mitigation model tested on worst-group and overall performance.

This is a plausible novelty claim, not yet a claim of being the first. Before publication, the final related-work search must be repeated and the wording must remain narrow.

## Concrete Finding We Already Have

The current GramVaani source-rate comparison is confounded.

The reproducible full-dev audit in `results/gramvaani_source_rate_confound_audit_v1.md` found:

- 1,169 native-8-kHz clips and 716 higher-rate clips;
- 976 of 1,279 male-labeled clips are native 8 kHz (`76.3%`);
- 89 of 492 female-labeled clips are native 8 kHz (`18.1%`);
- the male-versus-female native-8-kHz odds ratio is `14.59`;
- Cramer's V between dataset-provided gender and source-rate group is `0.543`;
- `inaudible` appears in 340 native-8-kHz clips versus 72 higher-rate clips.

Therefore the observed ARTPARK WER gap (`0.3091` on the native-8-kHz subset versus `0.1895` on the higher-rate subset) is useful as a deployment description, but it is not an estimate of the causal cost of 8 kHz audio. Gender composition, accent metadata, quality flags, speakers, content, and recording path all vary with source rate.

That is the first useful article finding:

> **An 8 kHz slice is not an 8 kHz experiment.** Comparing naturally occurring source-rate groups can attribute demographic and recording-pipeline differences to bandwidth.

## Research Questions

### RQ1: Channel penalty

How much does each controlled telephone channel change Hindi ASR error when speaker, utterance, reference, and recording are held fixed?

### RQ2: Disparity amplification

Does the channel penalty differ by dataset-provided gender or geographic group?

The question is about an interaction, not only whether groups have different raw WER.

### RQ3: Model ranking

Do models that lead on original audio remain best after narrowband and codec transformations?

### RQ4: Reference sensitivity

Does single-reference WER exaggerate or change the apparent channel penalty or model ranking compared with multi-reference WER?

### RQ5: Mitigation

Can a 244M-parameter channel-adapted Whisper-small reduce pooled telephone WER and worst-group WER below the 769M-parameter ARTPARK medium model without unacceptable original-audio regression?

## Evaluation Data

### Primary paired benchmark: Vaani Benchmark V1.0

Use the exact Hugging Face revision of [`ARTPARK-IISc/Vaani-Benchmark-V1.0`](https://huggingface.co/datasets/ARTPARK-IISc/Vaani-Benchmark-V1.0) available for the run.

The current dataset card describes 5,050 audio segments from 1,103 speakers across 104 districts. Each row includes gender, district, state, speaker ID, and three independent transcripts. Access is gated but the dataset is CC BY 4.0 after accepting its conditions.

Important: the current Hub card and the June 2026 paper report different release sizes. Pin the dataset commit and record row count, hours, schema, and hashes in every result. Do not silently mix versions.

The benchmark is evaluation-only. Never train on it.

### Accent replication: LAHAJA

Use [`ai4bharat/Lahaja`](https://huggingface.co/datasets/ai4bharat/Lahaja) as a secondary replication set. It contains 12.5 hours from 132 speakers across 83 districts and includes native-language, gender, age, state, and district metadata. Its references are not multi-reference, so it must remain a separate table.

LAHAJA is evaluation-only.

### Real telephone validation: GramVaani

Keep the frozen GramVaani 100-file benchmark and later report the full dev set. This validates behavior on real spontaneous telephone recordings, but the natural source-rate groups remain observational.

The original [Gram Vaani challenge paper](https://www.isca-archive.org/interspeech_2022/bhanushali22_interspeech.html) explicitly documents spontaneous telephone speech, regional variation, natural background noise, and crowd-transcription variability. Those are features of the deployment data, not controlled variables.

## Paired Channel Matrix

Create deterministic transformed copies from every primary benchmark utterance:

| Condition | Purpose |
|---|---|
| `original` | Same-file reference condition |
| `bandlimit_8k` | 300-3400 Hz band limit, 8 kHz processing, then 16 kHz input for the ASR model |
| `g711_alaw` | PSTN A-law encode/decode |
| `g711_mulaw` | PSTN mu-law encode/decode |
| `gsm_fr` | Low-bitrate 2G-style speech codec stress |

Core conditions are fixed before model evaluation. Opus bitrates, packet loss, jitter, AMR-NB, noise, and combined degradations belong in an extension only after the core matrix works. Adding conditions after seeing results would create a metric-shopping risk.

Every transform must record:

- source dataset revision and row ID;
- transform name and parameters;
- input/output sample rate;
- codec/tool version;
- deterministic seed where relevant;
- source and output hashes;
- duration consistency and decode success.

Whisper-family inputs must be decoded/resampled to 16 kHz correctly. The channel damage happens before that final model-input conversion.

## Models

Minimum baseline matrix:

1. `openai/whisper-large-v3`;
2. `ARTPARK-IISc/whisper-medium-vaani-hindi`;
3. `adalat-ai/whisper-small-hi-high-lr`;
4. `adalat-ai/whisper-medium-hi-high-lr`;
5. the compact CallWhisper challenger.

Add Vaani Fast Conformer only if an official public checkpoint and reproducible inference recipe are available. API systems can be a separate cost-controlled table, not a requirement for the open-model study.

Use one pinned decoding contract per architecture. For Whisper models, begin with deterministic beam 1 and manifest language `hi`. Beam 5 is a secondary ablation, never a hidden per-model choice.

## Metrics And Statistical Contract

### Primary accuracy metric

**Pooled telephony multi-reference corpus WER** over the four predeclared transformed conditions, with each condition represented equally.

For each utterance, score against all three Vaani references and use the paper's segment-level minimum-reference protocol as the primary multi-reference implementation. Also report each individual reference and the alignment-based protocol if its official implementation is available.

### Required secondary metrics

- original-audio multi-reference corpus WER;
- WER/CER for every condition;
- paired per-utterance channel penalty;
- insertion, deletion, substitution, repetition, empty-output, and script-drift rates;
- pooled worst-group WER for predeclared gender and macro-region groups with sufficient sample size;
- 90th-percentile per-speaker WER;
- single-reference versus multi-reference rank stability;
- model parameters, peak memory, and real-time factor.

### Disparity metric

Report the **absolute difference in channel penalty** between groups:

```text
(group A transformed WER - group A original WER)
- (group B transformed WER - group B original WER)
```

Do not rely only on a ratio of maximum to minimum WER. Ratios become unstable near zero and can appear to improve when every group simply fails.

Use paired bootstrap confidence intervals over speakers. For group interactions, fit or bootstrap a model with channel, group, and channel-by-group terms. Do not call a visual difference a disparity amplification without uncertainty.

Metadata labels must be described as dataset-provided categories, not biological truth or independently verified identity.

## What It Means To Beat ARTPARK

The win condition is declared before running the compact challenger on the frozen benchmark:

1. CallWhisper-small has lower pooled telephony multi-reference WER than ARTPARK medium.
2. The paired-bootstrap 95% confidence interval for `CallWhisper - ARTPARK` is entirely below zero.
3. CallWhisper-small uses no more than 35% of ARTPARK medium's parameter count.
4. It also has no worse pooled worst-group WER.
5. Relative WER regression on original Vaani audio and the separate clean Hindi control is at most 5% versus its starting checkpoint.

If it wins only one codec, one gender, or one hand-picked slice, it did not beat ARTPARK under this contract. That result can still be reported, but not promoted as the main win.

## Compact Challenger

### Starting point

Start from `adalat-ai/whisper-small-hi-high-lr`, not ARTPARK weights. This uses a strong public general-Hindi base and makes our contribution specifically channel adaptation. Keep a from-OpenAI-Whisper control if compute permits.

### Training data

- `GV_Train_100h` for real telephone speech;
- a speaker-disjoint Hindi train corpus such as IndicVoices for clean/spontaneous replay;
- on-the-fly versions of training utterances using the same channel family as the benchmark, with independently sampled parameters where appropriate.

Never use Vaani Benchmark, LAHAJA, GramVaani Dev, FLEURS test, or any frozen benchmark utterance for training, checkpoint selection, or prompt tuning.

### First serious training recipe

- full fine-tune Whisper-small after a short LoRA wiring run;
- 25% original/clean replay to limit forgetting;
- balanced channel sampling;
- balanced dataset-provided gender/region sampling only where labels are reliable;
- best-checkpoint selection on a separate speaker-disjoint internal validation set;
- one fixed final evaluation on the primary benchmark.

### Model ablations

1. strong Hindi base, no additional training;
2. ordinary mixed-data fine-tune;
3. channel-balanced augmentation;
4. channel-balanced augmentation plus clean replay;
5. optional channel-consistency loss.

The optional consistency objective compares teacher-forced token distributions for original and transformed versions of the same training utterance. It is only useful if it beats the augmentation-plus-replay control; it is not presumed to be novel by itself.

## Minimum Article-Worthy Outcomes

The work is useful even if the model does not beat ARTPARK, provided one of these findings is measured rigorously:

- model rankings change under paired telephone channels;
- a channel significantly amplifies a gender or region penalty;
- the apparent disparity shrinks only because all groups approach failure;
- multi-reference scoring materially changes channel penalties or rankings;
- objective codec quality does not predict downstream Hindi ASR damage;
- the compact model reduces worst-group telephony error without improving average WER;
- no meaningful group interaction exists, contradicting a plausible expectation.

The article must report null results and failed mitigation attempts. The goal is a trustworthy answer, not a predetermined dramatic chart.

## Execution Order

### Gate 0: freeze protocol

- pin this document and metric definitions;
- pin dataset revisions and model revisions;
- define macro-region mapping and minimum group size;
- decide the exact multi-reference scorer;
- publish the config before challenger evaluation.

### Gate 1: benchmark pilot

- accept/download Vaani Benchmark V1.0;
- select a deterministic 500-utterance pilot stratified by speaker, gender, and region;
- generate the five-condition matrix;
- evaluate ARTPARK and Adalat Whisper-small;
- validate scoring, runtime, and confidence-interval code.

### Gate 2: full baseline

- run the full paired Vaani matrix;
- run LAHAJA replication;
- run frozen GramVaani real-telephone validation;
- write the baseline finding before training.

### Gate 3: model mitigation

- inventory and curate `GV_Train_100h`;
- run LoRA wiring smoke;
- run full Whisper-small ablations;
- select the checkpoint only on internal validation.

### Gate 4: one final comparison

- evaluate the selected checkpoint once;
- bootstrap against ARTPARK;
- report overall, worst-group, original, clean-control, runtime, and model size;
- write the result whether it wins or loses.

## Immediate Next Artifact

Implemented: `notebooks/11_vaani_paired_telephony_benchmark_colab.ipynb`. Its first version stops after:

1. downloading the pinned Vaani benchmark revision;
2. saving a dataset inventory and deterministic 500-file pilot manifest;
3. generating and validating the paired channel files/manifests;
4. writing transform metadata and hashes.

It should not run every model or train anything until the transformed audio and multi-reference scorer have been inspected.
