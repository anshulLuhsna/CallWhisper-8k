# Sample Rate Split v1

This note separates the current 50-file GramVaani GV Dev slice by source audio sample rate. The goal is to avoid treating a mixed-source slice as if every file were native 8 kHz telephone audio.

## Manifest Split

| Manifest | Files | Source sample rates |
|---|---:|---|
| `datasets/manifests/gramvaani_dev_50_8khz.csv` | 32 | 8 kHz |
| `datasets/manifests/gramvaani_dev_50_highrate.csv` | 18 | 44.1 kHz / 48 kHz |

Command:

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.datasets.split_manifest_by_sample_rate \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --low-output datasets/manifests/gramvaani_dev_50_8khz.csv \
  --high-output datasets/manifests/gramvaani_dev_50_highrate.csv
```

## Existing Raw Baseline By Split

These numbers are computed from the existing `results/baseline_small_50_v0.json` Whisper `small` raw MP3 run, not from a new decoding run.

| Model | Dataset Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper small | gramvaani_dev_50 | raw telephone MP3 mixed | 50 | 0.8434 | 0.5598 |
| Whisper small | gramvaani_dev_50_8khz | raw MP3 source 8 kHz | 32 | 0.9239 | 0.6528 |
| Whisper small | gramvaani_dev_50_highrate | raw MP3 source 44.1/48 kHz | 18 | 0.7003 | 0.3946 |

## Interpretation

- On this fixed slice, the true 8 kHz subset has higher WER/CER than the 44.1/48 kHz subset.
- This supports reporting source sample rate explicitly in future tables.
- This does not prove sample rate alone caused the gap. Speaker, topic, transcript quality, duration, and noise may differ across subsets.
- Future preprocessing/adaptation tables should include both mixed-slice totals and source-rate split rows.
