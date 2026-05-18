<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Short answer

This exact project has **partially** been done.
Whisper (and Whisper‑derived models) have already been **fine‑tuned and benchmarked on GramVaani / SLR118 telephone‑style Hindi**, and compared against other Indic ASR systems, but **nobody seems to have released a focused, reproducible “Whisper on 8 kHz Indian telephony + preprocessing ablations” benchmark**.[^1][^2][^3][^4][^5][^6][^7][^8][^9][^10]

So the novel space for CallWhisper‑8k is **narrow but real**: a careful, open benchmark on *telephone‑style* Hindi that (a) is Whisper‑centric, (b) explicitly targets 8 kHz / narrowband conditions, and (c) systematically studies preprocessing choices, while also comparing to strong Indic baselines.

***

## Closest prior work

### 1. Vistaar \& IndicWhisper (AI4Bharat)

- **Title/name:**
    - Paper: “Diverse Benchmarks and Training Sets for Indian Language ASR” (Vistaar).
    - Models: IndicWhisper.[^7][^9]
- **Links:**
    - Paper / description: https://arxiv.org/abs/2305.15386 (Vistaar).[^9]
    - Repo: https://github.com/AI4Bharat/vistaar.[^11][^7]
    - Models (JAX implementation): https://huggingface.co/parthiv11/indic_whisper_nodcil.[^12][^13][^10]
- **Year:** 2023 (paper \& initial models).[^7][^9]
- **Datasets used (Hindi subset):**
Kathbath, Kathbath‑Hard, Google FLEURS, Common Voice, IndicTTS, MUCS, **GramVaani**, and others in the Vistaar benchmark. GramVaani corresponds to telephone speech sourced from the Gram Vaani platform.[^3][^4][^11][^7]
- **Models tested:**
Multiple systems including Google STT, Azure STT, Nvidia ASR (medium/large), IndicWav2vec, and **IndicWhisper (fine‑tuned Whisper)**.[^5][^10][^12][^11][^7]
- **Metrics reported:**
Primarily **WER** on each dataset; IndicWhisper achieves WER = 26.8 % on GramVaani in the Hindi subset table, outperforming several other systems.[^13][^10][^5][^12][^11][^7]
- **What it covers:**
    - A **multi‑domain benchmark suite** (59 benchmarks over 12 Indian languages), including GramVaani (telephone speech) as one of the Hindi evaluation sets.[^9][^11][^7]
    - **Fine‑tuned Whisper (IndicWhisper)** trained on 10.7 k hours of labelled audio across languages, with systematic comparisons against commercial and open ASR systems using WER on all benchmarks (including GramVaani).[^5][^12][^7][^9]
- **What it does not cover:**
    - No **vanilla OpenAI Whisper** baselines on GramVaani; only **IndicWhisper** and non‑Whisper systems are reported.[^11][^7]
    - No explicit **8 kHz / telephony preprocessing ablation** (they work on datasets as standardised 16 kHz audio; GramVaani is resampled and integrated into a unified pipeline).[^14][^7]
    - No detailed focus on **call‑center style usage** or code‑switching; it is a broad ASR benchmark, not a telephony‑specific one.[^7][^9]

***

### 2. Whisper Hindi (Vasista22 fine‑tunes)

- **Title/name:**
    - “Whisper Hindi Small/Medium/Large‑v2” model series.[^2][^15][^16][^17][^1]
- **Links:**
    - Small: https://huggingface.co/vasista22/whisper-hindi-small.[^15][^2]
    - Medium: https://huggingface.co/vasista22/whisper-hindi-medium.[^17][^1]
    - Large‑v2: https://huggingface.co/vasista22/whisper-hindi-large-v2.[^16]
- **Year:** 2023 (Whisper fine‑tuning sprint).[^1][^15][^16]
- **Datasets used:**
    - **Training:** GramVaani ASR Corpus, ULCA ASR, Shrutilipi, Google/FLEURS (hi‑IN).[^2][^15][^16][^17][^1]
    - **Evaluation:** **GramVaani ASR test set**, FLEURS, Common Voice Hindi (sometimes also Mozilla Common Voice test).[^15][^16][^1][^2]
- **Models tested:**
    - Fine‑tuned **whisper‑small**, **whisper‑medium**, **whisper‑large‑v2**; sometimes baseline numbers vs stock Whisper are referenced via the separate whisper‑finetune repo.[^16][^1][^2]
- **Metrics reported:**
    - **WER** on FLEURS (e.g., ~6.8–6.82 % for some models) and **WER on Common Voice Hindi**; GramVaani is listed as training/eval data but card only exposes FLEURS and CV WER publicly.[^1][^2][^15][^16]
- **What it covers:**
    - Demonstrates that **fine‑tuned Whisper on Hindi (including GramVaani data) can reach strong WER on standard benchmarks**.[^2][^16][^1]
    - Code for training/evaluation is available via the **whisper‑finetune** repo, so there is a partially reproducible pipeline for evaluating Whisper on Hindi corpora (including telephony‑style GramVaani).[^18][^2]
- **What it does not cover:**
    - No explicit **telephony‑only or call‑center‑only benchmark**; everything is folded into one Hindi ASR model and evaluated mostly on FLEURS/common‑voice.[^15][^16][^1]
    - No analysis of **8 kHz vs 16 kHz resampling, bandpass filters, loudness normalization, or 8 kHz round‑trip artefacts**.[^16][^1][^2]
    - No systematic comparison against other Indic models (IndicWhisper, IndicWav2vec, Vakyansh) on **telephone‑style** Hindi; comparisons are primarily vs baseline Whisper.[^1][^2][^16]

