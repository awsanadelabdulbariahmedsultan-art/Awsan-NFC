"""
PROJECT: AWSAN NFC GLOBAL 2026 - Master Edition (V11.0)
-------------------------------------------------------
INTELLECTUAL PROPERTY & COPYRIGHT NOTICE:
Copyright (c) 2024-2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN.
All Rights Reserved.

DEVELOPER DETAILS:
- Name: Eng. Awsan Adel Abdulbari Ahmed Sultan
- Country: Yemen
- ID: 01010305468
- Phone: +967777852433
- Email: awsan.sultan@gmail.com
- LinkedIn: https://www.linkedin.com/in/awsan-adel-abdulbari-ahmed-sultan-8aa5a1a9
-------------------------------------------------------
"""

from flask import Flask, jsonify, request, render_template_string, redirect, session, url_for
import hashlib
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'awsan_secure_key_2026_vision')

# إعدادات الإدارة
ADMIN_USER = "awsan"
ADMIN_PASS_HASH = hashlib.sha256("2026".encode()).hexdigest()

# --- قوالب التصميم (UI Templates) كما في الصور ---
LOGIN_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>Login - Awsan NFC Global</title>
    <meta charset="utf-8">
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background: #001f3f; display: flex; align-items: center; height: 100vh; font-family: 'Segoe UI', Tahoma; }
        .login-card { background: white; border-radius: 25px; padding: 40px; width: 100%; max-width: 400px; margin: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .btn-awsan { background: #003366; color: white; border-radius: 12px; transition: 0.3s; }
        .btn-awsan:hover { background: #00509d; color: white; }
    </style>
</head>
<body>
    <div class="login-card text-center">
        <div class="mb-4">
            <h2 class="text-primary fw-bold">نظام أوسان NFC 🚀</h2>
            <small class="text-muted">Master Edition V11.0 - إصدار 2026</small>
        </div>
        <form method="POST">
            <input type="text" name="user" class="form-control mb-3 py-2" placeholder="اسم مستخدم المدير" required>
            <input type="password" name="pass" class="form-control mb-3 py-2" placeholder="كلمة المرور" required>
            <button type="submit" class="btn btn-awsan w-100 py-2 fw-bold">دخول للنظام</button>
        </form>
        {% if error %}<p class="text-danger mt-3 small fw-bold">{{ error }}</p>{% endif %}
        <p class="small text-muted mt-4">تطوير م. أوسان سلطان © 2026</p>
    </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>Dashboard - Awsan NFC</title>
    <meta charset="utf-8">
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background: #f4f7f6; font-family: 'Segoe UI', sans-serif; }
        .sidebar { background: #001f3f; color: white; min-height: 100vh; padding: 20px; }
        .card-stat { border-radius: 15px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: 0.3s; }
        .card-stat:hover { transform: translateY(-5px); }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 sidebar">
                <h4 class="text-center mb-5">Awsan Global</h4>
                <p>مرحباً، {{ admin_name }}</p>
                <hr>
                <a href="/" class="text-white d-block mb-3 text-decoration-none">🏠 الرئيسية</a>
                <a href="/logout" class="text-white d-block text-decoration-none">🔒 تسجيل الخروج</a>
            </div>
            <div class="col-md-10 p-5">
                <h2 class="mb-4">لوحة تحكم نظام الدفع الذكي</h2>
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card card-stat p-3 text-center">
                            <h6>رصيد المحفظة (USD)</h6>
                            <h3 class="text-success">${{ wallet.usd }}</h3>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-stat p-3 text-center">
                            <h6>الرصيد بالريال اليمني</h6>
                            <h3 class="text-primary">{{ wallet.yer }} YER</h3>
                        </div>
                    </div>
                </div>

                <div class="card card-stat p-4">
                    <h5>آخر العمليات المنفذة عبر NFC</h5>
                    <table class="table mt-3">
                        <thead>
                            <tr>
                                <th>رقم العملية</th>
                                <th>المتجر</th>
                                <th>المبلغ</th>
                                <th>التاريخ</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for tx in transactions %}
                            <tr>
                                <td>{{ tx.tx_id }}</td>
                                <td>{{ tx.vendor }}</td>
                                <td>{{ tx.amount }} {{ tx.currency }}</td>
                                <td>{{ tx.timestamp }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- قاعدة البيانات ---
def get_db():
    conn = sqlite3.connect('awsan_nfc_2026.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS vendors (name TEXT PRIMARY KEY)')
    conn.execute('CREATE TABLE IF NOT EXISTS wallets (nfc_id TEXT PRIMARY KEY, yer REAL, sar REAL, usd REAL, aed REAL)')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (tx_id TEXT, nfc_id TEXT, vendor TEXT, amount REAL, currency TEXT, timestamp DATETIME)')
    
    # بيانات أولية للتجربة
    conn.execute("INSERT OR IGNORE INTO vendors VALUES ('Awsan Tech Store')")
    conn.execute("INSERT OR IGNORE INTO wallets VALUES ('01010305468', 1250000, 1500, 500, 3200)")
    conn.commit()
    conn.close()

init_db()

# --- المسارات (Routes) ---
@app.route('/')
def index():
    return render_template_string("<h1>نظام أوسان NFC العالمي 2026 جاهز</h1><a href='/login'>دخول النظام</a>")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        if user == ADMIN_USER and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASS_HASH:
            session['logged_in'] = True
            session['admin_name'] = "Eng. Awsan Sultan"
            return redirect(url_for('dashboard'))
        error = "خطأ في بيانات الدخول، يرجى المحاولة مرة أخرى"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db()
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id='01010305468'").fetchone()
    txs = conn.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 5").fetchall()
    vendors = conn.execute("SELECT * FROM vendors").fetchall()
    conn.close()
    
    return render_template_string(DASHBOARD_HTML, admin_name=session['admin_name'], wallet=wallet, transactions=txs, vendors=vendors)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # التشغيل على المنفذ 5001 كما في صورتك
    app.run(host='0.0.0.0', port=5001, debug=False)
