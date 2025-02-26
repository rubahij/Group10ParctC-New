from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db_connector1 import insert_user, get_user_by_email, insert_appointment, get_appointments_by_user, \
    insert_contact_message, cancel_appointment, update_appointment
from dotenv import load_dotenv
import os
import hashlib
from datetime import datetime, date

# טעינת משתני סביבה מקובץ .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')


# ==================== 🏠 דף הבית ====================
@app.route('/')
def home():
    return render_template('HOME.html')


# ==================== 🔒 התחברות ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """בדיקת התחברות המשתמש ושמירה ב-Session"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if user and user.get('password') == password:
            session['logged_in'] = True
            session['user_email'] = email
            print("✅ אימייל נשמר ב-Session:", email)
            return redirect(url_for('personal_page'))  # ← מעביר לדף האזור האישי
        else:
            print("❌ פרטי התחברות שגויים")
            return render_template('LOGIN.html', error="פרטי התחברות שגויים")

    return render_template('LOGIN.html')

# ==================== 📝 יצירת חשבון ====================
@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        age = int(request.form['age'])
        phone = request.form['phone']

        # ✅ בדיקה אם האימייל כבר קיים במערכת
        if get_user_by_email(email):
            return render_template('CreateAccount.html', error="האימייל הזה כבר קיים במערכת. נסה להתחבר או השתמש באימייל אחר.")

        # שמירת המשתמש אם האימייל לא קיים
        insert_user({
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "age": age,
            "phone": phone
        })

        return redirect(url_for('login'))

    return render_template('CreateAccount.html')



# ==================== 📞 יצירת קשר ====================
@app.route('/callus', methods=['GET', 'POST'])
def callus():
    """שומר את הודעת יצירת הקשר באוסף contactMessages ב-MongoDB"""
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')

        # בדיקה שכל השדות מולאו
        if not all([name, phone, email, message]):
            flash('יש למלא את כל השדות', 'error')
            return redirect(url_for('callus'))

        # שמירת ההודעה במסד הנתונים
        try:
            insert_contact_message({
                "name": name,
                "phone": phone,
                "email": email,
                "message": message
            })
            flash('ההודעה נשלחה בהצלחה!', 'success')
            print("✅ ההודעה נשמרה במסד הנתונים")
            return redirect(url_for('home'))
        except Exception as e:
            flash('שגיאה בעת שליחת ההודעה', 'error')
            print(f"❌ שגיאה בעת שמירת ההודעה: {str(e)}")

    return render_template('CALLUS.html')



# ==================== 🧑‍⚕️ צוות הרופאים ====================
@app.route('/ourdoctors')
def our_doctors():
    return render_template('ourDOCTORS.html')


# ==================== 🗂 אזור אישי ====================
@app.route('/personalpage')
def personal_page():
    """מציג את האזור האישי של המשתמש"""
    if not session.get('logged_in'):
        print("🔒 המשתמש לא מחובר")
        return redirect(url_for('login'))

    user_email = session.get('user_email')
    return render_template('PersonalPage.html', user_email=user_email)

# ==================== 📅 קביעת תור ====================
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """שומר את פרטי קביעת התור באוסף appointments ב-MongoDB"""
    if not session.get('logged_in'):
        print("🔒 המשתמש לא מחובר")
        return redirect(url_for('login'))

    if request.method == 'POST':
        doctor_name = request.form.get('doctorName')
        treatment_type = request.form.get('treatmentType')
        appointment_date = request.form.get('appointmentDate')
        appointment_time = request.form.get('appointmentTime')
        user_email = session.get('user_email')  # ← וודא שזה קיים

        print("📥 נתונים שהתקבלו מהטופס:")
        print(f"User Email: {user_email}, Doctor Name: {doctor_name}, Treatment Type: {treatment_type}, Date: {appointment_date}, Time: {appointment_time}")

        if not all([user_email, doctor_name, treatment_type, appointment_date, appointment_time]):
            print("❌ אחד השדות ריק")
            return render_template('BOOKING.html', error="יש למלא את כל השדות")

        try:
            result = insert_appointment({
                "user_email": user_email,
                "doctor_name": doctor_name,
                "treatment_type": treatment_type,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time
            })
            print("✅ התור נשמר בהצלחה:", result.inserted_id)
            return render_template('BOOKING.html', success="התור נקבע בהצלחה!")
        except Exception as e:
            print("❌ שגיאה בעת שמירת התור:", str(e))
            return render_template('BOOKING.html', error="שגיאה בעת קביעת התור")

    return render_template('BOOKING.html')

