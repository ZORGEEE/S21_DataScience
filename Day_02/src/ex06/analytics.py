import os
from random import randint
import logging
import requests
import json

logging.basicConfig(
    filename='analytics.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info(f"Initialized Research with file path: {file_path}")

    def file_reader(self, has_header=True):
        logging.info(f"Reading file {self.file_path} with header: {has_header}")
        if not os.path.exists(self.file_path):
            logging.error(f"File not found: {self.file_path}")
            raise FileNotFoundError("File not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        data = []
        start_index = 1 if has_header else 0
        
        for line in lines[start_index:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            
            first, second = int(parts[0]), int(parts[1])
            
            data.append([first, second])
        
        logging.info(f"Successfully read {len(data)} observations from file")
        return data
    
    def send_notifications(self, success):
        from config import telegram_bot_token, telegram_chat_id
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        message = "The report has been successfully created" if success else "The report hasn’t been created due to an error"
        payload = {
            'chat_id': telegram_chat_id,
            'text': message
        }
        try:
            response = requests.post(url, data=payload)
            logging.info(f"Telegram notification sent: {message}")
            return response.json()
        except Exception as e:
            logging.error(f"Failed to send Telegram notification: {e}")
            return None
        

class Calculations:
    def __init__(self, data):
        self.data = data
        logging.info(f"Initialized Calculations with {len(data)} observations")

    def counts(self):
        logging.info("Calculating counts of heads and tails")
        heads = sum(1 for item in self.data if item[0] == 1)
        tails = sum(1 for item in self.data if item[1] == 1)
        logging.info(f"Counts: heads={heads}, tails={tails}")
        return heads, tails
    
    def fractions(self, heads, tails):
        logging.info("Calculating fractions of heads and tails")
        total = heads + tails
        if total == 0:
            logging.error("No observations to calculate fractions")
            return 0.0, 0.0
        head_percent = (heads / total) * 100
        tail_percent = (tails / total) * 100
        logging.info(f"Fractions: heads={head_percent:.2f}%, tails={tail_percent:.2f}%")
        return head_percent, tail_percent

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        logging.info(f"Generating {num_predictions} random predictions")
        predictions = []
        for _ in range(num_predictions):
            if randint(0, 1) == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        logging.info(f"Generated predictions: {predictions}")
        return predictions
    
    def predict_last(self):
        logging.info("Retrieving the last observation")
        return self.data[-1]
    
    def save_file(self, data, filename, extension):
        with open(f"{filename}.{extension}", 'w') as file:
            file.write(str(data))
        logging.info(f"Data successfully saved to {filename}.{extension}")