# CallWhisper-8k — 4-Week Execution Roadmap

Decision: **Path 2 — Locked Operator roadmap: A -> D -> Adaptation -> C**

Core promise: **CallWhisper-8k is a reproducible 8 kHz telephony ASR benchmark + inference system**, not a guaranteed "beat Whisper" fine-tune.

Operating budget: **5 evenings/week x 2.5 hours = ~12.5 hours/week**. Keep two evenings per week as buffer for academics, internship, fatigue, or debugging.

Non-negotiable: if something is not in this roadmap, it goes into `FUTURE_WORK.md`, not into v1.0.

---

## The 4-Week Shape

| Week | Theme | Main Output | Tag |
|---|---|---|---|
| Week 1 | Baseline + eval harness | First WER/CER benchmark on real audio | `v0.1-baseline` |
| Week 2 | Telephony preprocessing | Ablation table for codec/noise/VAD/preprocessing | `v0.2-preprocessing` |
| Week 3 | Adaptation experiments | LoRA if gated; otherwise decoding/prompt/chunking adaptation | `v0.3-adapted` |
| Week 4 | Productize + polish | CLI, FastAPI, Docker, demo, final README | `v1.0` |

---

## How To Track It

Use a single `TRACKING.md` in the project repo with this exact structure:

```md
# CallWhisper-8k Tracking

## Current Week
Week: [1/2/3/4]
Tag target: [v0.1/v0.2/v0.3/v1.0]
This week's non-negotiable deliverable:

## Daily Log
### YYYY-MM-DD
- Planned:
- Done:
- Blocked:
- Next action:

## Scoreboard
- Day-2 WER number shipped: [yes/no]
- Baseline table shipped: [yes/no]
- Preprocessing ablation shipped: [yes/no]
- LoRA smoke test run: [yes/no]
- Week-3 kill gate obeyed: [yes/no]
- v1.0 shipped: [yes/no]

## Cut List Temptations
- [feature idea] -> moved to FUTURE_WORK.md? [yes/no]
```

Tracking rules:

- Start each evening by writing the **one task** that must be done tonight.
- End each evening by writing the **next action** for tomorrow.
- Do not maintain a complex Notion/Trello setup. One markdown file is enough.
- Commit at least **twice per week**, ideally after each real artifact lands.
- Every Friday, tag the repo and post a public update.

---

## Weekly Public Proof

| Week | Public Post |
|---|---|
| Week 1 | "I built a WER/CER benchmark for Whisper on 8 kHz telephony-style Hindi audio." |
| Week 2 | "I tested whether telephony preprocessing actually changes ASR accuracy instead of assuming it helps." |
| Week 3 | "I compared adaptation strategies for narrowband speech: LoRA if viable, otherwise decoding/prompt/chunking experiments." |
| Week 4 | "I shipped CallWhisper-8k: reproducible benchmark + API for 8 kHz telephony ASR." |

Each post must include one concrete artifact: screenshot of table, repo link, CLI output, benchmark chart, demo clip, or README section.

---

## Week 1 — Baseline + Eval Harness

Goal: produce a real WER/CER number fast. This week decides whether the project is viable.

### Monday

Tasks:

- Initialize repo: `callwhisper-8k`.
- Add `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`.
- Create folders:
  - `src/callwhisper/eval/`
  - `src/callwhisper/datasets/`
  - `results/`
  - `configs/`
  - `examples/`
- Write README skeleton:
  - problem
  - goal
  - planned datasets
  - planned methodology
- Create `datasets/README.md` with dataset links and license notes.

Done condition:

- Repo exists and first commit is made.
- README clearly says this is a benchmark + inference system, not a guaranteed fine-tune.

### Tuesday

Tasks:

- Download or prepare first tiny evaluation slice.
- Use OpenSLR SLR103 if fast.
- If SLR103 stalls, immediately use a tiny Common Voice Hindi slice and synthetically degrade later.
- Implement minimal transcription script.
- Implement minimal WER using `jiwer`.

Hard gate:

- By end of Tuesday, this command or equivalent must output one WER number on 10 audio files:

```bash
python -m callwhisper.eval --manifest data/test_manifest.csv --model tiny
```

If this fails:

- Stop adding features.
- Spend Wednesday only debugging the smallest path to one WER number.

### Wednesday

Tasks:

- Clean up eval harness.
- Add CER.
- Add text normalization:
  - lowercase Roman text
  - strip punctuation
  - normalize digits
  - handle Hindi/Devanagari carefully, without over-normalizing
- Save results to JSON and Markdown.

Done condition:

- `results/baseline_v0.md` or `results/baseline_v0.json` exists.

### Thursday

Tasks:

- Run Whisper `tiny`, `base`, and `small` on at least two slices:
  - real 8 kHz/narrowband slice
  - clean or synthetic comparison slice
- If `medium` runs easily, include it. If not, skip.

Done condition:

- First baseline table exists:

| Model | Slice | Condition | WER | CER |
|---|---|---|---:|---:|

### Friday

Tasks:

- Write `results/baseline_v1.md`.
- Update README with first results table.
- Tag `v0.1-baseline`.
- Public post #1.

Week 1 GitHub artifact:

- `src/callwhisper/eval/`
- `src/callwhisper/datasets/`
- `datasets/README.md`
- `results/baseline_v1.md`
- `results/baseline_v1.json`
- README with first result table

---

## Week 2 — Telephony Preprocessing Ablations

Goal: test whether telephony-aware preprocessing changes WER/CER.

### Monday

Tasks:

- Implement `src/callwhisper/audio/telephony.py`.
- Add:
  - 16 kHz -> 8 kHz -> 16 kHz roundtrip
  - bandpass / IRS-like filter
  - µ-law encode/decode
  - A-law encode/decode

Rule:

- Do not study DSP deeply this week. Implement measurable transforms only.

### Tuesday

Tasks:

- Add `src/callwhisper/audio/noise.py`.
- Add MUSAN noise overlay at SNRs:
  - 20 dB
  - 10 dB
  - 5 dB
- Add manifest fields for condition names.

### Wednesday

Tasks:

- Add `src/callwhisper/audio/vad.py`.
- Implement simple VAD/chunking for longer clips.
- Optional: add `noisereduce` or another off-the-shelf denoise step.

Rule:

- If denoise takes more than one evening, cut it.

### Thursday

Tasks:

- Re-run eval harness across conditions:
  - raw
  - codec only
  - codec + noise
  - codec + VAD/chunking
  - codec + denoise, only if implemented cleanly

Done condition:

- Ablation table exists.

### Friday

Tasks:

- Write `results/preprocessing_v1.md`.
- Update README with preprocessing findings.
- Run **30-minute hello-LoRA smoke test**:
  - Whisper tiny
  - 5 clips
  - overfit only
  - goal is not quality, only proof that training loop runs
- Tag `v0.2-preprocessing`.
- Public post #2.

Week 2 GitHub artifact:

- `src/callwhisper/audio/telephony.py`
- `src/callwhisper/audio/noise.py`
- `src/callwhisper/audio/vad.py`
- `results/preprocessing_v1.md`
- `results/preprocessing_v1.json`
- README preprocessing section

---

## Week 3 — Adaptation Experiments

Goal: run controlled adaptation. LoRA is allowed only if gates pass.

Week 3 is not "fine-tuning week." It is **adaptation week**.

### Monday

Tasks:

- If Week 2 hello-LoRA passed, start Track A.
- Track A:
  - Whisper-small
  - HF `transformers` + `peft`
  - <=5 hours training data
  - 30-sample shard first
- If hello-LoRA failed, start Track B immediately.

Track B:

- initial prompt biasing
- beam size sweep
- temperature sweep
- chunk length sweep
- condition-on-previous-text on/off

### Tuesday

Tasks:

- Track A: complete one small training run, max 1-2 epochs.
- Track B: run at least 3 decoding/chunking variants through the eval harness.

Done condition:

- There is a measurable result table, not just code.

### Wednesday — Kill Gate

At **10 PM Wednesday**, decide:

- If adapter trained and eval ran: continue Track A.
- If OOM/debugging/harness issues remain: kill LoRA permanently for v1.0.
- No exceptions.

Write the decision into `TRACKING.md`:

```md
## Week 3 Kill Gate
Decision: [Continue LoRA / Kill LoRA and use Track B]
Reason:
Evidence:
```

### Thursday

Tasks:

- Lock final adaptation results.
- No new experiments after Thursday.
- Write analysis of what changed and what did not.

### Friday

Tasks:

- Write `results/adaptation_v1.md`.
- Update README with adaptation results.
- Tag `v0.3-adapted`.
- Public post #3.

Week 3 GitHub artifact:

- `src/callwhisper/adaptation/`
- either `lora_train.py` + adapter notes, or `decoding.py` / `chunking.py`
- `results/adaptation_v1.md`
- `results/adaptation_v1.json`
- README adaptation section

---

## Week 4 — Productize, Polish, Ship

Goal: turn the work into a complete, runnable flagship repo.

### Monday

Tasks:

- Add FastAPI service:
  - `POST /transcribe`
  - `POST /evaluate`
  - `GET /health`
  - `GET /models`
- Reuse existing modules. Do not duplicate eval/preprocessing logic.

### Tuesday

Tasks:

- Add Dockerfile.
- Add `docker-compose.yml`.
- Add benchmark CLI:

