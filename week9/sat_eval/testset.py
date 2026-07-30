TESTS = [
    # --- plain: words straight from the document ---
    {"q": "What time do you open?",
     "a": "8am to 9pm Monday to Saturday. Closed Sunday."},
    {"q": "Do you accept cards?",
     "a": "Yes. Cash, UPI and all major cards. No cheques."},
    {"q": "How do I get the loyalty card?",
     "a": "It is free at the counter."},
    {"q": "When does fish arrive?",
     "a": "Tuesday and Friday mornings only."},
    {"q": "Is parking free?",
     "a": "Free for the first hour. Ten spaces at the rear."},

    # --- synonym: customer words, not document words ---
    {"q": "Can I return tomatoes?",
     "a": "No. Fresh items cannot be returned once they leave the shop."},
    {"q": "Can I pay by phone?",
     "a": "Yes, UPI is accepted."},
    {"q": "Do you bring it to my house?",
     "a": "Yes, within 5km. Send the list on WhatsApp before 4pm."},
    {"q": "Where do I leave my car?",
     "a": "Ten spaces at the rear. Free for the first hour."},
    {"q": "Is there a discount for a big order?",
     "a": "Above 10,000 rupees, contact the manager two days in advance."},

    # --- sloppy: typos, one word, no punctuation ---
    {"q": "sunday?",
     "a": "Closed on Sunday."},
    {"q": "delivry charge",
     "a": "Free above 500 rupees, otherwise 40 rupees."},
    {"q": "how manny points for discount",
     "a": "200 points gives a 100 rupee discount."},
    {"q": "open time saturday",
     "a": "8am to 9pm."},
    {"q": "wats the whatsapp no",
     "a": "98765 43210."},

    # --- no answer in the document: must refuse ---
    {"q": "Are you open on Diwali?",
     "a": "The document does not mention holidays."},
    {"q": "Do you sell alcohol?",
     "a": "The document does not mention alcohol."},
    {"q": "Do you have a pharmacy?",
     "a": "The document does not mention a pharmacy."},
    {"q": "What is your email address?",
     "a": "The document does not give an email address."},
    {"q": "Is there a student discount?",
     "a": "The document does not mention a student discount."},
]

print(len(TESTS), "test pairs")