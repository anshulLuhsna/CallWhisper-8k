# Colab Benchmark Plan

This plan keeps the MacBook as the development machine and uses Colab/GPU for slower or stronger ASR checks.

## Goal

Verify local Whisper `small` findings on stronger models before making final claims.

Runnable notebooks are available in:

```text
notebooks/01_openai_whisper_gpu_benchmark.ipynb
notebooks/02_hindi_tuned_hf_models.ipynb
notebooks/03_decoding_adaptation_sweeps.ipynb
```

Minimum Colab table:

| Family | Model | Why |
|---|---|---|
| OpenAI Whisper | `small` | reproduce local reference result on GPU |
| OpenAI Whisper | `medium` | stronger vanilla Whisper baseline |
| Hindi-tuned Whisper | `ARTPARK-IISc/whisper-medium-vaani-hindi` | strong Hindi-tuned Whisper-family comparison |
| Hindi-tuned Whisper fallback | `vasista22/whisper-hindi-small` | older but lightweight Hindi fine-tune |
| Hindi-tuned Whisper fallback | `collabora/whisper-base-hindi` | compact Hindi-focused baseline |

Useful verified model pages:

- https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi
- https://huggingface.co/vasista22/whisper-hindi-small
- https://huggingface.co/collabora/whisper-base-hindi

## Dataset Inputs

Commit manifests only. Upload or mount raw audio separately.

Required manifests:

```text
datasets/manifests/gramvaani_dev_50.csv
datasets/manifests/gramvaani_dev_50_8khz.csv
datasets/manifests/gramvaani_dev_50_highrate.csv
```

Later, add:

```text
datasets/manifests/common_voice_hi_clean_10.csv
```

Do not upload raw audio to GitHub. In Colab, either:

- mount Google Drive containing `datasets/GV_Dev_5h/Audio/`, or
- upload the ignored local dataset directory directly to the Colab runtime.

## Colab Setup

```bash
git clone https://github.com/<owner>/callwhisper-8k.git
cd callwhisper-8k
python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m pip install transformers accelerate datasets evaluate soundfile
apt-get update && apt-get install -y ffmpeg
```

Set paths so manifests resolve:

```bash
export PYTHONPATH=src
```

If audio is mounted elsewhere, either mirror the repo-relative path:

```text
callwhisper-8k/datasets/GV_Dev_5h/Audio/
```

or rebuild manifests to point at the mounted audio path.

## OpenAI Whisper Runs

Start by reproducing local reference:

```bash
PYTHONPATH=src python -m callwhisper.eval \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --model small \
  --language-mode manifest \
  --seed 0 \
  --output-json results/colab_whisper_small_gramvaani_50_seed0.json
```

Then run stronger baseline:

```bash
PYTHONPATH=src python -m callwhisper.eval \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --model medium \
  --language-mode manifest \
  --seed 0 \
  --output-json results/colab_whisper_medium_gramvaani_50_seed0.json
```

Also run source-rate splits:

```bash
for slice in gramvaani_dev_50_8khz gramvaani_dev_50_highrate; do
  PYTHONPATH=src python -m callwhisper.eval \
    --manifest datasets/manifests/${slice}.csv \
    --model medium \
    --language-mode manifest \
    --seed 0 \
    --output-json results/colab_whisper_medium_${slice}_seed0.json
done
```

## Hindi-Tuned Model Runs

The current eval runner uses `openai-whisper`. Hindi-tuned Hugging Face models should be run through a small Transformers runner before comparing results.

Implementation:

- `src/callwhisper/eval/hf_runner.py` runs Hugging Face ASR models.
- It reuses `load_manifest()`, `score_row()`, `summarize()`, and `write_outputs()`.
- It saves JSON in the same schema as existing results.

First target:

```bash
PYTHONPATH=src python -m callwhisper.eval.hf_runner \
  --manifest datasets/manifests/gramvaani_dev_50.csv \
  --model-id ARTPARK-IISc/whisper-medium-vaani-hindi \
  --output-json results/colab_artpark_medium_vaani_hindi_gramvaani_50_seed0.json
```

Fallback targets if setup fails:

```bash
vasista22/whisper-hindi-small
collabora/whisper-base-hindi
```

## Reporting Rule

Report final numbers as:

> On the fixed GramVaani 50-file slice, model X changed WER/CER from A/B to C/D.

Do not claim that preprocessing or tuning fixes telephony ASR. Verify any promising local `small` result on at least one stronger or Hindi-tuned model before making it a headline.
