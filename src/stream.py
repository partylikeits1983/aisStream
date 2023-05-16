import atexit
import asyncio
import json
import websockets

data_list = []  # List to store data dictionaries

# Load existing data from the JSON file
try:
    with open("ais_data.json", "r") as json_file:
        data_list = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    pass

def save_data():
    # Save the data as JSON
    with open("ais_data.json", "w") as json_file:
        json.dump(data_list, json_file, indent=4)
    print("Data saved to 'ais_data.json'")

atexit.register(save_data)  # This will still ensure data is saved when the script is stopped

async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "32864804aa79bc05381996a688d91dc259ea42e5", "BoundingBoxes": [[[-180, -90], [180, 90]]]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        messageNumber = 0
        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "ShipStaticData":
                ais_message = message['Message']['ShipStaticData']

                latitude = message['MetaData']['latitude']
                longitude = message['MetaData']['longitude']
                time = message['MetaData']['time_utc']

                data = {
                    "AIS Message": ais_message,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Time": time,
                }

                data_list.append(data)  # Append new data to the list

                if messageNumber % 50 == 0:
                    save_data()  # Save data after every entry

                messageNumber += 1

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())
