"""All site copy in one place.

Everything here was written as a starting point. Lines marked PLACEHOLDER are
facts the business needs to confirm (prices, contact details, service area,
roaster) before the site goes public.
"""

BRAND = {
    "name": "Key & Kin",
    "tagline": "Specialty coffee, brought to your people.",
    "email": "hello@keyandkin.co",  # PLACEHOLDER
    "phone": "(555) 014-2290",  # PLACEHOLDER
    "phone_tel": "+15550142290",  # PLACEHOLDER, same number for tel: links
    "instagram": "keyandkincoffee",  # PLACEHOLDER
    "service_area": "Serving events within 50 miles of home base",  # PLACEHOLDER
}

HERO = {
    "headline": "Specialty coffee, brought to your people.",
    "body": (
        "Key & Kin is a mobile espresso cart for weddings, offices, showers and "
        "markets. We bring the machine, the baristas and a menu built for your "
        "event, and your guests get a proper cup without leaving the party."
    ),
    "cta": "Plan your event",
}

STEPS = [
    {
        "title": "Tell us about your event",
        "body": "Send the date, the place and a rough guest count. We reply within two days with availability and a quote.",
    },
    {
        "title": "Shape the menu together",
        "body": "Pick from our core drinks, add a signature named after the couple or the company, and settle milks and syrups.",
    },
    {
        "title": "We pull up and pour",
        "body": "We arrive an hour early, set up in a 10 by 10 foot space and serve until the last guest has a cup.",
    },
]

MENU = {
    "intro": (
        "Every event gets the full espresso bar. Signatures rotate with the "
        "season, and we'll build one just for you."
    ),
    "groups": [
        {
            "name": "Espresso bar",
            "items": [
                ("Espresso", "A double shot, pulled to order."),
                ("Cortado", "Equal parts espresso and steamed milk."),
                ("Cappuccino", "Six ounces, with a deep layer of foam."),
                ("Latte", "Hot or iced, in any milk we carry."),
                ("Americano", "Espresso lengthened with hot water."),
            ],
        },
        {
            "name": "Signatures",
            "items": [
                ("Honey lavender latte", "Local wildflower honey and dried lavender, steeped in house."),
                ("Brown butter cortado", "Brown butter and a pinch of sea salt, folded into the milk."),
                ("Cardamom cold foam", "Slow cold brew under a cardamom and vanilla cream."),
                ("Maple oat flat white", "Grade A maple with oat milk, smooth and not too sweet."),
            ],
        },
        {
            "name": "Not coffee",
            "items": [
                ("Masala chai", "Brewed from whole spices, not a concentrate."),
                ("Ceremonial matcha", "Whisked by hand, hot or over ice."),
                ("Seasonal refresher", "Sparkling and fruit-led, caffeine-free."),
                ("Steamer", "Steamed milk with vanilla or chocolate, for the kids."),
            ],
        },
    ],
    "notes": [
        "Whole, oat and almond milk are always on the cart.",
        "Decaf espresso is available for every espresso drink.",
        "Beans are roasted weekly by a local partner roaster.",  # PLACEHOLDER: name the roaster
    ],
}

PACKAGES = [
    {
        "key": "gathering",
        "name": "Gathering",
        "price": "From $650",  # PLACEHOLDER
        "summary": "For showers, small offices and dinner parties.",
        "details": ["2 hours of service", "Up to 50 guests", "One barista", "Core espresso menu"],
    },
    {
        "key": "celebration",
        "name": "Celebration",
        "price": "From $1,150",  # PLACEHOLDER
        "summary": "Our most booked package, built for weddings.",
        "details": [
            "3 hours of service",
            "Up to 150 guests",
            "Two baristas",
            "Core menu and two signature drinks",
            "Custom menu sign",
        ],
        "featured": True,
    },
    {
        "key": "full_day",
        "name": "Full day",
        "price": "From $2,200",  # PLACEHOLDER
        "summary": "For conferences, markets and brand activations.",
        "details": [
            "Up to 6 hours of service",
            "Up to 400 guests",
            "Two to three baristas",
            "Full menu with a custom signature",
            "Branded cups and sleeves available",
        ],
    },
]

EVENTS = [
    ("Weddings", "Morning-after brunches, cocktail hour and a late espresso before the dancing."),
    ("Offices", "Team days, launches and client visits."),
    ("Showers and birthdays", "Something warmer than a punch bowl."),
    ("Markets and pop-ups", "We run our own line and payment, or we serve on your tab."),
    ("Brand activations", "Logo on the cart, the cups and the foam."),
]

ABOUT = {
    "title": "Why Key & Kin",
    "paragraphs": [
        (
            "A key is small, and it gets you in. For us that's good coffee: the "
            "detail guests remember and keep coming back to the cart for."
        ),
        (
            "Kin is who you invite. We started Key & Kin to serve the people you "
            "bring together, with the care we'd give our own family."
        ),
    ],
}

FAQ = [
    (
        "What do you need from the venue?",
        "A flat 10 by 10 foot space and one standard 20-amp outlet within 50 feet. "
        "If there's no power, tell us and we'll bring a quiet generator for a small fee.",
    ),
    (
        "How far do you travel?",
        "Travel is included within 50 miles. Beyond that we add a per-mile fee, "
        "which we'll include in your quote.",
    ),
    (
        "How far ahead should we book?",
        "Weddings usually book 3 to 9 months out. Smaller events can often be "
        "booked 2 to 3 weeks ahead, so ask even if your date is close.",
    ),
    (
        "Can you handle allergies and dietary needs?",
        "Yes. We keep dairy-free milks on the cart, use nut-free syrups, and can "
        "keep almond milk off the cart entirely for nut-free events.",
    ),
    (
        "How does payment work?",
        "A 30% deposit holds your date. The balance is due a week before the event.",
    ),
]

EVENT_TYPES = [
    ("wedding", "Wedding"),
    ("corporate", "Office or corporate"),
    ("shower", "Shower or birthday"),
    ("market", "Market or pop-up"),
    ("activation", "Brand activation"),
    ("other", "Something else"),
]

PACKAGE_CHOICES = [("", "Not sure yet")] + [(p["key"], p["name"]) for p in PACKAGES]
