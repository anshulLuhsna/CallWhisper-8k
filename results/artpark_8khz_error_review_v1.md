# ARTPARK Native 8 kHz Error Review v1

This sheet ranks the highest-WER `ARTPARK` predictions and shows `large-v3` on the same files. Rankings select review candidates; they do not determine the human classification.

For each file, listen once or twice and fill the five review fields. Compare both hypotheses against what is actually audible, not only against the supplied reference.

Allowed primary classification: `model_failure`, `bad_audio`, `questionable_reference`, `mixed`, or `uncertain`.

## Pairwise Context

Across all 56 files, `ARTPARK` had lower per-file WER than `large-v3` on 53 files, tied on 2, and had higher WER on 1. The review list below still focuses on `ARTPARK`'s largest remaining errors, even when it remains better than the comparison model.

## 01. `02-14479-01`

- Review audio: `results/artpark_8khz_review_files/01_02-14479-01.mp3`
- ARTPARK: WER `0.6857`, CER `0.3314`
- large-v3: WER `0.8000`, CER `0.4114`
- WER delta (ARTPARK minus large-v3): `-0.1143`

Reference:

> मोबाइल वाणी को बताया की सिकंदरा प्रखण्ड अंतर्गत आँगनबाड़ी सँख्या एक सौ उन्नतीस की गुड़िया देवी को बंद पोषाहार की राशि चालू कराने के लिए सी डी पी ओ ने चालीस हजार रूपये माँगा था

ARTPARK hypothesis:

> मोबाइल वाणी को बताया की विकंदरा प्रखंड अंत को ध्यान लो मेडिशियल सबसे अब चौ उनतीस की शेर का गुड़िया देगी निबंध पोशाहार की राशी चालू कराने के लिए सिदीपियों ने चालीस हजार रूपए मांगना था

large-v3 hypothesis:

> मोबाइल वानी को बताया कि धिकंद्रा प्रखन अतको धानो मडिकेल संस्याब्शों उन्तीज की शेर का गुडिया ने भी तेबंद पोसाहार किराशिकालो पराने के लिए शिरीपियो ने टाले जारूपे मान ला था।

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: no noise
- Reviewer notes: ARTPARK got the parts i understood. Middle part is genuinely not understandable even after reading reference.

## 02. `01-04388-02`

- Review audio: `results/artpark_8khz_review_files/02_01-04388-02.mp3`
- ARTPARK: WER `0.6667`, CER `0.4500`
- large-v3: WER `0.6667`, CER `0.4500`
- WER delta (ARTPARK minus large-v3): `0.0000`

Reference:

> मैं कमलकुट्टी पश्चिमी सिंहभुम झारखण्ड से

ARTPARK hypothesis:

> मैं कमारपुर पश्चिम झारखण्ड ऐसी

large-v3 hypothesis:

> मैं कमाचुर्पी पत्मितिम्बुं धारखन से

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: clear audio no noise
- Reviewer notes: missed entire word - सिंहभुम, but the speaker did say it lightly. Also worse than large v3 for the से

## 03. `01-04496-02`

- Review audio: `results/artpark_8khz_review_files/03_01-04496-02.mp3`
- ARTPARK: WER `0.6500`, CER `0.3137`
- large-v3: WER `1.0000`, CER `1.0000`
- WER delta (ARTPARK minus large-v3): `-0.3500`

Reference:

> सोची मसल दिखाया खूब अपने प्रतिद्वंदी को धुल चटा कर अखाड़ा जीत लिया सलमान ने प्रशंसकों ने खूब तारीफ़ की

ARTPARK hypothesis:

> बहुत ही मतलब दिखाया खूब सुनसान भी अपने प्रतिदिन्दी को छूल जटाकर अखाड़ा जीत लिया सलमानी प्रसंशकों ने खूब तारीख की

large-v3 hypothesis:

> *(empty transcription)*

- Classification: mixed
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): incomplete - there is some speech between  खूब and अपने like ARTPARK has correctly shown
- Audio notes: speaker audio is distorted
- Reviewer notes: Model got some obvious words wrong, audio is also bad but it should have done better.

## 04. `01-03025-02`

- Review audio: `results/artpark_8khz_review_files/04_01-03025-02.mp3`
- ARTPARK: WER `0.5750`, CER `0.2806`
- large-v3: WER `0.9750`, CER `0.8418`
- WER delta (ARTPARK minus large-v3): `-0.4000`

Reference:

