"""
PROJECT: AWSAN NFC GLOBAL 2026 - Master Edition (V11.0)
-------------------------------------------------------
INTELLECTUAL PROPERTY & COPYRIGHT NOTICE:
Copyright (c) 2024-2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN.
All Rights Reserved.

DEVELOPER DETAILS:
- Name: Eng. Awsan Adel Abdulbari Ahmed Sultan
- Country: Yemen | ID: 01010305468
- Phone: +967777852433 | Email: awsan.sultan@gmail.com
- LinkedIn: https://linkedin.com

INNOVATION SCOPE:
This system includes a proprietary Hybrid Gateway for NFC-to-Crypto/NFT transactions.
Any reproduction or integration with Web3 protocols without license is prohibited.
-------------------------------------------------------
"""

from flask import Flask, jsonify, request, render_template_string, redirect, session, url_for
import hashlib
import sqlite3
import os
import requests # للربط مع أسعار العملات الرقمية والمنصات
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'awsan_crypto_nfc_secure_2026')

# إعدادات الإدارة
ADMIN_USER = "awsan"
ADMIN_PASS_HASH = hashlib.sha256("2026".encode()).hexdigest()

# --- قوالب التصميم المطورة لدعم الـ Crypto ---
COMMON_STYLES = """
<link href="https://jsdelivr.net" rel="stylesheet">
<link rel="stylesheet" href="https://cloudflare.com">
<style>
    :root { --awsan-dark: #0b0e11; --awsan-gold: #f3ba2f; --awsan-crypto: #00ffcc; }
    body { font-family: 'Segoe UI', sans-serif; background-color: #181a20; color: white; }
    .card-crypto { background: #2b2f36; border: 1px solid #474d57; border-radius: 15px; }
    .text-crypto { color: var(--awsan-crypto); }
</style>
"""

