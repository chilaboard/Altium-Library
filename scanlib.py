import os
import csv
import re

# === CONFIGURATION ===
input_folder = "AltiumSCHLIB"          # Change this to your folder path
output_csv = "component_list.csv"

# === REGEX FOR CASE-INSENSITIVE COMPONENT EXTRACTION ===
component_pattern = re.compile(
    r"\|LibRef(?P<num>\d+)=([^|]+)\|CompDescr(?P=num)=([^|]+)\|PartCount(?P=num)=\d+",
    re.IGNORECASE
)

# === SETUP ===
global_index = 1  # Counter for 'num' column

with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['num', 'lib name', 'part', 'desc'])

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".schlib"):
            file_path = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")

            try:
                with open(file_path, 'rb') as f:
                    binary_content = f.read()

                text_content = binary_content.decode('latin1', errors='ignore')
                

                components = component_pattern.findall(text_content)
                if not components:
                    print(f"No components found in {filename}")

                for _, part, desc in components:
                    writer.writerow([global_index, filename, part.strip(), desc.strip()])
                    global_index += 1

            except Exception as e:
                print(f"Error processing {filename}: {e}")