> ठंड का प्रकोप तेज़ होने की वजह से बाजार स्थित सिर्फ गर्म गर्म कपड़ो की स्थाई व अस्थाई दुकानों में गरम कपड़ो के बिक्री बिक्री में अचानक तेजी आ गयी है बाजार में लगे गरम कपड़ो के स्थाई अस्थाई दुकानों

ARTPARK hypothesis:

> का प्रकोप चेत बनी की वजह ऐसी वजह गर्म गर्म कपड़ों की स्थाई वहाँ स्थाई दुकानों में गर्म कपड़ों की बिक्री में बिक्री में अठाना किया गयी है बाजार में लगी गर्म कपड़ों की स्थाई और स्थाई दुकानों

large-v3 hypothesis:

> दुखान में लगी करम कपलों के अच्छा आप जो कर दो

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: speaker audio did echo but it's acccounted for in the reference transcript. No noise
- Reviewer notes: ARTPARK performed well but missed the start word ठंड

## 05. `01-01711-03`

- Review audio: `results/artpark_8khz_review_files/05_01-01711-03.mp3`
- ARTPARK: WER `0.5714`, CER `0.3571`
- large-v3: WER `0.7143`, CER `0.3214`
- WER delta (ARTPARK minus large-v3): `-0.1429`

Reference:

> इसी के साथ में अपने वक्तव को

ARTPARK hypothesis:

> इसी के साथ मैं अपनी बहत्ता लूँ को

large-v3 hypothesis:

> इपनी के साथ मैं अपनी बवत तबु को

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): wrong - it does not sound like वक्तव
- Audio notes: clear speaker, no noise
- Reviewer notes: audio is bad even i didn't understand and reference is also guessing.

## 06. `01-09354-02`

- Review audio: `results/artpark_8khz_review_files/06_01-09354-02.mp3`
- ARTPARK: WER `0.5385`, CER `0.3413`
- large-v3: WER `0.7308`, CER `0.4603`
- WER delta (ARTPARK minus large-v3): `-0.1923`

Reference:

> जन्मदिन पर पौधारोपण कर दिया भगत सिंह ने बोकारो के प्रगन में छायादार व फलादेश के पौधे लगाए यह प्रेरणा उनको उनके पिता आर सी गारी

ARTPARK hypothesis:

> जन्मदिन आरोप पौधा रोपण कर दिया भगत सिंह ने गोपाली की मंत्राह्यन में छायादार और खल्दा बीच के पौधे लगाए सिंह को यह रिना उनके पिता आर सी आई

large-v3 hypothesis:

> जन्मदिन पर प्रधारुपन कर दिया भड़क चिंद्रे गोपाली की मंतुरायन में छायादार और खल्दा दिविष के पोधे लगाये इसको यह रिनाउन के पिता आर्थियाई का

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): uncertain
- Audio notes: i dont know
- Reviewer notes: its just bad audio man i didn't understand most of it either

## 07. `01-04674-01`

- Review audio: `results/artpark_8khz_review_files/07_01-04674-01.mp3`
- ARTPARK: WER `0.5000`, CER `0.2101`
- large-v3: WER `0.7500`, CER `0.3406`
- WER delta (ARTPARK minus large-v3): `-0.2500`

Reference:

> नमस्कार मैं प्रमोद कुमार मोबाइल मीडिया रिपोर्टर हज़ारीबाग पदमा में आयोजित पीडीएस लाभार्थी व्यक्तियों ने पदमा प्रखंड के गारूपेड़ा सिमरतुहरा

ARTPARK hypothesis:

> नमस्कार मैं प्रमोद कुमार मोबाइल मीडिया रिपोर्टर हजारीबाग पद्मा में आयोगी पीडीएफ लाभ्याप्ति विचिंह पद्मा प्रखंड के गालपुरा सिमरपुरा

large-v3 hypothesis:

> नमस्तार मैं कर्मोत कुमार मोबाइल मेडिया रिपोर्टर हजारी बार पदमा में आयोगे पेटिया खिलाब्याप्ती विशी हैं पदमा परखंड केजार पूरा शीमर पूरा

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): barely
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: lots of echo, distortion
- Reviewer notes: what a mess of an audio.

## 08. `02-19849-01`

- Review audio: `results/artpark_8khz_review_files/08_02-19849-01.mp3`
- ARTPARK: WER `0.5000`, CER `0.2059`
- large-v3: WER `0.8333`, CER `0.4412`
- WER delta (ARTPARK minus large-v3): `-0.3333`