***

### 3. ARTPARK‑IISc Whisper‑Vaani Hindi models

- **Title/name:**
    - “whisper‑large‑v3‑vaani‑hindi” and related “whisper‑medium‑vaani‑hindi”, “whisper‑tiny‑vaani‑hindi”.[^6][^8][^19][^20]
- **Links:**
    - Large‑v3 model card: https://huggingface.co/ARTPARK-IISc/whisper-large-v3-vaani-hindi.[^20][^6]
    - Medium/tiny variants: https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi, https://huggingface.co/ARTPARK-IISc/whisper-tiny-vaani-hindi.[^8][^19]
    - Case study using these models: https://vaani.iisc.ac.in/case-studies/sandlogic.[^21]
- **Year:** 2025–2026.[^19][^21][^6][^8]
- **Datasets used:**
    - Training: ARTPARK‑IISc Vaani, **GramVaani**, IndicVoices, FLEURS, IndicTTS, Common Voice, Kathbath, etc.[^6][^8][^20]
    - Evaluation: same multi‑corpus setup with per‑dataset WER table including **GramVaani**.[^8][^19][^20][^6]
- **Models tested:**
    - Fine‑tuned **Whisper‑tiny**, **Whisper‑medium**, **Whisper‑large‑v3** variants specializing in Hindi.[^19][^20][^6][^8]
- **Metrics reported:**
    - **WER per dataset**; for example, Whisper‑large‑v3‑vaani‑hindi reports WER = 25.11 % on GramVaani, ~11.20 % on FLEURS, ~8.85 % on Kathbath, etc., while the medium/tiny variants get higher WER on GramVaani (e.g., 27.64 % and 42.34 %).[^20][^6][^8][^19]
- **What it covers:**
    - A strong **Whisper‑Hindi family** evaluated on **GramVaani (telephone)** and various non‑telephony Hindi datasets, with clear WER tables.[^6][^8][^20]
    - Case study where ARTPARK’s **whisper‑medium‑vaani‑hindi** is used as an ASR baseline for real **call‑analytics**; SandLogic report shows LAHAJA benchmark WER and real‑world improvements from their own model.[^22][^21]
- **What it does not cover:**
    - No systematic experimentation over **audio preprocessing for telephony** (resampling choices, bandpass filters, loudness normalization) in the public docs.[^8][^19][^20][^6]
    - No open, neutral **benchmark harness**; the models are released, but evaluation is mostly one‑lab.[^6][^8]

***

### 4. Gram Vaani ASR Challenge 2022 (1111 Hours Hindi ASR / SLR118)

- **Title/name:**
    - “Gram Vaani ASR Challenge on spontaneous telephone speech recordings in regional variations of Hindi” (Interspeech 2022).[^23][^24][^25]
- **Links:**
    - Challenge page: https://sites.google.com/view/gramvaaniasrchallenge/home.[^26]
    - Dataset description: https://sites.google.com/view/gramvaaniasrchallenge/dataset.[^3]
    - OpenSLR entry SLR118: https://www.openslr.org/118/.[^4]
    - Paper PDF: Interspeech archive / IITD page.[^24][^25][^23]
- **Year:** 2022.[^26][^23]
- **Datasets used:**
    - **Telephone‑quality Hindi speech**, 100 h labelled train, 5 h dev, 3 h eval, plus 1000 h unlabelled; speech collected via Gram Vaani Mobile Vaani platform, with regional variations and background noise.[^4][^23][^3]
- **Models tested:**
    - Baseline systems built by IIT‑Madras / collaborators (Kaldi‑style and self‑supervised models such as wav2vec‑based systems, plus challenge submissions); Whisper itself is **not** reported as a baseline.[^23][^18][^24]
- **Metrics reported:**
    - **WER** for baseline systems on the challenge splits; the precise numbers are in the Interspeech paper and baseline recipes.[^25][^24][^23]
- **What it covers:**
    - Defines the **core telephony Hindi dataset** you want to use (GramVaani / SLR118) with full telephone channel characteristics and metadata.[^3][^4][^23]
    - Provides **non‑Whisper baselines and recipes** for telephone Hindi recognition.[^18][^24][^23]
- **What it does not cover:**
    - No published **Whisper baselines** on GramVaani.[^24][^23]
    - No **preprocessing ablation** within the challenge description; they standardise data (including resampling) but don’t study preprocessing choices as variables.[^26][^24][^3]

***

### 5. Bridging the Reality Gap \& IndicWav2vec on GramVaani

- **Title/name:**
    - “Bridging the Reality Gap: Efficient Adaptation of ASR systems for Challenging Low‑Resource Domains.”[^27][^28]
    - Related description of IndicWav2vec data curation and GramVaani telephony pre‑processing.[^29][^14]
- **Links:**
    - arXiv: https://arxiv.org/abs/2512.16401.[^27]
    - Summary / review: EmergentMind.[^28]
    - IndicWav2vec overview: Indic voice toolkit article.[^14]
- **Year:** 2025.[^28][^27]
- **Datasets used:**
    - **GramVaani telephonic clinical audio** (rural healthcare use‑case), originally **8 kHz, upsampled to 16 kHz**; Kathbath used as a high‑quality Hindi anchor domain.[^30][^29][^27]
- **Models tested:**
    - **IndicWav2vec** as the primary acoustic backbone; LoRA‑based domain adaptation variants with and without multi‑domain experience replay.[^30][^27]
