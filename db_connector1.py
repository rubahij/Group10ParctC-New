import os
import pymongo
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from setting import DB

# ✅ טעינת משתני הסביבה מקובץ .env
load_dotenv()

# ✅ חיבור ל-MongoDB
uri = os.environ.get('DB_URI')
cluster = MongoClient(uri, server_api=ServerApi('1'))

# ✅ בחירת מסד הנתונים וה-collections
mydatabase = cluster['clinicDB']


# --- מטופלים ---
patients = mydatabase['patients']

# --- רופאים ---
doctors = mydatabase['doctors']

# --- תורים ---
appointments = mydatabase['appointments']
# --- הודעות יצירת קשר ---
contactMessages = mydatabase['contactMessages']


# ✅ הוספת נתוני דוגמה לרופאים אם הם לא קיימים
initial_doctors = [
    {"doctor_id": 1, "name": "ד\"ר יוסי כהן", "specialty": "שיננית"},
    {"doctor_id": 2, "name": "ד\"ר מרים לוי", "specialty": "כירורגיית פה ולסת"},
    {"doctor_id": 3, "name": "ד\"ר דני אלון", "specialty": "אורתודונטיה"},
]

for doctor in initial_doctors:
    if not doctors.find_one({"doctor_id": doctor["doctor_id"]}):
        doctors.insert_one(doctor)


# ✅ פונקציות CRUD התואמות ל-`app.py`

# --- USERS (מטופלים) ---
def insert_user(user_dict):
    """הוספת משתמש חדש (מטופל) לאוסף patients ב-MongoDB"""
    print("💾 מנסה להוסיף את המשתמש למסד הנתונים:", user_dict)
    result = patients.insert_one(user_dict)
    print("✅ Insert successful - ID:", result.inserted_id)
    return result



def get_user_by_email(email):
    """שליפת משתמש לפי אימייל מ-MongoDB"""
    from setting import DB
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi

    cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
    mydatabase = cluster[DB['database_name']]
    patients = mydatabase[DB['collections']['patients']]

    print(f"🔍 מחפש משתמש עם אימייל: {email}")
    user = patients.find_one({"email": email})
    print(f"🟢 תוצאת חיפוש: {user}")
    return user



# --- APPOINTMENTS (תורים) ---
def insert_appointment(appointment_dict):
    """הוספת תור חדש לאוסף appointments ב-MongoDB"""
    print("🔗 ניסיון חיבור ל-MongoDB")
    try:
        cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
        print("✅ חיבור ל-MongoDB הצליח")

        mydatabase = cluster[DB['database_name']]
        appointments = mydatabase[DB['collections']['appointments']]

        print("💾 ניסיון שמירת התור במסד הנתונים:", appointment_dict)
        result = appointments.insert_one(appointment_dict)

        print("✅ Insert successful - ID:", result.inserted_id)
        return result
    except Exception as e:
        print("❌ Insert failed:", e)
        raise


def get_appointments_by_user(email):
    """שליפת כל התורים של משתמש לפי אימייל"""
    try:
        cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
        db = cluster[DB['database_name']]
        appointments = db[DB['collections']['appointments']]
        return list(appointments.find({"user_email": email}))
    except Exception as e:
        print("❌ שגיאה בעת שליפת התורים:", str(e))
        return []

def update_appointment(appointment_id, update_dict):
    """עדכון תור לפי ID"""
    try:
        cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
        db = cluster[DB['database_name']]
        appointments = db[DB['collections']['appointments']]
        result = appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": update_dict})
        return result.modified_count > 0
    except Exception as e:
        print("❌ שגיאה בעת עדכון התור:", str(e))
        return False

def cancel_appointment(appointment_id):
    """ביטול תור לפי ID"""
    try:
        cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
        db = cluster[DB['database_name']]
        appointments = db[DB['collections']['appointments']]
        result = appointments.delete_one({"_id": ObjectId(appointment_id)})  # מחיקת התור ולא רק עדכון הסטטוס
        return result.deleted_count > 0
    except Exception as e:
        print("❌ שגיאה בעת ביטול התור:", str(e))
        return False

from datetime import datetime

def get_future_appointments_by_user(email):
    """שליפת כל התורים העתידיים של משתמש לפי אימייל"""
    today = datetime.now().strftime('%Y-%m-%d')
    return list(appointments.find({"user_email": email, "appointment_date": {"$gte": today}}).sort([("appointment_date", 1), ("appointment_time", 1)]))

# --- CONTACT MESSAGES (הודעות יצירת קשר) ---
def insert_contact_message(message_dict):
        """הוספת הודעת יצירת קשר לאוסף contactMessages ב-MongoDB"""
        from setting import DB
        from pymongo.mongo_client import MongoClient
        from pymongo.server_api import ServerApi

        cluster = MongoClient(DB['uri'], server_api=ServerApi('1'))
        mydatabase = cluster[DB['database_name']]
        contactMessages = mydatabase[DB['collections']['contact_messages']]

        print("💾 מנסה להוסיף את ההודעה למסד הנתונים:", message_dict)
        try:
            result = contactMessages.insert_one(message_dict)
            print("✅ Insert successful - ID:", result.inserted_id)
            return result
        except Exception as e:
            print("❌ Insert failed:", e)
            raise


