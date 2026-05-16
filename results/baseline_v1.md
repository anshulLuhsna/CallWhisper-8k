# Baseline v1

Initial Week 1 baseline on Gramvaani GV Dev 5h.

| Model | Dataset Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper tiny | gramvaani_dev_10 | telephone_mp3 | 10 | 1.5256 | 1.5637 |
| Whisper base | gramvaani_dev_10 | telephone_mp3 | 10 | 0.9981 | 0.9250 |
| Whisper small | gramvaani_dev_10 | telephone_mp3 | 10 | 0.8109 | 0.4963 |
| Whisper small | gramvaani_dev_50 | telephone_mp3 | 50 | 0.8434 | 0.5598 |

## Interpretation

- Larger Whisper models improved results on this tiny slice.
- `tiny` often hallucinated and produced mixed-script or unrelated output.
- `base` reduced hallucination but still had empty, wrong-script, or corrupted outputs.
- `small` produced mostly Devanagari output and had the best CER, but the WER is still high.
- On the larger 50-file slice, Whisper `small` stayed in the same high-error range: WER 0.8434 and CER 0.5598.

## Limitations

- The 10-file results are smoke tests; the 50-file `small` result is a stronger early baseline but still small.
- Gramvaani transcripts include imperfect labels such as `<incomplete>` and may contain transcription noise.
- These numbers should not be presented as final benchmark results.
- Raw audio is not committed to the repository.

## Next Step

Begin Week 2 preprocessing ablations against `gramvaani_dev_50` using Whisper `small` as the local reference model.
