"""
GreenLoop AI - Knowledge Engine & Waste-to-Value Repository
Curated rule-based recommendations, safety guidance, and bilingual (English + Tamil) instructions.
"""

import unicodedata

WASTE_CATEGORIES = {
    "plastic": {
        "id": "plastic",
        "name_en": "Plastic Waste",
        "name_ta": "நெகிழி (பிளாஸ்டிக்) கழிவு",
        "icon": "fa-bottle-water",
        "color": "#0ea5e9",
        "badge_class": "badge-plastic",
        "decomposition_time": "100–1,000+ years (estimate)",
        "common_items": ["PET Water Bottles", "Milk Jugs", "Takeout Containers", "Bottle Caps", "Detergent Bottles"],
        "summary_en": "Plastic items are lightweight, durable, and weather-resistant, making them ideal for garden planters and storage organizers.",
        "summary_ta": "பிளாஸ்டிக் பொருட்கள் உறுதியானவை மற்றும் நீர்ப்புகாதவை. இவற்றை செடி தொட்டிகளாகவும் மேஜை அமைப்பாளர்களாகவும் எளிதாக மாற்றலாம்.",
        "upcycling_projects": [
            {
                "id": "plastic-planter",
                "title_en": "Self-Watering Bottle Planter",
                "title_ta": "சுயமாக நீர் பாய்ச்சும் செடி தொட்டி",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "15 mins",
                "points": 50,
                "materials_en": ["1 large plastic bottle (1L or 2L)", "Scissors / Box cutter", "Cotton string or cloth strip", "Potting soil & seeds/seedling", "Water"],
                "materials_ta": ["1 பெரிய பிளாஸ்டிக் பாட்டில் (1L அல்லது 2L)", "கத்தரிக்கோல் அல்லது கட்டர்", "பருத்தி கயிறு அல்லது துணித் துண்டு", "செடி வளர்ப்பு மண் மற்றும் விதைகள்", "தண்ணீர்"],
                "steps_en": [
                    "Cut the plastic bottle in half horizontally about 4 inches from the top.",
                    "Punch a small hole in the bottle cap and thread a 6-inch cotton string through it, tying a knot inside the cap.",
                    "Screw the cap back onto the inverted top half. The string should hang down about 2 inches.",
                    "Invert the top funnel-shaped half into the bottom base half.",
                    "Fill the bottom base with water (about half full).",
                    "Add potting soil to the top funnel, plant your seed or herb, and water gently once. The string will continuously wick moisture up to the roots."
                ],
                "steps_ta": [
                    "பாட்டிலை மேல் பகுதியில் இருந்து 4 அங்குல இடைவெளியில் குறுக்காக வெட்டவும்.",
                    "பாட்டில் மூடியில் ஒரு சிறிய துளையிட்டு, 6 அங்குல பருத்தி கயிற்றை நுழைத்து உள்ளே முடிச்சு போடவும்.",
                    "மூடியை மீண்டும் தலைகீழான மேல் பாதியில் திருகவும். கயிறு 2 அங்குலம் கீழே தொங்க வேண்டும்.",
                    "மேல் பாதியை தலைகீழாக கீழ் பாதியில் வைக்கவும்.",
                    "கீழ் பாதியில் பாதியளவு தண்ணீர் நிரப்பவும்.",
                    "மேல் பாதியில் செடி மண் நிரப்பி, விதை அல்லது நாற்று நடவும். கயிறு வழியாக நீர் தொடர்ந்து செடி வேர்களுக்கு உறிஞ்சப்படும்."
                ],
                "safety_tip_en": "Ask an adult or wear work gloves when cutting plastic to prevent sharp edges.",
                "safety_tip_ta": "பிளாஸ்டிக் வெட்டும்போது கவனமாக இருக்கவும்; வெட்டப்பட்ட விளிம்புகள் கூர்மையாக இருக்கும்."
            },
            {
                "id": "plastic-organizer",
                "title_en": "Desktop Stationery & Cable Caddy",
                "title_ta": "மேஜை எழுதுபொருள் & கேபிள் அமைப்பாளர்",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "20 mins",
                "points": 40,
                "materials_en": ["2-3 plastic bottles of varying heights", "Sandpaper or masking tape", "Paints / stickers for decoration", "Strong glue or binder clips"],
                "materials_ta": ["2-3 பிளாஸ்டிக் பாட்டில்கள்", "மணற்காகிதம் அல்லது டேப்", "வண்ணப் பூச்சு / ஸ்டிக்கர்கள்", "பசை"],
                "steps_en": [
                    "Cut bottles at different heights (e.g., 3 inches, 4.5 inches, 6 inches).",
                    "Smooth the cut rims with sandpaper or cover them with colorful masking tape.",
                    "Decorate the exterior with paint, fabric scraps, or markers.",
                    "Glue the cylinders together side-by-side to create a multi-compartment pen and cable holder."
                ],
                "steps_ta": [
                    "பாட்டில்களை வெவ்வேறு உயரங்களில் (3 அங்குலம், 4.5 அங்குலம், 6 அங்குலம்) வெட்டவும்.",
                    "வெட்டிய விளிம்புகளை மணற்காகிதம் கொண்டு சமன் செய்யவும் அல்லது வண்ண டேப் ஒட்டவும்.",
                    "வெளிப்புறத்தை பெயிண்ட் அல்லது ஸ்டிக்கர்கள் கொண்டு அலங்கரிக்கவும்.",
                    "அனைத்து பாகங்களையும் ஒன்றாக ஒட்டி பல அறைகள் கொண்ட மேஜை ஸ்டாண்டாக பயன்படுத்தவும்."
                ],
                "safety_tip_en": "Smooth cut edges thoroughly to avoid scratches.",
                "safety_tip_ta": "காயம் ஏற்படாமல் இருக்க விளிம்புகளை டேப் கொண்டு மூடவும்."
            },
            {
                "id": "plastic-bird-feeder",
                "title_en": "Hanging Eco Bird Feeder",
                "title_ta": "பறவைகளுக்கான தொங்கும் தானியக் கூண்டு",
                "difficulty": "Medium",
                "difficulty_ta": "நடுத்தரம்",
                "time_required": "25 mins",
                "points": 60,
                "materials_en": ["Clean 1L or 500ml plastic bottle", "2 wooden spoons or chopsticks", "Hanging wire or twine", "Bird seed / grains"],
                "materials_ta": ["சுத்தமான பிளாஸ்டிக் பாட்டில்", "2 மரக் கரண்டிகள் அல்லது குச்சிகள்", "கயிறு", "தானியங்கள்"],
                "steps_en": [
                    "Make two small holes directly opposite each other on the bottle, about 3 inches from the base.",
                    "Insert a wooden spoon through the holes so birds have a perch, and widen the hole slightly on the spoon side so grain spills out onto the spoon.",
                    "Repeat 3 inches higher at a 90-degree angle with the second spoon.",
                    "Fill the bottle with grains and screw the cap on.",
                    "Attach twine around the bottle neck and hang securely in a shaded balcony or garden."
                ],
                "steps_ta": [
                    "பாட்டிலின் அடியில் இருந்து 3 அங்குலம் மேலே இருபுறமும் துளையிடவும்.",
                    "ஒரு மரக் கரண்டியை நுழைக்கவும். கரண்டி மீது தானியங்கள் விழும் வகையில் துளையை சற்று பெரிதாக்கவும்.",
                    "பாட்டிலில் தானியங்களை நிரப்பி மூடி போடவும்.",
                    "கழுத்துப் பகுதியில் கயிறு கட்டி பால்கனி அல்லது மரத்தில் தொங்கவிடவும்."
                ],
                "safety_tip_en": "Keep the feeder clean and refill regularly with dry bird seed.",
                "safety_tip_ta": "தானியங்கள் மழையில் நனையாமல் பார்த்துக் கொள்ளவும்."
            }
        ],
        "disposal_guidance": {
            "unsuitable_reasons_en": [
                "Cracked or brittle plastic degrading into microplastics.",
                "Containers that held chemical pesticides, motor oil, or hazardous solvents.",
                "Single-use thin bags under 50 microns (cannot be upcycled safely)."
            ],
            "unsuitable_reasons_ta": [
                "உடைந்த அல்லது நசுங்கிய பழைய பிளாஸ்டிக்.",
                "பூச்சிக்கொல்லி மருந்து அல்லது விஷ ரசாயன பாட்டில்கள்.",
                "50 மைக்ரானுக்கு குறைவான மெல்லிய நெகிழி பைகள்."
            ],
            "safe_disposal_steps_en": [
                "Rinse containers thoroughly to remove food grease or chemical residues.",
                "Check recycling triangle symbols: Code 1 (PET) and Code 2 (HDPE) are widely recycled.",
                "Crush bottles to save space and place into your local dry-waste segregation bin.",
                "Hazardous chemical bottles must go directly to municipal hazardous waste collection points."
            ],
            "safe_disposal_steps_ta": [
                "உணவு எண்ணெய் அல்லது அழுக்குகளை தண்ணீரில் கழுவி உலர்த்தவும்.",
                "மறுசுழற்சி குறியீடு எண் 1 (PET) மற்றும் 2 (HDPE) எளிதில் மறுசுழற்சி செய்யக்கூடியவை.",
                "பாட்டில்களை நசுக்கி உலர் கழிவுப் பெட்டியில் போடவும்.",
                "ரசாயன பாட்டில்களை அபாயகர கழிவு மையத்தில் ஒப்படைக்கவும்."
            ]
        }
    },
    "paper": {
        "id": "paper",
        "name_en": "Paper & Cardboard",
        "name_ta": "காகிதம் மற்றும் அட்டை கழிவு",
        "icon": "fa-newspaper",
        "color": "#f59e0b",
        "badge_class": "badge-paper",
        "decomposition_time": "2–4 weeks for paper; about 3 months for plain cardboard",
        "common_items": ["Cardboard Boxes", "Newspapers", "Egg Cartons", "Paper Bags", "Notebook Covers"],
        "summary_en": "Paper and cardboard decompose naturally and absorb moisture well. They are perfect for organic gardening pots and home organizers.",
        "summary_ta": "காகிதம் மற்றும் அட்டைப்பெட்டிகள் எளிதில் மக்கும் தன்மை கொண்டவை. இவற்றை தோட்டக்கலை தொட்டிகளாகவும் சேமிப்பு பெட்டிகளாகவும் பயன்படுத்தலாம்.",
        "upcycling_projects": [
            {
                "id": "paper-seedling-pots",
                "title_en": "Biodegradable Seedling Pots",
                "title_ta": "மண்ணில் மக்கக்கூடிய நாற்று வளர்ப்பு தொட்டிகள்",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "10 mins",
                "points": 40,
                "materials_en": ["Egg cartons or old newspaper sheets", "Small glass cup / cylinder (for newspaper rolling)", "Potting soil", "Vegetable seeds"],
                "materials_ta": ["முட்டை அட்டை அல்லது பழைய செய்தித்தாள்கள்", "சிறிய உருளை பாட்டில்", "மண்", "விதைகள்"],
                "steps_en": [
                    "If using egg cartons, simply cut each cup out into individual cups.",
                    "If using newspaper, wrap a strip around a small cup, fold the bottom closed, and slide the cup out.",
                    "Fill each paper cup with potting soil and plant 1-2 seeds.",
                    "Water gently with a spray mister.",
                    "When seedlings sprout, plant the ENTIRE paper cup directly into the ground or a pot—the paper will naturally compost!"
                ],
                "steps_ta": [
                    "முட்டை அட்டையை தனித்தனி கோப்பைகளாக வெட்டவும்.",
                    "செய்தித்தாளை ஒரு சிறிய கிண்ணத்தில் சுற்றி அடியை மடித்து எடுக்கவும்.",
                    "அதில் செடி மண் நிரப்பி விதைகளை விதைக்கவும்.",
                    "நாற்று முளைத்ததும், காகிதக் கோப்பையுடன் சேர்த்து நேரடியாக மண்ணில் நடவும்—காகிதம் உரமாக மக்கிவிடும்!"
                ],
                "safety_tip_en": "Do not use glossy or colored magazine pages as they may contain heavy metal inks.",
                "safety_tip_ta": "பளபளப்பான வண்ண பத்திரிகைகளை பயன்படுத்த வேண்டாம்; எளிய செய்தித்தாள்களை பயன்படுத்தவும்."
            },
            {
                "id": "cardboard-drawer-dividers",
                "title_en": "Custom Modular Drawer Dividers",
                "title_ta": "அலமாரி பகுப்பாய்வு தடுப்புகள்",
                "difficulty": "Medium",
                "difficulty_ta": "நடுத்தரம்",
                "time_required": "20 mins",
                "points": 50,
                "materials_en": ["Corrugated delivery boxes", "Ruler & pencil", "Utility knife / scissors", "Decorative wrapping paper or tape"],
                "materials_ta": ["அட்டைப்பெட்டிகள்", "அளவுகோல் & பென்சில்", "கத்தரிக்கோல்", "ஒட்டு டேப்"],
                "steps_en": [
                    "Measure the height, width, and depth of your desk or clothes drawer.",
                    "Cut cardboard strips matching the drawer height.",
                    "Cut interlocking half-slots into the strips at desired intervals.",
                    "Slot the strips together in a grid to keep socks, cables, or stationery neatly organized."
                ],
                "steps_ta": [
                    "உங்கள் அலமாரியின் உயரம் மற்றும் அகலத்தை அளவிடவும்.",
                    "அந்த உயரத்திற்கு ஏற்ப அட்டைத் துண்டுகளை வெட்டவும்.",
                    "துண்டுகளின் நடுவே பாதியளவு இடைவெளிகளை வெட்டி ஒன்றோடொன்று இணைக்கவும்.",
                    "அலமாரியில் வைத்து பொருட்களை ஒழுங்காக அடுக்கவும்."
                ],
                "safety_tip_en": "Cut cardboard on a cutting mat or flat wooden board.",
                "safety_tip_ta": "அட்டை வெட்டும்போது விரல்களில் காயம் படாமல் எச்சரிக்கையுடன் வெட்டவும்."
            },
            {
                "id": "paper-gift-bag",
                "title_en": "Eco-Friendly Newspaper Gift Bag",
                "title_ta": "சுற்றுச்சூழல் நட்பு செய்தித்தாள் பரிசுப் பை",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "15 mins",
                "points": 50,
                "materials_en": ["Old newspapers, calendar sheets, or kraft paper", "Non-toxic craft glue or paper tape", "Jute twine or cotton string for handles", "Hole puncher & scissors"],
                "materials_ta": ["பழைய செய்தித்தாள் அல்லது காலண்டர் தாள்கள்", "பசை அல்லது காகித டேப்", "சணல் கயிறு அல்லது நூல்", "துளையிடும் கருவி மற்றும் கத்தரிக்கோல்"],
                "steps_en": [
                    "Cut two equal rectangular sheets from sturdy newspaper and layer them for extra durability.",
                    "Fold the bottom edge up by 2 inches and crease firmly to form the flat gusseted base.",
                    "Fold both side edges inward by 1 inch so the bag expands neatly.",
                    "Glue bottom flaps securely and place a small piece of scrap cardboard inside the base for reinforcement.",
                    "Punch two small holes at the top rim, thread jute twine through, and knot securely inside to make carry handles."
                ],
                "steps_ta": [
                    "நாளிதழை சம செவ்வக வடிவில் வெட்டி உறுதிக்காக இரட்டை அடுக்காக வைக்கவும்.",
                    "அடிப்பகுதியை 2 அங்குலம் மேல்நோக்கி மடித்து உறுதியான அடிப்பாகத்தை உருவாக்கவும்.",
                    "பையின் பக்கவாட்டு பகுதிகளை 1 அங்குலம் உள்நோக்கி மடிக்கவும்.",
                    "அடிப்பகுதியை பசை கொண்டு ஒட்டி, உறுதிக்காக உள்ளே ஒரு சிறிய அட்டைத் துண்டை வைக்கவும்.",
                    "மேல் பகுதியில் துளையிட்டு சணல் கயிற்றை நுழைத்து முடிச்சிட்டு கைப்பிடி உருவாக்கவும்."
                ],
                "safety_tip_en": "Always use child-safe scissors and non-toxic water-based glue.",
                "safety_tip_ta": "கத்தரிக்கோல் பயன்படுத்தும்போது விரல்களில் படாமல் கவனமாக வெட்டவும்; நச்சுத்தன்மையற்ற பசையைப் பயன்படுத்தவும்."
            }
        ],
        "disposal_guidance": {
            "unsuitable_reasons_en": [
                "Grease-stained paper (e.g., oil-soaked pizza boxes cannot be recycled into pulp).",
                "Waxed paper or plastic-coated cups.",
                "Shredded paper too fine for recycling sorting machinery."
            ],
            "unsuitable_reasons_ta": [
                "எண்ணெய் பசை படிந்த பீட்சா மற்றும் உணவுப் பெட்டிகள்.",
                "மெழுகு அல்லது பிளாஸ்டிக் பூசப்பட்ட காகிதக் கோப்பைகள்.",
                "ஈரமான அழுக்கு காகிதங்கள்."
            ],
            "safe_disposal_steps_en": [
                "Keep paper completely dry; wet paper loses fiber strength.",
                "Tear away grease-free clean portions of cardboard for paper recycling.",
                "Greasy, food-stained cardboard can be shredded and added to your compost bin as carbon-rich brown material.",
                "Tie clean newspapers and boxes with twine for dry-waste collectors."
            ],
            "safe_disposal_steps_ta": [
                "காகிதங்களை ஈரம் படாமல் உலர்ந்த நிலையில் வைக்கவும்.",
                "எண்ணெய் பசை இல்லாத பகுதிகளை மட்டும் காகித மறுசுழற்சிக்கு அனுப்பவும்.",
                "எண்ணெய் படிந்த அட்டைகளை சிறு துண்டுகளாக வெட்டி கம்போஸ்ட் உரக் குழியில் சேர்க்கலாம்.",
                "சுத்தமான தாள்களை கட்டி பழைய பேப்பர் கடைக்கு கொடுக்கலாம்."
            ]
        }
    },
    "glass": {
        "id": "glass",
        "name_en": "Glass Bottles & Jars",
        "name_ta": "கண்ணாடி பாட்டில்கள் மற்றும் ஜாடிகள்",
        "icon": "fa-wine-bottle",
        "color": "#10b981",
        "badge_class": "badge-glass",
        "decomposition_time": "Thousands to millions of years (very broad estimate)",
        "common_items": ["Jam & Pickle Jars", "Beverage Bottles", "Sauce Bottles", "Perfume Vials"],
        "summary_en": "Glass is 100% inert, non-toxic, and non-porous. It preserves food freshness without leaching chemicals and lasts indefinitely.",
        "summary_ta": "கண்ணாடி முற்றிலும் பாதுகாப்பானது மற்றும் நச்சுத்தன்மையற்றது. மளிகைப் பொருட்களை நீண்ட காலம் கெடாமல் வைக்க சிறந்தது.",
        "upcycling_projects": [
            {
                "id": "glass-spice-jar",
                "title_en": "Pantry Spice & Dry Ingredient Jars",
                "title_ta": "மளிகைப் பொருட்கள் சேமிக்கும் கண்ணாடி ஜாடி",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "15 mins",
                "points": 40,
                "materials_en": ["Empty sauce or pickle jars", "Warm soapy water & baking soda (for label removal)", "Chalkboard paint or paper labels", "Permanent marker"],
                "materials_ta": ["காலி ஊறுகாய் அல்லது சாஸ் ஜாடிகள்", "வெதுவெதுப்பான சோப்பு நீர் & சமையல் சோடா", "லேபிள்கள்", "மார்க்கர் பேனா"],
                "steps_en": [
                    "Soak jars in warm soapy water with a spoonful of baking soda for 15 minutes to slide sticky labels off easily.",
                    "Scrub any remaining adhesive with cooking oil or baking soda paste.",
                    "Sterilize by washing with hot water and allowing to air dry completely.",
                    "Affix labels and write spice names (e.g., Cumin, Turmeric, Lentils, Seeds).",
                    "Store in your pantry for an aesthetic zero-waste kitchen setup."
                ],
                "steps_ta": [
                    "ஜாடிகளை வெதுவெதுப்பான சோப்பு நீரில் 15 நிமிடங்கள் ஊறவைத்து லேபிளை உரிக்கவும்.",
                    "ஒட்டியிருக்கும் பசையை சமையல் சோடா கொண்டு துடைக்கவும்.",
                    "சுடுநீரில் கழுவி நன்றாக உலர வைக்கவும்.",
                    "மஞ்சள், சீரகம், பருப்பு போன்ற பெயர்களை லேபிளில் எழுதி ஒட்டி அஞ்சறைப் பெட்டியாக பயன்படுத்தவும்."
                ],
                "safety_tip_en": "Never pour boiling water directly into cold glass jars to avoid thermal shock cracking.",
                "safety_tip_ta": "குளிர்ந்த கண்ணாடி பாட்டிலில் கொதிக்கும் நீரை நேரடியாக ஊற்ற வேண்டாம்; விரிசல் ஏற்படலாம்."
            },
            {
                "id": "glass-fairy-lantern",
                "title_en": "Cozy Ambient Fairy Light Lantern",
                "title_ta": "அலங்கார விளக்கு கண்ணாடி கூடு",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "10 mins",
                "points": 40,
                "materials_en": ["Clean glass jar or wine bottle", "Battery-powered micro LED fairy lights", "Jute twine or dried flowers for decoration"],
                "materials_ta": ["சுத்தமான கண்ணாடி பாட்டில்", "எல்.இ.டி விளக்கு சரங்கள்", "சணல் கயிறு அல்லது காய்ந்த பூக்கள்"],
                "steps_en": [
                    "Ensure the inside of the jar is sparkling clean and dry.",
                    "Thread the string of micro LED fairy lights inside the bottle or jar.",
                    "Secure the tiny battery pack underneath the lid or behind the base.",
                    "Wrap rustic jute twine around the jar neck for a bohemian lantern finish."
                ],
                "steps_ta": [
                    "பாட்டிலை நன்றாக துடைத்து உலர்த்தவும்.",
                    "எல்.இ.டி விளக்கு கம்பியை பாட்டிலின் உள்ளே வைக்கவும்.",
                    "பாட்டிலின் கழுத்துப் பகுதியில் சணல் கயிறு கட்டி அலங்கரிக்கவும்.",
                    "இரவு நேரத்தில் அழகான மேஜை விளக்காக பயன்படுத்தலாம்."
                ],
                "safety_tip_en": "Use only low-voltage battery/USB LED lights. Do not use open flames in enclosed bottles.",
                "safety_tip_ta": "பாட்டிலின் உள்ளே மெழுகுவர்த்தி தீக்குச்சிகளை கொளுத்த வேண்டாம்; எல்.இ.டி விளக்குகளை மட்டும் பயன்படுத்தவும்."
            },
            {
                "id": "glass-hydroponic-vase",
                "title_en": "Hydroponic Money Plant & Herb Propagation Vase",
                "title_ta": "நீர்நிலை தாவர மற்றும் மூலிகை வளர்ப்பு கண்ணாடி குவளை",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "10 mins",
                "points": 50,
                "materials_en": ["Empty glass bottle or wide-mouth sauce jar", "Clean room-temperature tap or RO water", "Healthy money plant, pothos, or mint cuttings", "A few smooth decorative glass pebbles or stones"],
                "materials_ta": ["காலி கண்ணாடி பாட்டில் அல்லது ஜாடி", "சுத்தமான குடிநீர்", "மணி பிளான்ட் அல்லது புதினா கிளைகள்", "சிறு அலங்காரக் கற்கள்"],
                "steps_en": [
                    "Wash the glass bottle thoroughly with warm soapy water and rinse to remove all food traces or odor.",
                    "Drop 5-6 smooth clean pebbles to the bottom of the bottle to weigh down and support delicate stem bases.",
                    "Fill the bottle three-quarters full with fresh room-temperature water.",
                    "Take a 6-inch healthy stem cutting with at least 2 leaf nodes and remove any lower leaves that would sit submerged in water.",
                    "Place the stem into the bottle so nodes are submerged in water. Place near indirect sunlight; healthy white roots will sprout in 7 to 10 days!"
                ],
                "steps_ta": [
                    "கண்ணாடி பாட்டிலை வெதுவெதுப்பான சோப்பு நீரில் நன்றாகக் கழுவி வாசனை போக உலர்த்தவும்.",
                    "பாட்டிலின் அடியில் தாவர வேர்களைத் தாங்க சில சிறிய கூழாங்கற்களைப் போடவும்.",
                    "பாட்டிலில் முக்கால் பங்கு சுத்தமான தண்ணீர் நிரப்பவும்.",
                    "மணி பிளான்ட் அல்லது புதினா கிளையின் கீழ் இலைகளை நீக்கிவிட்டு தண்டைத் தண்ணீரில் வைக்கவும்.",
                    "சூரிய ஒளி நேரடியாக படாத இடத்தில் வைக்கவும். 7-10 நாட்களில் புதிய வேர்கள் வளர்ந்து செழிப்பாக வளரும்!"
                ],
                "safety_tip_en": "Change the standing water once every 5 to 7 days to keep it oxygenated and prevent mosquito breeding.",
                "safety_tip_ta": "கொசுக்கள் முட்டையிடுவதைத் தடுக்கவும் நன்னீர் பராமரிக்கவும் 5-7 நாட்களுக்கு ஒருமுறை தண்ணீரை மாற்றவும்."
            }
        ],
        "disposal_guidance": {
            "unsuitable_reasons_en": [
                "Chipped, cracked, or shattered glass that poses a severe cut risk.",
                "Pyrex cookware, window panes, light bulbs, or mirrors (contain additives with different melting points).",
                "Medical medicine vials with toxic residue."
            ],
            "unsuitable_reasons_ta": [
                "உடைந்த அல்லது விரிசல் விழுந்த கண்ணாடி.",
                "கண்ணாடி ஜன்னல் துண்டுகள், முகம் பார்க்கும் கண்ணாடி அல்லது பல்புகள்.",
                "நச்சு மருந்து பாட்டில்கள்."
            ],
            "safe_disposal_steps_en": [
                "Never mix broken glass into general loose trash where it can cut sanitation workers.",
                "Wrap broken glass securely in several layers of newspaper or cardboard and tape it shut.",
                "Label the package clearly: 'DANGER: BROKEN GLASS'.",
                "Deposit intact bottles into segregated dry glass collection streams."
            ],
            "safe_disposal_steps_ta": [
                "உடைந்த கண்ணாடியை திறந்த குப்பைத் தொட்டியில் வீச வேண்டாம்; துப்புரவுப் பணியாளர்களுக்கு காயம் ஏற்படும்.",
                "உடைந்த துண்டுகளை பழைய செய்தித்தாள் அல்லது அட்டையில் பலமுறை சுற்றி டேப் ஒட்டவும்.",
                "'எச்சரிக்கை: உடைந்த கண்ணாடி' என்று அதன் மேல் எழுதவும்.",
                "முழு பாட்டில்களை உலர் கண்ணாடி மறுசுழற்சியில் சேர்க்கவும்."
            ]
        }
    },
    "metal": {
        "id": "metal",
        "name_en": "Metal Cans & Tins",
        "name_ta": "உலோக டப்பாக்கள் & தகரக் கேன்கள்",
        "icon": "fa-can-food",
        "color": "#64748b",
        "badge_class": "badge-metal",
        "decomposition_time": "80–100 years for steel; 200–400 years for aluminum",
        "common_items": ["Tin Food Cans", "Aluminum Beverage Cans", "Biscuit Tins", "Metal Bottle Caps"],
        "summary_en": "Metals are infinitely recyclable without loss of quality. Clean cans make sturdy desk organizers and kitchen herb pots.",
        "summary_ta": "உலோகங்கள் தரத்தை இழக்காமல் எத்தனை முறை வேண்டுமானாலும் மறுசுழற்சி செய்யக்கூடியவை. இவற்றில் செடிகள் வளர்க்கலாம்.",
        "upcycling_projects": [
            {
                "id": "metal-herb-planter",
                "title_en": "Rustic Tin Can Herb Planter",
                "title_ta": "மூலிகைச் செடி வளர்க்கும் தகரப் பாத்திரம்",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "15 mins",
                "points": 45,
                "materials_en": ["Clean empty tin can (food or soup can)", "Hammer and nail", "Acrylic paint", "Small pebbles & potting mix", "Mint, coriander, or basil seeds"],
                "materials_ta": ["சுத்தமான தகர டப்பா", "சுத்தியல் மற்றும் ஆணி", "வர்ணம்", "சிறு கற்கள் & மண்", "புதினா அல்லது கொத்தமல்லி விதைகள்"],
                "steps_en": [
                    "Wash the tin can and remove any paper label by soaking in water.",
                    "Turn the can upside down and use a hammer and nail to punch 3-4 drainage holes in the bottom.",
                    "Paint the outside in your favorite color or leave it metallic for an industrial look.",
                    "Place a handful of small pebbles at the bottom for drainage, add potting soil, and plant fresh kitchen herbs."
                ],
                "steps_ta": [
                    "டப்பாவை தண்ணீரில் கழுவி லேபிளை நீக்கவும்.",
                    "டப்பாவை தலைகீழாக வைத்து அடியில் ஆணியால் 3 துளைகள் இடவும் (தண்ணீர் வடிய).",
                    "வெளிப்புறத்தில் வர்ணம் பூசவும்.",
                    "அடியில் சிறு கற்கள் போட்டு மண் நிரப்பி புதினா அல்லது கொத்தமல்லி நடவும்."
                ],
                "safety_tip_en": "Check the interior rim with a spoon or cloth. If sharp, press smooth with pliers before handling.",
                "safety_tip_ta": "டப்பாவின் மேல் விளிம்பு கூர்மையாக இருந்தால் இடுக்கி கொண்டு மடக்கி விடவும்."
            },
            {
                "id": "metal-punched-lantern",
                "title_en": "Punched-Tin Luminary Lantern",
                "title_ta": "துளைகள் கொண்ட மெழுகுவர்த்தி கூண்டு",
                "difficulty": "Medium",
                "difficulty_ta": "நடுத்தரம்",
                "time_required": "25 mins",
                "points": 60,
                "materials_en": ["Clean tin can", "Water & freezer (to fill with ice so it doesn't dent)", "Hammer and different sized nails", "LED tealight candle"],
                "materials_ta": ["தகர டப்பா", "தண்ணீர் (பனிக்கட்டியாக்க)", "சுத்தியல் மற்றும் ஆணிகள்", "மெழுகுவர்த்தி"],
                "steps_en": [
                    "Fill the can with water and freeze it solid overnight. The ice prevents the metal from denting while hammering!",
                    "Draw a dot pattern (star, flower, geometric dots) with marker on paper and tape it around the frozen can.",
                    "Gently hammer nails along the pattern dots to punch light holes.",
                    "Melt the ice with warm water, dry thoroughly, and insert an LED tealight candle to create magical ambient shadows."
                ],
                "steps_ta": [
                    "டப்பாவில் தண்ணீர் ஊற்றி ஃப்ரீசரில் வைத்து பனிக்கட்டியாக்க வேண்டும் (துளையிடும்போது நசுங்காமல் இருக்க).",
                    "காகிதத்தில் நட்சத்திரம் அல்லது பூ போன்ற புள்ளிகளை வரைந்து டப்பாவில் ஒட்டவும்.",
                    "ஆணி வைத்து லேசாக தட்டி அழகான துளைகள் போடவும்.",
                    "பனிக்கட்டி உருகியதும் உலர்த்தி, உள்ளே விளக்கு வைத்து ஒளிரச் செய்யவும்."
                ],
                "safety_tip_en": "Wear protective eyewear when punching holes with nails.",
                "safety_tip_ta": "ஆணி அடிக்கும்போது கண்கள் மற்றும் விரல்களில் படாமல் பார்த்துக் கொள்ளவும்."
            },
            {
                "id": "metal-desk-caddy",
                "title_en": "Tiered Magnetic Desk Organizer & Tool Caddy",
                "title_ta": "அடுக்கு மேஜை எழுதுபொருள் & சிறு கருவி டப்பா",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "20 mins",
                "points": 50,
                "materials_en": ["2-3 empty metal food or biscuit tins of different heights", "Sandpaper or electrical tape", "Acrylic craft paint or twine", "Strong magnet or adhesive"],
                "materials_ta": ["வெவ்வேறு உயரமுள்ள 2-3 தகர டப்பாக்கள்", "மணற்காகிதம் அல்லது இன்சுலேஷன் டேப்", "வர்ணப் பூச்சு அல்லது சணல் கயிறு", "பசை அல்லது காந்தம்"],
                "steps_en": [
                    "Wash cans thoroughly with warm dish soap and scrub away all sticky grease and label residues.",
                    "Inspect top cut rims carefully. Use pliers to bend any sharp metal burrs flush inside, then line the rim with durable cloth or electrical tape.",
                    "Paint exterior cans in matching pastel or metallic tones, or wrap in rustic jute twine for a natural look.",
                    "Glue the cans side-by-side or stack on a small reclaimed wooden block to form tiered compartments.",
                    "Attach a small neodymium magnet to the side to instantly hold paper clips, hair pins, or metal screwdrivers!"
                ],
                "steps_ta": [
                    "தகர டப்பாக்களை சோப்பு நீரில் நன்றாகக் கழுவி லேபிள்களை நீக்கவும்.",
                    "மேல் விளிம்பில் கூர்மையான பகுதிகள் இருந்தால் இடுக்கி கொண்டு உள்பக்கமாக மடித்து, டேப் ஒட்டவும்.",
                    "டப்பாவின் வெளிப்புறத்தில் வர்ணம் பூசவும் அல்லது சணல் கயிறு சுற்றி அழகுபடுத்தவும்.",
                    "டப்பாக்களை பக்கவாட்டில் ஒன்றாக ஒட்டி பல அறைகள் கொண்ட அமைப்பாக மாற்றவும்.",
                    "பக்கவாட்டில் ஒரு சிறிய காந்தத்தை ஒட்டி கிளிப்புகள், ஊசிகள் மற்றும் திருப்புளிகளை எளிதாக ஒட்ட வைக்கலாம்!"
                ],
                "safety_tip_en": "Always sand or tape cut metal edges before handling to prevent skin nicks or abrasions.",
                "safety_tip_ta": "கைகளில் காயம் ஏற்படாமல் இருக்க விளிம்புகளை மணற்காகிதம் தேய்த்தோ அல்லது டேப் ஒட்டியோ மூடவும்."
            }
        ],
        "disposal_guidance": {
            "unsuitable_reasons_en": [
                "Severely rusted or corroded cans with dangerous sharp jagged edges.",
                "Aerosol spray cans that are pressurized or contain flammable propellants.",
                "Cans used for automotive oils or harsh industrial acids."
            ],
            "unsuitable_reasons_ta": [
                "அதிக துருப்பிடித்த அல்லது கிழிந்த கூர்மையான டப்பாக்கள்.",
                "தீப்பிடிக்கக்கூடிய ஏரோசால் ஸ்ப்ரே கேன்கள்.",
                "ஆயில் அல்லது விஷ ரசாயன கேன்கள்."
            ],
            "safe_disposal_steps_en": [
                "Rinse thoroughly to remove grease and food remnants.",
                "Aerosol spray cans must be completely empty before disposal; never puncture a pressurized can.",
                "Fold the sharp cut lid inside the can and pinch the top slightly shut.",
                "Place in the designated dry metal recyclable stream; metal is high-value for local scrap collectors."
            ],
            "safe_disposal_steps_ta": [
                "உணவுப் பொருட்களை நீக்கி தண்ணீரில் கழுவவும்.",
                "ஸ்ப்ரே கேன்களில் காற்று முற்றிலும் தீர்ந்த பிறகே அப்புறப்படுத்த வேண்டும்; துளையிடக் கூடாது.",
                "கூர்மையான மூடியை உள்பக்கமாக மடித்து வைக்கவும்.",
                "பழைய இரும்பு மற்றும் உலோக வியாபாரிகளிடம் கொடுத்து மறுசுழற்சி செய்யலாம்."
            ]
        }
    },
    "organic": {
        "id": "organic",
        "name_en": "Organic & Kitchen Waste",
        "name_ta": "உயிர்க்கழிவு & சமையலறை கழிவு",
        "icon": "fa-apple-whole",
        "color": "#16a34a",
        "badge_class": "badge-organic",
        "decomposition_time": "About 2–4 weeks for fruit scraps",
        "common_items": ["Vegetable Peels", "Fruit Rinds", "Coffee Grounds", "Tea Leaves", "Dry Garden Leaves", "Eggshells"],
        "summary_en": "Organic scraps can be composted to return organic matter to soil. Composting outcomes depend on the process and local waste handling.",
        "summary_ta": "சமையலறைக் கழிவுகள் தாவரங்களுக்குத் தேவையான சத்துக்களைக் கொண்டுள்ளன. இவற்றை எளிதாக இயற்கை உரமாக மாற்றலாம்.",
        "upcycling_projects": [
            {
                "id": "organic-citrus-enzyme",
                "title_en": "Citrus Peel Fermented Cleaning Trial",
                "title_ta": "எலுமிச்சை தோல் இயற்கை சுத்தப்படுத்தி (பயோ-என்சைம்)",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "15 mins (+ ferment time)",
                "points": 50,
                "materials_en": ["Citrus peels (lemon, orange, sweet lime) - 300g", "Jaggery or brown sugar - 100g", "Water - 1 Liter", "Wide-mouth plastic container with a vented lid or fermentation airlock"],
                "materials_ta": ["எலுமிச்சை / ஆரஞ்சு பழத்தோல் - 300 கிராம்", "நாட்டுச் சர்க்கரை அல்லது வெல்லம் - 100 கிராம்", "தண்ணீர் - 1 லிட்டர்", "பிளாஸ்டிக் பாட்டில்"],
                "steps_en": [
                    "Follow the 1:3:10 ratio: 1 part jaggery, 3 parts citrus peels, 10 parts water.",
                    "Dissolve jaggery in water inside a wide-mouth plastic bottle (leave 20% empty space for gases).",
                    "Add citrus peels cut into small pieces.",
                    "Fit a vented fermentation lid or airlock and follow its directions. Never use glass or an airtight lid; fermentation gas can build pressure. Keep the container in a cool place away from children, and discard it safely if it swells or leaks.",
                    "After about 3 months, strain the liquid. If you choose to try it, dilute 1:10 and spot-test a small non-food-contact surface. It is not a disinfectant; do not use it on food or food-contact surfaces."
                ],
                "steps_ta": [
                    "1:3:10 விகிதம்: 1 பங்கு வெல்லம், 3 பங்கு பழத்தோல், 10 பங்கு தண்ணீர்.",
                    "பாட்டிலில் தண்ணீருடன் வெல்லத்தைக் கரைக்கவும் (வாயு வெளிவர 20% இடம் விடவும்).",
                    "பழத்தோல்களை நறுக்கி உள்ளே போடவும்.",
                    "பாட்டிலை மூடி வைக்கவும். முதல் மாதத்தில் தினமும் ஒருமுறை மூடியை லேசாக திறந்து வாயுவை வெளியேற்றவும்.",
                    "3 மாதங்களுக்குப் பிறகு வடிகட்டி, தண்ணீரில் கலந்து வீடு மற்றும் தரை துடைக்கப் பயன்படுத்தலாம்!"
                ],
                "safety_tip_en": "Use a vented lid or fermentation airlock; never seal the container or use glass. Keep it away from children and discard it safely if it swells or leaks.",
                "safety_tip_ta": "கண்ணாடி பாட்டிலில் செய்ய வேண்டாம்; வாயு அழுத்தத்தால் கண்ணாடி வெடிக்கலாம். பிளாஸ்டிக் பாட்டில்களைப் பயன்படுத்தவும்."
            },
            {
                "id": "organic-pot-composting",
                "title_en": "Balcony Pot Composting",
                "title_ta": "பால்கனி மண்பானை இயற்கை உரம்",
                "difficulty": "Medium",
                "difficulty_ta": "நடுத்தரம்",
                "time_required": "15 mins daily",
                "points": 60,
                "materials_en": ["Earthen clay pot or perforated bucket", "Daily kitchen wet peels", "Dry leaves, cocopeat, or shredded cardboard (browns)", "A small amount of water if the mix is dry"],
                "materials_ta": ["மண்பானை அல்லது துளையிட்ட வாளி", "சமையலறை காய்கறி கழிவுகள்", "காய்ந்த இலைகள் அல்லது தூள் அட்டை", "கலவை காய்ந்திருந்தால் சிறிதளவு தண்ணீர்"],
                "steps_en": [
                    "Place a 2-inch layer of dry leaves or shredded plain cardboard at the bottom of the pot.",
                    "Add your drained, chopped daily kitchen vegetable and fruit scraps.",
                    "Cover immediately with an equal layer of dry brown leaves to prevent fruit flies and bad odor.",
                    "Keep the mix slightly moist and aerated, never waterlogged; add a little water only if it feels dry.",
                    "Mix regularly and allow it to mature; composting can take several months. Use it only when it is cool, crumbly, and earthy-smelling. If it smells rotten, add dry browns and allow more time."
                ],
                "steps_ta": [
                    "மண்பானையின் அடியில் 2 அங்குலம் காய்ந்த இலைகள் போடவும்.",
                    "நறுக்கிய காய்கறி மற்றும் பழக்கழிவுகளை போடவும்.",
                    "ஈக்கள் மற்றும் துர்நாற்றம் வராமல் இருக்க மீண்டும் காய்ந்த இலைகள் கொண்டு மூடவும்.",
                    "கலவை சற்றே ஈரமாகவும் காற்றோட்டமாகவும் இருக்கட்டும்; நீர் தேங்கக்கூடாது. காய்ந்திருந்தால் சிறிது தண்ணீர் மட்டும் சேர்க்கவும்.",
                    "4 முதல் 6 வாரங்களில் கருப்பு நிற இயற்கை உரம் தயாராகிவிடும்."
                ],
                "safety_tip_en": "Do not add cooked or oily foods, meat, dairy, or pet feces to a small balcony compost pot; they can attract pests and cause odors or health risks.",
                "safety_tip_ta": "சமைத்த அல்லது எண்ணெய் உணவுகள், இறைச்சி, பால் பொருட்கள், செல்லப்பிராணி கழிவுகளை சிறிய பால்கனி உரத் தொட்டியில் சேர்க்க வேண்டாம்; பூச்சிகள், துர்நாற்றம் அல்லது உடல்நல ஆபத்து ஏற்படலாம்."
            },
            {
                "id": "organic-liquid-fertilizer",
                "title_en": "Kitchen Scrap Nutrient Booster Tea (Banana & Eggshell)",
                "title_ta": "வாழைத்தோல் & முட்டை ஓடு திரவ ஊட்டச்சத்து உரம்",
                "difficulty": "Easy",
                "difficulty_ta": "எளிது",
                "time_required": "10 mins (+ 48 hrs steep)",
                "points": 40,
                "materials_en": ["Banana peels (potassium) & crushed eggshells (calcium)", "Used coffee grounds or tea leaves (nitrogen)", "1 Liter tap water", "Large reusable plastic container or jar"],
                "materials_ta": ["வாழைப்பழத்தோல் மற்றும் தூள் செய்த முட்டை ஓடுகள்", "பயன்படுத்திய தேயிலைத் தூள்", "1 லிட்டர் தண்ணீர்", "பிளாஸ்டிக் பாத்திரம்"],
                "steps_en": [
                    "Rinse 3-4 clean eggshells to remove yolk residues, dry in the sun, and crush finely with a spoon.",
                    "Chop 2-3 ripe banana peels into small 1-inch strips for quick nutrient extraction.",
                    "Place crushed eggshells, chopped banana peels, and 2 tablespoons of used tea leaves into a 1-liter plastic jug.",
                    "Fill with water, cover loosely with a lid or cloth, and let steep in a shaded corner for 48 to 72 hours.",
                    "Strain the concentrated tea through a mesh sieve. Dilute 1:5 with fresh water and pour directly into soil around flowering plants and herbs!"
                ],
                "steps_ta": [
                    "முட்டை ஓடுகளைக் கழுவி வெயிலில் காயவைத்து, கரண்டியால் நசுக்கி தூளாக்கவும்.",
                    "வாழைப்பழத்தோல்களை சிறு துண்டுகளாக நறுக்கவும்.",
                    "ஒரு பாத்திரத்தில் தூள் செய்த முட்டை ஓடு, நறுக்கிய வாழைப்பழத்தோல் மற்றும் 2 ஸ்பூன் தேயிலைத் தூள் போடவும்.",
                    "அதில் 1 லிட்டர் தண்ணீர் ஊற்றி மூடி 48 முதல் 72 மணி நேரம் நிழலில் ஊற வைக்கவும்.",
                    "ஊறிய நீரை வடிகட்டி, 1 பங்கு திரவத்திற்கு 5 பங்கு நல்ல தண்ணீர் கலந்து செடிகளுக்கு ஊற்றவும். பூக்கள் மற்றும் காய்கள் செழிப்பாக வளரும்!"
                ],
                "safety_tip_en": "Rinse eggshells thoroughly before soaking to avoid unpleasant sulfur odors, and always dilute before applying to sensitive young seedlings.",
                "safety_tip_ta": "துர்நாற்றம் வராமல் இருக்க முட்டை ஓடுகளை நன்றாக கழுவிய பின்னரே பயன்படுத்தவும்; செடிகளுக்கு ஊற்றும்போது தண்ணீரில் கலந்து ஊற்றவும்."
            }
        ],
        "disposal_guidance": {
            "unsuitable_reasons_en": [
                "Rotten cooked food with heavy fungal mold or pathogens.",
                "Dog/cat pet waste (carries parasites unsafe for vegetable gardens).",
                "Diseased plants infested with active garden pests."
            ],
            "unsuitable_reasons_ta": [
                "அழுகிய பூஞ்சை பிடித்த சமைத்த உணவு.",
                "நாய்கள் மற்றும் பூனைகளின் மலக்கழிவு.",
                "பூச்சி தாக்கிய தாவரங்கள்."
            ],
            "safe_disposal_steps_en": [
                "Always separate wet organic waste from dry plastics and metals at the source.",
                "Keep organic waste in a lidded green bin and drain excess gravies/water.",
                "Deposit in your municipal green wet-waste collection cart daily to prevent pest breeding.",
                "Never pack organic wet waste inside plastic bags into landfills—anaerobic rotting produces greenhouse gases."
            ],
            "safe_disposal_steps_ta": [
                "ஈரக் கழிவுகளையும் உலர் கழிவுகளையும் எப்போதும் தனித்தனியாக பிரிக்கவும்.",
                "பச்சை நிற மூடியுள்ள குப்பைத் தொட்டியில் வைக்கவும்.",
                "நகராட்சி துப்புரவுப் பணியாளர்களிடம் ஈரக்கழிவாக தினமும் ஒப்படைக்கவும்.",
                "பிளாஸ்டிக் பைகளில் கட்டி குப்பையில் வீச வேண்டாம்."
            ]
        }
    }
}

