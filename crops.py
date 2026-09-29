"""Crop calendars, market prices and government schemes.

Crop calendars: simplified from state agricultural university Package of Practices.
Market prices: live from Agmarknet (data.gov.in) when DATA_GOV_API_KEY is set, otherwise a
clearly labelled SAMPLE series so the demo still shows the feature.
"""
import os
import random
from datetime import date, timedelta

import httpx

# crop key -> list of (stage name, start DAS, end DAS, icon, tasks)
CALENDAR = {
    "cotton": [
        ("Seedling", 0, 20, "🌱", ["Gap filling within 10 days", "Watch for sucking pests on young leaves"]),
        ("Vegetative", 21, 45, "🌿", ["First top-dress of nitrogen", "Check undersides of leaves for whitefly and jassids every 3 days"]),
        ("Squaring", 46, 65, "🌼", ["Install pheromone traps for pink bollworm (5 per acre)", "Second top-dress of nitrogen"]),
        ("Flowering", 66, 100, "🌸", ["Look for rosette flowers (pink bollworm)", "Avoid heavy nitrogen now", "Keep yellow sticky traps up"]),
        ("Boll development", 101, 140, "🥚", ["Open 20 green bolls per acre to check for pink bollworm", "Irrigate if soil is dry at boll formation"]),
        ("Picking", 141, 190, "☁️", ["Pick in the morning, keep kapas dry and clean", "Stop spraying 2 weeks before picking"]),
    ],
    "chilli": [
        ("Establishment", 0, 20, "🌱", ["Replace dead seedlings", "Drench Trichoderma near the roots if damping-off appears"]),
        ("Vegetative", 21, 50, "🌿", ["Watch for leaf curl (thrips, mites, whitefly)", "Put up blue and yellow sticky traps"]),
        ("Flowering", 51, 80, "🌸", ["Avoid water stress: flowers drop", "Check for flower drop and thrips"]),
        ("Fruiting", 81, 120, "🌶️", ["Watch for fruit rot and borer", "Top-dress potash"]),
        ("Harvest pickings", 121, 200, "🧺", ["Pick red ripe fruits every 10-15 days", "Dry on tarpaulin, not on bare soil (aflatoxin)"]),
    ],
    "wheat": [
        ("Germination", 0, 20, "🌱", ["Check even germination"]),
        ("Crown root (CRI)", 21, 25, "💧", ["First irrigation at 21 days is the most important one"]),
        ("Tillering", 26, 45, "🌿", ["Top-dress urea after irrigation", "Weed control before 35 days"]),
        ("Jointing", 46, 65, "🎋", ["Watch for yellow rust stripes on leaves"]),
        ("Heading & flowering", 66, 95, "🌾", ["Irrigate at flowering", "Do not irrigate in strong wind (lodging)"]),
        ("Grain filling & harvest", 96, 135, "🌾", ["Last irrigation at milk stage", "Harvest when grains are hard"]),
    ],
    "paddy": [
        ("Establishment", 0, 25, "🌱", ["Keep 2-3 cm water", "Fill gaps within 10 days"]),
        ("Tillering", 26, 55, "🌿", ["Top-dress nitrogen", "Check for stem borer dead hearts"]),
        ("Panicle initiation", 56, 80, "🎋", ["Keep 5 cm water", "Watch for blast spots on leaves"]),
        ("Flowering", 81, 105, "🌸", ["Do not let the field dry", "Watch for brown planthopper at the base"]),
        ("Maturity & harvest", 106, 140, "🌾", ["Drain field 10 days before harvest"]),
    ],
    "groundnut": [
        ("Emergence", 0, 20, "🌱", ["Check for collar rot"]),
        ("Flowering", 21, 40, "🌸", ["Apply gypsum at 40-45 days"]),
        ("Pegging", 41, 70, "🥜", ["Do not disturb soil after pegging", "Light irrigation"]),
        ("Pod development", 71, 100, "🥜", ["Watch for leaf spot and rust"]),
        ("Maturity", 101, 125, "🧺", ["Harvest when inner shell turns dark"]),
    ],
}

# Minimum Support Price, ₹/quintal (Govt of India). Verify each season.
MSP = {"cotton": (7710, "Medium staple, KMS 2025-26"), "paddy": (2369, "Common, KMS 2025-26"),
       "wheat": (2585, "RMS 2026-27"), "groundnut": (7263, "KMS 2025-26")}
BASE_PRICE = {"cotton": 7450, "chilli": 13200, "wheat": 2650, "paddy": 2300, "groundnut": 6900}
AGMARK_NAME = {"cotton": "Cotton", "chilli": "Dry Chillies", "wheat": "Wheat", "paddy": "Paddy(Dhan)(Common)",
               "groundnut": "Groundnut"}