# ==================== 🗓 היסטוריית טיפולים ====================
@app.route('/mybooking', methods=['GET'])
def my_booking():
    """מציג את כל התורים של המשתמש עם אפשרות עדכון או ביטול תורים עתידיים"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_email = session.get('user_email')
    appointments = get_appointments_by_user(user_email)

    future_appointments = [a for a in appointments if a['appointment_date'] >= str(date.today())]
    past_appointments = [a for a in appointments if a['appointment_date'] < str(date.today())]

    return render_template('MYBOOKING.html', future_appointments=future_appointments, past_appointments=past_appointments)


@app.route('/update_appointment/<appointment_id>', methods=['POST'])
def update_appointment_route(appointment_id):
    """עדכון תור לפי ה-ID שלו"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    update_dict = {
        "appointment_date": request.form.get('appointmentDate'),
        "appointment_time": request.form.get('appointmentTime')
    }
    success = update_appointment(appointment_id, update_dict)
    return redirect(url_for('my_booking', success="התור עודכן בהצלחה!" if success else "שגיאה בעת עדכון התור"))


@app.route('/cancel_appointment/<appointment_id>', methods=['POST'])
def cancel_appointment_route(appointment_id):
    """ביטול תור לפי ה-ID שלו"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    success = cancel_appointment(appointment_id)
    return redirect(url_for('my_booking', success="התור בוטל בהצלחה!" if success else "שגיאה בעת ביטול התור"))

# ==================== 🚪 התנתקות ====================
@app.route('/logout')
def logout():
    session.clear()
    flash('התנתקת בהצלחה!', 'success')
    return redirect(url_for('home'))


# ==================== 🟢 בדיקת חיבור ====================
@app.route('/health')
def health_check():
    return "השרת פועל בהצלחה", 200


# ==================== 🛡️ סיסמה זמנית לניהול מערכת ====================
def generate_temp_password():
    """יצירת סיסמה זמנית המתעדכנת כל 30 דקות"""
    current_time = datetime.now()
    time_key = f"{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute // 30}"
    hashed_password = hashlib.sha256(time_key.encode()).hexdigest()[:6]
    return hashed_password


@app.route('/admin/temp_password')
def admin_temp_password():
    """הצגת סיסמה זמנית למנהל המערכת"""
    temp_password = generate_temp_password()
    return jsonify({"Temporary Password": temp_password})


# ==================== 📂 ניתוח מסד הנתונים ====================
from db_connector1 import mydatabase

@app.route('/admin/analyze_db')
def analyze_database():
    """הצגת תוכן כל ה-collections במסד הנתונים"""
    collections = mydatabase.list_collection_names()
    result = {}

    if not collections:
        return jsonify({"message": "אין collections במסד הנתונים."})

    for collection_name in collections:
        collection = mydatabase[collection_name]
        documents = list(collection.find({}))

        if documents:
            keys = documents[0].keys()
            collection_data = []
            for doc in documents:
                collection_data.append({key: str(doc[key]) for key in keys})
            result[collection_name] = collection_data
        else:
            result[collection_name] = "אין מסמכים ב-collection הזה."

    return jsonify(result)


# ================


# ==================== ✅ הפעלת השרת ====================
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
