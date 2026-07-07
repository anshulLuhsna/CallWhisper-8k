# CallWhisper-8k Benchmark Expansion Plan

Last updated: 2026-07-07

This document redefines the benchmark side of CallWhisper-8k before the next fine-tuning push.

## Thesis

CallWhisper-8k should not try to be "another Hindi ASR WER table."

The stronger benchmark thesis is:

> CallWhisper-8k is a deployment-oriented benchmark for Indian telephony ASR: it measures not only WER/CER, but also where models break under 8 kHz channel constraints, spontaneous Hindi, transcript noise, code-switching pressure, entity preservation, repetition/hallucination, and deployability constraints.

The model track is separate. The benchmark should stay useful even if our own fine-tuned model loses to ARTPARK, IndicWhisper, or commercial APIs.

## What Already Exists

### Vistaar / IndicWhisper

Vistaar is a broad Indian-language ASR benchmark covering 59 benchmarks over 12 languages. It includes GramVaani as one Hindi benchmark and compares IndicWhisper against public and commercial ASR systems.

What it contributes:

- broad multi-language and multi-domain ASR coverage,
- a strong IndicWhisper baseline,
- evidence that model performance varies heavily by benchmark/domain.

What CallWhisper should not claim:

- first Hindi ASR benchmark,
- first Whisper-derived model evaluated on GramVaani,
- first multi-model Indian ASR comparison.

Gap for CallWhisper:

- Vistaar is broad; CallWhisper can be deep on telephony.
- It does not center 8 kHz handling, preprocessing choices, hallucination patterns, or production-style telephony errors.

Source: https://github.com/AI4Bharat/vistaar and https://ar5iv.labs.arxiv.org/html/2305.15386

### Gram Vaani ASR Challenge / SLR118

The Gram Vaani ASR Challenge dataset is telephone-quality Hindi collected through Mobile Vaani, with regional and dialectal variation plus metadata such as location, dialect, emotion, and audio quality.

What it contributes:

- real telephone-quality Hindi speech,
- a credible anchor for Indian telephony ASR,
- metadata that can support richer slice analysis.

Gap for CallWhisper:

- use the dataset as a diagnostic benchmark, not only a WER row,
- split by sample rate, transcript quality, duration, audio quality, repetition/hallucination, and entity types.

Source: https://sites.google.com/view/gramvaaniasrchallenge/dataset

### ARTPARK / Vaani Whisper

ARTPARK's Hindi Whisper checkpoints are strong public baselines and include GramVaani in training/evaluation. Our current fixed-slice benchmark shows `ARTPARK-IISc/whisper-medium-vaani-hindi` is far ahead of vanilla Whisper and our small LoRA pilot.

What it contributes:

- a strong public Hindi-tuned Whisper baseline,
- evidence that domain-tuned Hindi Whisper models can perform strongly on GramVaani-style speech.

Gap for CallWhisper:

- ARTPARK is model-centric; CallWhisper can be benchmark-centric.
- We can compare public ARTPARK against other models on frozen slices, additional diagnostic metrics, and reproducible telephony transformations.

Source: https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi

### Vividh-ASR

Vividh-ASR introduces a complexity-stratified Indic ASR benchmark for Hindi and Malayalam with tiers such as studio/read, broadcast, spontaneous/crowdsourced, and synthetic noise. Its core insight is that domain labels are not enough; acoustic complexity needs to be measured directly.

What it contributes:

- a useful design pattern: evaluate by acoustic difficulty tiers,
- evidence that clean read-speech gains can hide spontaneous-speech weakness.

Gap for CallWhisper:

- specialize that idea for telephony: native 8 kHz, high-rate telephone-like MP3, synthetic 8 kHz, noisy/channel-degraded, and transcript-risk slices.

Source: https://arxiv.org/html/2605.13087v2

### Sarvam Indic ASR Evaluation

Sarvam's recent evaluation writing argues for layered Indic ASR metrics beyond WER/CER, including LLM-WER, LLM-CER, intent score, and entity preservation score.

