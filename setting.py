import os
from dotenv import load_dotenv

# ✅ טעינת משתני הסביבה מקובץ .env
load_dotenv()


# ==================== 🔒 Flask Settings ====================
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ==================== 💾 MongoDB Settings ====================
DB = {
    'uri': os.environ.get('DB_URI'),
    'database_name': os.environ.get('DB_NAME', 'clinicDB'),
    'collections': {
        'patients': os.environ.get('DB_COLLECTION_PATIENTS', 'patients'),
        'doctors': os.environ.get('DB_COLLECTION_DOCTORS', 'doctors'),
        'appointments': os.environ.get('DB_COLLECTION_APPOINTMENTS', 'appointments'),
        'contact_messages': os.environ.get('DB_COLLECTION_CONTACT_MESSAGES', 'contactMessages')
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

# ==================== 🕒 Admin Settings ====================
TEMP_PASSWORD_INTERVAL = int(os.environ.get('TEMP_PASSWORD_INTERVAL', 30))

# ✅ הדפסות Debug כדי לבדוק שהערכים נטענים נכון
if __name__ == "__main__":
    print("✅ Flask Settings:")
    print(f"SECRET_KEY: {SECRET_KEY}")
    print(f"FLASK_ENV: {FLASK_ENV}")
    print(f"DEBUG: {DEBUG}")

    print("\n💾 MongoDB Settings:")
    print(f"URI: {DB['uri']}")
    print(f"Database Name: {DB['database_name']}")
    print("Collections:", DB['collections'])

    print("\n🕒 Admin Settings:")
    print(f"TEMP_PASSWORD_INTERVAL: {TEMP_PASSWORD_INTERVAL} דקות")
