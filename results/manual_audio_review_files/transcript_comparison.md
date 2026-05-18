# Manual Audio Review Transcript Comparison

Raw MP3 files are in `raw_mp3/`. Normalized WAV files are in `normalized_wav/`.

## 01. `02-12557-02`

Reason: normalization helped a lot; mixed-script hallucination in raw output

Raw audio: `results/manual_audio_review_files/raw_mp3/01_02-12557-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/01_02-12557-02.wav`

Raw WER/CER: `1.273` / `1.171`
Normalized WER/CER: `0.727` / `0.315`

Actual transcript:

शीशे की बोतल यूज़ करिये और थर्मस यूज़ करिये दोस्तों ऐसे में यह होगा कि हमारा जो वायु प्रदूषित है हमारे पर्यावरण

Whisper transcript on raw MP3:

एक स्यषokol refreshing are bhatal and thinnes floating on a饥ा जू� bagheonarms. से यर भोचल 2020 कि ज़ग mergedam kire opn reached in a Bplane in a Sky map.

Whisper transcript on normalized WAV:

खेशे की बोथल यूज करयें और खर्मस यूज करयें दोस्टा अप्टिंगी यह होगा, हमारा जो वायों कर दूषिठ है, हमारे परया दरआड

## 02. `02-19188-01`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/02_02-19188-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/02_02-19188-01.wav`

Raw WER/CER: `0.568` / `0.254`
Normalized WER/CER: `0.676` / `0.321`

Actual transcript:

श्रोताओं मोबाईल वाणी के बेहद लोकप्रिय और खास कार्यक्रम खबरें ज़रा हटके में आपका स्वागत है इसमें हम बात करते हैं वैसे मुद्दों के बारे में जिससे आपकी जिंदगी का सीधा सरोकार है वैसी खबरें जो जिंदगी

Whisper transcript on raw MP3:

बवाईल वानी के बिहद्डोग प्रियए और खास कारिक्रम खबरे जरा हटके में आपका स्वागत है. इस में हम बाग कते हैं वैसे मुद्दों के बारे में जिसे आपकी जिल्गी का सीधा सरुकार है. वैसी खबरे जो जिल्गी के लिए वागते है.

Whisper transcript on normalized WAV:

बवाईल वानी के भिहद्दोख प्रियए और खास कारिक्रम खबरे जरा हटके में आपका स्वागत है. इस में हम बाग कते है, वैसे मुद्दों के बारे में, जिसे आपकी जिल्गी का सीधा सरुकार है. बाग कते है, वैसी खबरे है, जो जिन्दिकी का सीधार है.

## 03. `13-00240-05`

Reason: reference starts with <incomplete>

Raw audio: `results/manual_audio_review_files/raw_mp3/03_13-00240-05.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/03_13-00240-05.wav`

Raw WER/CER: `0.458` / `0.190`
Normalized WER/CER: `0.458` / `0.190`

Actual transcript:

<incomplete> और सिर्फ बच्चे ही नहीं बल्कि कई बार बरसात के दिनों में पूरा का पूरा गाँव ही बिमारियों की चपेट में आ जाता है ऐसे में गाँव में बीमारियाँ न फैले इस के लिए स्थानीय स्तर पर किस तरह की व्यवस्था की जाती है दोस्तों आपको पता

Whisper transcript on raw MP3:

अर सर्फ बच्चे ही नहीं बलकी कई बार बरसाथ के दिनों में पूरा का पूरा गाँ ही बिमारियो के चबेट में आजाता है आफे में गाँ में बिमारिया नाफ्यले इसके लिए च्थान्यास्टर पर किस तरह की बेवस्थाग की जाती है तो आपको पता...

Whisper transcript on normalized WAV:

अर सर्फ बच्चे ही नहीं बलकी कई बार बरसाथ के दिनों में पूरा का पूरा गाँ ही बिमारियो के चबेट में आजाता है आफे में गाँ में बिमारिया नाफ्यले इसके लिए च्थान्यास्टर पर किस तरह की बेवस्थाग की जाती है तो आपको पता...

## 04. `01-02976-02`

Reason: reference ends with <incomplete>; high raw error

Raw audio: `results/manual_audio_review_files/raw_mp3/04_01-02976-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/04_01-02976-02.wav`

Raw WER/CER: `1.000` / `0.904`
Normalized WER/CER: `1.000` / `0.592`

Actual transcript:

संजीत कुमार किसान सलाहकार हिमांशु कुमार नित्यानंद प्रसाद विनोद कुमार आदि मौजूद हैं मैं जय कुमार शुक्ला मोबाइल वाणी <incomplete>

Whisper transcript on raw MP3:

आटक चढतोड ंझिल tanto Zhong-Com...

Whisper transcript on normalized WAV:

च्यान तरादार हमाच्तू कुवार, निस्जानन पकाख दिरोज कुवार आदी मोदिया, जाएच्माच्तू फुट्रा मोपाईल वानीजम।

