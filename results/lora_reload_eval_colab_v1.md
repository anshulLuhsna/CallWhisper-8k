# LoRA Reload Eval Colab v1

This note records the Colab reload evaluation of the committed Whisper-small LoRA adapter. The goal was to verify that the adapter saved from the Kaggle pilot can be reloaded from the repository and evaluated through the same Hugging Face pipeline as the base model.

This is a same-pipeline comparison: **base HF Whisper-small vs LoRA-adapted HF Whisper-small**. It should not be read as a claim that the adapter beats stronger Hindi-tuned systems such as ARTPARK or Whisper large-v3.

## Run Setup

| Item | Value |
|---|---|
| Base model | `openai/whisper-small` |
| Adapter | `models/whisper-small-lora-gramvaani-pilot-seed0/final_adapter` |
| Processor | `models/whisper-small-lora-gramvaani-pilot-seed0/processor` |
| Runtime | Colab T4 GPU |
| Evaluation runner | `callwhisper.eval.lora_runner` |
| Language mode | `manifest` |
| Decoding | beam 1 and beam 5 |
| Report source | `whisper-small-lora-gramvaani-pilot-seed0_colab_reload_report_tables.xlsx` |

## Base vs LoRA Results

| slice                     | condition         | num_beams | files | macro_wer_base | macro_wer_lora | delta_macro_wer | macro_cer_base | macro_cer_lora | delta_macro_cer | corpus_wer_base | corpus_wer_lora | delta_corpus_wer |
| ------------------------- | ----------------- | --------- | ----- | -------------- | -------------- | --------------- | -------------- | -------------- | --------------- | --------------- | --------------- | ---------------- |
| fleurs_hi_clean_50        | clean_read_speech | 1         | 50    | 0.7686         | 0.5236         | -0.2450         | 0.4317         | 0.2074         | -0.2244         | 0.6909          | 0.5162          | -0.1747          |
| fleurs_hi_clean_50        | clean_read_speech | 5         | 50    | 0.5667         | 0.5128         | -0.0539         | 0.2822         | 0.1944         | -0.0878         | 0.5573          | 0.5051          | -0.0522          |
| gramvaani_dev_50          | telephone_mp3     | 1         | 50    | 1.5187         | 0.7473         | -0.7714         | 1.3071         | 0.4671         | -0.8400         | 1.2446          | 0.7129          | -0.5317          |
| gramvaani_dev_50          | telephone_mp3     | 5         | 50    | 1.0292         | 0.7532         | -0.2760         | 0.7571         | 0.5772         | -0.1798         | 0.9431          | 0.7386          | -0.2045          |
| gramvaani_dev_50_8khz     | telephone_mp3     | 1         | 32    | 1.7725         | 0.8708         | -0.9016         | 1.6367         | 0.5823         | -1.0543         | 1.3547          | 0.8512          | -0.5035          |
| gramvaani_dev_50_8khz     | telephone_mp3     | 5         | 32    | 1.1579         | 0.8946         | -0.2633         | 0.9158         | 0.7869         | -0.1289         | 1.0459          | 0.9166          | -0.1293          |
| gramvaani_dev_50_highrate | telephone_mp3     | 1         | 18    | 1.0675         | 0.5277         | -0.5398         | 0.7213         | 0.2622         | -0.4590         | 1.0947          | 0.5246          | -0.5701          |
| gramvaani_dev_50_highrate | telephone_mp3     | 5         | 18    | 0.8006         | 0.5018         | -0.2988         | 0.4748         | 0.2044         | -0.2704         | 0.8030          | 0.4962          | -0.3068          |

## Interpretation

- On this Colab reload run, the LoRA adapter reduced WER and CER versus base HF Whisper-small on every evaluated slice.
- The largest macro WER reductions appeared on the GramVaani telephone-style slices, especially the 8 kHz subset under beam 1.
- The FLEURS clean-control result also improved versus base HF Whisper-small, which is encouraging because it does not show an obvious clean-speech regression on this small slice.
- Beam 1 and beam 5 behave differently after adaptation. Beam 1 is strongest on the mixed GramVaani and 8 kHz GramVaani slices in this run, while beam 5 remains strongest on the high-rate GramVaani subset and FLEURS clean control.

## Report Artifacts

CSV exports are stored in:

```text
results/lora_reload_eval_colab/
```

Generated files:

```text
whisper-small-lora-gramvaani-pilot-seed0_colab_reload_summary.csv
whisper-small-lora-gramvaani-pilot-seed0_colab_reload_base_vs_lora_comparison.csv
whisper-small-lora-gramvaani-pilot-seed0_colab_reload_per_sample_predictions.csv
```

## Claim Boundary

Careful wording:

> On these fixed slices, the committed Whisper-small LoRA adapter reduced WER versus base HF Whisper-small when both were evaluated through the same Hugging Face pipeline.

Do not claim:

> This adapter beats all Hindi ASR models.

The next ambitious benchmark target is to adapt and evaluate a stronger Hindi-tuned checkpoint such as `ARTPARK-IISc/whisper-medium-vaani-hindi` against its public baseline on the same frozen slices.