- **Metrics reported:**
    - **WER** on GramVaani (40.94 % baseline, ~17.1 % relative WER reduction after adaptation).[^27][^30]
    - WER on Kathbath to measure catastrophic forgetting.[^30]
- **What it covers:**
    - Strong evidence that **telephony GramVaani audio (8 kHz→16 kHz) is challenging**, and that domain adaptation can significantly reduce WER.[^29][^27][^30]
    - Explicit description of **preprocessing for telephony corpora** (resampling to 16 kHz, VAD, SNR‑based filtering, etc.) in the IndicWav2vec pipeline.[^14][^29]
- **What it does not cover:**
    - **No Whisper models**; this is an IndicWav2vec‑centric story.[^14][^27]
    - Even though they mention upsampling 8 kHz → 16 kHz, there is **no ablation between different telephony preprocessing strategies** (no comparison of bandpass vs no bandpass, 8 kHz round‑trip, etc.).[^29][^27][^14]

***

### 6. Collabora’s Whisper Hindi models \& blog posts

- **Title/name:**
    - Models: `collabora/whisper-base-hindi`, `Whisper-Hindi v1/v2`.[^31][^32]
    - Blogs: “Breaking language barriers: Fine-tuning Whisper for Hindi” \& “Moving closer towards fully reliable, production‑ready Hindi ASR”.[^33][^31]
- **Links:**
    - Model card: https://huggingface.co/collabora/whisper-base-hindi.[^32]
    - Blog posts on Collabora site.[^33][^31]
- **Year:** 2025–2026 (v2 announced May 2026).[^31][^32]
- **Datasets used:**
    - Shrutilipi (~1.5 k h), other Hindi corpora including FLEURS, Shrutilipi, and additional curated data; they focus on ~3000 h of Hindi speech.[^32][^33][^31]
- **Models tested:**
    - Fine‑tuned **Whisper‑base** and later larger models (v2 uses multilingual Whisper models across sizes).[^31][^32]
- **Metrics reported:**
    - WER on FLEURS Hindi; baseline openai/whisper‑base yields WER ≈ 149 % vs ~8.49 % for collabora/whisper‑base‑hindi with Whisper normalization; v2 reaches ~5 % WER on FLEURS.[^33][^32][^31]
- **What it covers:**
    - Very strong **Whisper Hindi** models, with detailed discussion of **normalization choices and their effect on WER vs semantic fidelity**.[^32][^33][^31]
- **What it does not cover:**
    - Not telephony‑specific; evaluations are on FLEURS and similar 16 kHz corpora, not explicitly on GramVaani or call‑center 8 kHz.[^31][^32]
    - No preprocessing ablation for narrowband speech.[^33][^32][^31]

***

### 7. SandLogic + Vaani case study (call analytics)

- **Title/name:**
    - “Fine‑Tuning Hindi ASR for Real‑World Call Analytics Leveraging Vaani.”[^21]
- **Link:**
    - https://vaani.iisc.ac.in/case-studies/sandlogic.[^21]
- **Year:** Not dated in snippet; context suggests 2024–2025.[^21]
- **Datasets used:**
    - Hindi subset of **Vaani** dataset (multi‑accent, multi‑domain); **LAHAJA benchmark** used as an eval set for accent diversity (not strictly telephony).[^22][^21]
    - Real **Indian call‑center audio** from SandLogic’s clients.[^21]
- **Models tested:**
    - Baseline: **ARTPARK‑IISc/whisper-medium-vaani-hindi**.[^8][^6][^21]
    - SandLogic proprietary ASR before and after fine‑tuning on Vaani Hind.[^21]
- **Metrics reported:**
    - WER on **LAHAJA** benchmark for multiple systems (e.g., Whisper‑based ARTPARK model vs SandLogic’s models).[^22][^21]
    - Real client call‑center WER reductions (~55 % relative improvement for one client, ~47 % for another).[^21]
- **What it covers:**
    - Evidence that **Whisper‑based Hindi ASR is used in Indian call‑analytics**, with real‑world WER numbers and improvement reports.[^21]
- **What it does not cover:**
    - No open‑source **code or benchmark harness** for the call‑center data.[^21]
    - LAHAJA is not necessarily 8 kHz telephony; call‑center datasets are proprietary.[^22][^21]
    - No preprocessing ablation; they treat audio as given.[^21]

***

### 8. SPEECH‑24 and other Whisper‑based India call‑center efforts

- **Title/name:**
    - “SPEECH‑24 — custom ASR model built on top of Whisper, fine‑tuned on real Indian call center data.”[^34]
- **Link:**
    - LinkedIn post: https://www.linkedin.com/posts/ansh-nahar_whos-been-listening-activity-7319245237141323776-PczU.[^34]
- **Year:** 2025.[^34]
- **Datasets used:**
    - Real **Indian call‑center audio**, multilingual (Hindi, Tamil, Telugu, Kannada, plus English mix).[^34]
- **Models tested:**
    - Custom **Whisper‑based ASR** (SPEECH‑24), presumably compared to unreported baselines.[^34]
- **Metrics reported:**
    - Post emphasises **real‑time factor, throughput and cost**, rather than WER; no public numeric WER in the snippet.[^34]
- **What it covers:**
    - Confirms that **Whisper is already being fine‑tuned on Indian call‑center data**, including Hindi and Hinglish‑like mixes.[^34]
- **What it does not cover:**
    - No open data, no reproducible benchmark, no detailed WER/CER breakdown, and no 8 kHz preprocessing analysis.[^34]

