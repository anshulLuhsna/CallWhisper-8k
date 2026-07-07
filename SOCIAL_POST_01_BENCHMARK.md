# Social Post Draft 01: Benchmark Before Fine-Tuning

Purpose: first public post before the next large fine-tuning push.

Tone: honest, technical, ambitious.

## Short Version

I started CallWhisper-8k as a simple question:

> How badly does Whisper break on 8 kHz Indian telephony audio?

After the first benchmark runs, the more interesting question is bigger:

> What should a serious benchmark for Indian telephony ASR actually measure?

WER/CER are necessary, but they are not enough.

On my fixed GramVaani Hindi telephone-style slice:

| Model | Mixed 50 WER | 8 kHz WER | High-rate WER |
|---|---:|---:|---:|
| Whisper medium | 0.7683 | 0.8108 | 0.6584 |
| Whisper large-v3 | 0.5616 | 0.6511 | 0.3984 |
| ARTPARK Whisper-medium Vaani Hindi | 0.2597 | 0.2900 | 0.2057 |

The obvious result is that domain-tuned Hindi ASR beats vanilla Whisper.

The less obvious result is what the benchmark needs to capture next:

- native 8 kHz vs high-rate audio,
- clean Hindi vs telephone-style Hindi,
- preprocessing that helps one file and hurts another,
- incomplete or risky transcripts,
- repetition loops and hallucinated continuations,
- entity preservation for names, places, numbers, and actionability,
- runtime and deployability, not just accuracy.

So I am splitting CallWhisper-8k into two tracks:

1. a reproducible benchmark for Indian telephony ASR,
2. a separate model/adaptation track that tries to improve on that benchmark.

The benchmark comes first.

Because if the measurement is weak, the fine-tuning result does not mean much.

Repo: [add GitHub link]

## Longer Version

I have been working on CallWhisper-8k, a small but serious Voice AI project around Indian telephone-style ASR.

The initial version was straightforward:

Run Whisper-family models on Hindi telephony-style audio, measure WER/CER, test preprocessing, then try lightweight adaptation.

But after testing Whisper small/medium/large-v3, ARTPARK's Hindi-tuned Whisper model, a clean FLEURS control, and a small LoRA pilot, I think the benchmark itself is the more important first artifact.

Current fixed-slice results:

| Model | Mixed GramVaani 50 WER | 8 kHz subset WER | High-rate subset WER |
|---|---:|---:|---:|
| Whisper medium | 0.7683 | 0.8108 | 0.6584 |
| Whisper large-v3 | 0.5616 | 0.6511 | 0.3984 |
| ARTPARK Whisper-medium Vaani Hindi | 0.2597 | 0.2900 | 0.2057 |

So yes, domain-tuned Hindi ASR crushes vanilla Whisper here. That part is expected.

What is more interesting is the measurement problem.

A useful telephony ASR benchmark should not only ask:

> What is the WER?

It should also ask:

- Does the model degrade more on native 8 kHz audio?
- Does it preserve names, places, numbers, and intent?
- Does it hallucinate or repeat tokens under bad audio?
- Are failures caused by model behavior, audio quality, or imperfect references?
- Does a preprocessing step help consistently, or only move errors around?
- Can the model run cheaply enough for real call analytics or voice agents?

That is the direction I am taking CallWhisper-8k now:

> A deployment-oriented benchmark for Indian telephony ASR, with fine-tuning as a second track rather than the whole project.

This is not a "we beat everyone" post.

It is the first checkpoint in building the measurement system I wish existed before training models for Hindi/Indian call audio.

Next step: add benchmark diagnostics beyond WER/CER: hallucination flags, repetition detection, transcript-risk splits, and entity preservation.

Repo: [add GitHub link]

## One-Line Hook Options

- WER is necessary for ASR evaluation, but it is not enough for Indian telephony.
- I thought I was building a Whisper fine-tuning project. I was actually missing the benchmark.
- If your benchmark cannot detect hallucinated repetitions, transcript noise, and lost phone numbers, it is not enough for call audio.
- Domain-tuned Hindi ASR beating vanilla Whisper is expected. Measuring exactly how and where models fail is the real project.

## Suggested Image

Use a screenshot/table with:

- Whisper medium,
- Whisper large-v3,
- ARTPARK,
- mixed GramVaani,
- 8 kHz subset,
- high-rate subset.

Caption:

> Same fixed Hindi telephony slice, very different behavior across models and channel conditions.

## Do Not Say

- "state of the art"
- "first Hindi ASR benchmark"
- "fixed Whisper"
- "production-ready"
- "beats ARTPARK"

## Good Closing

The next public update should show the diagnostic table, not the fine-tuned model.

Fine-tuning comes after the benchmark can tell us something more useful than one WER number.
