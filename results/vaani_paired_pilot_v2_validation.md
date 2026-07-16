# Vaani Paired Pilot v2 Validation

Status: **accepted for model evaluation**.

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

The run used Vaani revision `1bf019521d12d742178acc32bf2a42f81cf7c8ef` and generation commit `23972f30a5eef51f53298f54725ed55248fe5d4e`.

## Channel Contract

The five frozen conditions are:

1. `original`
2. `bandlimit_8k`
3. `bandlimit_8k_g711_alaw`
4. `bandlimit_8k_g711_mulaw`
5. `bandlimit_8k_gsm_fr`

Every codec condition applies the 300-3400 Hz telephone passband before codec encode/decode. All outputs are then decoded as mono 16 kHz WAV inputs for Whisper-family evaluation.

## Manual Listening

The post-repair listening check passed. The stacked codec conditions sounded recognizably narrowband, with no observed silence, clipping, speed change, or mismatched speech in the displayed review samples.

## Decision

Freeze v2 for model evaluation. Do not alter its utterance selection, channel transforms, references, or condition names after model results exist. The next gate is a tested multi-reference scorer followed by same-pipeline ARTPARK and Adalat Whisper-small smoke inference.
