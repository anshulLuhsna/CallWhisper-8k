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

`05_whisper_small_lora_edge_smoke.ipynb` is the first compact fine-tuning notebook. It can run a smoke test from `GV_Dev_5h` while excluding frozen benchmark IDs, but any serious result should use a separate training split such as `GV_Train_100h`.

For Kaggle, create a Kaggle Dataset and attach it with **Add Input**. The notebook can also download GramVaani directly from OpenSLR if Kaggle internet is enabled, but uploading once as a Kaggle Dataset is more repeatable.

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

Kaggle outputs are written to `/kaggle/working/checkpoints/` and `/kaggle/working/results/`.

If no `GV_Train_100h` input is attached, notebook 05 can download `GV_Train_100h.tar.gz` from OpenSLR into `/kaggle/working/data`. This is about 2 GB before extraction.
