import csv
import os
from datetime import datetime

class LOGGER:
    def __init__(self, filename):
        self.filename = filename
        self.headers = ["clientID", "timestamp", "transmitter", "topic", "message"]
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def add_record(self, clientID, transmitter, topic, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([clientID, timestamp, transmitter, topic, message])

    def get_all_records(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def filter_records(self, **kwargs):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader if all(row[key] == str(value) for key, value in kwargs.items())]
