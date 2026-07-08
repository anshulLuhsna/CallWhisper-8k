# Benchmark Slice v2

This note documents the first expanded GramVaani benchmark slice after the original 50-file smoke slice.

## Manifests

| Manifest | Files | Purpose |
|---|---:|---|
| `datasets/manifests/gramvaani_dev_100.csv` | 100 | Mixed real GramVaani telephone-style Hindi slice |
| `datasets/manifests/gramvaani_dev_100_8khz.csv` | 56 | Native 8 kHz subset |
| `datasets/manifests/gramvaani_dev_100_highrate.csv` | 44 | Higher-rate subset |

## Source Sample Rates

| Source sample rate | Files |
|---|---:|
| 8 kHz | 56 |
| 16 kHz | 1 |
| 44.1 kHz | 37 |
| 48 kHz | 6 |

## Commands

Build the 100-file manifest:

```bash
PYTHONPATH=src python -m callwhisper.datasets.build_gramvaani_manifest \
  --dataset-dir datasets/GV_Dev_5h \
  --output datasets/manifests/gramvaani_dev_100.csv \
  --limit 100
```

Split by source sample rate:

```bash
PYTHONPATH=src python -m callwhisper.datasets.split_manifest_by_sample_rate \
  --manifest datasets/manifests/gramvaani_dev_100.csv \
  --low-output datasets/manifests/gramvaani_dev_100_8khz.csv \
  --high-output datasets/manifests/gramvaani_dev_100_highrate.csv
```

## Why This Exists

The previous 50-file slice was useful for fast smoke tests and early model comparison. This 100-file slice is the next benchmark layer before larger model comparison or fine-tuning.

The split matters because the mixed slice contains both native 8 kHz telephone audio and higher-rate source audio. Future benchmark tables should report the mixed result and the sample-rate splits separately.

## Next Step

Run the main model comparison on all three manifests:

- `gramvaani_dev_100`
- `gramvaani_dev_100_8khz`
- `gramvaani_dev_100_highrate`

Minimum models:

- Whisper `large-v3`
- `ARTPARK-IISc/whisper-medium-vaani-hindi`

Then write:

```text
results/model_comparison_v2.md
results/model_comparison_v2.json
```