## 05. `02-19849-01`

Reason: high WER short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/05_02-19849-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/05_02-19849-01.wav`

Raw WER/CER: `1.167` / `0.765`
Normalized WER/CER: `1.000` / `0.676`

Actual transcript:

नमस्कार मित्रों में रंजन स्वजना से

Whisper transcript on raw MP3:

नवप्काई में कि वो मैरन्यां सुवागा नासीएँ

Whisper transcript on normalized WAV:

नवप्काई मेंच्वो मैराड्यं स्वागाना सेईज़्।

## 06. `01-06773-03`

Reason: worst raw WER; very short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/06_01-06773-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/06_01-06773-03.wav`

Raw WER/CER: `1.000` / `0.684`
Normalized WER/CER: `1.000` / `0.684`

Actual transcript:

झारखण्ड मोबाइल वाणी

Whisper transcript on raw MP3:

ज्यार्कल मबाल वान्दि

Whisper transcript on normalized WAV:

ज्यार्कल मबाल वान्दि

## 07. `01-00748-01`

Reason: worst raw WER

Raw audio: `results/manual_audio_review_files/raw_mp3/07_01-00748-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/07_01-00748-01.wav`

Raw WER/CER: `1.000` / `0.936`
Normalized WER/CER: `0.960` / `0.624`

Actual transcript:

दंगे में कौन मारता है किसका घर जलता है क्या कोई पाकिस्तानी या जापानी मारता है क्या कोई पाकिस्तानी या जापानी मारता है क्या कोई

Whisper transcript on raw MP3:

। । । । । । । । ।

Whisper transcript on normalized WAV:

धँगे में कों न मरथा हैं... किसके जफता हैं यNOUN कोरी पासि appro यаты यह जपाने सें के को對啊

## 08. `01-01598-02`

Reason: normalization improvement

Raw audio: `results/manual_audio_review_files/raw_mp3/08_01-01598-02.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/08_01-01598-02.wav`

Raw WER/CER: `0.964` / `0.761`
Normalized WER/CER: `0.714` / `0.384`

Actual transcript:

कूड़े कचड़े को फेंकते हैं उनको बुला कर उसको फेंकवाया गया और फिर से हमारी बाजार को स्वच्छ बनाया गया मैं रंजन गिरी युवा वाणी क्लब से धन्यवाद

Whisper transcript on raw MP3:

भी बजार थो सुवच दोनार गया। मैं रनकिर गी लिए वानिक प्रस्या जाँँवाः

Whisper transcript on normalized WAV:

तुरे कट्रे को थेखें, उंको बुलागार उस्टो खेखवाया गया और खिल से हमारी बजार को सुवच बुनाया गया मैं रंकिर गिल युआनिख त्रस्टे जाँग़

## 09. `02-19469-01`

Reason: normalization improvement; reference ends with <incomplete>

Raw audio: `results/manual_audio_review_files/raw_mp3/09_02-19469-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/09_02-19469-01.wav`

Raw WER/CER: `1.000` / `0.563`
Normalized WER/CER: `0.750` / `0.418`

Actual transcript:

अभी तो ये नेता बरसाती मेढक की तरह टरटराना आरम्भ कर दिए है जब जनता जागरूक नहीं होगा तबतक सत्ता के दलालो को सबक नहीं सिखाया जा सकता है गिद्धौर मोबाइल <incomplete>

Whisper transcript on raw MP3:

अभी ते निता बर्काँषी मेजा की तराटा चाचनाना आरोम कर दिये है, गभ जंपा जाग।ुख नहीं होगा, तब तब तब ष्खष्टा की तरालों को तब अख मैं शिखाया जाचता है, यदोर मुवाई वाई वाई वाई वाई वाई वाई वाई

Whisper transcript on normalized WAV:

अभी ते नेता बखाषी मेज़ की तराटा चाचनाना आरवम कर जीए है गभ जंप्ता जागुरुष नहीं होगा सब तर शखता की तरालों को सब अख़क नहीं शिखाया जाचता है इदोर मुवाईवाश्ठाः

## 10. `01-02689-01`

Reason: normalization improvement; short utterance

Raw audio: `results/manual_audio_review_files/raw_mp3/10_01-02689-01.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/10_01-02689-01.wav`

Raw WER/CER: `1.000` / `0.750`
Normalized WER/CER: `0.857` / `0.750`

Actual transcript:

ये संघ के जीतने भी सदस्य हैं

Whisper transcript on raw MP3:

अपने साँई के जिते है रूँज का दबते हैं

Whisper transcript on normalized WAV:

अपनी तेजी तेजी लुज साद़ाखते हैं

## 11. `01-02494-03`

Reason: normalization regression by WER

Raw audio: `results/manual_audio_review_files/raw_mp3/11_01-02494-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/11_01-02494-03.wav`