KEYWORD_MAP = {
    # Plastic
    "bottle": "plastic",
    "bottles": "plastic",
    "plastic": "plastic",
    "plastics": "plastic",
    "pet": "plastic",
    "cup": "plastic",
    "cups": "plastic",
    "jug": "plastic",
    "jugs": "plastic",
    "container": "plastic",
    "containers": "plastic",
    "poly": "plastic",
    "polythene": "plastic",
    "straw": "plastic",
    "straws": "plastic",
    "cap": "plastic",
    "caps": "plastic",
    "shampoo": "plastic",
    "detergent": "plastic",
    "wrapper": "plastic",
    "wrappers": "plastic",
    "pouch": "plastic",
    "pouches": "plastic",
    "packet": "plastic",
    "packets": "plastic",
    "waterbottle": "plastic",
    "hdpe": "plastic",
    "ldpe": "plastic",
    "pvc": "plastic",
    # Paper & Cardboard
    "paper": "paper",
    "papers": "paper",
    "cardboard": "paper",
    "box": "paper",
    "boxes": "paper",
    "carton": "paper",
    "cartons": "paper",
    "newspaper": "paper",
    "newspapers": "paper",
    "book": "paper",
    "books": "paper",
    "sheet": "paper",
    "sheets": "paper",
    "envelope": "paper",
    "envelopes": "paper",
    "egg": "paper",
    "magazine": "paper",
    "magazines": "paper",
    "notebook": "paper",
    "notebooks": "paper",
    # Glass
    "glass": "glass",
    "glasses": "glass",
    "jar": "glass",
    "jars": "glass",
    "jam": "glass",
    "pickle": "glass",
    "pickles": "glass",
    "wine": "glass",
    "vial": "glass",
    "vials": "glass",
    "sauce": "glass",
    "sauces": "glass",
    "ketchup": "glass",
    # Metal
    "metal": "metal",
    "metals": "metal",
    "can": "metal",
    "cans": "metal",
    "tin": "metal",
    "tins": "metal",
    "aluminum": "metal",
    "aluminium": "metal",
    "steel": "metal",
    "foil": "metal",
    "soda": "metal",
    "coke": "metal",
    "pepsi": "metal",
    "sprite": "metal",
    "beverage": "metal",
    # Organic
    "organic": "organic",
    "peel": "organic",
    "peels": "organic",
    "food": "organic",
    "fruit": "organic",
    "fruits": "organic",
    "vegetable": "organic",
    "vegetables": "organic",
    "leaf": "organic",
    "leaves": "organic",
    "coffee": "organic",
    "tea": "organic",
    "banana": "organic",
    "orange": "organic",
    "lemon": "organic",
    "apple": "organic",
    "apples": "organic",
    "compost": "organic",
    "eggshell": "organic",
    "eggshells": "organic",
    "kitchen": "organic",
    "waste": "organic",
    # Tamil Keywords / தமிழ் சொற்கள்
    "பாட்டில்": "plastic",
    "பாட்டில்கள்": "plastic",
    "நெகிழி": "plastic",
    "பிளாஸ்டிக்": "plastic",
    "குவளை": "plastic",
    "மூடி": "plastic",
    "காகிதம்": "paper",
    "காகிதங்கள்": "paper",
    "அட்டை": "paper",
    "அட்டைகள்": "paper",
    "செய்தித்தாள்": "paper",
    "புத்தகம்": "paper",
    "உறை": "paper",
    "கண்ணாடி": "glass",
    "ஜாடி": "glass",
    "குடுவை": "glass",
    "உலோகம்": "metal",
    "தகரம்": "metal",
    "டப்பா": "metal",
    "கேன்": "metal",
    "இரும்பு": "metal",
    "காய்கறி": "organic",
    "காய்கறிகள்": "organic",
    "பழம்": "organic",
    "பழங்கள்": "organic",
    "பழத்தோல்": "organic",
    "தோல்": "organic",
    "உரம்": "organic",
    "இலை": "organic",
    "இலைகள்": "organic",
    "கழிவு": "organic"
}