***

### 9. Oriserve Whisper‑Hindi2Hinglish models

- **Title/name:**
    - Whisper–Hindi2Hinglish model family (e.g., “Whisper‑Hindi2Hinglish‑Apex”, “Whisper‑Hindi2Hinglish‑Swift”).[^35][^36]
- **Links:**
    - HF model card: https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Swift.[^35]
    - Blog: Oriserve open‑sources India‑focused speech models fine‑tuned on Whisper.[^36]
- **Year:** 2025.[^36]
- **Datasets used:**
    - Indian conversational speech with **Hindi, Hinglish and Indian‑accented English**, often in customer‑support / contact‑center settings; exact datasets are not fully specified.[^35][^36]
- **Models tested:**
    - Multiple **Whisper‑based fine‑tunes** targeted at Hindi, Hinglish, and Indian‑accented English.[^36][^35]
- **Metrics reported:**
    - They claim improved accuracy over baseline Whisper on Indian mixed‑language speech, but public snippets do not expose exact WER/CER numbers.[^35][^36]
- **What it covers:**
    - Whisper **code‑switching (Hindi/English) and Hinglish** for Indian conversational audio.[^36][^35]
- **What it does not cover:**
    - No open 8 kHz telephony benchmark, no GramVaani/SLR118 mention in public cards, and no systematic preprocessing study.[^35][^36]

***

### 10. Voicegain 8 kHz call‑center benchmark (non‑Hindi but Whisper‑based)

- **Title/name:**
    - “2025 Speech‑to‑Text Accuracy Benchmark for 8 kHz Call Center Audio Files.”[^37]
- **Link:**
    - Voicegain blog: https://www.voicegain.ai/post/2025-speech-to-text-accuracy-benchmark-for-8-khz-call-center-audio-files.[^37]
- **Year:** 2025.[^37]
- **Datasets used:**
    - Proprietary **8 kHz call‑center audio** (language not specified in snippet; likely English).[^37]
- **Models tested:**
    - Amazon AWS STT, Google, Microsoft, Voicegain’s own engine, and **Voicegain‑Whisper‑Large‑V3** (Whisper‑based).[^37]
- **Metrics reported:**
    - Accuracy percentages on 8 kHz audio, with AWS slightly ahead of Voicegain‑Whisper‑Large‑V3 (e.g., AWS ~87.67 % vs Voicegain‑Whisper‑Large‑V3 ~86.17 %).[^37]
- **What it covers:**
    - A **telephony‑specific 8 kHz benchmark including a Whisper‑based engine**, showing Whisper can work competitively in narrowband call‑center audio.[^37]
- **What it does not cover:**
    - Not Hindi / India‑specific, not open, and does **not expose preprocessing details** or scripts.[^37]

***

### 11. Kaggle IITB IndicWhisper notebook

- **Title/name:**
    - “IITB Indic_whisper” Kaggle notebook.[^38]
- **Link:**
    - https://www.kaggle.com/code/sujaykapadnis/iitb-indic-whisper.[^38]
- **Year:** 2024.[^38]
- **Datasets used:**
    - Multiple Hindi datasets; the notebook explicitly mentions **IndicWhisper – GramVaani** in the solution write‑up, implying experiments on GramVaani.[^38]
- **Models tested:**
    - Baselines include **OpenAI Whisper** and **IndicWhisper**, with experiments on Hindi tasks (exact dataset splits not fully visible in snippet).[^38]
- **Metrics reported:**
    - The notebook references WER‑based evaluation, though numbers are not visible in the snippet.[^38]
- **What it covers:**
    - Concrete examples of **using both vanilla Whisper and IndicWhisper on Hindi benchmarks, including GramVaani**.[^5][^7][^38]
- **What it does not cover:**
    - Not a polished benchmark or reusable evaluation harness; more of a competition/experiment notebook.[^38]
    - No explicit telephony preprocessing ablation or 8 kHz analysis.[^38]

***

## Direct overlap with CallWhisper‑8k

CallWhisper‑8k’s core ideas overlap with prior work in several ways:

1. **Using GramVaani / SLR118 telephony Hindi as a benchmark dataset.**
    - GramVaani telephone‑quality Hindi is already the basis of the **Gram Vaani ASR Challenge**, the SLR118 dataset, and multiple later evaluations.[^4][^23][^3]
    - Vistaar and IndicWhisper use GramVaani as a **benchmark subset**, reporting WER figures (e.g., IndicWhisper’s WER = 26.8 % on GramVaani in the Hindi table).[^10][^11][^5][^7]
    - Whisper Hindi and ARTPARK Whisper‑Vaani models explicitly **train on GramVaani** and evaluate on its test set.[^17][^19][^20][^2][^15][^16][^1][^6][^8]
2. **Benchmarking Whisper‑family models on Hindi ASR.**
    - Multiple teams have fine‑tuned Whisper on Hindi corpora (Collabora, Vasista, ARTPARK‑IISc, AI4Bharat/IndicWhisper), publishing strong WER numbers and model cards.[^12][^19][^20][^11][^2][^5][^16][^32][^1][^33][^31][^6][^8]
    - IndicWhisper is explicitly a **Whisper‑derived model evaluated on GramVaani** alongside non‑Whisper systems.[^10][^12][^9][^5][^7]
