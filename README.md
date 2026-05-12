"""
PROJECT: AWSAN NFC GLOBAL 2026 - Master Edition (V11.0)
-------------------------------------------------------
INTELLECTUAL PROPERTY & COPYRIGHT NOTICE:
Copyright (c) 2024-2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN.
-------------------------------------------------------
"""

from flask import Flask, jsonify, request, render_template_string, redirect, session, url_for
import hashlib
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'awsan_nfc_vision_2026_secure_key')

# --- قوالب التصميم المتطورة (Advanced UI/UX) ---
PAYMENT_UI_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة أوسان للدفع الذكي</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --main-gold: #f3ba2f; --bg-dark: #0b0e11; --card-bg: #1e2329; }
        body { background-color: var(--bg-dark); color: white; font-family: 'Segoe UI', sans-serif; }
        .pay-card { background: var(--card-bg); border-radius: 24px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); border: 1px solid #333; margin-top: 50px; }
        .currency-pill { background: #2b3139; border-radius: 12px; padding: 10px 15px; margin-bottom: 10px; border: 1px solid transparent; cursor: pointer; transition: 0.3s; }
        .currency-pill:hover { border-color: var(--main-gold); }
        .btn-pay { background: var(--main-gold); color: black; border-radius: 12px; font-weight: bold; padding: 15px; width: 100%; border: none; font-size: 1.1rem; }
        .nfc-icon { color: var(--main-gold); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="pay-card text-center">
                    <i class="fas fa-nfc-symbol fa-3x nfc-icon mb-3"></i>
                    <h4 class="fw-bold mb-1">تأكيد عملية الدفع</h4>
                    <p class="text-muted small">نظام أوسان NFC - النسخة العالمية 11.0</p>
                    <hr class="my-4 border-secondary">
                    
                    <div class="text-start mb-4">
                        <label class="form-label text-muted small">المتجر المستفيد</label>
                        <div class="h5 fw-bold"><i class="fas fa-store ms-2"></i> {{ vendor }}</div>
                    </div>

                    <div class="text-start mb-4">
                        <label class="form-label text-muted small">المبلغ المطلوب</label>
                        <div class="display-5 fw-bold text-warning">{{ amount }} <small class="h4">{{ currency }}</small></div>
                    </div>

                    <div class="currency-pill d-flex justify-content-between align-items-center">
                        <span><i class="fas fa-wallet ms-2"></i> رصيدك المتاح:</span>
                        <span class="text-success fw-bold">{{ balance }} {{ currency }}</span>
                    </div>

                    <form action="/execute_pay" method="POST" class="mt-4">
                        <input type="hidden" name="nfc_id" value="{{ nfc_id }}">
                        <input type="hidden" name="amount" value="{{ amount }}">
                        <input type="hidden" name="currency" value="{{ currency }}">
                        <input type="hidden" name="vendor" value="{{ vendor }}">
                        <button type="submit" class="btn-pay shadow">تأكيد وخصم المبلغ الآن</button>
                    </form>
                    
                    <p class="mt-4 x-small text-muted">Protected by Awsan Intellectual Property © 2026</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# --- المنطق البرمجي (Back-end Logic) ---

def get_db():
    conn = sqlite3.connect('awsan_nfc_2026.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/checkout')
def checkout():
    """محاكاة لمسح بطاقة NFC وعرض واجهة الدفع"""
    # بيانات افتراضية للمحاكاة (سيتم استبدالها ببيانات حقيقية من الحساس)
    nfc_id = "01010305468"
    amount = 100.50
    currency = "USDT"
    vendor = "Awsan Tech Store"
    
    conn = get_db()
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id=?", (nfc_id,)).fetchone()
    conn.close()
    
    return render_template_string(PAYMENT_UI_HTML, 
                                 nfc_id=nfc_id, 
                                 amount=amount, 
                                 currency=currency, 
                                 vendor=vendor, 
                                 balance=wallet[currency.lower()])

@app.route('/execute_pay', methods=['POST'])
def execute_pay():
    """تنفيذ الخصم الفعلي بعد تأكيد المستخدم"""
    # (هنا يتم وضع كود الخصم من قاعدة البيانات الذي جهزناه سابقاً)
    return "<h1>تمت العملية بنجاح! شكراً لاستخدامك نظام أوسان NFC.</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
