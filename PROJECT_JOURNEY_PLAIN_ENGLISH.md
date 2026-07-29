# CallWhisper-8k: The Whole Project in Plain English

Last updated: 24 July 2026

This document was reconstructed from the full local task history, the Git
commit trail, the saved benchmark reports, and the final frozen-evaluation
output. It explains what we tried, what worked, what failed, and whether the
project is actually significant.

## The 60-Second Answer

We built a serious test system for Hindi speech recognition on telephone-style
audio.

The project itself did **not** fail. The final training experiment failed its
most important test.

Three different things happened:

1. **The benchmark succeeded.** We built a reproducible way to compare speech
   recognition models on the same speech before and after telephone
   degradation.
2. **We found a real result.** The compact Adalat Whisper-small model is faster
   than ARTPARK Whisper-medium, but it consistently loses more accuracy when
   the same speech is changed into telephone-quality audio. We reproduced this
   finding on two different datasets.
3. **Our attempted fix did not generalize.** LoRA training made Adalat much
   better on held-out GramVaani data, but it became worse on the untouched
   Vaani and LAHAJA benchmarks. The adapter learned the GramVaani domain more
   than it learned general telephone robustness.

The honest bottom line is:

> We did not build a better production model. We did build a credible Hindi
> telephony ASR benchmark, found and externally replicated a model-specific
> telephone robustness gap, and demonstrated why an impressive internal
> fine-tuning result can fail on new data.

That is meaningful engineering and experimental work. It is not a
state-of-the-art model result.

## A Few Terms

- **ASR:** automatic speech recognition, or speech-to-text.
- **8 kHz audio:** narrowband audio commonly associated with traditional phone
  calls. It contains less speech information than wideband recording.
- **WER:** word error rate. Lower is better. A WER of 20% roughly means one word
  error for every five reference words.
- **CER:** character error rate. Lower is better.
- **Telephone transform:** a controlled change such as 8 kHz bandlimiting,
  G.711 A-law, G.711 mu-law, or GSM-FR compression.
- **Channel penalty:** how much a model's WER increases after the same utterance
  is converted from original audio to telephone-style audio.
- **LoRA:** a lightweight way to fine-tune a model without updating every model
  weight.
- **Held-out internal data:** examples from the same dataset family that were
  excluded from training.
- **Frozen external benchmark:** a test set that is not used to choose training
  settings. It is the final exam.

## What We Originally Wanted to Build

CallWhisper-8k started as a four-week flagship Voice AI project. The goal was
not merely to call Whisper from an API. The project was supposed to show that
we could:

- prepare and audit real speech datasets;
- run Whisper and Hindi-tuned models reproducibly;
- measure WER and CER;
- simulate telephone channels correctly;
- investigate model failures instead of hiding them;
- try lightweight model adaptation;
- package the work into a CLI, API, Docker image, demo, and clear report.

The research questions were:

1. How well do Whisper-family models handle Hindi telephone speech?
2. Does simple preprocessing improve it?
3. Does telephone degradation hurt every model equally?
4. Can we make a compact, fast model more robust?

## What Happened, Step by Step

### 1. We Built the Basic Evaluation Pipeline

The first pipeline was:

```text
CSV manifest
  -> load audio and reference transcript
  -> transcribe with a model
  -> normalize text consistently
  -> calculate WER and CER
  -> save per-file and summary results
```

We began with a small GramVaani development slice containing spontaneous Hindi
telephone-style speech.

We discovered that the first 50-file slice mixed different source sample
rates:

- 32 files were native 8 kHz;
- 16 files were 44.1 kHz;
- 2 files were 48 kHz.

Whisper-small WER was 92.39% on the native-8-kHz group and 70.03% on the
higher-rate group.

At first glance this looked like proof that 8 kHz caused the problem. It was
not. The groups also differed in speaker distribution, noise, recording
quality, and transcript quality. Later analysis found a strong association
between dataset-provided gender and source-rate group. That made the natural
8-kHz versus high-rate split a useful observation, but not a fair causal
experiment.

This was an important early correction: we learned not to turn a convenient
table into a stronger claim than the data supports.

### 2. We Tested Simple Preprocessing

We tried basic audio changes before transcription:

- convert to mono 16 kHz;
- normalize loudness;
- apply a telephone bandpass;
- perform an 8 kHz round trip.

On the first 50-file Whisper-small run:

