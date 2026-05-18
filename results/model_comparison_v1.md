# Model Comparison v1

This note summarizes the Colab/GPU model comparison runs saved under `results/results/`.

The benchmark slice is GramVaani GV Dev, using the same fixed 50-file manifest and the source-sample-rate splits created earlier.

## Results

| Model | Slice | Files | WER | CER |
|---|---|---:|---:|---:|
| Whisper small | gramvaani_dev_50 | 50 | 0.8697 | 0.5540 |
| Whisper medium | gramvaani_dev_50 | 50 | 0.7683 | 0.4860 |
| Whisper medium | gramvaani_dev_50_8khz | 32 | 0.8108 | 0.5060 |
| Whisper medium | gramvaani_dev_50_highrate | 18 | 0.6584 | 0.3858 |
| Whisper large-v3 | gramvaani_dev_50 | 50 | 0.5616 | 0.3057 |
| Whisper large-v3 | gramvaani_dev_50_8khz | 32 | 0.6511 | 0.3798 |
| Whisper large-v3 | gramvaani_dev_50_highrate | 18 | 0.3984 | 0.1665 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_50 | 50 | 0.2597 | 0.1298 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_50_8khz | 32 | 0.2900 | 0.1581 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_50_highrate | 18 | 0.2057 | 0.0794 |

## Key Comparisons

| Comparison | Slice | WER Change |
|---|---|---:|
| Whisper medium -> Whisper large-v3 | gramvaani_dev_50 | 0.7683 -> 0.5616 |
| Whisper large-v3 -> ARTPARK Hindi-tuned Whisper | gramvaani_dev_50 | 0.5616 -> 0.2597 |
| Whisper large-v3 -> ARTPARK Hindi-tuned Whisper | gramvaani_dev_50_8khz | 0.6511 -> 0.2900 |
| Whisper large-v3 -> ARTPARK Hindi-tuned Whisper | gramvaani_dev_50_highrate | 0.3984 -> 0.2057 |

## Interpretation

- Model scaling helps: Whisper `large-v3` reduced mixed-slice WER from `0.7683` with Whisper `medium` to `0.5616`.
- Hindi/domain tuning helps much more on this slice: `ARTPARK-IISc/whisper-medium-vaani-hindi` reduced mixed-slice WER from `0.5616` with Whisper `large-v3` to `0.2597`.
- The true 8 kHz subset remains harder than the 44.1/48 kHz subset across models.
- Even after Hindi/domain tuning, the 8 kHz subset has higher WER (`0.2900`) than the high-rate subset (`0.2057`).
- These are slice-specific results. They should be reported as fixed-manifest benchmark findings, not as claims that one model is globally best for Hindi ASR.

## Source Files

OpenAI Whisper outputs:

```text
results/results/colab_openai_whisper_summary.md
results/results/colab_whisper_small_gramvaani_dev_50_seed0.json
results/results/colab_whisper_medium_gramvaani_dev_50_seed0.json
results/results/colab_whisper_medium_gramvaani_dev_50_8khz_seed0.json
results/results/colab_whisper_medium_gramvaani_dev_50_highrate_seed0.json
results/results/colab_whisper_large_v3_gramvaani_dev_50_seed0.json
results/results/colab_whisper_large_v3_gramvaani_dev_50_8khz_seed0.json
results/results/colab_whisper_large_v3_gramvaani_dev_50_highrate_seed0.json
```

Hindi-tuned Hugging Face outputs:

```text
results/results/colab_hf_model_summary.md
results/results/colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_50_seed0.json
results/results/colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_50_8khz_seed0.json
results/results/colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_50_highrate_seed0.json
```
