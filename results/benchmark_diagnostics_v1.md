# Benchmark Diagnostics v1

This report adds deployment-oriented diagnostics on top of WER/CER.

Source data: existing per-sample prediction CSV exports. These diagnostics are heuristics, not final human labels.

## Summary By Model And Slice

| model | slice | num_beams | files | macro_wer | macro_cer | hallucination_risk_rate | repetition_rate | length_explosion_rate | script_drift_rate | empty_or_near_empty_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hf_whisper_small_base | fleurs_hi_clean_50 | 1 | 50 | 0.7686 | 0.4317 | 0.1000 | 0.1000 | 0.0400 | 0.0000 | 0.0000 |
| hf_whisper_small_base | fleurs_hi_clean_50 | 5 | 50 | 0.5667 | 0.2822 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0200 |
| hf_whisper_small_base | gramvaani_dev_50 | 1 | 50 | 1.5187 | 1.3071 | 0.3200 | 0.3200 | 0.1400 | 0.0000 | 0.0000 |
| hf_whisper_small_base | gramvaani_dev_50 | 5 | 50 | 1.0293 | 0.7571 | 0.1600 | 0.1600 | 0.0400 | 0.0000 | 0.0000 |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 1 | 32 | 1.7725 | 1.6367 | 0.3125 | 0.3125 | 0.1875 | 0.0000 | 0.0000 |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 5 | 32 | 1.1579 | 0.9158 | 0.1875 | 0.1875 | 0.0625 | 0.0000 | 0.0000 |
| hf_whisper_small_base | gramvaani_dev_50_highrate | 1 | 18 | 1.0675 | 0.7212 | 0.3333 | 0.3333 | 0.0556 | 0.0000 | 0.0000 |
| hf_whisper_small_base | gramvaani_dev_50_highrate | 5 | 18 | 0.8006 | 0.4748 | 0.1111 | 0.1111 | 0.0000 | 0.0000 | 0.0000 |
| hf_whisper_small_lora | fleurs_hi_clean_50 | 1 | 50 | 0.5236 | 0.2074 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| hf_whisper_small_lora | fleurs_hi_clean_50 | 5 | 50 | 0.5128 | 0.1944 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| hf_whisper_small_lora | gramvaani_dev_50 | 1 | 50 | 0.7473 | 0.4671 | 0.0800 | 0.0800 | 0.0000 | 0.0000 | 0.0200 |
| hf_whisper_small_lora | gramvaani_dev_50 | 5 | 50 | 0.7532 | 0.5772 | 0.1600 | 0.1600 | 0.0000 | 0.0000 | 0.0200 |
| hf_whisper_small_lora | gramvaani_dev_50_8khz | 1 | 32 | 0.8708 | 0.5823 | 0.1250 | 0.1250 | 0.0000 | 0.0000 | 0.0312 |
| hf_whisper_small_lora | gramvaani_dev_50_8khz | 5 | 32 | 0.8946 | 0.7869 | 0.2500 | 0.2500 | 0.0000 | 0.0000 | 0.0312 |
| hf_whisper_small_lora | gramvaani_dev_50_highrate | 1 | 18 | 0.5277 | 0.2622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| hf_whisper_small_lora | gramvaani_dev_50_highrate | 5 | 18 | 0.5018 | 0.2044 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## High-Risk Examples

| model | slice | num_beams | wer | cer | flags | reference | hypothesis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 1 | 10.7143 | 7.7500 | hallucination, repetition, length_explosion | ये संघ के जीतने भी सदस्य हैं | तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो ... |
| hf_whisper_small_base | gramvaani_dev_50 | 1 | 10.7143 | 7.7500 | hallucination, repetition, length_explosion | ये संघ के जीतने भी सदस्य हैं | तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो तो ... |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 1 | 4.8571 | 6.1071 | hallucination, repetition, length_explosion | इसी के साथ में अपने वक्तव को | अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव... |
| hf_whisper_small_base | gramvaani_dev_50 | 1 | 4.8571 | 6.1071 | hallucination, repetition, length_explosion | इसी के साथ में अपने वक्तव को | अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव्टल्ब को अपनी बव... |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 1 | 3.2222 | 3.2979 | hallucination, repetition, length_explosion | स्कूल समय के पश्चात् ईमेल मोबाइल के जरिए शिक्षक | इस्खुज़् सणेके पाँताख इनेल मुवाल्ग यजर्ये सिथ खाएगा वाँगा वाँगा वाँगा वाँगा वाँगा वाँगा... |
| hf_whisper_small_base | gramvaani_dev_50 | 1 | 3.2222 | 3.2979 | hallucination, repetition, length_explosion | स्कूल समय के पश्चात् ईमेल मोबाइल के जरिए शिक्षक | इस्खुज़् सणेके पाँताख इनेल मुवाल्ग यजर्ये सिथ खाएगा वाँगा वाँगा वाँगा वाँगा वाँगा वाँगा... |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 5 | 3.7778 | 3.2128 | hallucination, repetition, length_explosion | स्कूल समय के पश्चात् ईमेल मोबाइल के जरिए शिक्षक | इखुर सने के पाँताग इनेल मुवाल दिजर ये सिथ खाएगे तुद खाएगे तुद खाएगे तुद खाएगे तुद खाएगे... |
| hf_whisper_small_base | gramvaani_dev_50 | 5 | 3.7778 | 3.2128 | hallucination, repetition, length_explosion | स्कूल समय के पश्चात् ईमेल मोबाइल के जरिए शिक्षक | इखुर सने के पाँताग इनेल मुवाल दिजर ये सिथ खाएगे तुद खाएगे तुद खाएगे तुद खाएगे तुद खाएगे... |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 5 | 3.4545 | 3.0175 | hallucination, repetition, length_explosion | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो | अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अप... |
| hf_whisper_small_base | gramvaani_dev_50 | 5 | 3.4545 | 3.0175 | hallucination, repetition, length_explosion | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो | अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अपने अप... |
| hf_whisper_small_base | gramvaani_dev_50_8khz | 1 | 4.0909 | 2.8947 | hallucination, repetition, length_explosion | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो | अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर... |
| hf_whisper_small_base | gramvaani_dev_50 | 1 | 4.0909 | 2.8947 | hallucination, repetition, length_explosion | स्थिती को देखते हुए तथा इस मामले को गंभीरतापूर्वक लेगी तो | अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर अगर... |

## Flag Definitions

- `hallucination_risk_rate`: share of files with length explosion, repetition, repeated characters, or script drift.
- `repetition_rate`: share of files with repeated token, n-gram, or character-loop patterns.
- `length_explosion_rate`: hypothesis has at least 2.5x as many tokens as reference and at least 8 tokens.
- `script_drift_rate`: mostly Devanagari reference but substantial Latin-script hypothesis.
- `empty_or_near_empty_rate`: hypothesis has 0-1 tokens while reference has at least 3 tokens.

Interpretation: these flags are meant to catch ASR behavior that can matter in voice-agent or call-analytics settings even when WER/CER already look bad.
