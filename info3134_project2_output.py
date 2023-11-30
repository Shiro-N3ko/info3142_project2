# project2_output.py

# Read the stored text file
with open("output_data.txt", "r") as output_file:
    output_data = output_file.read().split("\n")

# Process and print the console output
total_amount = 0

for entry in output_data:
    if entry:
        print(entry)
        total_amount += float(entry.split(":")[1].split()[0].replace("$", "").replace(",", ""))

print(f"\nTotal Requests: ${'{:,.2f}'.format(total_amount)}")
