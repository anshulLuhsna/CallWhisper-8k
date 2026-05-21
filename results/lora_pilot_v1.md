# LoRA Pilot v1

This note summarizes the first Kaggle Whisper-small LoRA pilot run.

This is a compact-model adaptation experiment, not a final claim that the model is globally better. The fair comparison here is **base HF Whisper-small vs LoRA-adapted HF Whisper-small in the same evaluation pipeline**.

## Run Setup

| Field | Value |
|---|---|
| Base model | `openai/whisper-small` |
| Adapter method | LoRA |
| Train data | `GV_Train_100h` |
| Train clips | 3,200 |
| Internal eval clips | 200 |
| Steps | 800 |
| Seed | 0 |
| Duration filter | 1.0-30.0 seconds |
| LoRA target modules | `q_proj`, `v_proj` |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |

The frozen benchmark manifests were not used for training:

- `gramvaani_dev_50`
- `gramvaani_dev_50_8khz`
- `gramvaani_dev_50_highrate`

## Base vs LoRA Results

Macro WER/CER are means over per-file scores. Corpus WER/CER are computed over the full concatenated reference/hypothesis lists.

| Slice | Beams | Files | Base Macro WER | LoRA Macro WER | Delta Macro WER | Base Corpus WER | LoRA Corpus WER | Delta Corpus WER |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gramvaani_dev_50 | 1 | 50 | 1.5187 | 0.7473 | -0.7714 | 1.2446 | 0.7129 | -0.5317 |
| gramvaani_dev_50 | 5 | 50 | 1.0303 | 0.7532 | -0.2771 | 0.9439 | 0.7386 | -0.2053 |
| gramvaani_dev_50_8khz | 1 | 32 | 1.7725 | 0.8708 | -0.9016 | 1.3547 | 0.8512 | -0.5035 |
| gramvaani_dev_50_8khz | 5 | 32 | 1.1595 | 0.8946 | -0.2649 | 1.0473 | 0.9166 | -0.1307 |
| gramvaani_dev_50_highrate | 1 | 18 | 1.0675 | 0.5277 | -0.5398 | 1.0947 | 0.5246 | -0.5701 |
| gramvaani_dev_50_highrate | 5 | 18 | 0.8006 | 0.5018 | -0.2988 | 0.8030 | 0.4962 | -0.3068 |

## Interpretation

- The LoRA adapter produced a clear adaptation signal against base HF Whisper-small on every frozen GramVaani slice and both beam settings.
- Beam 5 remained stronger for the high-rate subset after adaptation, but beam 1 was slightly better on the mixed and 8 kHz slices in this run.
- These scores should not be compared directly against earlier OpenAI Whisper CLI results as if the pipeline were identical. Use this note for same-pipeline base-vs-LoRA conclusions.
- The adapted model does not yet beat the strongest Hindi-tuned public model measured earlier (`ARTPARK-IISc/whisper-medium-vaani-hindi`), but it substantially improves the compact Whisper-small baseline.

## Artifacts

Final adapter and processor:

```text
models/whisper-small-lora-gramvaani-pilot-seed0/final_adapter/
models/whisper-small-lora-gramvaani-pilot-seed0/processor/
```

Detailed JSON, splits, config, package versions, and per-sample predictions:

```text
results/lora_pilot_seed0/
```

## Reproduce Adapter Evaluation

The adapter can be reloaded from the committed repo artifact and evaluated against the frozen GramVaani manifests:

```bash
pip install -e ".[finetune]"

callwhisper-lora-eval \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --manifest datasets/manifests/gramvaani_dev_50_8khz.csv \
  --manifest datasets/manifests/gramvaani_dev_50_highrate.csv \
  --adapter-dir models/whisper-small-lora-gramvaani-pilot-seed0/final_adapter \
  --processor-dir models/whisper-small-lora-gramvaani-pilot-seed0/processor \
  --output-dir results/lora_reload_eval
```

This evaluates base HF Whisper-small and the LoRA-adapted Whisper-small through the same Hugging Face generation path, then writes per-sample JSON plus Markdown summary tables.

Source Kaggle archive retained locally but not committed:

```text
callwhisper_lora_pilot_seed0_artifacts.tar.gz
```
