import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the EmailLog.txt file
with open("EmailLog.txt", "r") as file:
    email_log = file.read()

# Split the log entries based on "<<End>>" tag
log_entries = email_log.split("<<End>>")

# Process each log entry
output_data = {}

for entry in log_entries:
    doc = nlp(entry)

    # check if the doc is not empty
    if len(doc) > 0:
        # Extract email address
        emailAddress = None
        entities = set()
        amounts = []

        for token in doc:
            # check if the email is there
            if token.like_email:
                emailAddress = token.text

        current_amount = 0
        for ent in doc.ents:
            if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
                entities.add(ent.text)
            elif ent.label_ == "MONEY":
                # Handle the case where the amount is given in words
                amount_text = ent.text.replace("$", "").replace(",", "")
                if amount_text.isdigit():
                    amounts.append(float(amount_text))
                else:
                    # Convert words to numbers
                    amount_in_words = {'thousand': 1000, 'million': 1000000}
                    words = amount_text.split()
                    total_amount = 0
                    current_amount = 0
                    for word in words:
                        if word.isdigit():
                            current_amount = float(word)
                        elif word in amount_in_words:
                            current_amount *= amount_in_words[word]
                            total_amount += current_amount
                            current_amount = 0
                    if current_amount != 0:
                        total_amount += current_amount
                        current_amount = 0
                    amounts.append(total_amount)

        # format the amount as currency
        formatAmounts = " and ".join(["${:,.2f}".format(amount) for amount in amounts]) if amounts else ""
        formattedEntities = ", ".join(entities)

        # Combine entities and amounts for output
        if emailAddress:
            if emailAddress not in output_data:
                output_data[emailAddress] = {"amounts": [], "entities": set()}
            
            output_data[emailAddress]["amounts"].extend(amounts)
            output_data[emailAddress]["entities"].update(entities)

# Write the output to a text file
with open("output_data.txt", "w") as output_file:
    for email, data in output_data.items():
        total_amount = sum(data["amounts"])
        formattedAmount = "${:,.2f}".format(total_amount)
        formattedEntities = ", ".join(data["entities"])
        output_line = f"{email} : {formattedAmount} to {formattedEntities}"
        output_file.write(output_line + "\n")
