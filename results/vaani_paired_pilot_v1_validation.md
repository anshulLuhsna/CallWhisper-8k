# Vaani Paired Pilot v1 Validation

Status: **integrity passed; condition semantics superseded before model evaluation**.

## Automated Validation

| Check | Result |
|---|---:|
| Source utterances | 500 |
| Unique speakers | 500 |
| Paired rows | 2,500 / 2,500 |
| Samples with all five conditions | 500 / 500 |
| Output format | mono 16 kHz |
| Missing output files | 0 |
| Duration-tolerance violations | 0 |
| Maximum duration delta | 0.019 s |

The deterministic pilot contains 259 female-labeled and 241 male-labeled speakers across 22 states. It uses Vaani revision `1bf019521d12d742178acc32bf2a42f81cf7c8ef` and repository commit `83b0f18b1a454d910976a6651bbbbe0825040b1b`.

## Manual Listening Finding

The explicit `bandlimit_8k` condition sounded recognizably telephone-like. The v1 G.711 A-law, G.711 mu-law, and GSM-FR conditions sounded closer to the original.

Code inspection explained the difference: `bandlimit_8k` applied a 300-3400 Hz filter, while the v1 codec conditions performed 8 kHz codec round trips without first applying that explicit telephone passband. Those rows measured codec/resampling effects, not the complete telephone channel implied by their labels.

## Decision

Do not evaluate models on the v1 codec conditions. Preserve v1 for provenance and build v2 with these predeclared conditions:

1. `original`
2. `bandlimit_8k`
3. `bandlimit_8k_g711_alaw`
4. `bandlimit_8k_g711_mulaw`
5. `bandlimit_8k_gsm_fr`

Notebook `11b_vaani_stacked_codec_repair_colab.ipynb` reuses the valid v1 source, original, and bandwidth-only archives and regenerates only the three stacked codec conditions.
