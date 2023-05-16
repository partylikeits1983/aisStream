import csv
import json

def convert_json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Prepare the CSV file
    csv_data = []
    fieldnames = ['UserID', 'AIS Message', 'Latitude', 'Longitude', 'Time']

    for item in data:
        user_id = item['AIS Message']['UserID']
        csv_item = {
            'UserID': [user_id],  # UserID is now a list
            'AIS Message': json.dumps(item['AIS Message']),
            'Latitude': item['Latitude'],
            'Longitude': item['Longitude'],
            'Time': item['Time']
        }

        # Check if the UserID already exists in the CSV data
        duplicate = next((row for row in csv_data if row['UserID'] == user_id), None)
        if duplicate:
            duplicate['UserID'].append(user_id)  # Append the duplicate UserID to the list
        else:
            csv_data.append(csv_item)

    # Write the data to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

# Usage
json_file = 'ais_data.json'
csv_file = 'output.csv'
convert_json_to_csv(json_file, csv_file)