STAGE_I18N = {
    "Seedling": {"te": "మొలక దశ", "hi": "अंकुरण अवस्था", "ta": "நாற்று நிலை", "ml": "മുളയ്ക്കുന്ന ഘട്ടം", "en": "Seedling"},
    "Vegetative": {"te": "ఎదుగుదల దశ", "hi": "वानस्पतिक अवस्था", "ta": "வளர்ச்சி நிலை", "ml": "വളർച്ചാ ഘട്ടം", "en": "Vegetative"},
    "Squaring": {"te": "మొగ్గ దశ", "hi": "कलियां बनने की अवस्था", "ta": "மொட்டு நிலை", "ml": "മൊട്ടിടുന്ന ഘട്ടം", "en": "Squaring"},
    "Flowering": {"te": "పూత దశ", "hi": "फूल आने की अवस्था", "ta": "பூக்கும் நிலை", "ml": "പൂവിടുന്ന ഘട്ടം", "en": "Flowering"},
    "Boll development": {"te": "కాయ దశ", "hi": "टिंडे बनने की अवस्था", "ta": "காய் நிலை", "ml": "കായ് വളരുന്ന ഘട്ടം", "en": "Boll development"},
    "Picking": {"te": "పత్తి తీత దశ", "hi": "चुनाई की अवस्था", "ta": "பருத்தி எடுக்கும் நிலை", "ml": "വിളവെടുപ്പ് ഘട്ടം", "en": "Picking"},
    "Establishment": {"te": "మొక్కలు నిలదొక్కుకునే దశ", "hi": "पौध स्थापना", "ta": "நாற்று நிலை", "ml": "വേരുപിടിക്കുന്ന ഘട്ടം", "en": "Establishment"},
    "Fruiting": {"te": "కాయ దశ", "hi": "फल बनने की अवस्था", "ta": "காய் நிலை", "ml": "കായ്ക്കുന്ന ഘട്ടം", "en": "Fruiting"},
    "Harvest pickings": {"te": "కోత దశ", "hi": "तुड़ाई की अवस्था", "ta": "அறுவடை நிலை", "ml": "വിളവെടുപ്പ് ഘട്ടം", "en": "Harvest pickings"},
    "Tillering": {"te": "పిలకల దశ", "hi": "कल्ले फूटने की अवस्था", "ta": "தூர்கட்டும் நிலை", "ml": "കൂമ്പ് പൊട്ടൽ", "en": "Tillering"},
    "Panicle initiation": {"te": "చిరుపొట్ట దశ", "hi": "बाली निकलने की अवस्था", "ta": "கருப்பிடிக்கும் நிலை", "ml": "കതിരിടൽ ഘട്ടം", "en": "Panicle initiation"},
    "Maturity & harvest": {"te": "గింజ పక్వత & కోత దశ", "hi": "परिपक्वता एवं कटाई", "ta": "முதிர்ச்சி & அறுவடை", "ml": "വിളവെടുപ്പ് ഘട്ടം", "en": "Maturity & harvest"},
    "Germination": {"te": "మొలక దశ", "hi": "अंकुरण अवस्था", "ta": "முளைக்கும் நிலை", "ml": "മുളയ്ക്കുന്ന ഘട്ടം", "en": "Germination"},
    "Crown root (CRI)": {"te": "కిరీట వేర్ల దశ", "hi": "शिखर जड़ अवस्था (CRI)", "ta": "முடி வேர் நிலை", "ml": "വേര് പടരുന്ന ഘട്ടം", "en": "Crown root (CRI)"},
    "Jointing": {"te": "కణుపుల దశ", "hi": "गांठ बनने की अवस्था", "ta": "கணு நிலை", "ml": "തണ്ട് വളരുന്ന ഘട്ടം", "en": "Jointing"},
    "Heading & flowering": {"te": "వెన్ను & పూత దశ", "hi": "बाली एवं फूल अवस्था", "ta": "கதிர் & பூக்கும் நிலை", "ml": "പൂവിടുന്ന ഘട്ടം", "en": "Heading & flowering"},
    "Grain filling & harvest": {"te": "గింజ పాలుపోసుకునే & కోత దశ", "hi": "दाना भराव एवं कटाई", "ta": "தானிய முதிர்ச்சி & அறுவடை", "ml": "വിളവെടുപ്പ് ഘട്ടം", "en": "Grain filling & harvest"},
    "Emergence": {"te": "మొలక దశ", "hi": "अंकुरण अवस्था", "ta": "முளைப்பு நிலை", "ml": "മുളയ്ക്കുന്ന ഘട്ടം", "en": "Emergence"},
    "Pegging": {"te": "ఊడలు దిగే దశ", "hi": "सुइयां बनने की अवस्था", "ta": "விழுது இறங்கும் நிலை", "ml": "കതിരൂന്നൽ ഘട്ടം", "en": "Pegging"},
    "Pod development": {"te": "కాయ ఊరే దశ", "hi": "फली विकास अवस्था", "ta": "காய் பிடிக்கும் நிலை", "ml": "കായ് വളരുന്ന ഘട്ടം", "en": "Pod development"},
    "Maturity": {"te": "పక్వత దశ", "hi": "परिपक्वता अवस्था", "ta": "முதிர்ச்சி நிலை", "ml": "വിളവെടുപ്പ് ഘട്ടം", "en": "Maturity"},
}