Raw WER/CER: `0.909` / `0.738`
Normalized WER/CER: `1.000` / `0.639`

Actual transcript:

बिहार मोबाइल वाणी के लिए खजौली मधुबनी से रामाशीष सिंह धन्यवाद

Whisper transcript on raw MP3:

यहाँ नोगे बनिकलिएद को दिरी माँद्यान से चींग लगाएद

Whisper transcript on normalized WAV:

यहाँ नुवेल बनिकलिएद, ख़िरी मज्विन्ची रामवाशेशीं रानेवाश.

## 12. `01-08315-03`

Reason: normalization regression by WER but CER improved

Raw audio: `results/manual_audio_review_files/raw_mp3/12_01-08315-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/12_01-08315-03.wav`

Raw WER/CER: `0.500` / `0.207`
Normalized WER/CER: `0.571` / `0.159`

Actual transcript:

प्रतिदिन सुनिश्चित किया गया है मजदूरी नही मिलने पर मनरेगा मजदूरों ने किया प्रदर्शन

Whisper transcript on raw MP3:

प्रतिदिन सुनिस्थ्टीच्टीट क्या गया है मजदूरी नहीं मिलने पर मन्रेगा मजदूरोनी किया प्रदाशन

Whisper transcript on normalized WAV:

प्रतिदिन सुनिस्थ चिट क्या गया है मजदूरी नहीं मिलने पर मन्रेगा मजदूरोनी किया प्रदवषन

## 13. `01-05855-03`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/13_01-05855-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/13_01-05855-03.wav`

Raw WER/CER: `0.862` / `0.437`
Normalized WER/CER: `0.931` / `0.459`

Actual transcript:

धर्म सम्प्रदाय के हो क्योंकि यहाँ शराब बनती नहीं थी तो पी कैसे जायेगा परन्तु धीरे धीरे लोगो में आदत सी पड़ गयी जब अंग्रेज चले गए उस समय

Whisper transcript on raw MP3:

दर्म खंभर्दाए क्यों है, क्यों कि नहां दरा बंदी नहीं ती तो पीचे जाएगा, परन्तु दिगे दिले लोगो में आजध इपर गगी, जदल्म दिग ज़ने गे उस्कम है।

Whisper transcript on normalized WAV:

दर्म कम गर्दाए कियों है, क्यों कि नहां दरा बंदी नहीं ती तो पीचे जाएगा, परन्तू दिगे दिले लोगो में आजध्द इपर देगी, जदल्म दिग जले डे उस्कम है।

## 14. `01-08138-03`

Reason: normalization regression

Raw audio: `results/manual_audio_review_files/raw_mp3/14_01-08138-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/14_01-08138-03.wav`

Raw WER/CER: `0.800` / `0.453`
Normalized WER/CER: `0.867` / `0.473`

Actual transcript:

दिलाया लच्छा ने फाइनल मुकाबले मैं मौजूदा जूनियर के कुलनाउत बीती दर्शन को सीधा गेमो मैं हरा कर अपनी झोली में डाला तो दोस्तों सुनते रहे ऐसे ही मुख्या खब

Whisper transcript on raw MP3:

लच्छने प्ऊनल मुकाबले में मुजुदा जुन्यर के कुन्लाउद विती दर्सशन को शीधे गेमो में हरा कर इसकिट आपनी जोलि में डाला तो तो सुन्ते रहें आपनी मुकाबले में जुदा विपी लगा

Whisper transcript on normalized WAV:

रखषे ने पार्ईल मुखाबले में मोजुदा जुन्�यर के कुन्लाउद विटी दर्षन कृषीदध गेमों में हरा कर एजकि अपनी जोली में डला तो दोर सुंथे रहें आजके ही मुखे क्धाए आप पारग है

## 15. `01-05816-03`

Reason: reference ends with <incomplete>

Raw audio: `results/manual_audio_review_files/raw_mp3/15_01-05816-03.mp3`
Normalized audio: `results/manual_audio_review_files/normalized_wav/15_01-05816-03.wav`

Raw WER/CER: `1.000` / `0.653`
Normalized WER/CER: `0.909` / `0.628`

Actual transcript:

इसकी वजह भ्र्ष्टाचार है अमेरिका की तर्ज पर यहाँ की उच्च शिक्षण संस्थानों में निशुल्क और अनुसंधान के साथ ही साथ <incomplete>

Whisper transcript on raw MP3:

इस्टी बज्याँ सब च़्चार है अगर में साथी बज्चार यहाँ ती विछ विछ विछ विछ खालन विछ वाँ और अवर संभाल की वाँची खाँटी

Whisper transcript on normalized WAV:

इस्टी बज्याँ सब ख़्चार है अग्टाटी ख़्चार यहाँ ती विछ्ठी खिल्ष्ट्वालन्ने सोढा और अव्शंभाल की खाछी खाछी
