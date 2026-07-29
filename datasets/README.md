# Datasets

CallWhisper-8k does not redistribute raw speech. Keep downloaded audio in local
or mounted storage and commit only manifests, scripts, metadata audits, and
aggregate results.

## Datasets Used

| Dataset | Project role | Access and use notes |
|---|---|---|
| GramVaani GV Dev 5h | Initial real telephone-style Hindi benchmark and manual error review | Obtain from the upstream OpenSLR/GramVaani release. Academic and commercial terms may differ; follow the publisher's current terms. |
| GramVaani GV Train 100h | LoRA pilot and serious Adalat adaptation | Raw audio is not committed. The serious split is recording-group-disjoint because released speaker IDs are unavailable. |
| Vaani Benchmark V1.0 | 500-speaker paired, multi-reference telephone robustness benchmark | Gated Hugging Face access is required. ARTPARK's published training mixture includes Vaani, so absolute ranking claims need caution. |
| LAHAJA | 132-speaker external paired replication | Gated Hugging Face access is required. The project uses one deterministic eligible utterance per speaker. |
| FLEURS Hindi | Small cleaner-speech control | Used as a practical control, not as a pure channel-only comparison with GramVaani. |

Upstream pages:

- [GramVaani/OpenSLR SLR103](https://www.openslr.org/103/)
- [Vaani Benchmark V1.0](https://huggingface.co/datasets/ARTPARK-IISc/Vaani-Benchmark-V1.0)
- [LAHAJA](https://huggingface.co/datasets/ai4bharat/Lahaja)
- [FLEURS](https://huggingface.co/datasets/google/fleurs)

Always review the current upstream dataset card or license before downloading,
publishing derived artifacts, or using data commercially.

## Manifest Format

The local evaluator uses CSV:

```csv
audio_path,reference_text,slice,condition,language
data/example.wav,reference transcript,example,original,hi
```

- `audio_path`: local path relative to the repository root, or an absolute path.
- `reference_text`: ground-truth transcript.
- `slice`: stable dataset subset name.
- `condition`: audio condition such as `original` or `bandlimit_8k`.
- `language`: language hint such as `hi`.

Fixed manifests under [`manifests/`](manifests/) preserve row selection, but
they do not make the raw datasets redistributable.

## Paired Benchmark Conditions

The canonical paired benchmark holds speaker, utterance, content, and reference
fixed across:

1. `original`
2. `bandlimit_8k`
3. `bandlimit_8k_g711_alaw`
4. `bandlimit_8k_g711_mulaw`
5. `bandlimit_8k_gsm_fr`

Every codec condition applies the telephone bandlimit first. Outputs are
returned to mono 16 kHz for Whisper inference and validated for format,
duration, completeness, and codec support.

See [`notebooks/README.md`](../notebooks/README.md) for the canonical CPU/GPU
construction and evaluation flow.
