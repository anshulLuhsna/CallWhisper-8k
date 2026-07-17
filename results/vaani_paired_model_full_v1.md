# Vaani Paired 500-Speaker Baseline v1

## Scope

This is the completed `full` profile of the frozen 500-speaker pilot, not the entire 5,050-segment Vaani Benchmark V1.0 corpus. It evaluates one utterance per speaker under five matched conditions with pinned ARTPARK medium and Adalat Whisper-small checkpoints.

- Speakers: 500
- Conditions: original, bandlimit 8 kHz, G.711 A-law, G.711 mu-law, GSM-FR
- Predictions: 5,000
- Decoding: beam 1, forced Hindi, deterministic
- Primary score: Vaani alignment-based multi-reference corpus WER
- Robustness score: conventional corpus WER against each reference separately
- Uncertainty: 20,000 paired speaker bootstrap replicates, seed 0

## Main Result

| Model | Original WER | Pooled telephone WER | Absolute channel penalty | 95% bootstrap CI |
|---|---:|---:|---:|---:|
| ARTPARK medium Vaani Hindi | 0.1460 | 0.1509 | +0.0049 | [+0.0008, +0.0088] |
| Adalat Whisper-small Hindi high-LR | 0.1740 | 0.2020 | +0.0280 | [+0.0223, +0.0340] |

Adalat's pooled channel penalty exceeded ARTPARK's by `0.0232` absolute WER. The paired-bootstrap 95% CI was `[0.0166, 0.0300]`, entirely above zero.

## Per-Condition Channel Penalty

| Condition | ARTPARK penalty | ARTPARK 95% CI | Adalat penalty | Adalat 95% CI | Adalat minus ARTPARK penalty |
|---|---:|---:|---:|---:|---:|
| Bandlimit 8 kHz | +0.0024 | [-0.0016, +0.0062] | +0.0188 | [+0.0130, +0.0248] | +0.0165 |
| G.711 A-law | +0.0039 | [-0.0002, +0.0081] | +0.0187 | [+0.0126, +0.0249] | +0.0148 |
| G.711 mu-law | +0.0032 | [-0.0013, +0.0076] | +0.0208 | [+0.0150, +0.0268] | +0.0176 |
| GSM-FR | +0.0100 | [+0.0039, +0.0161] | +0.0538 | [+0.0452, +0.0632] | +0.0438 |

The ARTPARK intervals for bandlimiting and both G.711 codecs include zero. Its GSM-FR and pooled penalties do not. Every Adalat penalty is positive with an interval excluding zero. GSM-FR is the hardest transform for both models and widens their robustness gap most.

## Absolute Model Gap

Positive values mean Adalat has higher WER.

| Slice | Adalat minus ARTPARK WER | 95% bootstrap CI |
|---|---:|---:|
| Original | +0.0279 | [+0.0165, +0.0399] |
| Bandlimit 8 kHz | +0.0444 | [+0.0327, +0.0564] |
| G.711 A-law | +0.0427 | [+0.0312, +0.0546] |
| G.711 mu-law | +0.0455 | [+0.0339, +0.0575] |
| GSM-FR | +0.0718 | [+0.0587, +0.0855] |
| Pooled telephone | +0.0511 | [+0.0399, +0.0627] |

Fixed-reference scoring preserves the same ranking: mean single-reference pooled WER was `0.2222` for ARTPARK and `0.2679` for Adalat.

## Efficiency

Mean pooled real-time factor was `0.2839` for ARTPARK and `0.1552` for Adalat on the same T4 run. Adalat used about 55% of ARTPARK's inference time despite having higher WER. This accuracy-efficiency tradeoff is why Adalat remains the compact adaptation base.

## Critical Provenance Caveat

The [ARTPARK model card](https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi) says its approximately 718-hour fine-tuning mixture includes Vaani. The [benchmark card](https://huggingface.co/datasets/ARTPARK-IISc/Vaani-Benchmark-V1.0) says this evaluation set is also drawn from Vaani. Exact utterance-level overlap between the checkpoint's training split and Vaani Benchmark V1.0 is not documented.

Therefore:

- ARTPARK's absolute advantage is descriptive for this slice, not proof of global superiority.
- The paired transform analysis still measures how each frozen model responds when identical utterances are degraded.
- The comparison mixes model architecture, capacity, and training exposure; it does not isolate architecture alone.
- A clean final claim needs an external held-out paired corpus plus explicit leakage checks.

## Reproduce Uncertainty Analysis

Keep the two prediction JSONL checkpoints from Drive, then run:

```bash
callwhisper-paired-bootstrap \
  --reference-predictions artpark_medium_vaani_hindi_predictions.jsonl \
  --candidate-predictions adalat_whisper_small_hi_high_lr_predictions.jsonl \
  --output-dir results/vaani_paired_model_full_v1 \
  --replicates 20000 \
  --seed 0
```

## Finding

On this frozen 500-speaker pilot, telephone degradation produced a significantly larger WER penalty for compact Adalat Whisper-small than for ARTPARK medium. GSM-FR caused the largest penalty and the largest widening of the model gap. This rejects the 10-speaker smoke artifact in which ARTPARK appeared to improve after degradation.

## Next Gate

1. Add predeclared gender and macro-region slices with minimum group sizes and paired bootstrap intervals.
2. Replicate the paired channel experiment on an external corpus not used to train either evaluated model, or document why overlap can be excluded.
3. Train the Adalat-based compact challenger only on leakage-safe training data using balanced channel augmentation plus clean replay.
4. Select checkpoints on internal validation; evaluate the frozen Vaani pilot once after settings are locked.
