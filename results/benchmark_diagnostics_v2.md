# Benchmark Diagnostics v2

This report adds deployment-oriented diagnostics on top of WER/CER.

Source data: per-sample prediction exports. These diagnostics are heuristics, not final human labels.

## Summary By Model And Slice

| model | slice | num_beams | files | macro_wer | macro_cer | hallucination_risk_rate | repetition_rate | length_explosion_rate | script_drift_rate | empty_or_near_empty_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100 | 0 | 100 | 0.2565 | 0.1275 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100_8khz | 0 | 56 | 0.3091 | 0.1650 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ARTPARK-IISc/whisper-medium-vaani-hindi | gramvaani_dev_100_highrate | 0 | 44 | 0.1895 | 0.0798 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| large-v3 | gramvaani_dev_100 | 0 | 100 | 0.5182 | 0.2780 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0200 |
| large-v3 | gramvaani_dev_100_8khz | 0 | 56 | 0.6083 | 0.3505 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0179 |
| large-v3 | gramvaani_dev_100_highrate | 0 | 44 | 0.4036 | 0.1856 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0227 |
| medium | gramvaani_dev_100 | 0 | 100 | 0.7182 | 0.4316 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0600 |
| medium | gramvaani_dev_100_8khz | 0 | 56 | 0.7889 | 0.4962 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0893 |
| medium | gramvaani_dev_100_highrate | 0 | 44 | 0.6281 | 0.3494 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0227 |

## High-Risk Examples

| model | slice | num_beams | wer | cer | flags | reference | hypothesis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large-v3 | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | सोची मसल दिखाया खूब अपने प्रतिद्वंदी को धुल चटा कर अखाड़ा जीत लिया सलमान ने प्रशंसकों ने... |  |
| large-v3 | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | सोची मसल दिखाया खूब अपने प्रतिद्वंदी को धुल चटा कर अखाड़ा जीत लिया सलमान ने प्रशंसकों ने... |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | दंगे में कौन मारता है किसका घर जलता है क्या कोई पाकिस्तानी या जापानी मारता है क्या कोई ... |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | सोची मसल दिखाया खूब अपने प्रतिद्वंदी को धुल चटा कर अखाड़ा जीत लिया सलमान ने प्रशंसकों ने... |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | जन्मदिन पर पौधारोपण कर दिया भगत सिंह ने बोकारो के प्रगन में छायादार व फलादेश के पौधे लग... |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | शीशे की बोतल यूज़ करिये और थर्मस यूज़ करिये दोस्तों ऐसे में यह होगा कि हमारा जो वायु प्रद... |  |
| medium | gramvaani_dev_100 | 0 | 1.0000 | 1.0000 | empty, collapse | श्रोताओं मोबाईल वाणी के बेहद लोकप्रिय और खास कार्यक्रम खबरें ज़रा हटके में आपका स्वागत ह... |  |
| medium | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | दंगे में कौन मारता है किसका घर जलता है क्या कोई पाकिस्तानी या जापानी मारता है क्या कोई ... |  |
| medium | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | सोची मसल दिखाया खूब अपने प्रतिद्वंदी को धुल चटा कर अखाड़ा जीत लिया सलमान ने प्रशंसकों ने... |  |
| medium | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो |  |
| medium | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | जन्मदिन पर पौधारोपण कर दिया भगत सिंह ने बोकारो के प्रगन में छायादार व फलादेश के पौधे लग... |  |
| medium | gramvaani_dev_100_8khz | 0 | 1.0000 | 1.0000 | empty, collapse | शीशे की बोतल यूज़ करिये और थर्मस यूज़ करिये दोस्तों ऐसे में यह होगा कि हमारा जो वायु प्रद... |  |
| medium | gramvaani_dev_100_highrate | 0 | 1.0000 | 1.0000 | empty, collapse | श्रोताओं मोबाईल वाणी के बेहद लोकप्रिय और खास कार्यक्रम खबरें ज़रा हटके में आपका स्वागत ह... |  |
| large-v3 | gramvaani_dev_100 | 0 | 1.0000 | 0.9739 | empty, collapse | <incomplete> के सदस्य हूँ और स्वास्थ्य सम्बंधित कुछ जानकारी <incomplete> के दौरान देखभा... | सथियों |

## Flag Definitions

- `hallucination_risk_rate`: share of files with length explosion, repetition, repeated characters, or script drift.
- `repetition_rate`: share of files with repeated token, n-gram, or character-loop patterns.
- `length_explosion_rate`: hypothesis has at least 2.5x as many tokens as reference and at least 8 tokens.
- `script_drift_rate`: mostly Devanagari reference but substantial Latin-script hypothesis.
- `empty_or_near_empty_rate`: hypothesis has 0-1 tokens while reference has at least 3 tokens.

Interpretation: these flags are meant to catch ASR behavior that can matter in voice-agent or call-analytics settings even when WER/CER already look bad.