TASK_I18N = {
    "Gap filling within 10 days": {"te": "10 రోజుల్లో ఖాళీలను పూరించండి", "hi": "10 दिनों के भीतर खाली जगह भरें", "ta": "10 நாட்களுக்குள் இடைவெளி நிரப்புதல்", "ml": "10 ദിവസത്തിനകം വിടവുകൾ നികത്തുക", "en": "Gap filling within 10 days"},
    "Watch for sucking pests on young leaves": {"te": "లేత ఆకులపై రసం పీల్చే పురుగులను గమనించండి", "hi": "कोमल पत्तियों पर रस चूसने वाले कीटों की निगरानी करें", "ta": "இளந்தளிர்களில் சாறு உறிஞ்சும் பூச்சிகளைக் கண்காணிக்கவும்", "ml": "ഇളം ഇലകളിൽ നീരൂറ്റിക്കുടിക്കുന്ന കീടങ്ങളെ ശ്രദ്ധിക്കുക", "en": "Watch for sucking pests on young leaves"},
    "First top-dress of nitrogen": {"te": "నత్రజని ఎరువు మొదటి విడత వేయండి", "hi": "नाइट्रोजन की पहली खुराक दें", "ta": "முதல் முறை தழைச்சத்து இடவும்", "ml": "ആദ്യ തവണ നൈട്രജൻ വളം നൽകുക", "en": "First top-dress of nitrogen"},
    "Check undersides of leaves for whitefly and jassids every 3 days": {"te": "ప్రతి 3 రోజులకు ఆకుల అడుగున తెల్లదోమ, పచ్చదోమలను పరిశీలించండి", "hi": "हर 3 दिन में पत्तियों के नीचे सफेद मक्खी और हरा तेला देखें", "ta": "3 நாட்களுக்கு ஒருமுறை இலைகளின் அடிப்பகுதியில் வெள்ளை ஈக்களைப் பார்க்கவும்", "ml": "3 ദിവസത്തിലൊരിക്കൽ ഇലകളുടെ അടിയിൽ വെള്ളീച്ചകളെ പരിശോധിക്കുക", "en": "Check undersides of leaves for whitefly and jassids every 3 days"},
    "Install pheromone traps for pink bollworm (5 per acre)": {"te": "గులాబీ రంగు పురుగు కోసం లింగాకర్షక బుట్టలు (ఎకరాకు 5) అమర్చండి", "hi": "गुलाबी सुंडी के लिए फेरोमोन ट्रैप (5 प्रति एकड़) लगाएं", "ta": "இளஞ்சிவப்பு காய்ப்புழுவிற்கு இனக்கவர்ச்சி பொறிகள் (ஏக்கருக்கு 5) அமைக்கவும்", "ml": "റോസ് പുഴുവിനായി ഫെറോമോൺ കെണികൾ (ഏക്കറിന് 5) സ്ഥാപിക്കുക", "en": "Install pheromone traps for pink bollworm (5 per acre)"},
    "Second top-dress of nitrogen": {"te": "రెండవ విడత నత్రజని ఎరువు వేయండి", "hi": "नाइट्रोजन की दूसरी खुराक दें", "ta": "இரண்டாம் முறை தழைச்சத்து இடவும்", "ml": "രണ്ടാം തവണ നൈട്രജൻ വളം നൽകുക", "en": "Second top-dress of nitrogen"},
    "Look for rosette flowers (pink bollworm)": {"te": "గులాబీ రంగు పురుగు కోసం వికసించిన పువ్వులను గమనించండి", "hi": "गुलाबी सुंडी के लिए खिले हुए फूलों की जांच करें", "ta": "இளஞ்சிவப்பு காய்ப்புழு உள்ளதா என விரிந்த பூக்களை கவனியுங்கள்", "ml": "റോസ് പുഴുവിനായി വിരിഞ്ഞ പൂക്കൾ പരിശോധിക്കുക", "en": "Look for rosette flowers (pink bollworm)"},
    "Avoid heavy nitrogen now": {"te": "ఈ సమయంలో ఎక్కువ నత్రజని వాడకండి", "hi": "इस समय अधिक नाइट्रोजन खाद न डालें", "ta": "இப்போது அதிக தழைச்சத்து இட வேண்டாம்", "ml": "ഇപ്പോൾ കൂടുതൽ നൈട്രജൻ ഒഴിവാക്കുക", "en": "Avoid heavy nitrogen now"},
    "Keep yellow sticky traps up": {"te": "పసుపు రంగు జిగురు అట్టలను పొలంలో ఉంచండి", "hi": "पीले चिपचिपे ट्रैप लगाए रखें", "ta": "மஞ்சள் ஒட்டும் பொறிகளை வைத்திருக்கவும்", "ml": "മഞ്ഞ പശ കെണികൾ നിലനിർത്തുക", "en": "Keep yellow sticky traps up"},
    "Open 20 green bolls per acre to check for pink bollworm": {"te": "గులాబీ పురుగు కోసం ఎకరాకు 20 పచ్చి కాయలను తెరిచి చూడండి", "hi": "गुलाबी सुंडी की जांच के लिए प्रति एकड़ 20 हरे टिंडे खोलकर देखें", "ta": "காய்ப்புழு உள்ளதா என ஏக்கருக்கு 20 காய்களைப் பிரித்துப் பார்க்கவும்", "ml": "കായ്തുരപ്പൻ പുഴുവിനായി ഏക്കറിന് 20 കായ്കൾ തുറന്നു പരിശോധിക്കുക", "en": "Open 20 green bolls per acre to check for pink bollworm"},
    "Irrigate if soil is dry at boll formation": {"te": "కాయ ఏర్పడే సమయంలో నేల ఆరిపోతే నీటి తడి ఇవ్వండి", "hi": "टिंडे बनते समय मिट्टी सूखी हो तो सिंचाई करें", "ta": "காய் உருவாகும் போது நிலம் காய்ந்திருந்தால் நீர் பாய்ச்சவும்", "ml": "മണ്ണ് വരണ്ടതാണെങ്കിൽ നനച്ചു കൊടുക്കുക", "en": "Irrigate if soil is dry at boll formation"},
    "Pick in the morning, keep kapas dry and clean": {"te": "ఉదయం వేళల్లో పత్తి తీయండి, పత్తిని పొడిగా శుభ్రంగా ఉంచండి", "hi": "सुबह के समय कपास चुनें, कपास को सूखा और साफ रखें", "ta": "காலையில் பருத்தி எடுக்கவும், காய்ந்த நிலையில் சுத்தமாக வைக்கவும்", "ml": "രാവിലെ പരുത്തി എടുക്കുക, ഉണങ്ങിയതും വൃത്തിയുള്ളതുമായി സൂക്ഷിക്കുക", "en": "Pick in the morning, keep kapas dry and clean"},
    "Stop spraying 2 weeks before picking": {"te": "పత్తి తీతకు 2 వారాల ముందు పిచికారీ ఆపండి", "hi": "चुनाई से 2 हफ्ते पहले छिड़काव बंद करें", "ta": "பருத்தி எடுப்பதற்கு 2 வாரங்களுக்கு முன் தெளிப்பதை நிறுத்தவும்", "ml": "വിളവെടുപ്പിന് 2 ആഴ്ച മുമ്പ് തളിക്കൽ നിർത്തുക", "en": "Stop spraying 2 weeks before picking"},
    "Replace dead seedlings": {"te": "చనిపోయిన మొక్కల స్థానంలో కొత్తవి నాటండి", "hi": "सूखे पौधों की जगह नए पौधे लगाएं", "ta": "பட்டுப்போன நாற்றுகளை மாற்றவும்", "ml": "നശിച്ച തൈകൾ മാറ്റി നടുക", "en": "Replace dead seedlings"},
    "Drench Trichoderma near the roots if damping-off appears": {"te": "మొక్క కుళ్ళు కనిపిస్తే వేర్ల వద్ద ట్రైకోడెర్మా ద్రావణాన్ని పోయండి", "hi": "आर्द्र-पतन दिखने पर जड़ों के पास ट्राइकोडर्मा डालें", "ta": "நாற்று அழுகல் தெரிந்தால் வேர் பகுதியில் டிரைக்கோடெர்மா ஊற்றவும்", "ml": "തൈചീയൽ കണ്ടാൽ വേരുകളിൽ ട്രൈക്കോഡെർമ ഒഴിക്കുക", "en": "Drench Trichoderma near the roots if damping-off appears"},
    "Watch for leaf curl (thrips, mites, whitefly)": {"te": "ఆకు ముడత (తామర పురుగులు, నల్లి, తెల్లదోమ) గమనించండి", "hi": "पत्ती मरोड़ (थ्रिप्स, माइट, सफेद मक्खी) पर नजर रखें", "ta": "இலை சுருட்டலைக் கண்காணிக்கவும்", "ml": "ഇലച്ചുരുൾ ശ്രദ്ധിക്കുക", "en": "Watch for leaf curl (thrips, mites, whitefly)"},
    "Put up blue and yellow sticky traps": {"te": "నీలం మరియు పసుపు జిగురు అట్టలను అమర్చండి", "hi": "नीले और पीले चिपचिपे ट्रैप लगाएं", "ta": "நீல மற்றும் மஞ்சள் ஒட்டும் பொறிகளை வைக்கவும்", "ml": "നീലയും മഞ്ഞയും പശ കെണികൾ വെക്കുക", "en": "Put up blue and yellow sticky traps"},
    "Avoid water stress: flowers drop": {"te": "నీటి ఎద్దడి లేకుండా చూడండి: పూత రాలిపోతుంది", "hi": "पानी की कमी न होने दें: फूल झड़ते हैं", "ta": "நீர்ப் பற்றாக்குறை தவிர்க்கவும்: பூக்கள் உதிரும்", "ml": "വെള്ളക്കുറവ് ഒഴിവാക്കുക: പൂക്കൾ കൊഴിയും", "en": "Avoid water stress: flowers drop"},
    "Check for flower drop and thrips": {"te": "పూత రాలడం మరియు తామర పురుగులను పరిశీలించండి", "hi": "फूलों का गिरना और थ्रिप्स की जांच करें", "ta": "பூ உதிர்தல் மற்றும் இலைப்பேன்களை கண்காணிக்கவும்", "ml": "പൂ കൊഴിച്ചിലും കീടങ്ങളും പരിശോധിക്കുക", "en": "Check for flower drop and thrips"},
    "Watch for fruit rot and borer": {"te": "కాయ కుళ్ళు మరియు కాయ తొలుచు పురుగును గమనించండి", "hi": "फल सड़न और फल छेदक पर नजर रखें", "ta": "காய் அழுகல் மற்றும் காய் துளைப்பானைக் கண்காணிக்கவும்", "ml": "കായ്ചീയലും തുരപ്പൻ പുഴുവും ശ്രദ്ധിക്കുക", "en": "Watch for fruit rot and borer"},
    "Top-dress potash": {"te": "పొటాష్ ఎరువును పైపాటుగా వేయండి", "hi": "पोटाश खाद ऊपर से डालें", "ta": "பொட்டாஷ் உரம் இடவும்", "ml": "പൊട്ടാഷ് വളം നൽകുക", "en": "Top-dress potash"},
    "Pick red ripe fruits every 10-15 days": {"te": "ప్రతి 10-15 రోజులకు పండిన ఎర్ర మిరపకాయలను కోయండి", "hi": "हर 10-15 दिनों में पके लाल फल तोड़ें", "ta": "10-15 நாட்களுக்கு ஒருமுறை பழுத்த மிளகாயை பறிக்கவும்", "ml": "10-15 ദിവസത്തിലൊരിക്കൽ ചുവന്ന മുളക് പറിക്കുക", "en": "Pick red ripe fruits every 10-15 days"},
    "Dry on tarpaulin, not on bare soil (aflatoxin)": {"te": "నేలమీద కాకుండా టార్పాలిన్ పట్టాలపై ఆరబెట్టండి", "hi": "तिरपाल पर सुखाएं, नंगी मिट्टी पर नहीं", "ta": "தார்பாயில் உலர்த்தவும், வெறும் தரையில் அல்ல", "ml": "ടാർപോളിനിൽ ഉണക്കുക, മണ്ണിൽ ഇടരുത്", "en": "Dry on tarpaulin, not on bare soil (aflatoxin)"},
    "Keep 2-3 cm water": {"te": "2-3 సెం.మీ నీరు ఉంచండి", "hi": "2-3 सेमी पानी बनाए रखें", "ta": "2-3 செ.மீ நீர் வைக்கவும்", "ml": "2-3 സെ.മീ വെള്ളം നിർത്തുക", "en": "Keep 2-3 cm water"},
    "Fill gaps within 10 days": {"te": "10 రోజుల్లో ఖాళీలను పూరించండి", "hi": "10 दिनों के भीतर खाली जगह भरें", "ta": "10 நாட்களில் இடைவெளி நிரப்பவும்", "ml": "10 ദിവസത്തിനകം വിടവുകൾ നികത്തുക", "en": "Fill gaps within 10 days"},
    "Top-dress nitrogen": {"te": "నత్రజని ఎరువు పైపాటుగా వేయండి", "hi": "नाइट्रोजन खाद दें", "ta": "தழைச்சத்து உரம் இடவும்", "ml": "നൈട്രജൻ വളം നൽകുക", "en": "Top-dress nitrogen"},
    "Check for stem borer dead hearts": {"te": "కాండం తొలుచు పురుగు (ఎండిన మొవ్వు) పరిశీలించండి", "hi": "तना छेदक के डेड हार्ट्स की जांच करें", "ta": "தண்டு துளைப்பான் சேதத்தை கண்காணிக்கவும்", "ml": "തണ്ട് തുരപ്പൻ പുഴുവിനെ ശ്രദ്ധിക്കുക", "en": "Check for stem borer dead hearts"},
    "Keep 5 cm water": {"te": "5 సెం.మీ నీరు ఉంచండి", "hi": "5 सेमी पानी रखें", "ta": "5 செ.மீ நீர் வைக்கவும்", "ml": "5 സെ.മീ വെള്ളം സൂക്ഷിക്കുക", "en": "Keep 5 cm water"},
    "Watch for blast spots on leaves": {"te": "ఆకులపై అగ్గి తెగులు మచ్చలను గమనించండి", "hi": "पत्तियों पर झुलसा रोग के धब्बे देखें", "ta": "குலைநோய் புள்ளிகள் உள்ளதா என பார்க்கவும்", "ml": "ഇലപ്പുള്ളി രോഗം ശ്രദ്ധിക്കുക", "en": "Watch for blast spots on leaves"},
    "Do not let the field dry": {"te": "పొలాన్ని ఆరనివ్వకండి", "hi": "खेत को सूखने न दें", "ta": "நிலத்தை காய விடாதீர்கள்", "ml": "പാടം വരണ്ടുപോകാതെ സൂക്ഷിക്കുക", "en": "Do not let the field dry"},
    "Watch for brown planthopper at the base": {"te": "మొక్కల మొదళ్ల వద్ద సుడిదోమను గమనించండి", "hi": "पौधे के नीचे भूरा फुदका (BPH) देखें", "ta": "அடிப்பகுதியில் புகையான் உள்ளதா என பார்க்கவும்", "ml": "തവിട്ടു ചാഴിയെ ശ്രദ്ധിക്കുക", "en": "Watch for brown planthopper at the base"},
    "Drain field 10 days before harvest": {"te": "కోతకు 10 రోజుల ముందు పొలం నుండి నీటిని తీసివేయండి", "hi": "कटाई से 10 दिन पहले खेत का पानी निकाल दें", "ta": "அறுவடைக்கு 10 நாட்களுக்கு முன் நீரை வடிக்கவும்", "ml": "വിളവെടുപ്പിന് 10 ദിവസം മുമ്പ് വെള്ളം വാർക്കുക", "en": "Drain field 10 days before harvest"},
    "Check even germination": {"te": "మొలకలు సమానంగా వచ్చాయో లేదో చూడండి", "hi": "समान अंकुरण की जांच करें", "ta": "சீரான முளைப்பை சரிபார்க்கவும்", "ml": "ശരിയായ മുളപ്പ് പരിശോധിക്കുക", "en": "Check even germination"},
    "First irrigation at 21 days is the most important one": {"te": "21వ రోజు మొదటి తడి అత్యంత ముఖ్యమైనది", "hi": "21 दिनों पर पहली सिंचाई सबसे महत्वपूर्ण है", "ta": "21 நாட்களில் முதல் பாசனம் மிக முக்கியமானது", "ml": "21 ദിവസത്തിലെ ആദ്യ നനവ് ഏറ്റവും പ്രധാനമാണ്", "en": "First irrigation at 21 days is the most important one"},
    "Top-dress urea after irrigation": {"te": "నీటి తడి తర్వాత యూరియా వేయండి", "hi": "सिंचाई के बाद यूरिया डालें", "ta": "பாசனத்திற்கு பின் யூரியா இடவும்", "ml": "നനച്ച ശേഷം യൂറിയ നൽകുക", "en": "Top-dress urea after irrigation"},
    "Weed control before 35 days": {"te": "35 రోజుల్లోపు కలుపు నివారించండి", "hi": "35 दिनों से पहले खरपतवार नियंत्रण करें", "ta": "35 நாட்களுக்குள் களை கட்டுப்படுத்தவும்", "ml": "35 ദിവസത്തിനകം കള നിയന്ത്രിക്കുക", "en": "Weed control before 35 days"},
    "Watch for yellow rust stripes on leaves": {"te": "ఆకులపై పసుపు కుంకుమ తెగులు చారలను గమనించండి", "hi": "पत्तियों पर पीला रतुआ धारियां देखें", "ta": "இலைகளில் மஞ்சள் துரு நோயைக் கவனியுங்கள்", "ml": "മഞ്ഞ തുരുമ്പ് രോഗം ശ്രദ്ധിക്കുക", "en": "Watch for yellow rust stripes on leaves"},
    "Irrigate at flowering": {"te": "పూత సమయంలో నీరు పెట్టండి", "hi": "फूल आते समय सिंचाई करें", "ta": "பூக்கும் போது பாசனம் செய்யவும்", "ml": "പൂവിടുന്ന സമയം നനയ്ക്കുക", "en": "Irrigate at flowering"},
    "Do not irrigate in strong wind (lodging)": {"te": "తీవ్రమైన గాలి ఉన్నప్పుడు నీరు పెట్టకండి", "hi": "तेज हवा में सिंचाई न करें", "ta": "பலத்த காற்றில் பாசனம் செய்ய வேண்டாம்", "ml": "ശക്തമായ കാറ്റുള്ളപ്പോൾ നനയ്ക്കരുത്", "en": "Do not irrigate in strong wind (lodging)"},
    "Last irrigation at milk stage": {"te": "పాలుపోసుకునే దశలో చివరి తడి ఇవ్వండి", "hi": "दूधिया अवस्था में अंतिम सिंचाई करें", "ta": "பால் பருவத்தில் கடைசி பாசனம்", "ml": "പാൽ പരുവത്തിൽ അവസാന നനവ്", "en": "Last irrigation at milk stage"},
    "Harvest when grains are hard": {"te": "గింజలు గట్టిపడినప్పుడు కోయండి", "hi": "दाने सख्त होने पर कटाई करें", "ta": "தானியம் கடினமானதும் அறுவடை", "ml": "ധാന്യം ഉറച്ചാൽ വിളവെടുക്കുക", "en": "Harvest when grains are hard"},
    "Check for collar rot": {"te": "మొక్క మొదలు కుళ్ళును గమనించండి", "hi": "कॉलर रॉट (तना सड़न) की जांच करें", "ta": "கழுத்து அழுகல் உள்ளதா என பார்க்கவும்", "ml": "കഴുത്ത് ചീയൽ രോഗം പരിശോധിക്കുക", "en": "Check for collar rot"},
    "Apply gypsum at 40-45 days": {"te": "40-45 రోజుల వద్ద జిప్సం వేయండి", "hi": "40-45 दिनों पर जिप्सम डालें", "ta": "40-45 நாட்களில் ஜிப்சம் இடவும்", "ml": "40-45 ദിവസത്തിൽ ജിപ്സം നൽകുക", "en": "Apply gypsum at 40-45 days"},
    "Do not disturb soil after pegging": {"te": "ఊడలు దిగిన తర్వాత నేలను కదల్చకండి", "hi": "सुइयां बनने के बाद मिट्टी को न छेड़ें", "ta": "விழுது இறங்கிய பின் மண்ணை கிளற வேண்டாம்", "ml": "വിത്ത് ഇറങ്ങിയ ശേഷം മണ്ണിൽ ഇളക്കം വരുത്തരുത്", "en": "Do not disturb soil after pegging"},
    "Light irrigation": {"te": "తేలికపాటి తడి ఇవ్వండి", "hi": "हल्की सिंचाई करें", "ta": "லேசான பாசனம்", "ml": "നേരിയ നനവ്", "en": "Light irrigation"},
    "Watch for leaf spot and rust": {"te": "ఆకుమచ్చ మరియు తుప్పు తెగులును గమనించండి", "hi": "पत्ती धब्बा और रतुआ रोग देखें", "ta": "இலைப்புள்ளி மற்றும் துரு நோயைக் கவனியுங்கள்", "ml": "ഇലപ്പുള്ളിയും തുരുമ്പ് രോഗവും ശ്രദ്ധിക്കുക", "en": "Watch for leaf spot and rust"},
    "Harvest when inner shell turns dark": {"te": "కాయ లోపలి భాగం ముదురు రంగులోకి మారినప్పుడు పంట కోయండి", "hi": "भीतरी छिलका गहरा होने पर कटाई करें", "ta": "உள் ஓடு கருமை நிறமானதும் அறுவடை செய்யவும்", "ml": "ഉൾത്തോട് ഇരുണ്ട നിറമാകുമ്പോൾ വിളവെടുക്കുക", "en": "Harvest when inner shell turns dark"}
}