Reference:

> नमस्कार मित्रों में रंजन स्वजना से

ARTPARK hypothesis:

> नमस्कार मित्रों मई रंजन सौजाना ऐसी

large-v3 hypothesis:

> नमस्कार मिचलो मेरा जनस वाजानाती

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: clear audio no noise.
- Reviewer notes: ARTPARK consistently mis-classifies से to ऐसी

## 09. `02-18228-01`

- Review audio: `results/artpark_8khz_review_files/09_02-18228-01.mp3`
- ARTPARK: WER `0.4828`, CER `0.2244`
- large-v3: WER `0.6897`, CER `0.4103`
- WER delta (ARTPARK minus large-v3): `-0.2069`

Reference:

> दो हज़ार उन्नीस के लिए भारतीय जनता पार्टी वार्षिक एलान हर बूथ पर होगा सेलफोन प्रमुख राजस्थान एम पी छत्तीसगढ़ मिजोरम के साथ होगा तेलंगाना में विधान सभा चुनाव

ARTPARK hypothesis:

> दो हजार उन्नीस के लिए भारतीय जनता पार्टी का वास्तव अभियान हर बुझ आरोप होगा सेल फोन प्रमुख राजस्थान एंट्री छत्तीसगढ़ निजीरम के साथ होगा चलेंगाना में विधान संवच्छना हो

large-v3 hypothesis:

> 2019 के लिए भाती जनता पार्टी का वास्तु का जान हर बूत पर होगा एक सेलफोन परमुख राजसान MP36 वा निजेडम के साथ होगा चलिंगाना में विदान तवच्छना है

- Classification: bad_audio
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: too much distortion
- Reviewer notes: only understood the start. audio is like an echo chamber its all so distorted.

## 10. `01-11380-01`

- Review audio: `results/artpark_8khz_review_files/10_01-11380-01.mp3`
- ARTPARK: WER `0.4783`, CER `0.1600`
- large-v3: WER `0.5652`, CER `0.2240`
- WER delta (ARTPARK minus large-v3): `-0.0870`

Reference:

> वहीं जबकि बकरीद पर्व को देखते हुए प्रखंड के सभी इलाकों में बी डी ओ चिरंजीव पांडेय अंचलाधिकारी अखलेश कुमार सिन्हा थाना अध्यक्ष

ARTPARK hypothesis:

> वही जब की बकरीद वर्ग को देखते हुए प्रखंड के सभी इलाकों में विडियो चेंजिंग पांडे अंचला अधिकारी अखिलेश कुमार सिन्हा थाना अध्यक्ष

large-v3 hypothesis:

> वहीं जबकि बकरित बर्ग को ज़िखते हुए परखंड के सभी इलाकों में विद्यो चिंजिव पांडे अंतुला धिकारी अकलेश कुमार सिन्हा ठाना अधेस

- Classification: questionable_reference
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): wrong
- Audio notes: bit of distortion
- Reviewer notes: ARTPARK is better than reference. बी डी ओ is wrong विडियो is correct.

## 11. `13-00246-02`

- Review audio: `results/artpark_8khz_review_files/11_13-00246-02.mp3`
- ARTPARK: WER `0.4412`, CER `0.3750`
- large-v3: WER `0.6176`, CER `0.3214`
- WER delta (ARTPARK minus large-v3): `-0.1765`

Reference:

> अपराधियों को आरोपित किया गया है घट घटना में साढ़े तीन लाख रूपए लूट का खुलासा किया गया है दर्ज प्राथमिकी में कहा गया है कि शुक्रवार की रात अवधेश कुमार समस्तीपुर की दूकान

ARTPARK hypothesis:

> अपराधियों प्रदूषित किया गया है घटना में सारे तीन लाख रूपए लूट का खुलासा किया गया है दलपाद इसमें कहा गया है की शुक्रवार

large-v3 hypothesis:

> अपरादियों पारोषित किया गया है घतना में सारे 3 रात लुखे लूट का खुड़ा सा किया गया है दल पात्मित में कहा गया है जिस शुक्रवार परात अवधेत परात समस्ती परिश्चित दुखाव

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: end of the audio is distorted
- Reviewer notes: ARTPARK missed everything after शुक्रवार otherwise would've performed better.

## 12. `01-08044-01`

- Review audio: `results/artpark_8khz_review_files/12_01-08044-01.mp3`
- ARTPARK: WER `0.4348`, CER `0.1360`
- large-v3: WER `0.5217`, CER `0.2080`
- WER delta (ARTPARK minus large-v3): `-0.0870`