3. **Evaluating other Indic ASR models on telephone‑style Hindi.**
    - The Vistaar benchmark reports **GramVaani WER** for Google STT, Azure, Nvidia ASR, IndicWav2vec, and IndicWhisper, giving a multi‑model comparison on a telephone corpus.[^12][^11][^5][^7]
    - Gram Vaani ASR Challenge baselines provide non‑Whisper comparisons on telephone Hindi.[^23][^24][^4]
    - Bridging‑the‑Reality‑Gap paper shows IndicWav2vec’s WER on **8 kHz→16 kHz GramVaani clinical audio**, and improvements via LoRA + replay.[^29][^27][^30]
4. **Whisper on Indian call‑center or mixed‑language audio.**
    - SPEECH‑24, Oriserve’s Whisper‑Hindi2Hinglish models, and SandLogic’s call‑analytics case study all use **Whisper‑based ASR for Indian call‑center / conversational data** (including Hindi, Hinglish and other Indian languages).[^36][^35][^34][^21]
5. **WER‑centric evaluation.**
    - All of these works use **WER (and often CER)** as main metrics for Hindi ASR performance, including on GramVaani and call‑like data.[^9][^19][^20][^5][^7][^32][^27][^30][^6][^8]

So you **cannot claim** to be the first to:

- Benchmark Whisper (or Whisper‑derived models) on Hindi,
- Use GramVaani / SLR118 as an evaluation set, or
- Compare WER for Indian ASR systems (IndicWhisper, IndicWav2vec, commercial APIs) on telephone‑style Hindi.

Those parts are already well‑covered.

***

## Remaining gap CallWhisper‑8k can fill

Despite the overlap, there are several gaps where CallWhisper‑8k can add genuine value if you design it carefully:

### 1. Systematic preprocessing study for 8 kHz / telephony Whisper

- Existing works typically **fix** a preprocessing pipeline: resample everything to 16 kHz, apply VAD, maybe light filtering, then compute 16 kHz log‑mel spectrograms because Whisper expects 16 kHz input.[^39][^40][^32][^14]
- IndicWav2vec and the “Bridging the Reality Gap” paper explicitly mention upsampling **8 kHz → 16 kHz** for GramVaani but treat that as a standard step, not a variable to study.[^27][^14][^29]
- Community discussions (e.g., faster‑whisper issue on telephone 8 kHz stereo) show practitioners experimenting with custom preprocessing, but **no peer‑reviewed, telephony‑specific Whisper ablation** comparing:
    - naive upsampling vs high‑quality interpolation,
    - with/without band‑pass (e.g., 80 Hz–4 kHz/8 kHz),
    - loudness/DRC normalization schemes,
    - simulated **8 kHz round‑trip** on originally high‑bandwidth Hindi corpora.[^41][^42][^43][^44]

A **clean, reproducible ablation of preprocessing choices for Whisper on 8 kHz Indian telephone Hindi** is still missing.

### 2. Whisper‑centric, neutral benchmark rather than “my model” marketing

- Vistaar and Whisper Hindi releases are primarily **model‑centric**: they show WER to demonstrate how good their model is, not to provide a neutral, plug‑and‑play evaluation harness.[^2][^16][^7][^9][^1]
- SandLogic, SPEECH‑24, Oriserve, Voicegain and others report numbers mainly to sell their systems; **data, scripts and configs are not open**, and evaluation details on 8 kHz Hindi are thin.[^35][^36][^34][^37][^21]
- There is **no “Whisper‑first telephony Hindi benchmark” repo** where you can drop in any ASR (Whisper, IndicWhisper, Vakyansh, IndicWav2vec, commercial APIs) and get WER/CER under controlled telephony preprocessing conditions.

CallWhisper‑8k can be that **neutral, fully reproducible benchmark**.

### 3. Telephony‑specific focus for India (not just “one line in a big table”)

- GramVaani is often **one row in a large table** (Vistaar, ARTPARK models) that also includes high‑quality studio or field corpora.[^20][^11][^7][^6]
- There is **no deep dive** on:
    - failure modes specific to telephone Hindi (background noise, crowd‑source transcription noise, regional accents),
    - contrast between **true telephony** (GramVaani, call‑center datasets) and artificially band‑limited 16 kHz corpora.[^45][^3][^4][^14]
- CallWhisper‑8k can specialise in **telephony‑style input**, possibly combining:
    - GramVaani / SLR118,
    - an open 8 kHz or “call‑center‑like” Hindi dataset (if available via Bhashini or others),
    - high‑quality Hindi speech with synthetic 8 kHz round‑trip.


### 4. Cross‑family comparison on *telephony* Hindi

- Vistaar compares IndicWhisper vs Google/Azure/Nvidia/IndicWav2vec on multiple domains, including GramVaani, but **does not include stock OpenAI Whisper**.[^11][^5][^12][^7]
- Whisper Hindi and ARTPARK models evaluate **Whisper variants only** (fine‑tuned vs base), not in a big cross‑family telephony‑focused table.[^16][^1][^2][^6][^8]
- There is room for a **single benchmark** that, *on exactly the same telephony data and preprocessing variants*, compares:
    - vanilla OpenAI Whisper (several sizes),
    - Hindi‑tuned Whisper variants (Vasista, Collabora, ARTPARK, etc.),
    - non‑Whisper Indian models (IndicWhisper, IndicWav2vec, Vakyansh, others),
    - optionally commercial APIs,
with **WER/CER broken down by telephony condition** (native 8 kHz, upsampled 16 kHz, 8 kHz round‑trip, etc.).


### 5. Clarity on code‑switching and Hinglish under telephony constraints

