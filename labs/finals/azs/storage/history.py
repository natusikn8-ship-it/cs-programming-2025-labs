import json
import sys
from typing import List
from datetime import datetime
from models.transaction import Transaction

# Тут почти полностью нейронкой сделано, впадлу было, но вроде норм
class HistoryManager:
    def __init__(self, data_dir: str = "data/"):
        self.filepath = data_dir + "history.json"
        try: 
            with open(self.filepath, "r", encoding="utf-8") as f:
                pass
        except FileNotFoundError as e:
            print("Не обнаружены данные. Перед первым запуском запустить start_data.py")
            print(e)
            sys.exit()
    
    def add_transaction(self, transaction: Transaction):
        history = self.load_history()
        history.append(transaction)
        self.save_history(history)
    
    def load_history(self) -> List[Transaction]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Transaction.get_info(item) for item in data]
    
    def save_history(self, history: List[Transaction]):
        data = [t.info() for t in history]
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_recent(self, count: int = 10) -> List[Transaction]:
        history = self.load_history()
        return history[-count:]
    
    def filter_by_type(self, operation_type: str) -> List[Transaction]:
        history = self.load_history()
        return [t for t in history if t.operation_type == operation_type]
