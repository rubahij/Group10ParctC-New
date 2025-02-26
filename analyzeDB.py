from db_connector1 import mydatabase

def analyze_database():
    """מדפיס את כל ה-collections ואת תוכנם עם שמות השדות"""
    collections = mydatabase.list_collection_names()

    if not collections:
        print("⚠️ אין collections במסד הנתונים.")
        return

    for collection_name in collections:
        print(f"\n📂 Collection: {collection_name}")
        collection = mydatabase[collection_name]
        documents = list(collection.find({}))

        if not documents:
            print("אין מסמכים ב-collection הזה.")
            continue

        # הצגת שמות השדות בטבלה מסודרת
        keys = documents[0].keys()
        print("=" * 80)
        print(" | ".join(keys))
        print("=" * 80)

        # הדפסת כל המסמכים בצורה מסודרת עם בדיקת מפתחות חסרים
        for doc in documents:
            values = [str(doc.get(key, "N/A")) for key in keys]  # ✅ שימוש ב-.get() למניעת שגיאות
            print(" | ".join(values))
        print("=" * 80)


if __name__ == "__main__":
    analyze_database()
