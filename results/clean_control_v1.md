# Clean Control v1

This note compares clean Hindi read speech against the fixed GramVaani telephone-style Hindi slice.

Clean control dataset: FLEURS Hindi, 50 files

Clean manifest path in Colab/Drive:

```text
/content/drive/MyDrive/call-whisper/clean_control/fleurs_hi_50/fleurs_hi_clean_50.csv
```

## Clean Hindi Results

| Model | Slice | Condition | Files | WER | CER |
|---|---|---|---:|---:|---:|
| Whisper medium | fleurs_hi_clean_50 | clean_read_speech | 50 | 0.4363 | 0.1830 |
| Whisper large-v3 | fleurs_hi_clean_50 | clean_read_speech | 50 | 0.3112 | 0.1201 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | fleurs_hi_clean_50 | clean_read_speech | 50 | 0.1326 | 0.0475 |

## Clean vs Telephone Comparison

| Model | Clean Hindi WER | GramVaani Mixed WER | GramVaani 8 kHz WER | Clean -> Mixed Change |
|---|---:|---:|---:|---:|
| Whisper medium | 0.4363 | 0.7683 | 0.8108 | +0.3320 |
| Whisper large-v3 | 0.3112 | 0.5616 | 0.6511 | +0.2504 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | 0.1326 | 0.2597 | 0.2900 | +0.1271 |

## Interpretation

- All tested models perform better on clean FLEURS Hindi than on GramVaani telephone-style Hindi.
- The clean-to-telephone gap remains visible even for the Hindi-tuned ARTPARK model.
- Whisper `large-v3` improves substantially over Whisper `medium` on clean Hindi, but ARTPARK remains much stronger on this FLEURS slice.
- This supports the project framing: both model/domain fit and telephone-style audio conditions matter.
- These are fixed-slice results. FLEURS read speech and GramVaani spontaneous telephone-style speech differ in domain, channel, transcript style, and speaker conditions, so this is a practical control, not a perfectly isolated causal test.

## Reporting Language

Correct wording:

> On the 50-file FLEURS Hindi clean-control slice, Whisper `large-v3` achieved WER `0.3112`, while on the fixed GramVaani telephone-style slice it achieved WER `0.5616`.

> On the same FLEURS slice, `ARTPARK-IISc/whisper-medium-vaani-hindi` achieved WER `0.1326`, while on GramVaani it achieved WER `0.2597`.

Avoid:

> Telephone audio doubles WER in general.

The clean and telephone slices differ in more than channel alone.

## Source Files

```text
results/colab_fleurs_clean_control_summary.md
results/colab_whisper_medium_fleurs_hi_clean_50_seed0.json
results/colab_whisper_large_v3_fleurs_hi_clean_50_seed0.json
results/colab_hf_artpark_iisc_whisper_medium_vaani_hindi_fleurs_hi_clean_50_seed0.json
```
