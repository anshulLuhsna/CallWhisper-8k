# Baseline v0

First smoke-test baseline on 10 files from Gramvaani GV Dev 5h.

| Model | Dataset Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 10 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 10 | 0.9981 | 0.9250 |

## Notes

- This is a tiny smoke-test slice, not a final benchmark.
- The data is real telephone-style Hindi speech from Gramvaani GV Dev 5h.
- Whisper `tiny` produced heavy hallucinations on several files.
- Whisper `base` reduced the error rate, but still produced empty, wrong-script, or heavily corrupted outputs on multiple files.
- WER/CER can be greater than 1.0 when the hypothesis has many insertions.
- Next step: run `small` if local runtime is acceptable, otherwise move larger runs to Colab/GPU.
