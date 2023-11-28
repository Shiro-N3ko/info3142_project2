# Read the stored text file
with open("TaggedEmailLog.txt", "r") as output_file:
    output_data = output_file.read().split("<<End>>")

# Process and print the console output
total_amount = 0

for entry in output_data:
    lines = entry.strip().split('\n')
    if len(lines) < 2:
        continue
    
    email = lines[0].strip()
    print(email)
    
    # Extract amounts
    amounts = [int(amount.replace("$", "").replace(",", "")) for amount in lines[1].split() if amount[0] == "$"]
    total_amount += sum(amounts)
    
    # Print the email content
    content = '\n'.join(lines[2:])
    print(content)

    print("<<End>>\n")

print(f"Total Requests: ${'{:,.2f}'.format(total_amount)}")