What it contributes:

- a market-relevant evaluation direction: not every ASR error has the same downstream cost,
- a way to measure whether meaning and key entities survive even when exact word matching fails.

Gap for CallWhisper:

- build a small, transparent, non-overclaiming version for telephony Hindi:
  - entity preservation,
  - intent/topic preservation,
  - critical-number preservation,
  - hallucination/repetition flags.

Source: https://www.sarvam.ai/blogs/evaluating-indian-language-asr and https://github.com/sarvamai/llm_intent_entity

### μ-Bench And Production Call Benchmarks

Sierra's μ-Bench is an open multilingual transcription benchmark built from real 8 kHz mono customer-service phone calls. Production ASR buyer guides also emphasize that clean benchmarks such as FLEURS do not expose 8 kHz bandwidth limitations, codec compression, latency, or cost behavior.

What they contribute:

- the benchmark shape the market cares about: real calls, 8 kHz, customer-service use, provider comparison, and production utility.

Gap for CallWhisper:

- there is still room for an India/Hindi telephony benchmark that is open, reproducible, and model-neutral.

Sources: https://github.com/sierra-research/mu-bench and https://deepgram.com/learn/asr-buyers-guide-benchmarks-to-production-tests

## Redefined Benchmark Scope

CallWhisper-8k should expand from:

> WER/CER for Whisper on a small GramVaani slice.

to:

> A diagnostic benchmark for Indian telephony ASR, with fixed slices, standard WER/CER, and production-oriented failure metrics.

## Benchmark Layers

### Layer 1: Core Accuracy

Required metrics:

- WER
- CER
- macro WER/CER
- corpus WER/CER

Why:

- keeps comparability with prior work,
- makes tables easy to understand,
- prevents "LLM judge only" hand-waving.

### Layer 2: Telephony Channel Robustness

Slices:

- native 8 kHz GramVaani subset,
- high-rate GramVaani subset,
- clean FLEURS Hindi control,
- synthetic 8 kHz round-trip clean-control slice,
- optional codec/noise variants.

Metrics:

- WER/CER by slice,
- delta from clean control,
- delta from high-rate to 8 kHz,
- preprocessing delta.

Novel angle:

> We do not just ask "which model has lower WER?" We ask "which model degrades least when speech becomes telephone-like?"

### Layer 3: Transcript Trust And Human-Audibility Flags

Use manual review categories:

- human-understandable vs not,
- complete reference vs incomplete/cut,
- model-behavior failure vs audio-quality failure,
- background music/noise/multiple-speaker flags.

Metrics:

- WER on all files,
- WER excluding transcript-risk files,
- failure count by human-reviewed cause,
- examples where WER is misleading because the transcript is questionable.

Novel angle:

> A telephony benchmark should score the data, not only the model.

### Layer 4: Hallucination And Repetition Safety

Whisper-style failures on bad telephony audio often include repeated tokens, script drift, long hallucinated continuations, or empty/very short outputs.

Proposed automatic flags:

- repetition loop: same token or short n-gram repeated above threshold,
- length explosion: hypothesis length much longer than reference,
- empty/near-empty output,
- script drift: Devanagari reference but mostly Latin output, or vice versa,
- non-speech hallucination: output appears when VAD/low-energy audio suggests little speech.

Metrics:

- hallucination flag rate,
- repetition flag rate,
- length ratio distribution,
- flagged examples table.

Novel angle:

> In voice agents and call analytics, a hallucinated transcript can be worse than a blank.

### Layer 5: Entity And Actionability Evaluation

For a small curated subset, annotate or regex-detect:

- names,
- locations,
- numbers,
- dates/times,
- money amounts,
- organizations/schemes,
- phone-like digit sequences if present.

Metrics:

- entity recall,
- entity precision,
- critical number exact match,
- named-location preservation,
- intent/topic preservation for short utterances.

Implementation should start simple:

