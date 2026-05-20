# GPU Notebooks

These notebooks are designed for hosted GPU runs. The MacBook remains the development and quick-test machine; Colab/Kaggle is for slower model comparison and adaptation sweeps.

Run order:

1. `01_openai_whisper_gpu_benchmark.ipynb`
2. `02_hindi_tuned_hf_models.ipynb`
3. `03_decoding_adaptation_sweeps.ipynb`
4. `04_fleurs_clean_control.ipynb`
5. `05_whisper_small_lora_edge_smoke.ipynb` - Kaggle-first LoRA smoke notebook

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
