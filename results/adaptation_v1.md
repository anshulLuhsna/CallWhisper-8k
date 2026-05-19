# Adaptation v1

This note summarizes the first non-training adaptation sweep on the fixed 50-file GramVaani GV Dev slice.

Model: Whisper `large-v3`

Slice: `gramvaani_dev_50`

Condition: raw `telephone_mp3`

## Results

| Experiment | Files | WER | CER | Change vs Baseline |
|---|---:|---:|---:|---:|
| baseline_manifest_seed0 | 50 | 0.5616 | 0.3057 | baseline |
| beam_5_seed0 | 50 | 0.5248 | 0.2861 | -0.0368 WER |
| beam_1_seed0 | 50 | 0.5594 | 0.3065 | -0.0022 WER |
| language_hi_seed0 | 50 | 0.5616 | 0.3057 | no change |
| no_previous_text_seed0 | 50 | 0.5616 | 0.3057 | no change |
| temperature_0_seed0 | 50 | 0.5982 | 0.3272 | +0.0366 WER |
| hindi_prompt_seed0 | 50 | 0.6493 | 0.3967 | +0.0877 WER |
| temperature_02_seed0 | 50 | 0.6586 | 0.3855 | +0.0970 WER |
| language_auto_seed0 | 50 | 0.6685 | 0.4654 | +0.1069 WER |

## Interpretation

- Beam search helped on this slice. `beam_size=5` improved WER from `0.5616` to `0.5248`.
- Forcing Hindi produced the same result as the manifest Hindi hint on this run.
- Disabling `condition_on_previous_text` did not change the aggregate result.
- Auto language detection hurt WER and CER on this slice.
- The Hindi prompt hurt results on this slice. Do not assume prompt biasing helps without measuring it.
- Temperature changes hurt compared with the default decoding behavior in this run.

## Reporting Language

Correct wording:

> On the fixed GramVaani 50-file slice, Whisper `large-v3` with `beam_size=5` changed WER from `0.5616` to `0.5248`.

Avoid:

> Beam search fixes telephony ASR.

## Source Files

```text
results/results/results/colab_adaptation_large-v3_summary.md
results/results/results/colab_adaptation_large-v3_baseline_manifest_seed0.json
results/results/results/colab_adaptation_large-v3_beam_1_seed0.json
results/results/results/colab_adaptation_large-v3_beam_5_seed0.json
results/results/results/colab_adaptation_large-v3_hindi_prompt_seed0.json
results/results/results/colab_adaptation_large-v3_language_auto_seed0.json
results/results/results/colab_adaptation_large-v3_language_hi_seed0.json
results/results/results/colab_adaptation_large-v3_no_previous_text_seed0.json
results/results/results/colab_adaptation_large-v3_temperature_0_seed0.json
results/results/results/colab_adaptation_large-v3_temperature_02_seed0.json
```
