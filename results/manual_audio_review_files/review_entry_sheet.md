# Manual Audio Review Entry Sheet

Use this file while listening. Each section has the same short questions so you can move fast.

Answer style can be brief, for example:

- understandable: yes / mostly / no
- noise: low / medium / high
- transcript complete: yes / no / unclear
- main issue: audio / transcript / model / mixed

## 01. `02-12557-02`

Reason: normalization helped a lot; mixed-script hallucination in raw output

Raw audio: `results/manual_audio_review_files/raw_mp3/01_02-12557-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/01_02-12557-02.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: low
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model 
- did normalization help to human ears: no
- short note: normalized sounds identical to human. raw whisper had mixed-transcript.

## 02. `02-19188-01`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/02_02-19188-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/02_02-19188-01.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: high background music
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- did normalization hurt to human ears: no
- short note: normalization seems to lower background music along with the actual speaker. background noise is still there but the speaker is more difficult to hear

## 03. `13-00240-05`

Reason: reference starts with `<incomplete>`

Raw audio: `results/manual_audio_review_files/raw_mp3/03_13-00240-05.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/03_13-00240-05.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: high background music
- transcript complete: yes
- does audio sound like beginning is missing: yes
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: model.
- short note: normalized audio sounds the same just quiter overall. 

## 04. `01-02976-02`

Reason: reference ends with `<incomplete>`; high raw error

Raw audio: `results/manual_audio_review_files/raw_mp3/04_01-02976-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/04_01-02976-02.wav`

- understandable: mostly 
- background noise / music / echo / clipping / multi-speaker: Medium background noise.
- transcript complete: yes
- does audio sound like ending is missing from transcript: yes
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- short note: audio seems to be cut in places or fast forwarded near the end -- even before the incomplete tag. Also normalized audio sounds the same.

## 05. `02-19849-01`

Reason: high WER short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/05_02-19849-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/05_02-19849-01.wav`

- understandable: only first half is understandable (ending not clear at all)
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- is this mainly a short-utterance decoding failure: i dont know what that means. the second half is ambigious. without the refenrence transcript i couldn't say what he said.
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- short note: normalized sounds same

## 06. `01-06773-03`

Reason: worst raw WER; very short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/06_01-06773-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/06_01-06773-03.wav`

- understandable: 2 words understantable out 3 spoken.
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- is this mainly a short-utterance decoding failure: i dont know
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- short note:

## 07. `01-00748-01`

Reason: worst raw WER

Raw audio: `results/manual_audio_review_files/raw_mp3/07_01-00748-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/07_01-00748-01.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- short note: doesn't seem to anything wrong. raw whisper just completely had a stroke it seems. 

## 08. `01-01598-02`

Reason: normalization improvement

Raw audio: `results/manual_audio_review_files/raw_mp3/08_01-01598-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/08_01-01598-02.wav`

- understandable: mostly not
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- did normalization help to human ears: none
- short note: audio quality is shit.

## 09. `02-19469-01`

Reason: normalization improvement; reference ends with `<incomplete>`

Raw audio: `results/manual_audio_review_files/raw_mp3/09_02-19469-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/09_02-19469-01.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- does audio sound like ending is missing from transcript: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- did normalization help to human ears: yes 
- short note:

## 10. `01-02689-01`

Reason: normalization improvement; short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/10_01-02689-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/10_01-02689-01.wav`

- understandable: mostly
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- is this mainly a short-utterance decoding failure: i dont know
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- did normalization help to human ears: yes
- short note:

## 11. `01-02494-03`

Reason: normalization regression by WER

Raw audio: `results/manual_audio_review_files/raw_mp3/11_01-02494-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/11_01-02494-03.wav`

- understandable: no
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- did normalization hurt to human ears: sounds the same
- short note:

## 12. `01-08315-03`

Reason: normalization regression by WER but CER improved

Raw audio: `results/manual_audio_review_files/raw_mp3/12_01-08315-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/12_01-08315-03.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: low background music
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model 
- did normalization hurt to human ears: no
- short note:

## 13. `01-05855-03`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/13_01-05855-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/13_01-05855-03.wav`

- understandable: no
- background noise / music / echo / clipping / multi-speaker: none
- transcript complete: one word is wrong at the start.
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- did normalization hurt to human ears: no
- short note:

## 14. `01-08138-03`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/14_01-08138-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/14_01-08138-03.wav`

- understandable: yes
- background noise / music / echo / clipping / multi-speaker: low background music
- transcript complete: yes
- did raw Whisper fail mainly because of audio quality, transcript quality, or model behavior: model
- did normalization hurt to human ears: no it sounds the same
- short note:

## 15. `01-05816-03`

Reason: reference ends with `<incomplete>`

Raw audio: `results/manual_audio_review_files/raw_mp3/15_01-05816-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/15_01-05816-03.wav`

- understandable: no
- background noise / music / echo / clipping / multi-speaker: 
- transcript complete: yes
- does audio sound like ending is missing from transcript: yes
- did Whisper fail mainly because of audio quality, transcript quality, or model behavior: audio quality
- short note: worst audio quality