```bash
callwhisper bench --config configs/full.yaml
```

Done condition:

- One command reproduces result tables or clearly documents how to reproduce them.

### Wednesday

Tasks:

- Add Streamlit demo.
- Upload `.wav`.
- Show:
  - raw transcript
  - preprocessed transcript
  - adapted transcript, if available
  - WER/CER if reference text is provided

Hard rule:

- If Streamlit does not work by Wednesday night, cut it.
- README + result tables matter more.

### Thursday

Tasks:

- Final README pass.
- Add architecture diagram.
- Record 60-second demo video.
- Add `examples/` with 3 sample audios or sample manifests, depending on licensing.
- Write `LIMITATIONS.md` or a strong README limitations section.

### Friday

Tasks:

- Final validation run.
- Tag `v1.0`.
- Public post #4.
- DM repo to 3-5 Voice AI people/founders.

Week 4 GitHub artifact:

- `src/callwhisper/api/`
- `Dockerfile`
- `docker-compose.yml`
- `bench/cli.py`
- `app.py`
- `examples/`
- final README
- architecture diagram
- demo video link
- all results files

---

## Hard Cut List

Forbidden before `v1.0`:

- Whisper large / large-v3
- custom React/Next.js dashboard
- auth, users, multi-tenant API
- cloud deployment
- streaming transcription
- diarization
- WhisperX
- faster-whisper / CTranslate2 conversions
- second language beyond Hindi + Hindi-English code-switching
- training Whisper-medium or large
- custom KenLM training from scratch
- adding a fifth dataset
- long blog series
- refactoring Week 1 eval code during Week 3 or Week 4

If tempted, add it to `FUTURE_WORK.md`.

---

## Kill Switches

| Trigger | Action |
|---|---|
| End of Week 1 Day 2: no WER number | Stop everything and debug minimal eval only |
| End of Week 1: no baseline table | Slip Week 2 by 2 days, cut preprocessing scope |
| End of Week 2: hello-LoRA fails | Week 3 starts in Track B, no debate |
| Week 3 Wednesday 10 PM: no working adapter/eval | Kill LoRA and switch to Track B |
| Any week loses >=2 evenings | Cut polish/preprocessing, never eval/results |
| Week 4 Wednesday: demo not working | Cut demo, strengthen README/results |
| New feature idea appears | Add to `FUTURE_WORK.md`, do not code |

---

## Final README Structure

Use this exact order:

1. `# CallWhisper-8k`
2. One-line elevator
3. Results snapshot table
4. Problem: why 8 kHz telephony ASR is hard
5. What this project shows
6. Quickstart
7. Architecture
8. Datasets and licenses
9. Evaluation methodology
10. Results
11. Preprocessing ablations
12. Adaptation experiments
13. CLI usage
14. API usage
15. Demo
16. Limitations
17. Future work
18. What I learned
19. License and citations

README rule:

- Lead with results.
- Be honest about dataset limitations.
- Never claim universal improvement.
- Say: "On this slice, method X changed WER from A to B."
- Do not say: "This fixes Whisper for telephony."

---

## Daily Work Ritual

Use this every evening:

1. Open `TRACKING.md`.
2. Write tonight's one task.
3. Work for 90 minutes.
4. Spend 20 minutes making the result visible: commit, result file, README update, or issue note.
5. Spend 10 minutes writing tomorrow's next action.
6. Stop.

If stuck for more than 30 minutes:

- reduce the problem to a 10-file toy slice
- run the smallest script possible
- write down the exact error
- ask AI to debug the smallest repro
- do not redesign the whole system

---

## What Makes This Impressive

- Real WER/CER tables, not vague claims.
- Clear dataset and license handling.
- Two-layer benchmark: real narrowband + synthetic telephony.
- Audio preprocessing measured with ablations.
- Adaptation experiments with honest success/failure criteria.
- One-command benchmark reproduction.
- FastAPI + Docker only after the benchmark has substance.
- README that reads like applied engineering, not a tutorial.

---

## What Makes This Look Fake Or Shallow

- "Fine-tuned Whisper" with no baseline.
- No WER/CER.
- No dataset license explanation.
- One demo audio and no benchmark.
- Overclaiming improvement.
- Huge README but weak code.
- Custom frontend while core eval is unfinished.
- No limitations section.
- No reproducible command.

---

## Minimum Impressive Version

If everything goes wrong, ship this:

- one real 8 kHz/narrowband slice
- one synthetic telephony slice
- Whisper tiny/base/small baselines
- WER/CER table
- raw vs preprocessed comparison
- one-command benchmark runner
- FastAPI `/transcribe`
- Dockerfile
- honest README with limitations

That is still a legitimate flagship if it is clean, reproducible, and well-written.
