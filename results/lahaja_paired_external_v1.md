# LAHAJA External Paired Replication v1

## Scope

This is the completed external replication gate from `notebooks/13_lahaja_external_paired_replication_colab.ipynb` at repository commit `7539bc6db4480bdf47f41a5bfafbde7c84abd97a`.

- Dataset: `ai4bharat/Lahaja`, revision `d4ffd2ecbdd933e37c917ddcf620eef159ceb3a7`
- Sample: one deterministic 1-30 second utterance from each of 132 speakers
- Conditions: original, bandlimit 8 kHz, G.711 A-law, G.711 mu-law, GSM-FR
- Models: pinned ARTPARK Whisper-medium Vaani Hindi and Adalat Whisper-small Hindi high-LR
- Predictions: 1,320
- Decoding: beam 1, forced Hindi, deterministic
- Scoring: conventional single-reference corpus WER/CER
- Uncertainty: 20,000 paired speaker-bootstrap replicates, seed 0

## Primary Result

| Model | Original WER | Pooled telephone WER | Channel penalty | 95% bootstrap CI | Pooled RTF |
|---|---:|---:|---:|---:|---:|
| ARTPARK medium Vaani Hindi | 0.1914 | 0.1971 | +0.0058 | [-0.0023, +0.0135] | 0.2668 |
| Adalat Whisper-small Hindi high-LR | 0.1802 | 0.2152 | +0.0350 | [+0.0222, +0.0492] | 0.1418 |

The Adalat-minus-ARTPARK pooled channel-penalty gap was `+0.0292` absolute WER, with 95% CI `[+0.0137, +0.0459]`. Because the interval is entirely above zero, the Vaani channel-sensitivity finding is externally replicated on this speaker-balanced LAHAJA slice.

## What Replicated Means

The finding is about **change under controlled channel degradation**, not a global model ranking.

- On original audio, Adalat's WER was nominally lower by `0.0111`, but the 95% CI `[-0.0305, +0.0077]` includes zero.
- On pooled telephone audio, Adalat's WER was nominally higher by `0.0181`, but the 95% CI `[-0.0003, +0.0368]` narrowly includes zero.
- The statistically supported result is that Adalat loses more accuracy when the same utterances are passed through telephone channels.
- Adalat is also materially faster: its pooled RTF was `0.1418` versus `0.2668`, making ARTPARK about `1.88x` slower in this T4 run.

## Per-Condition Robustness

| Condition | ARTPARK penalty (95% CI) | Adalat penalty (95% CI) | Penalty gap (95% CI) |
|---|---:|---:|---:|
| Bandlimit 8 kHz | +0.0033 [-0.0061, +0.0123] | +0.0296 [+0.0154, +0.0454] | +0.0263 [+0.0093, +0.0446] |
| G.711 A-law | -0.0004 [-0.0096, +0.0083] | +0.0305 [+0.0166, +0.0459] | +0.0309 [+0.0134, +0.0499] |
| G.711 mu-law | +0.0045 [-0.0047, +0.0132] | +0.0288 [+0.0159, +0.0434] | +0.0243 [+0.0083, +0.0418] |
| GSM-FR | +0.0156 [+0.0056, +0.0259] | +0.0510 [+0.0366, +0.0664] | +0.0354 [+0.0187, +0.0526] |
| Pooled telephone | +0.0058 [-0.0023, +0.0135] | +0.0350 [+0.0222, +0.0492] | +0.0292 [+0.0137, +0.0459] |

All four Adalat channel penalties and all four Adalat-minus-ARTPARK penalty gaps exclude zero. ARTPARK's bandlimit and G.711 intervals include zero; only GSM-FR produces a clearly positive standalone ARTPARK penalty.

## Cross-Dataset Evidence

The same direction now appears on two different paired benchmarks:

| Dataset | Speakers | ARTPARK pooled penalty | Adalat pooled penalty | Penalty gap (95% CI) |
|---|---:|---:|---:|---:|
| Vaani paired v2 | 500 | +0.0049 | +0.0280 | +0.0232 [+0.0166, +0.0300] |
| LAHAJA external v1 | 132 | +0.0058 | +0.0350 | +0.0292 [+0.0137, +0.0459] |

The absolute WER values must not be compared across datasets because Vaani uses three-reference scoring and LAHAJA uses one reference. The paired penalty direction is the replication target.

## Adaptation Decision

The compact-model adaptation target is now supported. Start from Adalat Whisper-small and train only on leakage-safe training data. The verified GramVaani inventory is already telephone speech and no substantial clean Hindi training corpus is currently available in Drive, so the first experiment keeps every selected released source and adds balanced channel-stress views to one-third of sources. The objective is to keep Adalat's speed advantage while reducing the channel penalty on both frozen benchmarks.

Predeclared final gate:

1. lower pooled telephone WER than the unadapted Adalat checkpoint on both Vaani and LAHAJA;
2. paired-bootstrap improvement interval entirely below zero on both benchmarks;
3. original-audio relative WER regression no greater than 5%;
4. pooled Vaani telephone WER below ARTPARK with a 95% paired interval entirely below zero for the headline "beat ARTPARK" claim;
5. no benchmark utterance used for training, checkpoint selection, prompt tuning, or early stopping.

## Provenance And Open Checks

These repository tables were transcribed from the completed Colab output returned by the user on 2026-07-17. At ingestion time, the connected Drive folder exposed only `run_config.json`, `package_versions.json`, and an empty `archives/` listing; the final report bundle printed by Colab was not visible through Drive web or the connector. Preserve or recover the original prediction JSONL files before publication so the entire analysis can be regenerated.

The Colab run also emitted a current Transformers warning that the attention mask was not passed because Whisper's pad and EOS tokens are identical. The run remains a controlled same-pipeline comparison, but an attention-mask equivalence audit should be completed before treating these exact absolute numbers as publication-final.

## Files

- `summary.csv`: per-model, per-condition WER/CER and speed
- `artpark_vs_adalat.csv`: point-estimate model comparison
- `paired_channel_deltas.csv`: paired utterance change counts and mean deltas
- `paired_bootstrap_primary.csv`: all displayed channel-penalty and penalty-gap intervals
- `replication_conclusion.json`: exact machine-readable verdict returned by Colab

## Limitations

- LAHAJA provides one reference per utterance; Vaani used three-reference scoring.
- Absolute WER across LAHAJA and Vaani is not directly comparable.
- Model training-set disjointness from LAHAJA has not been independently proven.
- The paired effect is causal for these deterministic transforms, not for every real phone call.
- The sample contains one selected clip per speaker, not every LAHAJA utterance.