- Code‑switched Hindi‑English corpora exist (e.g., earlier Hindi‑English code‑switching speech corpora, VITB‑HEBiC) and Oriserve/SPEECH‑24 show Whisper used for Hinglish.[^46][^47][^36][^35][^34]
- However, the **intersection of “Hinglish / code‑switching” + “8 kHz telephony” + “Whisper WER/CER”** does not appear in any open benchmark.
- If you can include **code‑switched telephony Hindi‑English segments** and measure WER/CER for Whisper and Indic models under 8 kHz conditions, that’s another still‑open niche.

***

## Recommended positioning

Given the prior work, a **careful, honest description** for CallWhisper‑8k could be:

> “CallWhisper‑8k is an **open, reproducible benchmark and evaluation harness** for applying Whisper‑family and Indic ASR models to **Indian telephone‑style Hindi**.
> It builds on existing Hindi ASR datasets like GramVaani / SLR118 and others, where Whisper and Indic models have already been trained and evaluated, but focuses specifically on:
> 1. **8 kHz / telephony‑style audio conditions**,
> 2. **systematic preprocessing ablations** (resampling, band‑pass, loudness, 8 kHz round‑trip), and
> 3. **side‑by‑side evaluation** of stock Whisper, Hindi‑tuned Whisper variants, and Indic ASR models under identical telephony pipelines.”

Concretely, you can state:

- “Prior work has **already benchmarked Whisper‑derived models and other Indic ASR systems on GramVaani telephone speech** (e.g., Vistaar / IndicWhisper, Whisper Hindi, ARTPARK’s Whisper‑Vaani models), but these results are spread across model cards and papers and are **not a dedicated telephony‑focused benchmark**.”[^19][^5][^7][^9][^20][^1][^2][^6][^16][^8]
- “To our knowledge, **no open benchmark has systematically compared 8 kHz preprocessing strategies for Whisper on Indian telephone‑style Hindi** or provided a neutral plug‑and‑play evaluation harness for multiple ASR families on this domain.”[^44][^41][^14][^29]

This avoids overstating novelty while still articulating a **real contribution**.

***

## Red flags and weaknesses

You should be very clear about the limitations:

1. **Dataset \& domain are not new.**
    - GramVaani / SLR118 is already widely used as the canonical telephone Hindi dataset; you’re not introducing a new corpus.[^48][^3][^4][^23]
    - Several strong Whisper‑Hindi and Indic models are already trained and evaluated on this data.[^5][^12][^7][^19][^20][^11][^1][^2][^6][^16][^8]
2. **Whisper on telephony Hindi is not a blank space.**
    - IndicWhisper (a Whisper‑derived model) has clear WER on GramVaani in the Vistaar paper.[^10][^7][^9][^5]
    - ARTPARK’s Whisper‑Vaani models report WER on GramVaani, and SandLogic uses these for call‑analytics.[^19][^20][^6][^8][^21]
    - Whisper‑based systems are already used in production Indian call‑center settings (SPEECH‑24, Oriserve).[^36][^35][^34]
3. **Risk of being “just a re‑evaluation” of existing models.**
    - If CallWhisper‑8k **only** re‑reports WER for existing models on GramVaani without new angles (preprocessing, thorough cross‑family comparison, error analysis, or new datasets), it will look incremental and possibly weak as a research artifact.
4. **Engineering vs research gap.**
    - As a **student flagship project**, a highly engineered, fully reproducible benchmark with strong documentation and scripts is still valuable.
    - As a **research collaboration or publishable paper**, you will likely need to go beyond “benchmarking” into **new insights**: e.g., showing which preprocessing or domain‑adaptation strategies materially change telephony performance and why (or providing a new dataset variant / annotation).[^14][^29][^27]

So: the project is **not fully duplicated**, but its novelty is modest unless you expand the scope and depth.

***

## Better research angle and stronger framing

To make this project more compelling (and publishable), consider **pivoting from “just a benchmark” to “a systematic study of telephony adaptation for Whisper‑family and Indic ASR”**.

Here are some concrete ways to strengthen it:

### 1. Make preprocessing the central research question

Instead of “benchmarking Whisper on telephony Hindi,” pitch it as:

> “How do different **telephony preprocessing pipelines** affect Whisper‑family and Indic ASR models on Indian telephone‑style Hindi?”

Study:

- 8 kHz original → 16 kHz naive upsampling vs proper interpolation filters.[^44][^29][^14]
- With vs without **speech‑band band‑pass** (e.g., 80 Hz–4 kHz/8 kHz) before feeding Whisper.[^42][^43]
- Various **loudness normalization / dynamic range compression** strategies, tuned for telephone audio.[^41]
- Synthetic **8 kHz round‑trip**: take high‑quality Hindi (FLEURS, Kathbath) and pass through telephone channel simulation to compare to true GramVaani.[^7][^22][^14]

This kind of ablation is **not present** in current GramVaani or Whisper‑Hindi literature.

### 2. Align with domain adaptation work

Take inspiration from “Bridging the Reality Gap”:

- Reuse their idea of **domain adaptation + multi‑domain replay**, but apply it to **Whisper‑family models** instead of IndicWav2vec.[^30][^29][^27]
- Compare **preprocessing‑only improvements vs light adaptation (LoRA) on telephony Hindi** to quantify how much each knob buys you.

This turns your project into a **methodological comparison**: “Is it better to tune preprocessing, fine‑tune the model, or both, under realistic resource constraints?”

### 3. Explicit, multi‑family telephony comparison

Curate a **small but representative model zoo**:

- Vanilla Whisper (several sizes).[^49][^50]
- Hindi‑tuned Whisper from different groups (Vasista, Collabora, ARTPARK).[^32][^20][^1][^2][^31][^6][^16][^8][^19]
- IndicWhisper and IndicWav2vec (AI4Bharat).[^51][^12][^11][^5][^7]
- Possibly Vakyansh or other Indian ASR if licenses allow.

Run them all through the **same** telephony evaluation harness and preprocessing variants. This gives you a **comparative story** rather than a single‑model story.

### 4. Add error analysis and qualitative insights

Go beyond WER/CER:

- Analyse **error types** specific to telephone Hindi:
    - dropouts, false insertions during noise, regional lexical variants, mis‑transcription of named entities, etc.[^3][^23][^14]
- If you include **Hinglish/code‑switching telephone segments**, study how models fail on switches vs monolingual segments.[^47][^46][^35][^36]

This again is under‑developed in existing papers, which mostly report aggregate WER.

### 5. Deliverables: make it a real benchmark suite

To justify the “benchmark” label:

- Release a **clean, containerised evaluation toolkit** (Docker or Makefile) that:
    - downloads legally shareable subsets of GramVaani / other telephony datasets,
    - runs preprocessing configurations,
    - calls multiple models through a unified interface,
    - outputs WER/CER + error breakdowns.
- Provide **ready‑made YAML configs** for each model + preprocessing combo.

This engineering‑heavy angle is quite suitable as a flagship student project, even if the pure research novelty is moderate.

***

## Bottom line for novelty

- **Status:** The exact idea “Whisper on Indian telephone‑style Hindi (GramVaani)” is **partially done**; there are Whisper‑derived models and WERs on GramVaani, but scattered and model‑centric.[^20][^1][^2][^5][^6][^16][^7][^8][^19][^38]
- **Gap:** A **model‑agnostic, Whisper‑centric, telephony‑specific benchmark that systematically studies preprocessing and 8 kHz conditions for Indian Hindi/Hinglish** is still open.[^41][^44][^29][^14][^37]

As a **student flagship project**, CallWhisper‑8k can be novel enough **if you lean into the telephony + preprocessing + multi‑model evaluation angle**, and you’re transparent that you’re building on top of GramVaani / Vistaar rather than claiming to be “the first” to touch Whisper on this domain.
<span style="display:none">[^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^80][^81][^82][^83][^84][^85][^86][^87]</span>

<div align="center">⁂</div>

[^1]: https://huggingface.co/vasista22/whisper-hindi-medium

[^2]: https://huggingface.co/vasista22/whisper-hindi-small/raw/refs%2Fpr%2F6/README.md

[^3]: https://sites.google.com/view/gramvaaniasrchallenge/dataset

[^4]: https://www.openslr.org/118/

[^5]: https://github.com/parthiv11/IndicWhisper-JAX

[^6]: https://huggingface.co/ARTPARK-IISc/whisper-large-v3-vaani-hindi/blob/main/README.md

[^7]: https://github.com/AI4Bharat/vistaar

[^8]: https://huggingface.co/ARTPARK-IISc/whisper-medium-vaani-hindi

[^9]: https://ar5iv.labs.arxiv.org/html/2305.15386

[^10]: https://huggingface.co/parthiv11/indic_whisper_nodcil/blame/df9f82bb838f79fe189ae8e8663116679aba1895/README.md

[^11]: https://github.com/AI4Bharat/vistaar/blob/master/README.md

[^12]: https://huggingface.co/parthiv11/indic_whisper_nodcil

[^13]: https://huggingface.co/parthiv11/indic_whisper_nodcil/raw/main/README.md

[^14]: https://www.emergentmind.com/topics/indicwav2vec

[^15]: https://huggingface.co/vasista22/whisper-hindi-small

[^16]: https://huggingface.co/vasista22/whisper-hindi-large-v2

[^17]: https://dataloop.ai/library/model/vasista22_whisper-hindi-medium/

[^18]: https://github.com/vasistalodagala

[^19]: https://huggingface.co/ARTPARK-IISc/whisper-tiny-vaani-hindi

[^20]: https://huggingface.co/ARTPARK-IISc/whisper-large-v3-vaani-hindi/raw/main/README.md

[^21]: https://vaani.iisc.ac.in/case-studies/sandlogic

[^22]: https://arxiv.org/html/2408.11440v1

[^23]: https://www.isca-archive.org/interspeech_2022/bhanushali22_interspeech.html

[^24]: https://www.cse.iitd.ac.in/~aseth/Gram_Vaani_ASR_Challenge_Interspeech.pdf

[^25]: https://www.isca-archive.org/interspeech_2022/bhanushali22_interspeech.pdf

[^26]: https://sites.google.com/view/gramvaaniasrchallenge/home

[^27]: https://arxiv.org/abs/2512.16401v1

[^28]: https://www.emergentmind.com/papers/2512.16401

[^29]: https://arxiv.org/html/2512.16401v1

[^30]: https://www.themoonlight.io/en/review/bridging-the-reality-gap-efficient-adaptation-of-asr-systems-for-challenging-low-resource-domains

[^31]: https://www.collabora.com/news-and-blog/news-and-events/breaking-language-barriers-20-moving-closer-production-ready-hindi-asr.html

[^32]: https://huggingface.co/collabora/whisper-base-hindi

[^33]: https://www.collabora.com/news-and-blog/news-and-events/breaking-language-barriers-fine-tuning-whisper-for-hindi.html

