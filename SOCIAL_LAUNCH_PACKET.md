# Social Launch Packet: CallWhisper-8k Part 1

Use this when posting the first public benchmark update.

## Attach

```text
social_assets/benchmark_part1_card.png
```

## LinkedIn Post

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

Repo: https://github.com/anshulLuhsna/CallWhisper-8k

## X / Twitter Thread

### Post 1

I started CallWhisper-8k with a simple question:

How badly does Whisper break on 8 kHz Indian telephony audio?

The answer is useful, but the better question is bigger:

What should a serious benchmark for Indian telephony ASR actually measure?

### Post 2

On a fixed GramVaani Hindi telephone-style slice:

Whisper medium:
Mixed 50 WER 0.7683
8 kHz WER 0.8108

Whisper large-v3:
Mixed 50 WER 0.5616
8 kHz WER 0.6511

ARTPARK Whisper-medium Vaani Hindi:
Mixed 50 WER 0.2597
8 kHz WER 0.2900

### Post 3

The obvious result:

Domain-tuned Hindi ASR is much stronger than vanilla Whisper on this slice.

That part is expected.

The more interesting part is the measurement problem.

### Post 4

WER/CER are necessary, but for Indian telephony ASR they are not enough.

A useful benchmark should also ask:

- does the model degrade on native 8 kHz audio?
- does it hallucinate/repeat under bad audio?
- does it preserve names, places, numbers, and intent?

### Post 5

So I am splitting CallWhisper-8k into two tracks:

1. a reproducible benchmark for Indian telephony ASR,
2. a model/adaptation track that tries to improve on that benchmark.

The benchmark comes first.

Repo: https://github.com/anshulLuhsna/CallWhisper-8k

## Alt Text For Image

CallWhisper-8k benchmark card showing WER results on a fixed GramVaani telephone-style Hindi slice. Whisper medium has WER 0.7683 on mixed 50 files, 0.8108 on 8 kHz files, and 0.6584 on high-rate files. Whisper large-v3 has WER 0.5616, 0.6511, and 0.3984. ARTPARK Whisper-medium Vaani Hindi has WER 0.2597, 0.2900, and 0.2057. The card states that domain-tuned Hindi ASR beats vanilla Whisper on this slice, and asks what breaks under 8 kHz telephony beyond WER/CER.

## Short Caption

Part 1 of CallWhisper-8k: before fine-tuning anything bigger, I am making the benchmark itself more serious.

WER/CER are necessary, but for Indian telephony ASR they are not enough.

## Safe Reply If Someone Says "ARTPARK Already Wins"

Yes, exactly. That is the point of this first post. The benchmark should make that visible before I fine-tune anything. The model track comes second; the measurement track comes first.

## Safe Reply If Someone Asks "What Is Novel?"

The novelty is not "first Hindi ASR benchmark." Existing work already covers broad Hindi/Indic ASR and GramVaani. The narrower contribution is a telephony-focused benchmark that measures channel robustness, transcript trust, hallucination/repetition, entity preservation, and deployability under fixed Indian telephony slices.

## Safe Reply If Someone Asks "Are You Claiming SOTA?"

No. This is explicitly not a SOTA claim. These are slice-specific results and a benchmark-scope update before the next fine-tuning run.