| Condition | WER |
|---|---:|
| Raw audio | 84.34% |
| Mono 16 kHz | 83.27% |
| Loudness normalized | 82.23% |
| Telephone bandpass | 84.52% |
| 8 kHz round trip | 84.68% |

Loudness normalization helped slightly on that slice. The explicit telephone
changes did not help. There was no magic preprocessing fix.

### 3. We Listened to the Errors Ourselves

WER alone cannot tell us whether a failure came from bad audio, a bad
reference, or the model.

We created a human-review bundle containing:

- raw audio;
- normalized audio;
- the reference transcript;
- the raw model transcript;
- the normalized-audio model transcript;
- a short classification form.

For the first 15 flagged files:

- 9 failures were judged mainly to be model behavior;
- 6 were judged mainly to be audio quality;
- 0 were judged to be transcript quality alone.

Several severe model errors happened on speech that a human could understand.
Normalization sometimes changed WER without sounding noticeably better.

This listening step stopped us from blaming every error on "bad 8 kHz audio."

### 4. We Tested Stronger and Hindi-Tuned Models

We moved the heavier evaluations to Colab GPUs and tested the same fixed
100-file GramVaani slice.

| Model | Mixed WER | Native 8 kHz WER | Higher-rate WER |
|---|---:|---:|---:|
| Whisper medium | 71.82% | 78.89% | 62.81% |
| Whisper large-v3 | 51.82% | 60.83% | 40.36% |
| ARTPARK Hindi Whisper-medium | **25.65%** | **30.91%** | **18.95%** |

ARTPARK was far better on this slice. The main lesson was that model and
training-data choice mattered much more than our simple preprocessing.

We also added a clean Hindi FLEURS control. All models performed better on the
clean control, although this still mixed channel and speaking-domain
differences.

### 5. We Tried Cheap Decoding Changes

Before expensive training, we tested decoding settings on Whisper large-v3.

- Beam size 5 improved WER from 56.16% to 52.48%.
- Automatic language detection hurt.
- Hindi prompt biasing hurt.
- Temperature experiments hurt.

This showed another useful rule: plausible settings are not automatically
better. They must be measured.

### 6. We Ran the First LoRA Pilot

We trained a small LoRA adapter on GramVaani training data. This first pilot was
mainly proof that we could build and reload a real fine-tuning artifact.

Compared with the same base Hugging Face Whisper-small pipeline, beam-5 WER
changed:

| Slice | Base | LoRA |
|---|---:|---:|
| GramVaani mixed | 103.03% | 75.32% |
| Native 8 kHz subset | 115.95% | 89.46% |
| Higher-rate subset | 80.06% | 50.18% |

WER can exceed 100% when the model inserts many extra words.

The pilot proved that the adapter learned something useful about GramVaani. It
did not beat ARTPARK, and it did not prove general telephone robustness.

### 7. We Changed the Research Question

At this point, "a Hindi-tuned model beats vanilla Whisper" was not a new or
interesting conclusion.

The better question became:

> When the speaker and words stay exactly the same, do different models lose
> different amounts of accuracy under telephone degradation?

To answer that, we needed paired audio. Each source utterance would appear in
five matched conditions:

1. original;
2. 8 kHz bandlimited;
3. 8 kHz plus G.711 A-law;
4. 8 kHz plus G.711 mu-law;
5. 8 kHz plus GSM-FR.

Because every condition comes from the same utterance, speaker, words, and
reference remain fixed. This is much cleaner than comparing unrelated native
8-kHz and high-rate recordings.

### 8. We Built the 500-Speaker Vaani Paired Benchmark

The Vaani benchmark used:

- 500 speakers;
- one selected utterance per speaker;
- five matched conditions;
- two models;
- 5,000 total predictions;
- multi-reference scoring;
- 20,000 speaker-level bootstrap repetitions for uncertainty.

Manual listening caught a real bug before inference. Our first codec versions
did not include the explicit telephone bandlimit, so G.711 and GSM sounded too
similar to the original. We rejected those transformed files, fixed the
pipeline, rebuilt the audio, and only evaluated the corrected version.

The corrected result was:

| Model | Original WER | Telephone WER | Penalty |
|---|---:|---:|---:|
| ARTPARK medium | 14.60% | 15.09% | +0.49 points |
| Adalat small | 17.40% | 20.20% | +2.80 points |

