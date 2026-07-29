# Adalat Frozen External Evaluation v1

## Decision

**Verdict: `fail_external_generalization`**

The fixed `serious_labelsafe_v1` LoRA adapter passed its internal GramVaani
gate, but it did not improve absolute pooled telephone WER over base Adalat on
both frozen external benchmarks. It also exceeded the predeclared 5% relative
original-audio regression limit on both benchmarks.

No training, tuning, benchmark-row changes, decoding changes, or success-rule
changes were made during this final evaluation.

## Predeclared Gate

A pass required all of the following:

1. Adapted pooled telephone WER must improve over base Adalat on Vaani.
2. Adapted pooled telephone WER must improve over base Adalat on LAHAJA.
3. Each improvement must have a paired 95% bootstrap interval entirely below
   zero.
4. Relative original-audio WER regression must be at most 5% on each benchmark.

The benchmark used 20,000 speaker-clustered bootstrap replicates with seed 0.

## Vaani

| Metric | Base Adalat | Adapted Adalat | Adapted minus base |
|---|---:|---:|---:|
| Original WER | **0.174110** | 0.199300 | +0.025190 |
| Pooled telephone WER | **0.202219** | 0.226192 | +0.023973 |
| Original relative regression | - | - | +14.47% |

The pooled adapted-minus-base WER interval was
`[+0.015781, +0.032027]`. It was entirely above zero, so the adapter's harm on
pooled Vaani telephone audio was statistically supported.

The change in channel penalty was `-0.001217`, with interval
`[-0.007130, +0.004727]`. This interval crossed zero, so reduced channel
sensitivity was not established.

## LAHAJA

| Metric | Base Adalat | Adapted Adalat | Adapted minus base |
|---|---:|---:|---:|
| Original WER | **0.180247** | 0.200000 | +0.019753 |
| Pooled telephone WER | **0.215329** | 0.218930 | +0.003601 |
| Original relative regression | - | - | +10.96% |

The pooled adapted-minus-base WER interval was
`[-0.015690, +0.022348]`. The result was inconclusive statistically, but it did
not satisfy the required absolute-improvement gate.

The adapter reduced the LAHAJA channel penalty by `0.016152`, with interval
`[-0.032096, -0.001360]`. That reduction was statistically supported. It is
not a production win because original-audio WER simultaneously became worse;
the adapter reduced the gap partly by damaging the starting point.

## ARTPARK Headline Gate

On pooled Vaani telephone audio, adapted Adalat was `0.075284` WER worse than
the ARTPARK reference model. The paired 95% interval was
`[+0.064659, +0.086198]`.

The claim that the adapter beat ARTPARK was not established.

## Interpretation

The training pipeline worked, but the learned behavior did not generalize.
Held-out GramVaani WER improved substantially, while untouched Vaani and
LAHAJA did not. The most likely interpretation is domain overfitting: the
adapter learned GramVaani-specific speech and transcript patterns more than a
general resistance to telephone-channel degradation.

The result supports two engineering lessons:

- same-domain validation is necessary but not sufficient;
- a frozen external benchmark can reverse the conclusion suggested by an
  impressive internal score.

The existing Vaani and LAHAJA benchmarks must now remain observed evaluation
sets. A new adaptation recipe should use broader training and validation
domains and reserve a new untouched holdout for its final decision.

## Provenance

This report and
[`adalat_frozen_evaluation_v1.json`](adalat_frozen_evaluation_v1.json) were
curated from the completed output of
[`notebooks/15_adalat_frozen_evaluation_colab.ipynb`](../notebooks/15_adalat_frozen_evaluation_colab.ipynb).
Raw prediction checkpoints and the complete output bundle remain in the
experiment's persistent Colab/Drive directory.
