# =========================================================================================
#  █████╗ ██╗    ██╗███████╗ █████╗ ███╗   ██╗    ███╗   ██╗███████╗ ██████╗ 
# ██╔══██╗██║    ██║██╔════╝██╔══██╗████╗  ██║    ████╗  ██║██╔════╝██╔════╝ 
# ███████║██║ █╗ ██║███████╗███████║██╔██╗ ██║    ██╔██╗ ██║█████╗  ██║      
# ██╔══██║██║███╗██║╚════██║██╔══██║██║╚██╗██║    ██║╚██╗██║██╔══╝  ██║      
# ██║  ██║╚███╔███╔╝███████║██║  ██║██║ ╚████║    ██║ ╚████║██║     ╚██████╗ 
# ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚═╝      ╚═════╝ 
# -----------------------------------------------------------------------------------------
#                 🛡️ AWSAN NFC GLOBAL 2026 | MASTER EDITION (V11.0)
#           📜 COPYRIGHT (C) 2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN
# =========================================================================================
#
#  ⚠️  COMMERCIAL USE NOTICE:
#  -------------------------
#  ANY COMMERCIAL DEPLOYMENT OR PROFIT-GENERATING USE REQUIRES A PRIOR WRITTEN 
#  AGREEMENT TO DEFINE PROFIT-SHARING PERCENTAGES AND LICENSING FEES.
#
#  ⚠️  تنبيه الاستخدام التجاري:
#  -----------------------
#  أي تشغيل تجاري للنظام أو استخدامه في مشاريع ربحية يتطلب اتفاقاً خطياً مسبقاً
#  مع المالك لتحديد نسب الأرباح وحقوق الملكية البرمجية.
#
# =========================================================================================
#  👨‍💻 DEVELOPER: Eng. Awsan Adel Sultan | YEMEN (ID: 01010305468)
#  📞 PHONE: 00967777852433             | 📧 EMAIL: awsan.sultan@gmail.com
# =========================================================================================


from flask import Flask, jsonify, request, render_template_string, redirect, session
import hashlib, sqlite3, uuid, os
from datetime import datetime

app = Flask(__name__)
# استخدام مفتاح سري قوي لتأمين الجلسات
app.secret_key = os.environ.get('SECRET_KEY', 'awsan_secure_key_2026_vision')

# إعدادات الدخول الرسمية للمدير (Eng. Awsan)
ADMIN_USER = "awsan"
ADMIN_PASS_HASH = hashlib.sha256("2026".encode()).hexdigest()

def get_db():
    """الاتصال بقاعدة بيانات أوسان NFC"""
    conn = sqlite3.connect('awsan_nfc_2026.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """تهيئة جداول النظام وحفظ الملكية في قاعدة البيانات"""
    conn = get_db()
    # جدول الموردين المعتمدين
    conn.execute('CREATE TABLE IF NOT EXISTS vendors (name TEXT PRIMARY KEY)')
    # جدول المحفظة (برقم هوية المهندس أوسان)
    conn.execute('CREATE TABLE IF NOT EXISTS wallets (nfc_id TEXT PRIMARY KEY, yer REAL, sar REAL, usd REAL, aed REAL)')
    # جدول العمليات
    conn.execute('CREATE TABLE IF NOT EXISTS transactions (tx_id TEXT, nfc_id TEXT, amount REAL, currency TEXT, vendor TEXT, time TEXT, status TEXT)')
    
    # إضافة بيانات افتراضية للموردين
    default_vendors = ["Awsan Tech Store", "Future Supermarket", "Smart Energy Station"]
    for v in default_vendors:
        conn.execute("INSERT OR IGNORE INTO vendors VALUES (?)", (v,))
    
    # إيداع الرصيد الافتتاحي لمحفظة المالك
    conn.execute("INSERT OR IGNORE INTO wallets VALUES ('01010305468', 1250000, 1500, 450, 3200)")
    
    conn.commit()
    conn.close()

# --- واجهات النظام المطورة ---

LOGIN_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>Login - Awsan NFC Global</title>
    <meta charset="UTF-8">
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background: #001f3f; display: flex; align-items: center; height: 100vh; font-family: 'Segoe UI', Tahoma; }
        .login-card { background: white; border-radius: 25px; padding: 40px; width: 100%; max-width: 400px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.5); border: 2px solid #003366; }
        .btn-awsan { background: #003366; color: white; border-radius: 12px; transition: 0.3s; }
        .btn-awsan:hover { background: #00509d; color: white; }
    </style>
</head>
<body>
    <div class="login-card text-center">
        <div class="mb-4">
            <h2 class="text-primary fw-bold">🛡️ نظام أوسان NFC</h2>
            <small class="text-muted">الإصدار 11.0 - Master Edition</small>
        </div>
        <form action="/login" method="POST">
            <input type="text" name="user" class="form-control mb-3 py-2" placeholder="اسم مستخدم المدير" required>
            <input type="password" name="pass" class="form-control mb-3 py-2" placeholder="كلمة المرور" required>
            <button type="submit" class="btn btn-awsan w-100 py-2 fw-bold">دخول آمن</button>
        </form>
        {% if error %}<p class="text-danger mt-3 small fw-bold">{{ error }}</p>{% endif %}
        <hr>
        <p class="small text-muted">تطوير م. أوسان سلطان © 2026</p>
    </div>
</body>
</html>
"""

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')
        if user == ADMIN_USER and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASS_HASH:
            session['logged_in'] = True
            session['admin_name'] = "Eng. Awsan Sultan"
            return redirect('/dashboard')
        return render_template_string(LOGIN_HTML, error="عذراً، البيانات غير صحيحة!")
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    
    conn = get_db()
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id='01010305468'").fetchone()
    txs = conn.execute("SELECT * FROM transactions ORDER BY time DESC LIMIT 8").fetchall()
    vendors = conn.execute("SELECT * FROM vendors").fetchall()
    conn.close()
    
    return render_template_string(open_dashboard_html(), w=wallet, txs=txs, vendors=vendors)

def open_dashboard_html():
    # هنا يتم استدعاء التصميم الاحترافي الذي قمنا بتطويره سابقاً
    # مع إضافة توقيع م. أوسان في التذييل
    return """... (كود الـ HTML الاحترافي الذي أرسلته لك سابقاً مع ترويسة المهندس أوسان) ..."""

if __name__ == '__main__':
    init_db()
    # التشغيل على بورت 8081 كما حددت في مشروعك
    app.run(host='0.0.0.0', port=8081, debug=False)
