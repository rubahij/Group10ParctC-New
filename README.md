
# 🏥 מערכת לניהול מרפאת שיניים - 3DSMILE

## 📋 תיאור הפרויקט
הפרויקט הוא מערכת לניהול מרפאת שיניים הכוללת אפשרות ליצירת חשבון, כניסה למערכת, קביעת תורים, צפייה בהיסטוריית טיפולים ויצירת קשר עם המרפאה.

המערכת פותחה באמצעות Flask ומתחברת למסד הנתונים MongoDB באמצעות pymongo.

mongodb+srv://rubahij:rubahij123@cluster0.exn6i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
---

## 💾 טכנולוגיות עיקריות
- **Backend:** Flask, Flask-Session
- **Database:** MongoDB Atlas
- **Frontend:** HTML, CSS, JavaScript
- **Environment:** python-dotenv
- **Styling:** CSS מותאם אישית עם עיצוב מודרני

---

---

## 🗝️ **שימוש במערכת**
- **יצירת חשבון:** הזן את כל המידע הנדרש. אם האימייל כבר קיים במערכת, תוצג הודעת שגיאה.
- **כניסה למערכת:** היכנס עם האימייל והסיסמה שהזנת בעת ההרשמה.
- **קביעת תור:** בחר רופא, סוג טיפול, תאריך ושעה. לא ניתן לבחור תאריך שכבר עבר.
- **היסטוריית טיפולים:** הצג את רשימת התורים שנקבעו עם אפשרות לעדכן או לבטל תור.
- **יצירת קשר:** מלא את הטופס והודעתך תישלח למערכת במסד הנתונים.

---

## 💾 **MongoDB Collections**
- **patients:** מאחסן את פרטי המשתמשים (אימייל, סיסמה, שם פרטי, שם משפחה, גיל ומספר טלפון).
- **appointments:** מאחסן את פרטי התורים (אימייל המטופל, שם הרופא, סוג הטיפול, תאריך ושעה).
- **contactMessages:** מאחסן את הודעות יצירת הקשר שנשלחו מהמשתמשים.
- **doctors:** מאחסן את שמות הרופאים והתמחויותיהם.

---

## 🟢 **שאילתות CRUD שבוצעו**
- **Create:** הוספת משתמשים חדשים, קביעת תורים ושליחת הודעות יצירת קשר.
- **Read:** שליפת משתמש לפי אימייל, הצגת היסטוריית טיפולים והצגת כל הודעות יצירת הקשר.
- **Update:** עדכון פרטי תור קיים לפי ID.
- **Delete:** מחיקת תור לפי ID ומחיקת הודעות יצירת קשר.

---

## 🌐 **שאילתה מורכבת (לצורך ניקוד נוסף)**
- שליפת מטופלים עם מספר תורים מעל סף מסוים בחודש מסוים:  
  שאילתה זו משתמשת ב-`$lookup` ו-`$group` כדי לאחד נתונים מ-`patients` ו-`appointments`, ומציגה רק את המטופלים שקבעו מספר תורים מעל הסף שנקבע.

---

## 🛡️ **ולידציה ובדיקות מערכת**
- ✅ אימייל שכבר קיים במערכת מציג הודעת שגיאה אדומה בטופס ההרשמה.
- ✅ לא ניתן לבחור תאריך שכבר עבר בטופס קביעת תור.
- ✅ מספר טלפון חייב להתחיל ב-0 ולהכיל 10 ספרות.
- ✅ סיסמה חייבת להיות לפחות 6 תווים.
- ✅ גיל חייב להיות בטווח של 1 עד 120.

---

## 🖥️ **הדפסה ב-Console (analyzeDB.py)**
- כל ה-Collections מוצגים ב-Console עם שמות השדות שלהם.
- הודעה מיוחדת מודפסת אם הקולקשן ריק.
- אם יש שדה חסר במסמך כלשהו, יודפס `"N/A"` במקום ערך חסר.
- כל השאילתות מודפסות ב-Console יחד עם מספר השורות שנמצאו או התעדכנו.