def detect_category_from_keywords(query_text):
    """
    Transparent heuristic keyword search for waste categorization in English and Tamil.
    Returns matched category ('plastic', 'paper', 'glass', 'metal', 'organic')
    or None if no reliable match is found.
    """
    if not query_text:
        return None

    # Normalize query text by replacing punctuation with spaces
    text_lower = str(query_text).lower().replace(".", " ").replace("_", " ").replace("-", " ")
    words = text_lower.split()

    # 1. Exact word-level matching
    for word in words:
        clean_word = "".join(c for c in word if c.isalnum() or unicodedata.category(c).startswith("M"))
        if clean_word in KEYWORD_MAP:
            return KEYWORD_MAP[clean_word]

    # 2. Substring matching for compound words (e.g. 'waterbottle', 'picklejar', 'bananapeel')
    distinctive_short = ("can", "jar", "tin", "box", "cup", "egg", "tea", "pet")
    for kw, cat in KEYWORD_MAP.items():
        if len(kw) >= 4 or kw in distinctive_short:
            if kw in text_lower:
                return cat

    return None

def get_category_data(category_id):
    """
    Returns data dictionary for a category, or None if category is unknown or invalid.
    """
    if not category_id or category_id not in WASTE_CATEGORIES:
        return None
    return WASTE_CATEGORIES[category_id]