def get_all_contact_messages():
    """שליפת כל הודעות יצירת הקשר"""
    return list(contactMessages.find())


def delete_contact_message(message_id):
    """מחיקת הודעת יצירת קשר לפי ID"""
    return contactMessages.delete_one({"_id": message_id})


# ✅ יצירת סיסמה זמנית לניהול מערכת (מתעדכנת כל 30 דקות)
def generate_temp_password():
    current_time = datetime.now()
    time_key = f"{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute // 30}"
    hashed_password = hashlib.sha256(time_key.encode()).hexdigest()[:6]
    return hashed_password
# בדיקת פונקציות CRUD
def test_crud_operations():
    """בודק שכל הפעולות CRUD מבוצעות בהצלחה"""

    # CREATE - הוספת מטופל חדש
    patient_email = "test_patient@example.com"
    insert_user({
        "email": patient_email,
        "password": "password123",
        "name": "יוסי לוי",
        "phone": "0501234567",
        "age": 30
    })
    print("✅ CREATE - הוספת מטופל חדש: הצליח")

    # READ - שליפת המטופל לפי אימייל
    patient = get_user_by_email(patient_email)
    if patient:
        print("✅ READ - שליפת מטופל לפי אימייל: הצליח")
    else:
        print("❌ READ - שליפת מטופל לפי אימייל: נכשל")

    # UPDATE - עדכון מספר הטלפון של המטופל
    update_result = patients.update_one({"email": patient_email}, {"$set": {"phone": "0507654321"}})
    if update_result.modified_count > 0:
        print("✅ UPDATE - עדכון מספר הטלפון של המטופל: הצליח")
    else:
        print("❌ UPDATE - עדכון מספר הטלפון של המטופל: נכשל")

    # DELETE - מחיקת המטופל
    delete_result = patients.delete_one({"email": patient_email})
    if delete_result.deleted_count > 0:
        print("✅ DELETE - מחיקת המטופל: הצליח")
    else:
        print("❌ DELETE - מחיקת המטופל: נכשל")

def print_all_appointments():
    """הדפסת כל התורים בקולקשן לצורך בדיקה"""
    for appointment in appointments.find():
        print(appointment)

def get_frequent_patients(month, min_appointments):
            """שאילתה מורכבת: שליפת מטופלים עם מספר תורים מעל סף מסוים בחודש נתון"""
            pipeline = [
                {
                    "$addFields": {
                        "month": {"$month": {"$dateFromString": {"dateString": "$appointment_date"}}}
                        # חילוץ החודש מתאריך התור
                    }
                },
                {
                    "$match": {
                        "month": month  # סינון לפי חודש ספציפי
                    }
                },
                {
                    "$group": {
                        "_id": "$user_email",
                        "total_appointments": {"$sum": 1}  # ספירת התורים של כל מטופל באותו חודש
                    }
                },
                {
                    "$match": {
                        "total_appointments": {"$gte": min_appointments}  # סינון לפי סף מינימלי של תורים
                    }
                },
                {
                    "$lookup": {
                        "from": "patients",
                        "localField": "_id",
                        "foreignField": "email",
                        "as": "patient_details"
                    }
                },
                {
                    "$unwind": "$patient_details"
                },
                {
                    "$project": {
                        "email": "$_id",
                        "total_appointments": 1,
                        "name": {"$concat": ["$patient_details.firstName", " ", "$patient_details.lastName"]}
                        # שילוב של שם פרטי ומשפחה
                    }
                },
                {
                    "$sort": {"total_appointments": -1}  # סידור לפי מספר התורים בסדר יורד
                }
            ]

            result = list(appointments.aggregate(pipeline))
            return result

# הפעלה כאשר הקובץ מורץ ישירות
if __name__ == "__main__":
    test_crud_operations()
    # שליפת מטופלים עם יותר מ-3 תורים בחודש ינואר (1)
    result = get_frequent_patients(month=1, min_appointments=3)

    if result:
        for patient in result:
            print(f"👤 מטופל: {patient['name']} ({patient['email']})")
            print(f"📅 מספר תורים בחודש: {patient['total_appointments']}")
            print("-" * 50)
    else:
        print("⚠️ לא נמצאו מטופלים שעומדים בתנאי הסינון.")



# ✅ הדפסת הסיסמה הזמנית עבור המנהל (לבדיקות בלבד)
if __name__ == "__main__":
    print("📌 סיסמה זמנית למערכת הניהול:", generate_temp_password())
