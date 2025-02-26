// פונקציה לניווט בין עמודים
function navigateTo(page) {
    switch (page) {
        case 'החשבון שלי':
            alert("מעבר לעמוד החשבון שלי.");
            break;
        case 'יצירת קשר':
            alert("מעבר לעמוד יצירת קשר.");
            break;
        case 'קצת עלינו':
            alert("מעבר לעמוד קצת עלינו.");
            break;
        case 'עקבו אחרינו':
            alert("מעבר לעמוד עקבו אחרינו.");
            break;
        default:
            alert("העמוד המבוקש אינו קיים.");
    }
}

// מאזין לאירוע שליחה של טופס יצירת חשבון
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('signupForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirmPassword').value.trim();

        if (!name || !email || !password || !confirmPassword) {
            alert("נא למלא את כל השדות.");
            return;
        }

        if (!validateEmail(email)) {
            alert("נא להזין כתובת דואר אלקטרוני תקינה.");
            return;
        }

        if (password !== confirmPassword) {
            alert("הסיסמאות אינן תואמות.");
            return;
        }

        if (password.length < 6) {
            alert("הסיסמה חייבת להיות לפחות 6 תווים.");
            return;
        }

        alert(`ברוך הבא, ${name}! החשבון נוצר בהצלחה.`);
    });
});

// פונקציה לבדיקת אימייל תקין
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// מאזין לשליחת טופס כניסה
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!email || !password) {
            alert("נא למלא את כל השדות.");
            return;
        }

        alert("התחברת בהצלחה!");
        window.location.href = "/personalpage"; // מעבר לאיזור אישי
    });
});

// טופס קביעת תור
document.getElementById('appointmentForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const doctorName = document.getElementById('doctorName').value;
    const treatmentType = document.getElementById('treatmentType').value;
    const appointmentDate = document.getElementById('appointmentDate').value;
    const appointmentTime = document.getElementById('appointmentTime').value;

    if (!doctorName || !treatmentType || !appointmentDate || !appointmentTime) {
        alert("נא למלא את כל השדות.");
        return;
    }

    alert(`התור נקבע בהצלחה:
    רופא: ${doctorName}
    סוג טיפול: ${treatmentType}
    תאריך: ${appointmentDate}
    שעה: ${appointmentTime}`);
});

// הצגת טיפולים
document.addEventListener('DOMContentLoaded', function () {
    const futureTreatments = [
        { id: 1, doctor: "גוסון", type: "ניקוי שיניים", date: "2025-01-15", time: "10:00" },
        { id: 2, doctor: "יאסמין", type: "הלבנת שיניים", date: "2025-01-14", time: "09:00" }
    ];

    const pastTreatments = [
        { id: 3, doctor: "סנדס", type: "יישור שיניים", date: "2024-12-20", time: "14:00" }
    ];

    const futureList = document.getElementById("futureTreatments");
    const pastList = document.getElementById("pastTreatments");

    futureTreatments.forEach((treatment) => {
        const listItem = createTreatmentItem(treatment, "future");
        futureList.appendChild(listItem);
        if (isTreatmentClose(treatment.date)) {
            alert(`לתשומת ליבך, התור עם ד"ר ${treatment.doctor} ב-${treatment.date} בשעה ${treatment.time} מתקרב.`);
        }
    });

    pastTreatments.forEach((treatment) => {
        const listItem = createTreatmentItem(treatment, "past");
        pastList.appendChild(listItem);
    });
});

// יצירת פריט טיפול
function createTreatmentItem(treatment, type) {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
        <span>ד"ר ${treatment.doctor}</span>
        <span>${treatment.type}</span>
        <span>${treatment.date}, ${treatment.time}</span>
    `;

    if (type === "future") {
        const updateBtn = document.createElement("button");
        updateBtn.textContent = "עדכון";
        updateBtn.className = "update-btn";
        updateBtn.onclick = () => openModal(treatment.id);

        const cancelBtn = document.createElement("button");
        cancelBtn.textContent = "ביטול";
        cancelBtn.className = "cancel-btn";
        cancelBtn.onclick = () => cancelTreatment(treatment.id);

        listItem.appendChild(updateBtn);
        listItem.appendChild(cancelBtn);
    }

    return listItem;
}

// בדיקת קרבה לתור
function isTreatmentClose(date) {
    const currentDate = new Date();
    const treatmentDate = new Date(date);
    const diffInTime = treatmentDate.getTime() - currentDate.getTime();
    const diffInDays = diffInTime / (1000 * 3600 * 24);
    return diffInDays <= 3 && diffInDays >= 0;
}

// הצגת מודל לעדכון טיפול
function openModal(id) {
    const modal = document.getElementById("updateModal");
    modal.classList.remove("hidden");

    document.getElementById("updateForm").onsubmit = function (e) {
        e.preventDefault();
        const newDate = document.getElementById("updateDate").value;
        const newTime = document.getElementById("updateTime").value;

        if (newDate && newTime) {
            alert(`התור עודכן לתאריך ${newDate} בשעה ${newTime}.`);
            closeModal();
        }
    };
}

// סגירת המודל
function closeModal() {
    const modal = document.getElementById("updateModal");
    modal.classList.add("hidden");
}

// ביטול טיפול
function cancelTreatment(id) {
    const listItem = document.querySelector(`#futureTreatments li:nth-child(${id})`);
    if (confirm("האם אתה בטוח שברצונך לבטל את התור?")) {
        listItem.remove();
        alert("התור בוטל בהצלחה.");
    }
}

