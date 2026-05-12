"""
PROJECT: AWSAN NFC GLOBAL 2026 - Master Edition (V11.0)
-------------------------------------------------------
INTELLECTUAL PROPERTY & COPYRIGHT NOTICE:
Copyright (c) 2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN.
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

# --- قوالب التصميم الاحترافية (Professional UI) ---

COMMON_STYLES = """
<link href="https://jsdelivr.net" rel="stylesheet">
<link rel="stylesheet" href="https://cloudflare.com">
<style>
    :root { --awsan-dark: #001f3f; --awsan-gold: #FFD700; --awsan-blue: #003366; }
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; }
    .awsan-bg-dark { background-color: var(--awsan-dark) !important; }
    .awsan-text-gold { color: var(--awsan-gold) !important; }
    .card-custom { border-radius: 15px; border: none; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
</style>
"""

LOGIN_HTML = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>تسجيل الدخول - نظام أوسان NFC</title>
    <meta charset="utf-8">
    {COMMON_STYLES}
    <style>
        .login-container {{ height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .login-card {{ width: 100%; max-width: 450px; padding: 40px; background: #fff; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); border-top: 5px solid var(--awsan-gold); }}
        .btn-login {{ background: var(--awsan-blue); color: white; border-radius: 10px; padding: 12px; transition: 0.3s; width: 100%; border: none; }}
        .btn-login:hover {{ background: var(--awsan-dark); color: #fff; transform: scale(1.02); }}
    </style>
</head>
<body class="awsan-bg-dark">
    <div class="login-container">
        <div class="login-card text-center">
            <i class="fas fa-nfc-symbol fa-4x mb-3 awsan-text-gold" style="color: #003366;"></i>
            <h3 class="fw-bold mb-1">Awsan NFC Global</h3>
            <p class="text-muted mb-4 small">الرؤية العالمية لعام 2026</p>
            
            <form method="POST">
                <div class="mb-3 text-start">
                    <label class="form-label small">اسم المستخدم</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-user"></i></span>
                        <input type="text" name="user" class="form-control" placeholder="اسم مستخدم المدير" required>
                    </div>
                </div>
                <div class="mb-4 text-start">
                    <label class="form-label small">كلمة المرور</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fas fa-lock"></i></span>
                        <input type="password" name="pass" class="form-control" placeholder="********" required>
                    </div>
                </div>
                <button type="submit" class="btn-login fw-bold"><i class="fas fa-sign-in-alt ms-2"></i> دخول النظام</button>
            </form>
            
            {{% if error %}}
            <div class="alert alert-danger mt-3 py-2 small fw-bold">{{{{ error }}}}</div>
            {{% endif %}}
            
            <hr class="my-4">
            <p class="mb-0 x-small text-muted">تطوير المهندس أوسان سلطان © 2026</p>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_HTML = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>لوحة التحكم - أوسان NFC</title>
    <meta charset="utf-8">
    {COMMON_STYLES}
    <style>
        .sidebar {{ background: var(--awsan-dark); min-height: 100vh; position: fixed; right: 0; top: 0; width: 250px; padding-top: 20px; color: white; }}
        .main-content {{ margin-right: 250px; padding: 30px; }}
        .nav-link {{ color: #adb5bd; transition: 0.3s; padding: 12px 20px; }}
        .nav-link:hover, .nav-link.active {{ color: var(--awsan-gold); background: rgba(255,255,255,0.05); }}
        .stat-card {{ background: white; padding: 25px; border-radius: 15px; border-right: 5px solid var(--awsan-blue); }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="text-center mb-4">
             <i class="fas fa-shield-halved fa-2x awsan-text-gold mb-2"></i>
             <h5 class="fw-bold">Awsan NFC Global</h5>
             <small class="text-muted">Master Edition V11.0</small>
        </div>
        <nav class="nav flex-column mt-4">
            <a class="nav-link active" href="#"><i class="fas fa-chart-line ms-2"></i> الإحصائيات العامة</a>
            <a class="nav-link" href="#"><i class="fas fa-wallet ms-2"></i> إدارة المحافظ</a>
            <a class="nav-link" href="#"><i class="fas fa-exchange-alt ms-2"></i> سجل العمليات</a>
            <hr class="mx-3">
            <a class="nav-link text-danger" href="/logout"><i class="fas fa-power-off ms-2"></i> خروج آمن</a>
        </nav>
    </div>

    <div class="main-content">
        <div class="d-flex justify-content-between align-items-center mb-5">
            <h4><i class="fas fa-tachometer-alt ms-2 text-primary"></i> أهلاً بك، {{{{ admin_name }}}}</h4>
            <span class="badge bg-dark px-3 py-2 text-white">ID: 01010305468</span>
        </div>

        <div class="row g-4 mb-5">
            <div class="col-md-3">
                <div class="stat-card shadow-sm">
                    <p class="text-muted small mb-1">الرصيد الكلي (USD)</p>
                    <h3 class="fw-bold text-success">${{{{ "%.2f"|format(wallet.usd) }}}}</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card shadow-sm" style="border-right-color: #e67e22;">
                    <p class="text-muted small mb-1">الرصيد بالريال (YER)</p>
                    <h3 class="fw-bold text-primary">{{{{ "{:,.0f}".format(wallet.yer) }}}}</h3>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card shadow-sm" style="border-right-color: #2ecc71;">
                    <p class="text-muted small mb-1">الرصيد السعودي (SAR)</p>
                    <h3 class="fw-bold text-warning">{{{{ "{:,.0f}".format(wallet.sar) }}}}</h3>
                </div>
            </div>
        </div>

        <div class="card card-custom shadow-sm p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="fw-bold mb-0">آخر عمليات الدفع الذكي</h5>
                <button class="btn btn-sm btn-outline-primary"><i class="fas fa-print ms-1"></i> تصدير تقرير</button>
            </div>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>رقم العملية</th>
                            <th>المتجر المستفيد</th>
                            <th>المبلغ</th>
                            <th>العملة</th>
                            <th>تاريخ ووقت التنفيذ</th>
                            <th>الحالة</th>
                        </tr>
                    </thead>
                    <tbody>
                        {{% for tx in transactions %}}
                        <tr>
                            <td class="fw-bold text-secondary">{{{{ tx.tx_id }}}}</td>
                            <td><i class="fas fa-store ms-2 text-muted"></i>{{{{ tx.vendor }}}}</td>
                            <td class="fw-bold text-dark">{{{{ tx.amount }}}}</td>
                            <td><span class="badge bg-secondary">{{{{ tx.currency }}}}</span></td>
                            <td class="small">{{{{ tx.timestamp }}}}</td>
                            <td><span class="badge bg-success-subtle text-success border border-success px-3">مكتملة</span></td>
                        </tr>
                        {{% else %}}
                        <tr><td colspan="6" class="text-center py-4 text-muted small">لا توجد عمليات مسجلة حالياً</td></tr>
                        {{% endfor %}}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- منطق قاعدة البيانات (Database Logic) ---

def get_db():
    conn = sqlite3.connect('awsan_nfc_2026.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS vendors (name TEXT PRIMARY KEY)')
    conn.execute('CREATE TABLE IF NOT EXISTS wallets (nfc_id TEXT PRIMARY KEY, yer REAL, sar REAL, usd REAL, aed REAL)')
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (tx_id TEXT, nfc_id TEXT, vendor TEXT, amount REAL, currency TEXT, timestamp DATETIME)')
    
    # إدخال بيانات تجريبية (Test Data)
    conn.execute("INSERT OR IGNORE INTO vendors VALUES ('Awsan Tech Store')")
    conn.execute("INSERT OR IGNORE INTO vendors VALUES ('International Payment Hub')")
    conn.execute("INSERT OR IGNORE INTO wallets VALUES ('01010305468', 1250000.0, 1500.0, 500.0, 3200.0)")
    conn.commit()
    conn.close()

init_db()

# --- المسارات (Routes) ---

@app.route('/')
def index():
    return redirect(url_for('login'))

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
        error = "بيانات الدخول غير صحيحة، يرجى التحقق"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db()
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id='01010305468'").fetchone()
    txs = conn.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 10").fetchall()
    conn.close()
    
    return render_template_string(DASHBOARD_HTML, admin_name=session['admin_name'], wallet=wallet, transactions=txs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # التشغيل على المنفذ 5001 كما في صورتك الأصلية
    app.run(host='0.0.0.0', port=5001, debug=False)
