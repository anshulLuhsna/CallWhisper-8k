# GPU Notebooks

These notebooks are designed for hosted GPU runs. The MacBook remains the development and quick-test machine; Colab/Kaggle is for slower model comparison and adaptation sweeps.

For the expanded GramVaani 100-file benchmark, use the clean one-click Colab notebook:

```text
09_gramvaani_100_colab_clean.ipynb
```

It mounts Drive, clones the repo from a stable working directory, validates the expected `GV_Dev_5h` folder, runs Whisper `medium`, Whisper `large-v3`, and ARTPARK Vaani Hindi once each, derives all three fixed v2 slices from the same predictions, streams live progress, checkpoints after every model, and saves JSON/Markdown/CSV results to `MyDrive/call-whisper/results/benchmark_v2/`.

`08_gramvaani_100_colab_benchmark.ipynb` is superseded by notebook 09 and should not be used for new runs.

The equivalent step-by-step version remains available as:

```text
COLAB_BENCHMARK_V2_RUNBOOK.md
```

Run order:

1. `01_openai_whisper_gpu_benchmark.ipynb`
2. `02_hindi_tuned_hf_models.ipynb`
3. `03_decoding_adaptation_sweeps.ipynb`
4. `04_fleurs_clean_control.ipynb`
5. `05_whisper_small_lora_edge_smoke.ipynb` - Kaggle-first LoRA smoke notebook
6. `06_lora_reload_eval_colab_report.ipynb` - Colab reload/eval notebook for the committed LoRA adapter and Excel-ready report tables
7. `07_whisper_large_v3_challenger.ipynb` - Kaggle-first non-ARTPARK Whisper large-v3 LoRA notebook for the ambitious "beat public ARTPARK on fixed GramVaani slices" experiment
8. `08_gramvaani_100_colab_benchmark.ipynb` - one-click Colab GPU benchmark for the expanded 100-file GramVaani comparison
9. `09_gramvaani_100_colab_clean.ipynb` - canonical clean Colab run; one inference pass per model with immediate Drive checkpoints
10. `10_gv_train_100h_inventory_colab.ipynb` - CPU Colab inventory of GV Train 100h with frozen-ID exclusion and persistent Drive outputs; stops before training
11. `11_vaani_paired_telephony_benchmark_colab.ipynb` - CPU Colab construction of the revision-pinned 500-speaker Vaani paired-channel pilot; stops before model inference

Notebook 11 requires accepted access to the gated [`ARTPARK-IISc/Vaani-Benchmark-V1.0`](https://huggingface.co/datasets/ARTPARK-IISc/Vaani-Benchmark-V1.0) dataset and a read-only `HF_TOKEN` in Colab Secrets. It downloads the exact pinned revision, infers and records the dataset schema, exports audio without TorchCodec decoding, then saves source plus per-condition archives under:

```text
MyDrive/call-whisper/results/vaani_paired_pilot_v1/
```

Use a CPU runtime. Do not spend a GPU session on benchmark construction.

Before running, put the GramVaani audio somewhere Colab can access. The notebooks now expect this Google Drive layout:

```text
MyDrive/call-whisper/
  GV_Dev_5h/
  Metadata/
  manifests/
  notebooks/
```

In Colab this becomes:

```text
/content/drive/MyDrive/call-whisper/
```

The notebooks clone:

```text
https://github.com/anshulLuhsna/CallWhisper-8k.git
```

Then they symlink:

```text
/content/drive/MyDrive/call-whisper/GV_Dev_5h -> /content/CallWhisper-8k/datasets/GV_Dev_5h
/content/drive/MyDrive/call-whisper/Metadata -> /content/CallWhisper-8k/datasets/Metadata
```

They also copy CSV files from `MyDrive/call-whisper/manifests/` into `datasets/manifests/` inside the cloned repo.

The notebooks do not commit or redistribute raw audio.

`04_fleurs_clean_control.ipynb` expects the clean-control manifest created from FLEURS Hindi at:

```text
MyDrive/call-whisper/clean_control/fleurs_hi_50/fleurs_hi_clean_50.csv
```

`05_whisper_small_lora_edge_smoke.ipynb` is the compact fine-tuning notebook. It defaults to the `pilot` profile: train Whisper-small LoRA on `GV_Train_100h`, filter clips to 1-30 seconds, save exact split/config artifacts, and evaluate base HF Whisper-small versus LoRA on the frozen GramVaani manifests. It can still run a `smoke` profile from `GV_Dev_5h` while excluding frozen benchmark IDs, but that is only a pipeline check.

For Kaggle, create a Kaggle Dataset and attach it with **Add Input**. Notebook 05 can also download both labelled GramVaani splits directly from OpenSLR if Kaggle internet is enabled, then save the original tarballs under `/kaggle/working/saved_datasets/` so they can become a reusable Kaggle Dataset after the run. Extracted working copies are placed under `/kaggle/temp/data/` to avoid saving duplicate MP3 folders in the notebook output.

Minimum attached dataset layout:

```text
GV_Dev_5h/
  Audio/*.mp3
  text
  mp3.scp
  uttids
  utt2labels
```

For a serious run, also upload a separate training split:

```text
GV_Train_100h/
  Audio/*.mp3
  text
  mp3.scp
  uttids
  utt2labels
```

Kaggle outputs are written to `/kaggle/working/checkpoints/`, `/kaggle/working/results/`, and `/kaggle/working/saved_datasets/`.

Notebook 05 saves these dataset archives when downloads are enabled:

```text
/kaggle/working/saved_datasets/GV_Dev_5h.tar.gz
/kaggle/working/saved_datasets/GV_Train_100h.tar.gz
/kaggle/working/saved_datasets/gramvaani_saved_datasets.json
```

Notebook 05 also saves reproducibility/evaluation artifacts under:

```text
/kaggle/working/results/whisper_small_lora_pilot/
  *_run_config.json
  *_package_versions.json
  *_train_split.csv
  *_internal_eval_split.csv
  *_excluded_rows.csv
  *_eval_summary.json
  *_base_vs_lora_comparison.md
```

`06_lora_reload_eval_colab_report.ipynb` is the follow-up reporting notebook. It does not train. It clones the repo, mounts Google Drive, symlinks `MyDrive/call-whisper/GV_Dev_5h` into the repo, reloads the committed adapter under `models/whisper-small-lora-gramvaani-pilot-seed0/`, evaluates base HF Whisper-small versus the LoRA adapter, and writes Excel/CSV/JSON/Markdown outputs to:

```text
MyDrive/call-whisper/results/lora_reload_eval_colab/
```

`07_whisper_large_v3_challenger.ipynb` is the next ambitious training notebook. It starts from `openai/whisper-large-v3`, trains a LoRA adapter on `GV_Train_100h`, excludes frozen benchmark IDs, and writes public-ARTPARK-vs-independent-challenger summaries under:

```text
/kaggle/working/results/whisper_large_v3_challenger_v1/
```
