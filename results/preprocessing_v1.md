# Preprocessing v1

First preprocessing ablation on the 50-file Gramvaani GV Dev slice using Whisper `small`.

| Model | Dataset Slice | Condition | Files | WER | CER | Delta WER | Delta CER |
|---|---|---|---:|---:|---:|---:|---:|
| Whisper small | gramvaani_dev_50 | raw telephone MP3 | 50 | 0.8434 | 0.5598 | baseline | baseline |
| Whisper small | gramvaani_dev_50 | mono 16 kHz WAV | 50 | 0.8327 | 0.5240 | -0.0107 | -0.0358 |
| Whisper small | gramvaani_dev_50 | volume normalized WAV | 50 | 0.8223 | 0.5087 | -0.0210 | -0.0512 |

## Interpretation

- Simple conversion to mono 16 kHz WAV slightly improved WER and CER on this slice.
- Volume normalization improved more than plain WAV conversion on this slice.
- The change is small, so this should not be presented as a major improvement.
- This result is useful because it gives us a clean preprocessing baseline before trying stronger transforms.

## Next Steps

- Test telephone bandpass filtering.
- Test 8 kHz roundtrip conversion.
