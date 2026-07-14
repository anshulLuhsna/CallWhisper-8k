# GramVaani Source-Rate Confound Audit v1

## Finding

The native-8-kHz and higher-rate GramVaani groups are compositionally different. A raw WER difference between them is observational and must not be interpreted as the causal cost of 8 kHz bandwidth.

Audited files: `1885`. Native 8 kHz: `1169`. Higher rate: `716`.

## Gender Metadata

Gender values are dataset-provided metadata, not independently verified identity labels.

| Category | Native 8 kHz | Higher rate | Total | Native 8 kHz share |
|---|---:|---:|---:|---:|
| Male | 976 | 303 | 1279 | 76.3% |
| Female | 89 | 403 | 492 | 18.1% |
| unknown | 104 | 10 | 114 | 91.2% |

Cramer's V for gender versus source-rate group: `0.543`.

Using only the dataset's `Male` and `Female` labels, the odds that a male-labeled clip is native 8 kHz are `14.59x` the corresponding female-labeled odds.

## Accent Metadata

| Category | Native 8 kHz | Higher rate | Total | Native 8 kHz share |
|---|---:|---:|---:|---:|
| unknown | 724 | 525 | 1249 | 58.0% |
| Bihari | 429 | 169 | 598 | 71.7% |
| Bhojpuri | 14 | 22 | 36 | 38.9% |
| Lucknowi | 1 | 0 | 1 | 100.0% |
| Normal_hindi | 1 | 0 | 1 | 100.0% |

Cramer's V for accent versus source-rate group: `0.149`.

## State Metadata

| Category | Native 8 kHz | Higher rate | Total | Native 8 kHz share |
|---|---:|---:|---:|---:|
| unknown | 734 | 543 | 1277 | 57.5% |
| Bihar | 431 | 171 | 602 | 71.6% |
| Madhya_pradesh | 1 | 2 | 3 | 33.3% |
| Jharkhand | 2 | 0 | 2 | 100.0% |
| Uttar_pradesh | 1 | 0 | 1 | 100.0% |

Cramer's V for state versus source-rate group: `0.141`.

## Quality Markers

These counts come from substring matches in the dataset's `Other` metadata field.

| Marker | Native 8 kHz | Higher rate |
|---|---:|---:|
| inaudible | 340 | 72 |
| audio_jump | 82 | 135 |
| background_noise | 0 | 0 |
| multiple_speakers | 0 | 0 |

## Consequence

Use the native source-rate slice as a real-world deployment view, but use paired transformations of the same utterances to estimate a channel penalty. Speaker, content, region, reference, and recording should stay fixed while only the channel changes.

## Reproduction

```bash
callwhisper-metadata-audit \
  --dataset-dir datasets/GV_Dev_5h \
  --output-prefix results/gramvaani_source_rate_confound_audit_v1
```