Adalat's telephone penalty was 2.32 percentage points larger than ARTPARK's.
The 95% interval was +1.66 to +3.00 points, entirely above zero.

This was strong evidence, but ARTPARK's training mixture included Vaani. That
made an independent external replication necessary.

### 9. We Replicated the Finding on LAHAJA

Notebook 13 repeated the paired experiment on one deterministic utterance from
each of LAHAJA's 132 speakers.

| Model | Original WER | Telephone WER | Penalty |
|---|---:|---:|---:|
| ARTPARK medium | 19.14% | 19.71% | +0.58 points |
| Adalat small | 18.02% | 21.52% | +3.50 points |

The Adalat-minus-ARTPARK penalty gap was +2.92 percentage points. Its 95%
interval was +1.37 to +4.59 points, entirely above zero.

The direction from Vaani replicated on LAHAJA:

> Adalat loses more accuracy than ARTPARK when identical speech is converted
> to telephone-style audio.

Adalat was also about 1.88 times faster on the T4. This revealed a useful
accuracy-speed-robustness tradeoff: the compact model was faster, but more
channel-fragile.

This paired, externally replicated finding is the strongest result in the
project.

### 10. We Tried to Fix Adalat's Weakness

Notebook 14 trained a serious Adalat LoRA adapter.

The serious profile used:

- 18,000 GramVaani source clips;
- about 49 source hours;
- 23,989 training views;
- about 65 view-hours after augmentation;
- 3,000 optimizer steps;
- a recording-group-disjoint internal split;
- approximately 75% released GramVaani telephone audio;
- approximately 25% additional 8 kHz, G.711, and GSM stress views.

GramVaani was already telephone speech. We did not have a large, diverse clean
Hindi training set for replay.

On held-out GramVaani, the adapter looked very successful:

| Internal GramVaani result | Base Adalat | Adapted Adalat |
|---|---:|---:|
| Original WER | 60.31% | **49.91%** |
| Pooled telephone WER | 61.22% | **50.87%** |
| CER | 38.73% | **31.18%** |

All transformed conditions improved. The internal gate correctly said
`pass_to_frozen_benchmarks`.

But original and telephone audio improved by almost the same amount. The
channel penalty was about +0.92 points before training and +0.96 after. The
adapter had learned the GramVaani domain, but it had not shown reduced channel
sensitivity.

The internal gate was permission to take the final exam, not proof that the
model had passed it.

### 11. The Frozen External Evaluation Failed

Notebook 15 evaluated the fixed adapter once on untouched Vaani and LAHAJA
paired benchmarks. We did not change the success rule after seeing the result.

#### Vaani Final Test

| Result | Base Adalat | Adapted Adalat |
|---|---:|---:|
| Original WER | **17.41%** | 19.93% |
| Pooled telephone WER | **20.22%** | 22.62% |

The adapter was 2.40 points worse on pooled telephone audio. The paired 95%
interval was +1.58 to +3.20 points, so the harm was statistically supported.
Original WER regressed by about 14.47% relative.

There was no supported reduction in channel sensitivity on Vaani.

#### LAHAJA Final Test

| Result | Base Adalat | Adapted Adalat |
|---|---:|---:|
| Original WER | **18.02%** | 20.00% |
| Pooled telephone WER | **21.53%** | 21.89% |

The pooled difference was small and uncertain, but the adapter still did not
improve absolute WER. Original WER regressed by about 10.96% relative.

The channel penalty did decrease from about 3.51 points to 1.89 points, and
that reduction was statistically supported. Unfortunately, this happened
partly because the adapter became worse on the original audio. A smaller gap
created by damaging the starting point is not a useful production win.

#### ARTPARK Headline Gate

On pooled Vaani telephone audio, adapted Adalat remained 7.53 WER points worse
than ARTPARK. The 95% interval was +6.47 to +8.62 points.

The final machine verdict was:

```text
fail_external_generalization
```

The adapter did not beat ARTPARK and was not better than base Adalat on both
external benchmarks.

## Why the Model Failed

The most likely explanation is **domain overfitting**.

In simple words, the adapter became good at GramVaani rather than becoming
generally good at telephone speech.

Several design limits contributed:

1. **Training diversity was too narrow.** Most training speech came from one
   dataset with its own speakers, recording style, vocabulary, and transcript
   conventions.
2. **GramVaani was already telephone audio.** Additional codec stress was often
   degradation stacked on top of an existing telephone channel.
