from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# טען את משתני הסביבה מהקובץ .env
load_dotenv()

# קבלת ה-URI מה-.env
uri = os.environ.get('DB_URI')
print("🔗 URI:", uri)

try:
    # יצירת חיבור ל-MongoDB
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("✅ חיבור ל-MongoDB הצליח!")
except Exception as e:
    print("❌ חיבור ל-MongoDB נכשל:", e)
