# Colab Benchmark v2 Runbook

> **Recommended:** use `notebooks/09_gramvaani_100_colab_clean.ipynb` and select **Runtime > Run all**. The cells below remain as a manual reference.

This runbook evaluates the expanded GramVaani 100-file benchmark slice.

The MacBook is only for manifest/data work. Use Colab/Kaggle GPU for these model runs.

## Goal

Create:

```text
results/model_comparison_v2.md
results/model_comparison_v2.json
```

using these manifests:

```text
datasets/manifests/gramvaani_dev_100.csv
datasets/manifests/gramvaani_dev_100_8khz.csv
datasets/manifests/gramvaani_dev_100_highrate.csv
```

## Required Data

Google Drive should contain:

```text
MyDrive/call-whisper/GV_Dev_5h/
  Audio/*.mp3
  text
  mp3.scp
  uttids
  utt2labels
```

The manifests are committed to the repo. Do not upload raw audio to GitHub.

## Colab Setup Cell

```python
from google.colab import drive
drive.mount("/content/drive")

!nvidia-smi
!python -m pip install -U pip
!apt-get update -qq
!apt-get install -y -qq ffmpeg
!rm -rf /content/CallWhisper-8k
!git clone https://github.com/anshulLuhsna/CallWhisper-8k.git /content/CallWhisper-8k
%cd /content/CallWhisper-8k

!python -m pip install -e ".[dev]"
!python -m pip install transformers accelerate datasets evaluate soundfile librosa jiwer

from pathlib import Path

repo_data = Path("/content/CallWhisper-8k/datasets/GV_Dev_5h")
drive_data = Path("/content/drive/MyDrive/call-whisper/GV_Dev_5h")

if repo_data.exists() or repo_data.is_symlink():
    repo_data.unlink()
repo_data.symlink_to(drive_data)

print("Audio files:", len(list((repo_data / "Audio").glob("*.mp3"))))
```

## Manifests

```python
MANIFESTS = [
    "datasets/manifests/gramvaani_dev_100.csv",
    "datasets/manifests/gramvaani_dev_100_8khz.csv",
    "datasets/manifests/gramvaani_dev_100_highrate.csv",
]
```

## OpenAI Whisper Runs

Run `medium` first. Run `large-v3` after `medium` succeeds.

```python
import subprocess
import os
from pathlib import Path

OPENAI_MODELS = ["medium", "large-v3"]
MANIFESTS = [
    "datasets/manifests/gramvaani_dev_100.csv",
    "datasets/manifests/gramvaani_dev_100_8khz.csv",
    "datasets/manifests/gramvaani_dev_100_highrate.csv",
]

Path("results/benchmark_v2").mkdir(parents=True, exist_ok=True)

for model in OPENAI_MODELS:
    for manifest in MANIFESTS:
        slice_name = Path(manifest).stem
        output = f"results/benchmark_v2/colab_whisper_{model}_{slice_name}_seed0.json"
        cmd = [
            "python",
            "-m",
            "callwhisper.eval",
            "--manifest",
            manifest,
            "--model",
            model,
            "--language-mode",
            "manifest",
            "--seed",
            "0",
            "--output-json",
            output,
        ]
        print("RUN:", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True, env={**os.environ, "PYTHONPATH": "src"})
```

## Hindi-Tuned Hugging Face Runs

Run ARTPARK medium first.

Optional next target: `ARTPARK-IISc/whisper-large-v3-vaani-hindi`, if GPU memory allows.

```python
import subprocess
import os
from pathlib import Path

HF_MODELS = [
    "ARTPARK-IISc/whisper-medium-vaani-hindi",
    # "ARTPARK-IISc/whisper-large-v3-vaani-hindi",
]

MANIFESTS = [
    "datasets/manifests/gramvaani_dev_100.csv",
    "datasets/manifests/gramvaani_dev_100_8khz.csv",
    "datasets/manifests/gramvaani_dev_100_highrate.csv",
]

Path("results/benchmark_v2").mkdir(parents=True, exist_ok=True)

def safe_model_name(model_id: str) -> str:
    return model_id.lower().replace("/", "_").replace("-", "_")

for model_id in HF_MODELS:
    for manifest in MANIFESTS:
        slice_name = Path(manifest).stem
        output = f"results/benchmark_v2/colab_hf_{safe_model_name(model_id)}_{slice_name}_seed0.json"
        cmd = [
            "python",
            "-m",
            "callwhisper.eval.hf_runner",
            "--manifest",
            manifest,
            "--model-id",
            model_id,
            "--language-mode",
            "manifest",
            "--seed",
            "0",
            "--output-json",
            output,
        ]
        print("RUN:", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True, env={**os.environ, "PYTHONPATH": "src"})
```

## Summary Table Cell

```python
import json
from pathlib import Path

import pandas as pd

rows = []
for path in sorted(Path("results/benchmark_v2").glob("*.json")):
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary = payload["summary"]
    samples = payload["samples"]
    first = samples[0]
    rows.append({
        "file": str(path),
        "model": first["model"],
        "slice": first["slice"],
        "condition": first["condition"],
        "files": summary["num_files"],
        "wer": round(summary["wer"], 4),
        "cer": round(summary["cer"], 4),
    })

df = pd.DataFrame(rows).sort_values(["slice", "model"])
summary_md = df.to_markdown(index=False)
Path("results/model_comparison_v2.md").write_text(
    "# Model Comparison v2\n\n" + summary_md + "\n",
    encoding="utf-8",
)
Path("results/model_comparison_v2.json").write_text(
    df.to_json(orient="records", force_ascii=False, indent=2),
    encoding="utf-8",
)
print(summary_md)
```

## Save Back To Drive

```python
from pathlib import Path
import shutil

drive_out = Path("/content/drive/MyDrive/call-whisper/results/benchmark_v2")
drive_out.mkdir(parents=True, exist_ok=True)

for path in Path("results/benchmark_v2").glob("*.json"):
    shutil.copy2(path, drive_out / path.name)

for path in [
    Path("results/model_comparison_v2.md"),
    Path("results/model_comparison_v2.json"),
]:
    shutil.copy2(path, drive_out / path.name)

print("Saved to", drive_out)
```

## Interpretation Rule

Do not compare these numbers as a global ASR leaderboard.

Correct wording:

> On the fixed GramVaani 100-file slice, model X got WER A and CER B. On the native 8 kHz subset, it got WER C and CER D.

Incorrect wording:

> Model X is the best Hindi ASR model.