3. **We lacked clean replay.** A diverse clean Hindi replay set could have
   reminded the model how to handle broader speech while it adapted.
4. **The internal validation shared the same domain.** Recording groups were
   separated correctly, but train and validation still came from GramVaani.
5. **The training objective rewarded transcription improvement, not explicit
   channel invariance.** It could lower error by learning GramVaani-specific
   patterns without learning a general rule about channels.

This is why internal WER improved by around ten points while external WER got
worse.

## What Broke During the Thread

The work was not a smooth sequence of perfect notebooks. The main operational
problems were:

| Problem | What Happened | What We Changed |
|---|---|---|
| Non-portable paths | Generated manifests initially contained local absolute paths. | Switched artifacts to repository-relative paths. |
| Colab clone and import errors | URLs were pasted or interpreted incorrectly, and cloned source was not always importable. | Hardened clone cells, package installation, and source-path setup. |
| Hidden long-running work | Dataset probing and audio preparation appeared frozen. | Added progress bars and bounded scans. |
| Incorrect codec semantics | First G.711/GSM files lacked the intended telephone bandlimit. | Rebuilt the paired corpus with bandlimit first, then codec, and added listening/spectral checks. |
| Duration mismatches | Codec output differed from source duration enough to fail validation. | Added frame-level duration conformance and stricter validation. |
| GPU time used for CPU work | Audio cache preparation ran inside the GPU notebook. | Split it into Notebook 14a, a resumable CPU cache-preparation notebook. |
| Whisper label overflow | One transcript tokenized to 476 tokens, above Whisper's 448-token limit. | Added a pre-training audit and excluded the entire source consistently instead of silently truncating it. |
| Checkpoint resume failure | PyTorch 2.6 refused to load the trusted NumPy RNG state with its new safe default. | Added a path-contained trusted-checkpoint preflight and preserved checkpoint 1800. |
| Missing notebook outputs | Reopening the GitHub notebook did not restore ephemeral Colab cell output. | Recovered results from persistent Drive artifacts. |
| Missing LAHAJA baseline files | Notebook 15 expected a complete previous artifact folder. | Made it recompute and checkpoint the missing 660-row baseline. |

Some runtime and GPU time was genuinely wasted while discovering these issues.
The cache split, label audit, duration checks, and checkpoint recovery should
have existed earlier. The important point is that we did not hide the failures
or use partial runs as final evidence. We repaired the pipeline and eventually
completed the predeclared frozen test.

## What We Actually Achieved

### Benchmark and Evaluation Work

- Reproducible manifest-based ASR evaluation.
- WER and CER reporting.
- Per-file prediction artifacts.
- Real-time-factor speed measurements.
- Clean and telephone-style benchmark slices.
- Correct 8 kHz, G.711 A-law, G.711 mu-law, and GSM-FR transforms.
- Multi-reference Vaani scoring.
- Paired speaker-level bootstrap confidence intervals.
- Human audio and transcript review.
- Dataset confound and leakage checks.
- Frozen external evaluation rules.

### Model Work

- Compared vanilla Whisper medium and large-v3 with Hindi-tuned checkpoints.
- Measured decoding changes instead of guessing.
- Trained, saved, reloaded, and evaluated LoRA adapters.
- Built restartable Colab and Kaggle workflows.
- Preserved checkpoints and prediction progress in Drive.
- Ran both internal and external evaluations.
- Recorded a negative external result honestly.

### The Strongest Supported Finding

Across both Vaani and LAHAJA, the compact Adalat model had a significantly
larger telephone channel penalty than ARTPARK:

| Dataset | Speakers | Adalat minus ARTPARK penalty gap | 95% interval |
|---|---:|---:|---:|
| Vaani | 500 | +2.32 WER points | +1.66 to +3.00 |
| LAHAJA | 132 | +2.92 WER points | +1.37 to +4.59 |

This is not proof that ARTPARK is globally the best Hindi model. It is evidence
that these two frozen models respond differently when matched speech is passed
through controlled telephone transforms.

## What We Did Not Achieve

- We did not beat ARTPARK.
- We did not create a production-ready improved Adalat model.
- We did not prove a universal rule for every real phone call.
- We did not prove that sample rate alone caused the original GramVaani gap.
- We did not make simple preprocessing reliably solve the problem.
- We did not complete the original v1.0 product packaging.

