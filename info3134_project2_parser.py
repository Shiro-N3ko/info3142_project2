import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the EmailLog.txt file
with open("EmailLog.txt", "r") as file:
    email_log = file.read()

# Split the log entries based on "<<End>>" tag
log_entries = email_log.split("<<End>>")

# Process each log entry
output_data = []

for entry in log_entries:
    doc = nlp(entry)

    # Extract email address
    email_address = doc[0].text.strip()

    # Extract entities and amounts
    entities = []
    amounts = []
    for ent in doc.ents:
        if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
            entities.append(ent.text)
        elif ent.label_ == "MONEY":
            amounts.append(ent.text)

    # Combine entities and amounts for output
    output_line = f"{email_address} : {' and '.join(amounts)} to {' and '.join(entities)}"

    output_data.append(output_line)

# Write the output to a text file
with open("output_data.txt", "w") as output_file:
    for line in output_data:
        output_file.write(line + "\n")
