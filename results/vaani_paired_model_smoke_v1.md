# Vaani Paired Model Smoke v1

## Status

Pipeline validation only. This run used 10 speakers, five matched channel conditions, two pinned models, beam 1, forced Hindi, and Vaani's alignment-based multi-reference scorer. It is too small for benchmark or codec-effect claims.

## Multi-Reference Corpus WER

| Model | Original | Bandlimit 8 kHz | G.711 A-law | G.711 mu-law | GSM-FR | Pooled telephone |
|---|---:|---:|---:|---:|---:|---:|
| ARTPARK medium Vaani Hindi | 0.1661 | 0.1444 | 0.1444 | 0.1259 | 0.1168 | 0.1328 |
| Adalat Whisper-small Hindi high-LR | 0.1985 | 0.2243 | 0.2379 | 0.2279 | 0.2697 | 0.2398 |

ARTPARK beat Adalat on every smoke slice. Adalat's pooled-telephone WER was `0.1070` absolute higher.

## Paired Diagnostic

Each transformed clip was compared with its own original-audio prediction.

| Model | Condition | Improved | Unchanged | Worsened | Mean utterance WER delta | Total error delta |
|---|---|---:|---:|---:|---:|---:|
| ARTPARK | Bandlimit 8 kHz | 4 | 5 | 1 | -0.0144 | -6 |
| ARTPARK | G.711 A-law | 4 | 5 | 1 | -0.0144 | -6 |
| ARTPARK | G.711 mu-law | 4 | 5 | 1 | -0.0229 | -11 |
| ARTPARK | GSM-FR | 4 | 4 | 2 | -0.0349 | -13 |
| Adalat | Bandlimit 8 kHz | 1 | 6 | 3 | +0.0172 | +7 |
| Adalat | G.711 A-law | 1 | 5 | 4 | +0.0160 | +10 |
| Adalat | G.711 mu-law | 1 | 5 | 4 | +0.0064 | +8 |
| Adalat | GSM-FR | 1 | 4 | 5 | +0.0593 | +18 |

ARTPARK's apparent gain is not only a changing multi-reference denominator. Conventional corpus WER against each fixed reference shows the same direction when the three reference-specific WERs are averaged:

| Model | Original | Bandlimit 8 kHz | G.711 A-law | G.711 mu-law | GSM-FR |
|---|---:|---:|---:|---:|---:|
| ARTPARK | 0.2318 | 0.2196 | 0.2196 | 0.2014 | 0.1954 |
| Adalat | 0.2585 | 0.2840 | 0.3082 | 0.2876 | 0.3434 |

## Interpretation

This is an interesting smoke signal, not a finding. Five of ten ARTPARK clips were unchanged under simple bandlimiting, and one difficult long clip supplied four of the six reduced errors. Possible explanations include genuine regularization from filtering, model-specific decoding instability, or sampling noise. The 500-speaker paired run and speaker-level bootstrap intervals decide whether the effect survives.

## Decision

Smoke gate passed: row counts, pinned revisions, paired ordering, inference, checkpointing, and scoring all worked. Proceed to the frozen 500-speaker run. Report both alignment-based multi-reference WER and conventional WER against all three references, plus paired clip-level deltas.