[^34]: https://www.linkedin.com/posts/ansh-nahar_whos-been-listening-activity-7319245237141323776-PczU

[^35]: https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Swift

[^36]: https://oriserve.com/blog/oriserve-open-sources-india-focused-ai-speech-model-fine-tuned-on-whisper

[^37]: https://www.voicegain.ai/post/2025-speech-to-text-accuracy-benchmark-for-8-khz-call-center-audio-files

[^38]: https://www.kaggle.com/code/sujaykapadnis/iitb-indic-whisper

[^39]: https://huggingface.co/speechbrain/asr-whisper-medium-commonvoice-hi

[^40]: https://openai.com/hi-IN/index/whisper/

[^41]: https://github.com/SYSTRAN/faster-whisper/discussions/273

[^42]: https://mbrenndoerfer.com/writing/speech-representations-mel-spectrograms

[^43]: https://ieeexplore.ieee.org/iel8/6287639/11323511/11482122.pdf

[^44]: https://stackoverflow.com/questions/71995979/upsampling-audio-data

[^45]: https://defined.ai/datasets/hindi-call-center-1

[^46]: https://arxiv.org/abs/1810.00662

[^47]: https://www.sciencedirect.com/science/article/abs/pii/S0045790624009030

[^48]: https://aikosh.indiaai.gov.in/home/datasets/details/hindi_asr_benchmark_dataset_for_speech_recognition_gramvaani_hindi.html

[^49]: https://en.wikipedia.org/wiki/Whisper_(speech_recognition_system)

[^50]: https://openai.com/index/whisper/

[^51]: https://aikosh.indiaai.gov.in/home/models/details/ai4bharat_indicwav2vec_hindi_hindi_speech_recognition_model.html

[^52]: https://github.com/2003HARSH/OpenAI-Whisper-Automated-Hindi-Speech-Recognition

[^53]: https://github.com/ArkS0001/IIT-Bombay-Whisper-Hindi-ASR-Model-Machine-Learning-Intern

[^54]: https://github.com/Ayushverma135/Whisper-Hindi-ASR-model-IIT-Bombay-Internship

[^55]: https://huggingface.co/mjwong/whisper-small-singlish

[^56]: https://community.openai.com/t/whisper-api-for-hindi-speech-to-text/1046744

[^57]: https://www.1mg.com/otc/whisper-ultra-skin-love-soft-sanitary-pads-for-women-xl-otc545814

[^58]: https://www.isca-archive.org/interspeech_2023/bhogale23_interspeech.pdf

[^59]: https://www.openslr.org/resources.php

[^60]: https://marketplace.databricks.com/details/8d596e98-b4c0-4e0b-85c7-c6a8d62700a1/WiserBrandcom_Hindi-Call-Center-Conversation-Dataset-Real-customeragent-dialogues-for-AI-and-speech-model-

[^61]: https://aikosh.indiaai.gov.in/home/datasets/details/iit_m_asr_hindi_evaluation_benchmark.html

[^62]: https://arxiv.org/html/2602.03868v1

[^63]: https://www.linkedin.com/posts/artpark-in_artpark-vaanidataset-aiforbharat-activity-7389156568656707584-lx4R

[^64]: https://ai4bharat.iitm.ac.in/areas/model/ASR/IndicWhisper

[^65]: https://www.scribd.com/document/973903426/ASR-Model-Evaluation-Report

[^66]: https://play.google.com/store/apps/details?id=com.whisper.android.tflitecpp\&hl=en_IN

[^67]: https://huggingface.co/blog/danielrosehill/whisper-hebrish

[^68]: https://github.com/STiFLeR7/Whisper-Hindi-ASR-Model-IIT-Bombay-Internship

[^69]: https://aikosh.indiaai.gov.in/home/datasets/details/hindi_asr_benchmark_dataset_for_speech_recognition_commonvoice_hindi.html

[^70]: https://www.reddit.com/r/speechtech/comments/1mboz21/how_are_people_handling_codeswitching_in_asr/

[^71]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11581396/

[^72]: https://www.bmz-digital.global/wp-content/uploads/2026/02/Indic-Voice-Technologies-For-An-Inclusive-Digital-India_Toolkit-for-Developers.pdf

[^73]: https://arxiv.org/html/2312.15821v1

[^74]: https://github.com/AI4Bharat/Pratinidhi

[^75]: https://www.mathworks.com/help/pdf_doc/audio/audio_ref.pdf

[^76]: https://dict.hinkhoj.com/whisper-meaning-in-hindi.words

[^77]: https://www.facebook.com/gramvaani/posts/gram-vaani-with-its-community-voice-platforms-has-joined-hands-with-bhashini-equ/743531594469395/

[^78]: https://www.youtube.com/watch?v=ZwTi7eWGVuY

[^79]: https://arxiv.org/html/2603.28714v1

[^80]: https://lamarr-institute.org/blog/fine-tuning-whisper-marathi-asr/

[^81]: https://en.bab.la/dictionary/english-hindi/whisper

[^82]: https://www.context.news/ai/india-turns-to-ai-to-capture-its-121-languages

[^83]: https://dl.acm.org/doi/full/10.1145/3772318.3791734

[^84]: https://en.wikipedia.org/wiki/Interactive_voice_response

[^85]: https://openreview.net/pdf/90736d23d01aef5692339a5fd80fd5a72ccf3e08.pdf

[^86]: https://model.aibase.com/models/details/1915693349128003586

[^87]: https://model.aibase.com/models/details/1924737381886595072

