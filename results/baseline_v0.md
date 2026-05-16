# Baseline v0

First smoke-test baseline on 10 files from Gramvaani GV Dev 5h.

| Model | Dataset Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 10 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 10 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | telephone_mp3 | 10 | 0.8109 | 0.4963 |

## Notes

- This is a tiny smoke-test slice, not a final benchmark.
- The data is real telephone-style Hindi speech from Gramvaani GV Dev 5h.
- Whisper `tiny` produced heavy hallucinations on several files.
- Whisper `base` reduced the error rate, but still produced empty, wrong-script, or heavily corrupted outputs on multiple files.
- Whisper `small` was the strongest local model in this smoke test and produced mostly Devanagari output, but WER remains high.
- WER/CER can be greater than 1.0 when the hypothesis has many insertions.
- Next step: expand the slice and add a reproducible baseline summary.
