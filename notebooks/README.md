# Colab Notebooks

These notebooks are designed for Google Colab/GPU runs. The MacBook remains the development and quick-test machine; Colab is for slower model comparison and adaptation sweeps.

Run order:

1. `01_openai_whisper_gpu_benchmark.ipynb`
2. `02_hindi_tuned_hf_models.ipynb`
3. `03_decoding_adaptation_sweeps.ipynb`

Before running, put the GramVaani audio somewhere Colab can access. The notebooks expect either:

- `datasets/GV_Dev_5h/Audio/` already exists inside the cloned repo, or
- Google Drive contains `MyDrive/callwhisper-8k/datasets/GV_Dev_5h/Audio/`

The notebooks do not commit or redistribute raw audio.
