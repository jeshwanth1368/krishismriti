"""Supported languages. `code` works for Groq Whisper (speech-to-text) and gTTS (text-to-speech)."""

LANGUAGES = {
    "te": {"name": "Telugu", "native": "తెలుగు"},
    "hi": {"name": "Hindi", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "native": "தமிழ்"},
    "ml": {"name": "Malayalam", "native": "മലയാളം"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ"},
    "mr": {"name": "Marathi", "native": "मराठी"},
    "bn": {"name": "Bengali", "native": "বাংলা"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    "en": {"name": "English", "native": "English"},
}


def lang_name(code: str) -> str:
    return LANGUAGES.get(code, LANGUAGES["en"])["name"]


# Short fixed phrases used by the offline demo mode and follow-up prompts.
# Only the core demo languages are hand-written; others fall back to English
# (with a Groq key the LLM writes every language itself).
PHRASES = {
    "followup": {
        "en": "{days} days ago you used {product} for {target}. Did it work?",
        "hi": "{days} दिन पहले आपने {target} के लिए {product} डाला था। क्या फायदा हुआ?",
        "te": "{days} రోజుల క్రితం {target} కోసం {product} వాడారు. పని చేసిందా?",
        "ta": "{days} நாட்களுக்கு முன் {target}க்கு {product} பயன்படுத்தினீர்கள். பலன் கிடைத்ததா?",
        "ml": "{days} ദിവസം മുമ്പ് {target}ന് {product} ഉപയോഗിച്ചു. ഫലം കിട്ടിയോ?",
    },
    "avoid": {
        "en": "Do not spray {product} again. It failed {n} times on this plot. You save ₹{cost}.",
        "hi": "{product} दोबारा मत डालिए। इस खेत में यह {n} बार फेल हुआ है। आपके ₹{cost} बचेंगे।",
        "te": "{product} మళ్ళీ కొట్టకండి. ఈ పొలంలో {n} సార్లు పని చేయలేదు. మీకు ₹{cost} మిగులుతుంది.",
        "ta": "{product} மீண்டும் தெளிக்க வேண்டாம். இந்த நிலத்தில் {n} முறை பலன் இல்லை. ₹{cost} மிச்சம்.",
        "ml": "{product} വീണ്ടും തളിക്കരുത്. ഈ പാടത്ത് {n} തവണ ഫലിച്ചില്ല. ₹{cost} ലാഭിക്കാം.",
    },
    "reuse": {
        "en": "Last time {product} worked well and the crop stayed healthy for {days} days. Use it again.",
        "hi": "पिछली बार {product} से फायदा हुआ था, फसल {days} दिन स्वस्थ रही। फिर से वही इस्तेमाल करें।",
        "te": "పోయినసారి {product} బాగా పని చేసింది, పంట {days} రోజులు ఆరోగ్యంగా ఉంది. మళ్ళీ అదే వాడండి.",
        "ta": "கடந்த முறை {product} நன்றாக வேலை செய்தது, பயிர் {days} நாட்கள் நலமாக இருந்தது. மீண்டும் அதையே பயன்படுத்துங்கள்.",
        "ml": "കഴിഞ്ഞ തവണ {product} നന്നായി ഫലിച്ചു, വിള {days} ദിവസം ആരോഗ്യത്തോടെ നിന്നു. വീണ്ടും അതുതന്നെ ഉപയോഗിക്കൂ.",
    },
    "no_spray_weather": {
        "en": "Rain or strong wind is expected in the next 24 hours. Wait before spraying.",
        "hi": "अगले 24 घंटे में बारिश या तेज हवा की संभावना है। अभी छिड़काव मत कीजिए।",
        "te": "రాబోయే 24 గంటల్లో వర్షం లేదా గాలి ఎక్కువ. ఇప్పుడు పిచికారీ చేయకండి.",
        "ta": "அடுத்த 24 மணி நேரத்தில் மழை அல்லது பலத்த காற்று வரலாம். இப்போது தெளிக்க வேண்டாம்.",
        "ml": "അടുത്ത 24 മണിക്കൂറിൽ മഴയോ ശക്തമായ കാറ്റോ ഉണ്ടാകാം. ഇപ്പോൾ തളിക്കരുത്.",
    },
    "options": {
        "en": "For {problem}, safe options for your plot are on the screen. Start with the first one.",
        "hi": "{problem} के लिए आपके खेत के सुरक्षित उपाय स्क्रीन पर हैं। पहले वाले से शुरू करें।",
        "te": "{problem} కోసం మీ పొలానికి సురక్షితమైన మార్గాలు స్క్రీన్ మీద ఉన్నాయి. మొదటిది ముందు చేయండి.",
        "ta": "{problem}க்கு உங்கள் நிலத்திற்கு பாதுகாப்பான வழிகள் திரையில் உள்ளன. முதலாவதை முதலில் செய்யுங்கள்.",
        "ml": "{problem}ന് നിങ്ങളുടെ പാടത്തിന് സുരക്ഷിതമായ വഴികൾ സ്ക്രീനിൽ ഉണ്ട്. ആദ്യത്തേത് ആദ്യം ചെയ്യൂ.",
    },
    "unknown": {
        "en": "I could not find this problem in your farm memory. Tap a picture of what you see, or send it to the expert.",
        "hi": "यह समस्या आपके खेत की याद में नहीं मिली। जो दिख रहा है उसकी तस्वीर दबाइए, या विशेषज्ञ को भेजिए।",
        "te": "ఈ సమస్య మీ పొలం జ్ఞాపకంలో దొరకలేదు. మీకు కనిపించే దాని బొమ్మను నొక్కండి, లేదా నిపుణుడికి పంపండి.",
        "ta": "இந்த பிரச்சனை உங்கள் நில நினைவில் இல்லை. நீங்கள் பார்ப்பதன் படத்தை அழுத்துங்கள், அல்லது நிபுணருக்கு அனுப்புங்கள்.",
        "ml": "ഈ പ്രശ്നം നിങ്ങളുടെ പാട ഓർമ്മയിൽ ഇല്ല. കാണുന്നതിന്റെ ചിത്രം അമർത്തൂ, അല്ലെങ്കിൽ വിദഗ്ധന് അയക്കൂ.",
    },
    "same_group": {
        "en": "{product} is the same chemical group as {failed}, which failed here. It will likely fail too.",
        "hi": "{product} उसी दवा समूह की है जिसकी {failed} यहां फेल हुई। यह भी फेल होगी।",
        "te": "{product} కూడా {failed} లాంటి మందు గుంపుదే. ఇక్కడ అది పని చేయలేదు, ఇదీ పని చేయదు.",
        "ta": "{product} என்பது {failed} போன்ற அதே மருந்து வகை. இங்கு அது பலனில்லை, இதுவும் பலனளிக்காது.",
        "ml": "{product} {failed} പോലെ ഒരേ മരുന്ന് വിഭാഗമാണ്. ഇവിടെ അത് ഫലിച്ചില്ല, ഇതും ഫലിക്കില്ല.",
    },
    "first": {"en": "First: {x}.", "hi": "सबसे पहले: {x}।", "te": "ముందుగా: {x}.", "ta": "முதலில்: {x}.", "ml": "ആദ്യം: {x}."},
    "worked_rec": {
        "en": "{product} again (worked before)", "hi": "{product} फिर से (पहले काम किया था)",
        "te": "మళ్ళీ {product} (ఇంతకు ముందు పని చేసింది)", "ta": "மீண்டும் {product} (முன்பு பலன் கொடுத்தது)",
        "ml": "വീണ്ടും {product} (മുമ്പ് ഫലിച്ചു)",
    },
    "adopt": {
        "en": "Noted. In 7 days I will ask you if it worked.", "hi": "नोट कर लिया। 7 दिन बाद पूछूंगा कि फायदा हुआ या नहीं।",
        "te": "నమోదు చేశాను. 7 రోజుల తర్వాత పని చేసిందా అని అడుగుతాను.", "ta": "பதிவு செய்தேன். 7 நாட்களில் பலன் கிடைத்ததா என்று கேட்பேன்.",
        "ml": "രേഖപ്പെടുത്തി. 7 ദിവസം കഴിഞ്ഞ് ഫലിച്ചോ എന്ന് ചോദിക്കാം.",
    },
    "greet": {
        "en": "Hello {name}", "hi": "नमस्ते {name} जी", "te": "నమస్కారం {name} గారు",
        "ta": "வணக்கம் {name}", "ml": "നമസ്കാരം {name}",
    },
    "outbreak": {
        "en": "Alert: {pest} seen on {n} farms in {village} in the last {days} days. Check your crop today.",
        "hi": "सावधान: पिछले {days} दिनों में {village} के {n} खेतों में {pest} दिखा है। आज अपनी फसल जांचिए।",
        "te": "జాగ్రత్త: గత {days} రోజుల్లో {village}లో {n} పొలాల్లో {pest} కనిపించింది. ఈరోజు మీ పంట చూడండి.",
        "ta": "எச்சரிக்கை: கடந்த {days} நாட்களில் {village}ல் {n} வயல்களில் {pest} தென்பட்டது. இன்று உங்கள் பயிரை பாருங்கள்.",
        "ml": "ജാഗ്രത: കഴിഞ്ഞ {days} ദിവസത്തിൽ {village}ൽ {n} പാടങ്ങളിൽ {pest} കണ്ടു. ഇന്ന് നിങ്ങളുടെ വിള പരിശോധിക്കൂ.",
    },
    "saved": {
        "en": "Saved to your farm memory.",
        "hi": "आपके खेत की याद में सेव हो गया।",
        "te": "మీ పొలం జ్ఞాపకంలో సేవ్ అయింది.",
        "ta": "உங்கள் நில நினைவில் சேமிக்கப்பட்டது.",
        "ml": "നിങ്ങളുടെ പാടത്തിന്റെ ഓർമ്മയിൽ സേവ് ചെയ്തു.",
    },
}


PEST_NAMES = {
    "whitefly": {"en": "whitefly", "te": "తెల్లదోమ", "hi": "सफेद मक्खी", "ta": "வெள்ளை ஈ", "ml": "വെള്ളീച്ച"},
    "pink bollworm": {"en": "pink bollworm", "te": "గులాబీ రంగు పురుగు", "hi": "गुलाबी सुंडी", "ta": "இளஞ்சிவப்பு காய்ப்புழு", "ml": "റോസ് പുഴു"},
    "thrips": {"en": "thrips", "te": "తామర పురుగులు", "hi": "थ्रिप्स", "ta": "இலைப்பேன்", "ml": "ത്രീപ്സ്"},
    "aphids": {"en": "aphids", "te": "పేనుబంక", "hi": "माहू", "ta": "அசுவினி", "ml": "അഫിഡുകൾ"},
    "leaf curl": {"en": "leaf curl", "te": "ఆకు ముడత", "hi": "पत्ती मरोड़", "ta": "இலை சுருட்டல்", "ml": "இലച്ചുരുൾ"},
    "stem borer": {"en": "stem borer", "te": "కాండం తొలుచు పురుగు", "hi": "तना छेदक", "ta": "தண்டு துளைப்பான்", "ml": "തണ്ട് തുരപ്പൻ"},
    "blast": {"en": "blast", "te": "అగ్గి తెగులు", "hi": "झुलसा रोग", "ta": "குலைநோய்", "ml": "இലപ്പുള്ളി"},
    "wilt": {"en": "wilt", "te": "ఎండు తెగులు", "hi": "उकठा", "ta": "வாடல்", "ml": "வாட்டம்"},
    "root rot": {"en": "root rot", "te": "వేరు కుళ్ళు తెగులు", "hi": "जड़ सड़न", "ta": "வேர் அழுகல்", "ml": "വേരുചീയൽ"},
    "root rot patches": {"en": "root rot", "te": "వేరు కుళ్ళు తెగులు", "hi": "जड़ सड़न", "ta": "வேர் அழுகல்", "ml": "വേരുചീയൽ"},
    "bollworm": {"en": "bollworm", "te": "కాయతొలుచు పురుగు", "hi": "सुंडी", "ta": "காய்ப்புழு", "ml": "കായ് തുരപ്പൻ"},
    "borer": {"en": "borer", "te": "తొలుచు పురుగు", "hi": "छेदक", "ta": "துளைப்பான்", "ml": "തുരപ്പൻ"},
    "sheath blight": {"en": "sheath blight", "te": "పొడ తెగులు", "hi": "शीथ ब्लाइट", "ta": "இலை உறை அழுகல்", "ml": "പോള രോഗം"},
    "leaf spot": {"en": "leaf spot", "te": "ఆకు మచ్చ", "hi": "पत्ती धब्बा", "ta": "இலைப்புள்ளி", "ml": "இലപ്പുള്ളി"},
    "yellowing": {"en": "yellow leaves", "te": "ఆకులు పసుపు రంగు", "hi": "पीली पत्तियां", "ta": "மஞ்சள் இலைகள்", "ml": "മഞ്ഞ ഇലകൾ"},
    "yellow": {"en": "yellow leaves", "te": "ఆకులు పసుపు రంగు", "hi": "पीली पत्तियां", "ta": "மஞ்சள் இலைகள்", "ml": "மഞ്ഞ ഇലകൾ"},
    "rust": {"en": "rust", "te": "తుప్పు తెగులు", "hi": "रतुआ", "ta": "துரு நோய்", "ml": "തുരുമ്പ്"},
    "caterpillar": {"en": "caterpillar", "te": "గొంగళి పురుగు", "hi": "इल्ली", "ta": "கம்பளிப்புழு", "ml": "കമ്പിളിപ്പുഴു"},
}

VILLAGE_NAMES = {
    "Kondapur": {"en": "Kondapur", "te": "కొండపూరు", "hi": "कोंडापुर", "ta": "கொண்டாபூர்", "ml": "കൊണ്ടാപ്പൂർ"},
    "Rampur": {"en": "Rampur", "te": "రాంపూర్", "hi": "रामपुर", "ta": "ராம்பூர்", "ml": "രാംപൂർ"},
    "Papanasam": {"en": "Papanasam", "te": "పాపనాశం", "hi": "पापनाशम", "ta": "பாபநாசம்", "ml": "പാபநாശം"},
    "Kuttanad": {"en": "Kuttanad", "te": "కుట్టనాడ్", "hi": "कुट्टनाड", "ta": "குட்டநாடு", "ml": "കുട്ടനാട്"},
}

FARMER_NAMES = {
    "Ramaiah": {"en": "Ramaiah", "te": "రామయ్య", "hi": "रामैया", "ta": "ராமையா", "ml": "രാമയ്യ"},
    "Lakshmi": {"en": "Lakshmi", "te": "లక్ష్మి", "hi": "लक्ष्मी", "ta": "லக்ஷ்மி", "ml": "ലക്ഷ്മി"},
    "Srinivas": {"en": "Srinivas", "te": "శ్రీనివాస్", "hi": "श्रीनिवास", "ta": "சீனிவாஸ்", "ml": "ശ്രീനിവാസ്"},
    "Venkata": {"en": "Venkata", "te": "వెంకట", "hi": "वेंकट", "ta": "வெங்கட", "ml": "വെങ്കട"},
    "Suresh": {"en": "Suresh", "te": "సురేష్", "hi": "सुरेश", "ta": "சுரேஷ்", "ml": "സുരേഷ്"},
    "Kamla": {"en": "Kamla", "te": "కమల", "hi": "कमला", "ta": "கமலா", "ml": "കമല"},
    "Murugan": {"en": "Murugan", "te": "మురుగన్", "hi": "मुరుగన్", "ta": "முருகன்", "ml": "മുരുകൻ"},
    "Joseph": {"en": "Joseph", "te": "జోసెఫ్", "hi": "जोसेफ", "ta": "ஜோசப்", "ml": "ജോസഫ്"},
}


PRODUCT_NAMES = {
    "neem oil": {"en": "neem oil", "te": "వేప నూనె", "hi": "नीम का तेल", "ta": "வேப்ப எண்ணெய்", "ml": "വേപ്പെണ്ണ"},
    "trichoderma viride": {"en": "trichoderma viride", "te": "ట్రైకోడెర్మా విరిడే", "hi": "ट्राइकोडर्मा विरिडे", "ta": "ட்ரைக்கோடெர்மா விரிடி", "ml": "ട്രൈക്കോഡെർമ വിരിഡെ"},
    "pseudomonas fluorescens": {"en": "pseudomonas fluorescens", "te": "సూడోమోనాస్ ఫ్లోరోసెన్స్", "hi": "स्यूडोमोनास फ्लोरोसेंस", "ta": "சூடோமோனாஸ்", "ml": "സ്യൂഡോമോണസ്"},
    "imidacloprid": {"en": "imidacloprid", "te": "ఇమిడాక్లోప్రిడ్", "hi": "इमिडाक्लोप्रिड", "ta": "இமிடாக்ளோபிரிட்", "ml": "ഇമിഡാക്ലോപ്രിഡ്"},
    "thiamethoxam": {"en": "thiamethoxam", "te": "థయామెథోక్సామ్", "hi": "थायमेथोक्सम", "ta": "தயாமெத்தோக்சாம்", "ml": "തയാമെത്തോക്സാം"},
    "acetamiprid": {"en": "acetamiprid", "te": "ఎసిటామిప్రిడ్", "hi": "एसिटामिप्रिड", "ta": "அசிடாமோபிரிட்", "ml": "അസെറ്റാമിപ്രിഡ്"},
    "carbendazim": {"en": "carbendazim", "te": "కార్బెండజిమ్", "hi": "कार्बेन्डाजिम", "ta": "கார்பெண்டசிம்", "ml": "കാർബെൻഡാസിം"},
    "chlorpyrifos": {"en": "chlorpyrifos", "te": "క్లోర్‌పైరిఫాస్", "hi": "क्लोरपायरीफॉस", "ta": "குளோர்ைபரிபாஸ்", "ml": "ക്ലോർപൈറിഫോസ്"},
    "monocrotophos": {"en": "monocrotophos", "te": "మోనోక్రోటోఫాస్", "hi": "मोनोक्रोटोफॉस", "ta": "மோனோகுரோட்டோபாஸ்", "ml": "മോണോക്രോട്ടോഫോസ്"},
    "urea": {"en": "urea", "te": "యూరియా", "hi": "यूरिया", "ta": "யூரியா", "ml": "യൂറിയ"},
    "yellow sticky traps": {"en": "yellow sticky traps", "te": "పసుపు రంగు జిగురు అట్టలు", "hi": "पीले चिपचिपे ट्रैप", "ta": "மஞ்சள் ஒட்டும் பொறி", "ml": "മഞ്ഞ ഒട്ടുന്ന കെണികൾ"},
    "blue sticky traps": {"en": "blue sticky traps", "te": "నీలం రంగు జిగురు అట్టలు", "hi": "नीले चिपचिपे ट्रैप", "ta": "நீல ஒட்டும் பொறி", "ml": "നീല ഒട്ടുന്ന കെണികൾ"},
    "pheromone traps": {"en": "pheromone traps", "te": "లింగాకర్షక బుట్టలు", "hi": "फेरोमोन ट्रैप", "ta": "இனக்கவர்ச்சி பொறி", "ml": "ഫെറമോൺ കെണി"},
    "spinosad": {"en": "spinosad", "te": "స్పినోసాడ్", "hi": "स्पिनोसैड", "ta": "ஸ்பினோசாட்", "ml": "സ്പിനോസാഡ്"},
    "fipronil": {"en": "fipronil", "te": "ఫిప్రోనిల్", "hi": "फिप्रोनिल", "ta": "பிப்ரோனில்", "ml": "ഫിപ്രോനിൽ"},
    "flonicamid": {"en": "flonicamid", "te": "ఫ్లోనికామిడ్", "hi": "फ्लोनिकामाइड", "ta": "ப்ளோனிகாமிட்", "ml": "ഫ്ലോണിക്കമിഡ്"},
    "spiromesifen": {"en": "spiromesifen", "te": "స్పైరోమెసిఫెన్", "hi": "स्पिरोमेसिफेन", "ta": "ஸ்பைரோமெசிஃபென்", "ml": "സ്പൈറോമെസിഫെൻ"},
    "pyriproxyfen": {"en": "pyriproxyfen", "te": "పైరిప్రాక్సిఫెన్", "hi": "पायरीप्रॉक्सीफेन", "ta": "பைரிபிராக்ஸிஃபென்", "ml": "പൈറിപ്രോക്സിഫെൻ"},
    "hexaconazole": {"en": "hexaconazole", "te": "హెక్సాకొనజోల్", "hi": "हेक्साकोनाजोल", "ta": "ஹெக்ஸாகோனசோல்", "ml": "ഹെക്സാകൊണസോൾ"},
    "tricyclazole": {"en": "tricyclazole", "te": "ట్రైసైక్లాజోల్", "hi": "ट्राइसाइक्लाजोल", "ta": "ட்ரைசைக்ளசோல்", "ml": "ട്രൈസൈക്ലസോൾ"},
    "propiconazole": {"en": "propiconazole", "te": "ప్రొపికొనజోల్", "hi": "प्रोपिकोनाजोल", "ta": "ப்ரோபிகோனசோல்", "ml": "പ്രൊപ്പിക്കോണസോൾ"},
    "chlorantraniliprole": {"en": "chlorantraniliprole", "te": "క్లోరాంట్రానిలిప్రోల్", "hi": "क्लोरेंट्रानिलिप्रोल", "ta": "குளோரான்ட்ரனிலிப்ரோல்", "ml": "ക്ലോറാൻട്രാനിലിപ്രോൾ"},
    "emamectin benzoate": {"en": "emamectin benzoate", "te": "ఎమామెక్టిన్ బెంజోయేట్", "hi": "इमामेक्टिन बेंजोएट", "ta": "எமாமெக்டின் பென்சோயேட்", "ml": "എമാമെക്റ്റിൻ ബെൻസോയേറ്റ്"},
}


def local_pest(p: str, lang: str) -> str:
    k = (p or "").lower().strip()
    if not k:
        return ""
    if k in PEST_NAMES:
        return PEST_NAMES[k].get(lang, p)
    for pest_key, trans in PEST_NAMES.items():
        if pest_key in k:
            return trans.get(lang, p)
    return p


def local_product(prod: str, lang: str) -> str:
    k = (prod or "").lower().strip()
    if not k:
        return ""
    if k in PRODUCT_NAMES:
        return PRODUCT_NAMES[k].get(lang, prod)
    for prod_key, trans in PRODUCT_NAMES.items():
        if prod_key in k:
            return trans.get(lang, prod)
    return prod


def local_village(v: str, lang: str) -> str:
    return VILLAGE_NAMES.get(v, {}).get(lang, v)


def local_farmer(f: str, lang: str) -> str:
    first = (f or "").split()[0]
    return FARMER_NAMES.get(first, {}).get(lang, first)


def phrase(key: str, lang: str, **kw) -> str:
    table = PHRASES[key]
    return table.get(lang, table["en"]).format(**kw)