DASHBOARD_HTML = f"""
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>لوحة التحكم العالمية - أوسان NFC Crypto</title>
    {COMMON_STYLES}
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-2 p-4" style="background: #0b0e11; min-height: 100vh;">
                <h4 class="text-crypto fw-bold mb-4">AWSAN WEB3</h4>
                <nav class="nav flex-column">
                    <a class="nav-link text-white mb-2" href="#"><i class="fas fa-coins ms-2"></i> العملات الرقمية</a>
                    <a class="nav-link text-white mb-2" href="#"><i class="fas fa-image ms-2"></i> محفظة NFT</a>
                    <a class="nav-link text-white mb-2" href="#"><i class="fas fa-link ms-2"></i> ربط المنصات</a>
                    <hr>
                    <a class="nav-link text-danger" href="/logout"><i class="fas fa-power-off ms-2"></i> خروج</a>
                </nav>
            </div>
            
            <div class="col-md-10 p-5">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fab fa-bitcoin text-warning ms-2"></i> منصة الدفع الهجين (NFC + Crypto)</h2>
                    <span class="badge bg-success">أوسان سلطان - مطور معتمد</span>
                </div>

                <!-- أرصدة العملات الرقمية -->
                <div class="row g-3 mb-5">
                    <div class="col-md-3">
                        <div class="card-crypto p-3">
                            <small class="text-muted">رصيد Bitcoin (BTC)</small>
                            <h3 class="text-warning fw-bold">{{{{ wallet.btc }}}} BTC</h3>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card-crypto p-3">
                            <small class="text-muted">رصيد Ethereum (ETH)</small>
                            <h4 class="text-info fw-bold">{{{{ wallet.eth }}}} ETH</h4>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card-crypto p-3">
                            <small class="text-muted">رصيد USDT (Global)</small>
                            <h3 class="text-success fw-bold">${{{{ "{:,.2f}".format(wallet.usdt) }}}}</h3>
                        </div>
                    </div>
                </div>

                <!-- قسم الـ NFT -->
                <div class="card-crypto p-4 mb-4">
                    <h5 class="mb-4 text-crypto"><i class="fas fa-gallery-thumbnails ms-2"></i> أصول الـ NFT المربوطة بـ NFC</h5>
                    <div class="row g-3">
                        <div class="col-md-2 text-center">
                            <div style="height:100px; background:#474d57; border-radius:10px; display:flex; align-items:center; justify-content:center;">
                                <i class="fas fa-cube fa-2x"></i>
                            </div>
                            <p class="small mt-2">Awsan Golden Card #001</p>
                        </div>
                    </div>
                </div>

                <!-- جدول العمليات -->
                <div class="card-crypto p-4">
                    <h5 class="mb-3">سجل العمليات العالمية (Fiat & Crypto)</h5>
                    <table class="table table-dark table-hover">
                        <thead>
                            <tr>
                                <th>المعرف التشفيري</th>
                                <th>النوع</th>
                                <th>المبلغ</th>
                                <th>الشبكة (Blockchain)</th>
                                <th>التوقيت</th>
                            </tr>
                        </thead>
                        <tbody>
                            {{% for tx in transactions %}}
                            <tr>
                                <td class="small text-crypto">{{{{ tx.tx_id }}}}</td>
                                <td>{{{{ tx.type }}}}</td>
                                <td>{{{{ tx.amount }}}}</td>
                                <td><span class="badge bg-secondary">{{{{ tx.network }}}}</span></td>
                                <td class="small">{{{{ tx.timestamp }}}}</td>
                            </tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- منطق البرمجة المطوّر (Enhanced Crypto Logic) ---

def get_db():
    conn = sqlite3.connect('awsan_nfc_global_v2.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # تحديث جدول المحفظة ليشمل العملات الرقمية
    conn.execute('''CREATE TABLE IF NOT EXISTS wallets 
                    (nfc_id TEXT PRIMARY KEY, btc REAL, eth REAL, usdt REAL, yer REAL, usd REAL)''')
    
    # تحديث جدول العمليات ليشمل شبكات البلوكشين
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                    (tx_id TEXT, type TEXT, amount REAL, network TEXT, timestamp DATETIME)''')
    
    # رصيد افتراضي (تجريبي) للمهندس أوسان
    conn.execute("INSERT OR IGNORE INTO wallets VALUES ('01010305468', 0.05, 1.2, 5000.0, 2500000.0, 1000.0)")
    conn.commit()
    conn.close()

# دالة برمجية للربط مع المحافظ العالمية (MetaMask / WalletConnect)
def connect_global_wallet(wallet_address, provider="Binance"):
    """
    بروتوكول المهندس أوسان للربط البرمجي مع منصات التداول والمحافظ الرقمية.
    """
    # هنا يتم استدعاء الـ API الخاص بالمنصة (مثل Binance API) لجلب الأرصدة الحقيقية
    pass

init_db()






# --- محرك عمليات أوسان العالمي (Awsan Transaction Engine) ---

@app.route('/pay', methods=['POST'])
def process_payment():
    """
    بروتوكول معالجة الدفع الهجين - ابتكار المهندس أوسان
    يدعم الخصم من العملات التقليدية أو المحافظ الرقمية
    """
    data = request.get_json()
    nfc_id = data.get('nfc_id')
    amount = float(data.get('amount'))
    currency = data.get('currency') # مثل: USD, YER, BTC, USDT
    vendor = data.get('vendor')

    conn = get_db()
    # 1. التحقق من وجود المحفظة المربوطة بالـ NFC
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id=?", (nfc_id,)).fetchone()
    
    if not wallet:
        return jsonify({"status": "error", "message": "NFC Card not recognized"}), 404

    # 2. التحقق من كفاية الرصيد حسب نوع العملة
    current_balance = wallet[currency.lower()]
    if current_balance < amount:
        return jsonify({"status": "error", "message": "Insufficient balance"}), 400

    # 3. تنفيذ الخصم (العملية الحسابية)
    new_balance = current_balance - amount
    conn.execute(f"UPDATE wallets SET {currency.lower()} = ? WHERE nfc_id = ?", (new_balance, nfc_id))
    
    # 4. تسجيل العملية في سجل الملكية الفكرية الخاص بالنظام
    tx_id = "AWSAN-" + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:12].upper()
    conn.execute("INSERT INTO transactions (tx_id, type, amount, network, timestamp) VALUES (?, ?, ?, ?, ?)",
                 (tx_id, f"NFC Pay ({currency})", amount, "Awsan Hybrid Network", datetime.now()))
    
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "tx_id": tx_id,
        "remaining_balance": new_balance,
        "developer": "Eng. Awsan Sultan"
    })


# --- المسارات (Routes) ---

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, admin_name="Eng. Awsan Sultan", 
                                 wallet={'btc': 0.05, 'eth': 1.2, 'usdt': 5000.0, 'yer': 2500000},
                                 transactions=[])

# سيتم إضافة مسارات الـ API للـ NFT والـ Crypto هنا...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
