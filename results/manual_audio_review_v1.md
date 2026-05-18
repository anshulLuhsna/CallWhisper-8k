# Manual Audio Review v1

Status: complete for the 15 flagged files below.

This file tracks the manual listening review requested by `results/error_analysis_v1.md`. These notes come from human listening of the copied review files in `results/manual_audio_review_files/`.

## Review Questions

- Is the speech understandable to a human?
- Is there background noise, music, echo, clipping, or multiple speakers?
- Does the reference transcript look complete?
- Did Whisper fail mainly because of audio quality, transcript quality, or model behavior?

## Human Review Summary

- Reviewed files: 15
- Main failure judged as model behavior: 9 files
- Main failure judged as audio quality: 6 files
- Main failure judged as transcript quality alone: 0 files
- Normalization clearly helped human listening: 2 files
- Normalization clearly hurt human listening: 1 file
- Normalization sounded mostly unchanged to the reviewer: most files

Interpretation:

- Many severe WER failures happened even when a human could understand the audio. These are useful model-behavior examples, not only bad-audio examples.
- Several audio-quality failures are real and should stay in limitations: muffled speech, unclear endings, apparent cuts, or very poor intelligibility.
- `<incomplete>` markers remain a metric caveat. Even when the transcript looked usable, the marker often corresponded to audio that sounded cut at the beginning or end.
- Volume normalization improved WER on several examples, but the human review usually did not hear a large audio-quality improvement. In one case it made the speaker harder to hear by lowering both speech and background music.

## Priority Files

| File | Why Review | Raw WER | Raw CER | Normalized WER | Normalized CER | Listening Notes |
|---|---|---:|---:|---:|---:|---|
| `02-12557-02` | normalization helped a lot; mixed-script hallucination in raw output | 1.273 | 1.171 | 0.727 | 0.315 | Understandable, low noise, transcript complete. Raw failure judged as model behavior. Normalized audio sounded identical to human reviewer, despite better WER/CER. |
| `02-19188-01` | normalization regression | 0.568 | 0.254 | 0.676 | 0.321 | Understandable, high background music, transcript complete. Failure judged as model behavior. Normalization reduced background music and speaker together, making speaker harder to hear. |
| `13-00240-05` | reference starts with `<incomplete>` | 0.458 | 0.190 | 0.458 | 0.190 | Understandable, high background music. Audio sounds like beginning is missing. Failure judged mostly as model behavior; normalized audio is quieter overall. |
| `01-02976-02` | reference ends with `<incomplete>`; high raw error | 1.000 | 0.904 | 1.000 | 0.592 | Mostly understandable, medium background noise. Audio sounds cut or sped near the end even before the incomplete tag. Failure judged as audio quality; normalized audio sounds the same. |
| `02-19849-01` | high WER short utterance | 1.167 | 0.765 | 1.000 | 0.676 | First half understandable, ending unclear. No obvious background noise. Failure judged as audio quality; normalized audio sounds the same. |

## Additional Flagged Files

| File | Why Review | Raw WER | Raw CER | Normalized WER | Normalized CER | Listening Notes |
|---|---|---:|---:|---:|---:|---|
| `01-06773-03` | worst raw WER; very short utterance | 1.000 | 0.684 | 1.000 | 0.684 | Two of three spoken words understandable, no background noise. Failure judged as model behavior. |
| `01-00748-01` | worst raw WER | 1.000 | 0.936 | 0.960 | 0.624 | Understandable, no background noise, transcript complete. Failure judged as model behavior. |
| `01-01598-02` | normalization improvement | 0.964 | 0.761 | 0.714 | 0.384 | Mostly not understandable to human reviewer, no background noise. Failure judged as audio quality. Normalization did not clearly help to human ears. |
| `02-19469-01` | normalization improvement; reference ends with `<incomplete>` | 1.000 | 0.563 | 0.750 | 0.418 | Understandable, no background noise. Audio sounds like ending is missing from transcript. Failure judged as model behavior. Normalization helped to human ears. |
| `01-02689-01` | normalization improvement; short utterance | 1.000 | 0.750 | 0.857 | 0.750 | Mostly understandable, no background noise, transcript complete. Failure judged as model behavior. Normalization helped to human ears. |
| `01-02494-03` | normalization regression by WER | 0.909 | 0.738 | 1.000 | 0.639 | Not understandable to human reviewer, no background noise. Failure judged as audio quality. Normalization sounds the same. |
| `01-08315-03` | normalization regression by WER but CER improved | 0.500 | 0.207 | 0.571 | 0.159 | Understandable, low background music, transcript complete. Failure judged as model behavior. Normalization did not hurt to human ears. |
| `01-05855-03` | normalization regression | 0.862 | 0.437 | 0.931 | 0.459 | Not understandable to human reviewer, no background noise, one transcript word appears wrong near the start. Failure judged as audio quality. Normalization did not hurt to human ears. |
| `01-08138-03` | normalization regression | 0.800 | 0.453 | 0.867 | 0.473 | Understandable, low background music, transcript complete. Failure judged as model behavior. Normalization sounds the same. |
| `01-05816-03` | reference ends with `<incomplete>` | 1.000 | 0.653 | 0.909 | 0.628 | Not understandable to human reviewer; worst audio quality among reviewed examples. Audio sounds like ending is missing from transcript. Failure judged as audio quality. |

## Audio Paths

Raw audio lives under:

```text
datasets/GV_Dev_5h/Audio/
```

Generated normalized audio lives under:

```text
results/raw/audio/gramvaani_dev_50_normalize/
```