- regex + manual labels first,
- optional LLM judge later,
- keep WER/CER as primary until the new metrics are validated.

Novel angle:

> A transcript can have a mediocre WER but still preserve the thing a call-center system needs, or have a decent WER while losing the only important number.

### Layer 6: Deployability Score

For each model/backend, record:

- inference runtime,
- real-time factor,
- GPU/CPU used,
- approximate memory use,
- rough cost per audio hour when known,
- install friction,
- open weights vs API-only,
- license/redistribution status.

Metrics:

- WER vs real-time factor,
- WER vs memory,
- "edge candidate" flag for small/medium models,
- "benchmark-only" flag for models that are too expensive locally.

Novel angle:

> The best ASR for a production phone system is not always the lowest-WER model; it is the best point on the accuracy, cost, latency, and licensing curve.

## Proposed Benchmark Scorecard

Do not collapse everything into one fake universal score. Instead, report a scorecard:

| Axis | Metric | Why It Matters |
|---|---|---|
| Accuracy | WER/CER | Standard ASR comparison |
| Channel robustness | 8 kHz delta | Telephony degradation |
| Clean retention | FLEURS clean result | Detect overfitting to telephone data |
| Hallucination safety | repetition / length flags | Voice-agent reliability |
| Entity preservation | entity recall / number exact match | Production usefulness |
| Data trust | transcript-risk split | Honest benchmark quality |
| Deployability | RTF / memory / license | Real engineering tradeoff |

## v1 Ambitious But Realistic Deliverables

### Must Ship Before Fine-Tuning Part 2

1. Rename the benchmark thesis in README:
   - "deployment-oriented Indian telephony ASR benchmark."
2. Add a benchmark scorecard table for current models:
   - Whisper medium,
   - Whisper large-v3,
   - ARTPARK medium,
   - our small LoRA.
3. Add automatic failure flags:
   - repetition,
   - length explosion,
   - script drift,
   - empty output.
4. Add a report:
   - `results/benchmark_diagnostics_v1.md`.
5. Add first social post with:
   - current numbers,
   - why WER alone is insufficient,
   - what the benchmark will evaluate next.

### Nice To Have

1. Entity labels for 25-50 samples.
2. RTF and memory table for each model.
3. Synthetic telephony FLEURS slice.
4. Commercial API runner if credits are available.
5. Streamlit/static mini report after the benchmark is stable.

## Social Positioning

Good public framing:

> I started CallWhisper-8k as a Whisper-on-8-kHz experiment. The more I tested, the more obvious the real problem became: WER alone is not enough for Indian telephony ASR. A model can look decent on clean Hindi and still fail badly on narrowband spontaneous speech, repetition loops, transcript noise, or entities that matter in calls.

Avoid:

- "first benchmark,"
- "state of the art,"
- "beats ARTPARK,"
- "fixes Whisper,"
- "production-ready Hindi ASR."

## Next Engineering Step

Initial status: the first version is implemented as `callwhisper-diagnostics` / `python -m callwhisper.eval.diagnostics`, and the first report is saved at `results/benchmark_diagnostics_v1.md`.

Next, expand `benchmark_diagnostics_v1`:

1. Load existing per-sample JSON/CSV predictions.
2. Compute per-sample:
   - reference length,
   - hypothesis length,
   - length ratio,
   - repeated-token flag,
   - repeated-character/Devanagari loop flag,
   - script ratio,
   - empty/near-empty flag.
3. Aggregate by:
   - model,
   - slice,
   - condition,
   - beam size.
4. Save:
   - `results/benchmark_diagnostics_v1.json`,
   - `results/benchmark_diagnostics_v1.md`.

This gives us a credible public Part 1 before the next fine-tuning run.

Current caveat: the first generated report uses the Whisper-small base-vs-LoRA reload CSV. It includes both the mixed GramVaani slice and the derived 8 kHz/high-rate split manifests, so some audio files appear in more than one slice. This is acceptable for slice-level diagnostics but should not be read as 600 unique audio files.
