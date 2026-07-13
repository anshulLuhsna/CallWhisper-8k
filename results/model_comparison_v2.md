# Model Comparison v2

This is the expanded GPU comparison on the fixed GramVaani 100-file telephone-style Hindi slice. Each model transcribed the same 100 files once. The 56-file native 8 kHz and 44-file higher-rate views were derived from those exact per-file predictions rather than decoded again.

## Results

| model                                   | slice                      | condition     |   files |    wer |    cer | file                                                                                   |
|:----------------------------------------|:---------------------------|:--------------|--------:|-------:|-------:|:---------------------------------------------------------------------------------------|
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100          | telephone_mp3 |     100 | 0.2565 | 0.1275 | colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_100_seed0.json          |
| large-v3                                | gramvaani_dev_100          | telephone_mp3 |     100 | 0.5182 | 0.278  | colab_whisper_large_v3_gramvaani_dev_100_seed0.json                                    |
| medium                                  | gramvaani_dev_100          | telephone_mp3 |     100 | 0.7182 | 0.4316 | colab_whisper_medium_gramvaani_dev_100_seed0.json                                      |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100_8khz     | telephone_mp3 |      56 | 0.3091 | 0.165  | colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_100_8khz_seed0.json     |
| large-v3                                | gramvaani_dev_100_8khz     | telephone_mp3 |      56 | 0.6083 | 0.3505 | colab_whisper_large_v3_gramvaani_dev_100_8khz_seed0.json                               |
| medium                                  | gramvaani_dev_100_8khz     | telephone_mp3 |      56 | 0.7889 | 0.4962 | colab_whisper_medium_gramvaani_dev_100_8khz_seed0.json                                 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100_highrate | telephone_mp3 |      44 | 0.1895 | 0.0798 | colab_hf_artpark_iisc_whisper_medium_vaani_hindi_gramvaani_dev_100_highrate_seed0.json |
| large-v3                                | gramvaani_dev_100_highrate | telephone_mp3 |      44 | 0.4036 | 0.1856 | colab_whisper_large_v3_gramvaani_dev_100_highrate_seed0.json                           |
| medium                                  | gramvaani_dev_100_highrate | telephone_mp3 |      44 | 0.6281 | 0.3494 | colab_whisper_medium_gramvaani_dev_100_highrate_seed0.json                             |

## Finding

On the fixed mixed 100-file slice, ARTPARK Vaani Hindi changed WER from Whisper large-v3's `0.5182` to `0.2565`. On the native 8 kHz subset, the corresponding WERs were `0.6083` and `0.3091`. ARTPARK had the lowest WER and CER on every reported slice.

All three models had higher error on the native 8 kHz subset than on the higher-rate subset. This is an observed benchmark gap, not proof that source sample rate alone caused it: the groups may also differ in speakers, topics, noise, recording quality, and transcript quality.

## Reproducibility

- GPU: Tesla T4
- Seed: `0`
- Repo commit evaluated: `0bc28cf28b70b4154aac17f7d5344ac81885e805`
- Python: `3.12.13`
- PyTorch: `2.11.0+cu128`
- Transformers: `4.57.6`
- OpenAI Whisper: `20250625`
- Runtime metadata: `results/benchmark_v2/model_comparison_v2_run_metadata.json`
- Per-sample prediction JSON: `results/benchmark_v2/`

These fixed-slice results compare models under one reproducible pipeline. They are not a global Hindi ASR leaderboard.
