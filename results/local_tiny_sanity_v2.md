# Local Tiny Sanity Result v2

This is a local development sanity check for the expanded GramVaani 100-file slice and its source-sample-rate splits. It is not a headline benchmark result.

## Purpose

The goal was to verify that the new `gramvaani_dev_100.csv` manifest and the derived 8 kHz/high-rate split manifests can run end-to-end through the existing OpenAI Whisper evaluation runner and produce WER/CER outputs.

## Command

```bash
PYTHONPATH=src .venv/bin/python -m callwhisper.eval \
  --manifest datasets/manifests/gramvaani_dev_100.csv \
  --model tiny \
  --language-mode manifest \
  --seed 0 \
  --output-json results/benchmark_v2/local_whisper_tiny_gramvaani_dev_100_seed0.json
```

The same command was also run for:

- `datasets/manifests/gramvaani_dev_100_8khz.csv`
- `datasets/manifests/gramvaani_dev_100_highrate.csv`

## Result

| Model | Slice | Files | WER | CER |
|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_100 | 100 | 1.1324 | 1.0720 |
| Whisper tiny | gramvaani_dev_100_8khz | 56 | 1.1158 | 1.0764 |
| Whisper tiny | gramvaani_dev_100_highrate | 44 | 1.1090 | 1.0579 |

## Notes

- This was run locally on CPU, so Whisper used FP32 instead of FP16.
- These results are mainly pipeline checks. They should not be compared as final model results against GPU runs unless the same manifest, language mode, seed, normalization, and decoding settings are documented.
- The next benchmark step is to run `COLAB_BENCHMARK_V2_RUNBOOK.md` on GPU for Whisper medium, Whisper large-v3, and ARTPARK Vaani Hindi on the same 100-file mixed/8 kHz/high-rate slices.
