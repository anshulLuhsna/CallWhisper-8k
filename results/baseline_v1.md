# Baseline v1

Initial Week 1 baseline on 10 files from Gramvaani GV Dev 5h.

| Model | Dataset Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 10 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 10 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | telephone_mp3 | 10 | 0.8109 | 0.4963 |

## Interpretation

- Larger Whisper models improved results on this tiny slice.
- `tiny` often hallucinated and produced mixed-script or unrelated output.
- `base` reduced hallucination but still had empty, wrong-script, or corrupted outputs.
- `small` produced mostly Devanagari output and had the best CER, but the WER is still high.

## Limitations

- This is only a 10-file smoke-test slice.
- Gramvaani transcripts include imperfect labels such as `<incomplete>` and may contain transcription noise.
- These numbers should not be presented as final benchmark results.
- Raw audio is not committed to the repository.

## Next Step

Expand the manifest to a larger fixed slice and begin Week 2 preprocessing ablations against the same baseline.
