# Preprocessing v1

First preprocessing ablation on the 50-file Gramvaani GV Dev slice using Whisper `small`.

| Model | Dataset Slice | Condition | Files | WER | CER | Delta WER | Delta CER |
|---|---|---|---:|---:|---:|---:|---:|
| Whisper small | gramvaani_dev_50 | raw telephone MP3 | 50 | 0.8434 | 0.5598 | baseline | baseline |
| Whisper small | gramvaani_dev_50 | mono 16 kHz WAV | 50 | 0.8327 | 0.5240 | -0.0107 | -0.0358 |
| Whisper small | gramvaani_dev_50 | volume normalized WAV | 50 | 0.8223 | 0.5087 | -0.0210 | -0.0512 |
| Whisper small | gramvaani_dev_50 | telephone bandpass WAV | 50 | 0.8452 | 0.5709 | +0.0019 | +0.0111 |
| Whisper small | gramvaani_dev_50 | 8 kHz roundtrip WAV | 50 | 0.8468 | 0.5457 | +0.0034 | -0.0141 |

## Interpretation

- Simple conversion to mono 16 kHz WAV slightly improved WER and CER on this slice.
- Volume normalization improved more than plain WAV conversion on this slice.
- Telephone bandpass filtering slightly hurt WER and CER on this slice.
- 8 kHz roundtrip slightly hurt WER but improved CER compared with raw MP3.
- The change is small, so this should not be presented as a major improvement.
- Volume normalization is the best preprocessing method in this first ablation.

## Next Steps

- Inspect error examples for raw MP3 versus normalized WAV.
- Move to Week 3 adaptation only after writing a short error-analysis note.