def crop_stage(crop_key: str, sown: str | None, lang: str = "en") -> dict | None:
    if not sown or crop_key not in CALENDAR:
        return None
    das = (date.today() - date.fromisoformat(sown)).days
    stages = CALENDAR[crop_key]
    cur_i = next((i for i, s in enumerate(stages) if s[1] <= das <= s[2]), len(stages) - 1)
    name_en, start, end, icon, tasks_en = stages[cur_i]
    nxt = stages[cur_i + 1] if cur_i + 1 < len(stages) else None
    
    name = STAGE_I18N.get(name_en, {}).get(lang, name_en)
    tasks = [TASK_I18N.get(t, {}).get(lang, t) for t in tasks_en]

    stages_out = []
    for i, s in enumerate(stages):
        st_en = s[0]
        st_loc = STAGE_I18N.get(st_en, {}).get(lang, st_en)
        stages_out.append({"name": st_loc, "name_en": st_en, "icon": s[3], "start": s[1], "end": s[2], "current": i == cur_i})

    next_out = None
    if nxt:
        nxt_en = nxt[0]
        nxt_loc = STAGE_I18N.get(nxt_en, {}).get(lang, nxt_en)
        next_out = {"name": nxt_loc, "name_en": nxt_en, "in_days": max(0, nxt[1] - das)}

    return {"das": das, "stage": name, "stage_en": name_en, "icon": icon, "tasks": tasks, "tasks_en": tasks_en,
            "progress": min(100, round(das / stages[-1][2] * 100)),
            "stages": stages_out,
            "next": next_out}