// ניווט חזרה
function goBack() {
    window.history.back();
}

// שליחת טופס יצירת קשר
document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (!name || !phone || !email || !message) {
        alert("נא למלא את כל השדות.");
        return;
    }

    alert(`ההודעה נשלחה בהצלחה!
    שם: ${name}
    טלפון: ${phone}
    דוא"ל: ${email}
    הודעה: ${message}`);
});

// ניווט חזרה
function goBack() {
    window.history.back();
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("צוות הרופאים נטען בהצלחה!");
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('signupForm').addEventListener('submit', function (e) {
        e.preventDefault(); // מונע רענון של הדף

        // שליפת הערכים מהשדות
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirmPassword').value.trim();
        const age = parseInt(document.getElementById('age').value.trim(), 10);

        // בדיקות ולידציה
        if (!name || !email || !password || !confirmPassword || isNaN(age)) {
            alert("נא למלא את כל השדות.");
            return; // עוצר את המשך התהליך
        }

        if (!validateEmail(email)) {
            alert("נא להזין כתובת דואר אלקטרוני תקינה.");
            return; // עוצר את המשך התהליך
        }

        if (password !== confirmPassword) {
            alert("הסיסמאות אינן תואמות.");
            return; // עוצר את המשך התהליך
        }

        if (password.length < 6) {
            alert("הסיסמה חייבת להיות לפחות 6 תווים.");
            return; // עוצר את המשך התהליך
        }

        if (age <= 0 || age > 120) {
            alert("נא להזין גיל תקין .");
            return; // עוצר את המשך התהליך
        }

        // הצלחה
        alert(`ברוך הבא, ${name}! החשבון נוצר בהצלחה.`);
        // כאן ניתן להוסיף לוגיקה לשליחת המידע לשרת
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signupForm');
    const phoneInput = document.getElementById('phone');
    const phoneError = document.getElementById('phoneError');

    signupForm.addEventListener('submit', function (e) {
        const phone = phoneInput.value.trim();
        const phoneRegex = /^0\d{9}$/; // מתחיל ב-0, בדיוק 10 ספרות

        if (!phoneRegex.test(phone)) {
            e.preventDefault(); // מונע את שליחת הטופס
            phoneError.style.display = 'block'; // מציג הודעת שגיאה
        } else {
            phoneError.style.display = 'none'; // מסתיר הודעת שגיאה
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signupForm');
    signupForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirmPassword').value.trim();

        if (!name || !email || !password || !confirmPassword) {
            alert("נא למלא את כל השדות.");
            return;
        }

        if (!validateEmail(email)) {
            alert("נא להזין כתובת דואר אלקטרוני תקינה.");
            return;
        }

        if (password !== confirmPassword) {
            alert("הסיסמאות אינן תואמות.");
            return;
        }

        if (password.length < 6) {
            alert("הסיסמה חייבת להיות לפחות 6 תווים.");
            return;
        }

        // תצוגת הודעת הצלחה
        alert(`הצלחתה ביצירת חשבון, ברוך הבא למרפאה שלנו, ${name}!`);
        // ניתן להוסיף כאן קוד לשליחת נתונים לשרת או לניתוב לעמוד אחר
    });
});
// מאזין לשליחת טופס יצירת קשר
document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault(); // מונע את רענון הדף

    // שליפת הנתונים מהשדות
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    // ולידציה פשוטה לדוגמה
    if (!name || !phone || !email || !message) {
        alert("נא למלא את כל השדות.");
        return;
    }

    // אם הוזן כל הנתונים בהצלחה
    alert(`ההודעה נשלחה בהצלחה! שם: ${name}, טלפון: ${phone}, דוא"ל: ${email}, הודעה: ${message}`);
});