Reference:

> उनको आगे बढ़ने तथा स्वतंत्र रूप से लोग काम नहीं करने दिया क्यूँकी महिलायें जन प्रतिनिधि चाहती थी की विकास करें लेकिनसूत्र आदि

ARTPARK hypothesis:

> उसको आगे बढ़ने तथा स्वतंत्र रूप ऐसी लोग काम नहीं करने दिया क्यूँकी महिलाएँ जनप्रतिनिधि चाहती विकास करे लेकिन पुत्र आदि

large-v3 hypothesis:

> उसको आगे बढ़ने तथा स्वचंत्र रूप से लोग काम नहीं करने दिया ज्यादा कि महिलाएं जन पर्थिमर्थि मिदी चाती ती की विकास करें लेकिन पुत्र आदी

- Classification: questionable_reference
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): wrong
- Audio notes: clear
- Reviewer notes: ARTPARK missed  थी की but got लेकिन पुत्र correct which seems to be wrong in the reference.

## 13. `01-02689-01`

- Review audio: `results/artpark_8khz_review_files/13_01-02689-01.mp3`
- ARTPARK: WER `0.4286`, CER `0.2857`
- large-v3: WER `0.8571`, CER `0.6071`
- WER delta (ARTPARK minus large-v3): `-0.4286`

Reference:

> ये संघ के जीतने भी सदस्य हैं

ARTPARK hypothesis:

> के जीतने भी सदस्य है

large-v3 hypothesis:

> प्रतियसंते जितने रिश्चादत्य हैं

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: perfect
- Reviewer notes: missed the start ये संघ otherwise perfect. large-v3 is a joke at this point.

## 14. `01-03237-02`

- Review audio: `results/artpark_8khz_review_files/14_01-03237-02.mp3`
- ARTPARK: WER `0.3871`, CER `0.3043`
- large-v3: WER `0.4516`, CER `0.2919`
- WER delta (ARTPARK minus large-v3): `-0.0645`

Reference:

> पीड़ित की सहायता करने वाला ही पुलिस की जायतियों का पहला शिकार होता है आज प्रत्यक्ष दर्शी एवं गवाहों के सुरक्षा के साथ पुलिस को भी अपना व्यवहार बदलाव होगा धन्यवाद

ARTPARK hypothesis:

> पुलिस की सहायता करने वाला ही पुलिस की जायजातियों का फसल शिकार होता आज प्रत्यक्ष पुलिस को भी अपना व्यवहार बदलना होगा धन्यवाद

large-v3 hypothesis:

> पुलिस की सहायता करने वाला है पुलिस की जायचतियों का प्रश्ना शिकार होता है आज पर्चस रशियों वो गवाओं के वर्षत पुलिस को भी अपना वैभार बदलना होगा दन्दवाश

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: clear
- Reviewer notes: ARTPARK missed some parts in between which were a bit haarder

## 15. `02-13674-02`

- Review audio: `results/artpark_8khz_review_files/15_02-13674-02.mp3`
- ARTPARK: WER `0.3714`, CER `0.1472`
- large-v3: WER `0.6571`, CER `0.3604`
- WER delta (ARTPARK minus large-v3): `-0.2857`

Reference:

> जमुई सदर प्रखंड में पन्द्रह सितम्बर को पोषण जागरूकता रैली छब्बीस सितम्बर को पोषण मेला का आयोजन किया जाना है उन्होंने ने तमाम उपस्थित जन प्रतिनिधियों पदाधिकारी तथा कर्मियों से अनुरोध करते हुए कहा कि

ARTPARK hypothesis:

> जमुई सदर प्रखंड ने पंद्रह सितम्बर को पोषण जागता रही ली तथा बीस सितम्बर को पोषण मेला का आयोजन किया जाना है उन्होंने तमाम उपस्थित जनप्रतिनिधि पदाधिकारी तथा कर्मियों सन्वेद करते हुए कहा की

large-v3 hypothesis:

> जमूँ सदर प्रखने 15 सितंबर को पोषण जजिता रह ली तथा 20 सितंबर को पोषण मेला काइजन किया जाना है उन्होंने तमाम उपस्तेज़न परतिमीद्रित राधिकारी के तक पर्विनोशन वेट करते हुए कहा की

- Classification: uncertain
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: a bit distorted
- Reviewer notes: ARTPARK did better than me at understanding.
