from datetime import datetime
from pymongo import MongoClient

# connection string (string de conexão) – ajuste depois para a EC2 do MongoDB
MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)
db = client["assignment9"]
logs_collection = db["interaction_logs"]


def log_action(action, ip=None, success=True, message=None):
    doc = {
        "timestamp": datetime.utcnow(),
        "action": action,          # ex: "auth", "list_devices", "show_interfaces"
        "device_ip": ip,
        "success": success,
        "message": message,
    }
    logs_collection.insert_one(doc)
