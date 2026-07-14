# ARTPARK Native 8 kHz Manual Review Summary v1

This report summarizes the completed human review of the 15 highest-WER ARTPARK predictions from the 56-file native 8 kHz GramVaani v2 slice. The reviewed files were deliberately selected from the worst-scoring tail, so these counts must not be treated as prevalence estimates for the full slice.

## Review Outcome

| Classification | Files | Interpretation |
|---|---:|---|
| Bad audio | 6 | The recording was the primary limitation. |
| Model failure | 5 | ARTPARK made a meaningful error despite a usable reference. |
| Questionable reference | 2 | The supplied reference did not reliably match the audible speech. |
| Mixed | 1 | Both audio/reference quality and model behavior contributed. |
| Uncertain | 1 | The reviewer could not assign a reliable cause. |

Understandability was marked `yes` for 4 files, `partly` for 10, and `barely` for 1. Reference quality was marked `good` for 10 files, `wrong` for 3, `incomplete` for 1, and `uncertain` for 1.

The completed structured review is stored in `results/artpark_8khz_manual_review_v1.json`. The original per-file judgments and transcripts remain in `results/artpark_8khz_error_review_v1.md`.

## What The Audit Changes

The canonical ARTPARK WER of `0.3091` remains the reproducible score against the published GramVaani references. The manual review does not replace that score. It shows that part of the worst-scoring tail is caused by unintelligible audio and imperfect references rather than transcription mistakes alone.

In particular:

- only 5 of the 15 reviewed files were classified primarily as model failures;
- only 2 of those 5 model-failure files were marked fully understandable;
- 4 references were marked wrong or incomplete, with 1 additional reference marked uncertain;
- ARTPARK was often still substantially better than large-v3 on recordings the reviewer found difficult.

This means raw WER is necessary but insufficient for diagnosing the model. It also means the benchmark should preserve both a canonical-reference score and a separately documented human-audited view.

## Residual Model-Failure Themes

The five model-failure cases suggest four testable weaknesses:

1. **Short function-word confusion:** `से` was decoded as `ऐसी` in more than one reviewed utterance.
2. **Leading-phrase deletion:** ARTPARK omitted opening words such as `ये संघ`.
3. **Tail or span omission:** one prediction stopped after `शुक्रवार`, and another omitted a harder middle span.
4. **Local names and lightly spoken entities:** a district/location term such as `सिंहभुम` was dropped even though it was audible.

These are hypotheses from a small, deliberately difficult sample. They define data strata to investigate; they are not yet population-level conclusions.

## Training Implications

Do not train on these 100 benchmark clips. Do not use the six `bad_audio` cases or the questionable-reference cases as supervised examples without new transcription and adjudication.

The independent challenger training set should instead come from `GV_Train_100h` and emphasize:

- clear native-8-kHz utterances with verified transcripts;
- utterances containing district names, people, institutions, dates, and numbers;
- examples with audible leading and trailing speech to reduce endpoint deletion;
- mildly distorted but still human-understandable telephone speech;
- explicit exclusion of unintelligible audio, clipped endpoints, and mismatched references.

The next implementation plan is in `TARGETED_8KHZ_CHALLENGER_PLAN.md`.

## Reporting Language

Recommended:

> On the 56-file native-8-kHz slice, ARTPARK achieved canonical WER 0.3091. Manual review of its 15 highest-WER files classified 5 as model failures, while 6 were primarily bad audio and 4 had wrong or incomplete references. Because the review set was selected from the worst-scoring tail, these counts diagnose failure modes but do not estimate their frequency across the full benchmark.

Do not claim that the corrected WER is lower: the audit did not adjudicate every reference in the 56-file slice.