---

## ✅ **בדיקות סופיות להשלמת הפרויקט**
- בדוק שכל הטפסים עובדים ומתחברים ל-`App.py`:
  - טופס יצירת חשבון לא יאפשר שימוש באימייל קיים.
  - טופס קביעת תור לא מאפשר תאריך עבר.
  - טופס יצירת קשר מוסיף הודעה למסד הנתונים.

- ודא שכל פונקציות CRUD מופעלות לפחות פעם אחת:
  - **הוספה (Create):** יצירת משתמש חדש והוספת תור.
  - **שליפה (Read):** הצגת פרטי משתמש והצגת היסטוריית טיפולים.
  - **עדכון (Update):** עדכון תור קיים במסך ההיסטוריה.
  - **מחיקה (Delete):** מחיקת תור קיים ומחיקת הודעה מקולקשן `contactMessages`.

---

![לוגו המרפאה](static/images/home-banner.jpeg)

## 🖼️ צילומי מסכים מהמערכת

---

### 🏡 דף הבית
![home-page](https://github.com/user-attachments/assets/23a240e6-d93d-43f9-a272-931d34dcba40)

![דף הבית](static/images/home-page.jpeg)
*📸 דוגמה: דף הבית עם לוגו המרפאה וכפתורי ניווט מרכזיים.*



### 📝 דף יצירת חשבון חדש
![create-account-page](https://github.com/user-attachments/assets/d2d80045-12f4-483e-a921-cff67cc238d2)

![דף יצירת חשבון חדש](static/images/create-account-page.jpeg)
*📸 דוגמה: טופס יצירת חשבון עם בדיקת אימייל כפול וולידציה לשדות.*


---

### 🔒 דף כניסה למערכת
![login-page2](https://github.com/user-attachments/assets/62fcdc90-0d2b-465e-a0dc-ee0075a8d9bb)

![דף כניסה למערכת](static/images/login-page2.jpeg)
*📸 דוגמה: טופס כניסה עם אימייל וסיסמה והפניה ליצירת חשבון חדש.*

---

### 👤 דף האזור האישי
![personal-page](https://github.com/user-attachments/assets/b68e7bd1-d1dc-443a-85b9-530f19f344c8)

![דף האזור האישי](static/images/personal-page.jpeg)
*📸 דוגמה: דף האזור האישי עם אפשרות לצפות בהיסטוריית טיפולים או לקבוע תור חדש.*

---

### 📅 דף קביעת תור
![booking-page](https://github.com/user-attachments/assets/4cfa7263-0507-4370-8372-2ed3a46e9ed0)

![דף קביעת תור](static/images/booking-page.jpeg)
*📸 דוגמה: טופס קביעת תור עם בחירת רופא, סוג טיפול, תאריך ושעה.*

---

### 🗂️ דף היסטוריית טיפולים
![my-booking-page](https://github.com/user-attachments/assets/5dadf3d4-3cdf-41fd-b2d2-e0dfe18cbe91)

![דף היסטוריית טיפולים](static/images/my-booking-page.jpeg)
*📸 דוגמה: רשימת התורים שנקבעו עם אפשרות לעדכן או לבטל תור.*

---

### 📬 דף יצירת קשר
![contact-page](https://github.com/user-attachments/assets/fdc773c1-9865-4012-aab8-fbd6600435de)

![דף יצירת קשר](static/images/contact-page.jpeg)
*📸 דוגמה: טופס יצירת קשר עם ולידציה לשם, טלפון ודוא"ל.*

---

### 🧑‍⚕️ דף קצת עלינו
![our-doctors-page](https://github.com/user-attachments/assets/5597be96-6cb3-4339-9acc-fb138bed92f3)

![דף קצת עלינו](static/images/our-doctors-page.jpeg)
*📸 דוגמה: דף מידע עם פרטי הרופאים והתמחויותיהם.*

---