The repository still lacks the planned FastAPI service, Docker setup, and
simple demo. The research phase is much more complete than the product phase.

## Is This Significant?

### As a New State-of-the-Art Model: No

The adapter failed external generalization and did not beat ARTPARK. It should
not be advertised as a better model.

### As Scientific Research: Moderately Significant

The project did not invent telephony ASR or Hindi Whisper fine-tuning. Its
useful contribution is narrower:

- it used matched utterances instead of comparing unrelated recordings;
- it measured uncertainty with paired speaker bootstrapping;
- it reproduced the robustness difference on a second dataset;
- it tested a mitigation model against frozen external benchmarks;
- it preserved the negative result instead of tuning until a benchmark looked
  good.

That is a credible experimental story, even if it is not a major research
breakthrough.

### As a Voice AI Engineering Portfolio Project: Yes

This project demonstrates much more than an API wrapper:

- speech dataset handling;
- telephony codec processing;
- ASR evaluation;
- statistical testing;
- model adaptation;
- GPU notebook reliability;
- human error analysis;
- reproducibility;
- honest failure analysis.

For an internship or Voice AI role, that engineering depth is valuable.

## The Correct Public Claim

A defensible short description is:

> Built CallWhisper-8k, a reproducible Hindi telephony ASR benchmark using
> matched 8 kHz, G.711, and GSM transformations, human error review, and
> speaker-paired bootstrap evaluation. Replicated a larger telephone accuracy
> penalty for compact Adalat Whisper-small than ARTPARK Whisper-medium on
> Vaani and LAHAJA. A leakage-aware LoRA adapter improved held-out GramVaani
> WER but failed frozen external generalization, demonstrating domain
> overfitting.

Do not say:

- "I solved Hindi telephone ASR."
- "My model beats ARTPARK."
- "Fine-tuning improved all benchmarks."
- "8 kHz alone caused every observed error."

## Is Another Training Attempt Worth It?

Not for the current v1.0 using the same data and the same two external
benchmarks.

Repeatedly changing training after looking at Vaani and LAHAJA would turn them
into tuning sets. Their next scores would no longer be a clean external test.

A future v2 attempt could be worthwhile only if it changes the experiment
substantially:

1. obtain a large and diverse clean Hindi or Hinglish training corpus;
2. create clean-to-telephone pairs from that clean source;
3. mix clean replay with real telephone speech;
4. use gentler LoRA settings and stronger anti-forgetting controls;
5. maintain separate internal clean and telephone validation sets;
6. reserve a new untouched external dataset for the final test.

That is a new project phase, not a small rerun of Notebook 14.

## What Should Happen Next

The research answer is complete enough. The best next move is to finish the
artifact:

1. commit the Notebook 15 final result files and a concise final results page;
2. simplify the README around the replicated finding and failed mitigation;
3. expose one reproducible benchmark command;
4. add the planned FastAPI endpoint;
5. add Docker;
6. add a small demo and a short result walkthrough;
7. tag v1.0 and stop changing the research result.

## Final Bottom Line

We began by asking whether Hindi speech recognition gets worse on telephone
audio and whether we could fix it.

We learned that:

- simple preprocessing was not enough;
- stronger Hindi-specific training mattered a lot;
- compact Adalat was faster but more telephone-sensitive than ARTPARK;
- this sensitivity difference replicated on two datasets;
- LoRA training produced a large same-domain improvement;
- that improvement disappeared and reversed on untouched external data.

So the model experiment failed, but the project uncovered exactly the kind of
failure a good benchmark is supposed to reveal.

That is the real value of CallWhisper-8k.

## Evidence in This Repository

- [100-file model comparison](results/model_comparison_v2.md)
- [First manual audio review](results/manual_audio_review_v1.md)
- [Decoding adaptation sweep](results/adaptation_v1.md)
- [Whisper-small LoRA pilot](results/lora_pilot_v1.md)
- [Vaani paired 500-speaker result](results/vaani_paired_model_full_v1.md)
- [LAHAJA external replication](results/lahaja_paired_external_v1.md)
- [Notebook 14a CPU cache preparation](notebooks/14a_adalat_channel_cache_cpu_colab.ipynb)
- [Notebook 14 serious Adalat adaptation](notebooks/14_adalat_channel_adaptation_colab.ipynb)
- [Notebook 15 frozen external evaluation](notebooks/15_adalat_frozen_evaluation_colab.ipynb)