def market(crop_key: str, district: str, state: str) -> dict:
    key = os.getenv("DATA_GOV_API_KEY")
    if key and crop_key in AGMARK_NAME:
        try:
            r = httpx.get("https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070", timeout=6, params={
                "api-key": key, "format": "json", "limit": 50,
                "filters[state]": state, "filters[commodity]": AGMARK_NAME[crop_key]})
            recs = r.json().get("records", [])
            if recs:
                rows = [{"market": x["market"], "date": x["arrival_date"], "modal": int(float(x["modal_price"])),
                         "min": int(float(x["min_price"])), "max": int(float(x["max_price"]))} for x in recs]
                return {"crop": crop_key, "source": "Agmarknet (live)", "sample": False, "today": rows[0]["modal"],
                        "markets": rows[:6], "series": [], "msp": MSP.get(crop_key)}
        except Exception as e:
            print("[market] live fetch failed:", e)
    # sample series: deterministic random walk so it looks the same every reload
    base = BASE_PRICE.get(crop_key, 3000)
    rnd = random.Random(crop_key + district)
    series, p = [], base * 0.95
    for i in range(30, -1, -1):
        p = p * (1 + rnd.uniform(-0.012, 0.016))
        series.append({"date": (date.today() - timedelta(days=i)).isoformat(), "modal": round(p / 10) * 10})
    today = series[-1]["modal"]
    week = series[-8]["modal"]
    return {"crop": crop_key, "source": "SAMPLE data (set DATA_GOV_API_KEY for live Agmarknet prices)", "sample": True,
            "today": today, "change_7d_pct": round((today - week) / week * 100, 1), "series": series,
            "markets": [{"market": f"{district} APMC", "modal": today}, {"market": "Nearest eNAM mandi", "modal": round(today * 1.02 / 10) * 10}],
            "msp": MSP.get(crop_key)}


