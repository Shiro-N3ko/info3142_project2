import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the EmailLog.txt file
#with open("EmailLog.txt", "r") as file:
with open("info3142_project2\EmailLog.txt", "r") as file:
    email_log = file.read()

# Split the log entries based on "<<End>>" tag
log_entries = email_log.split("<<End>>")

# Process each log entry
output_data = []

for entry in log_entries:
    doc = nlp(entry)

    #check if the doc is not empty
    if len(doc) > 0: 
        # Extract email address
        #email_address = doc[0].text.strip()

        # Extract entities and amounts
        emailAddress = None
        entities = set() #K:Changed from [] to a set()
        amounts = set() #K:Changed from [] to a set()

        for token in doc:
            # check if the email is there
            if token.like_email:
                emailAddress = token.text

        for ent in doc.ents:
            if ent.label_ == "ORG" or ent.label_ == "PRODUCT":
                entities.add(ent.text) #K: Chnaged from append to Add so that a batch of tokens is added at once 
            elif ent.label_ == "MONEY":
                amounts.add(ent.text)

        #fromat the amount as currency
        formatAmounts = "$" + " and ".join(amounts) if amounts else "" 
        formattedEntities = ", ".join(entities)

        #get the total of requests

        # Combine entities and amounts for output
        output_line = f"{emailAddress} : {formatAmounts} and {formattedEntities} " #{' and '.join(amounts)} to {' and '.join(entities)}"
        output_data.append(output_line)


# Write the output to a text file
with open("output_data.txt", "w") as output_file:
    for line in output_data:
        output_file.write(line + "\n")