SCHEMES = [
    {"id": "pmkisan", "name": "PM-KISAN", "icon": "💰", "what": "₹6,000 a year in three instalments to land-holding farmer families.",
     "who": "Farmers with land records in their name. e-KYC and Aadhaar-linked bank account needed.", "where": "pmkisan.gov.in or CSC centre"},
    {"id": "pmfby", "name": "PM Fasal Bima Yojana (crop insurance)", "icon": "🛡️",
     "what": "Crop loss insurance. Farmer premium is 2% for kharif, 1.5% for rabi, 5% for commercial/horticulture crops.",
     "who": "All farmers growing notified crops. Enrol before the season cut-off (usually 31 July kharif, 31 December rabi).",
     "where": "Bank, CSC, or pmfby.gov.in. Your KrishiSmriti plot record can support a claim."},
    {"id": "kcc", "name": "Kisan Credit Card", "icon": "💳", "what": "Low-interest crop loan with interest subvention for prompt repayment.",
     "who": "Owner farmers, tenant farmers, sharecroppers.", "where": "Any bank branch"},
    {"id": "shc", "name": "Soil Health Card", "icon": "🧪", "what": "Free soil test with nutrient and fertiliser advice.",
     "who": "All farmers.", "where": "Agriculture office / soilhealth.dac.gov.in"},
    {"id": "kusum", "name": "PM-KUSUM (solar pump)", "icon": "☀️", "what": "Subsidy for solar irrigation pumps.",
     "who": "Individual farmers, FPOs, panchayats.", "where": "State renewable energy agency"},
]
