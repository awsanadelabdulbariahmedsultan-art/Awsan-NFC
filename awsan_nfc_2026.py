"""
PROJECT: AWSAN NFC GLOBAL 2026 - Master Edition (V11.0)
-------------------------------------------------------
INTELLECTUAL PROPERTY & COPYRIGHT NOTICE:
Copyright (c) 2026 ENG. AWSAN ADEL ABDULBARI AHMED SULTAN.
All Rights Reserved.
-------------------------------------------------------
"""

from flask import Flask, jsonify, request, render_template_string, redirect, session, url_for
import hashlib
import sqlite3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv 
from web3 import Web3          
from Crypto.Cipher import AES  

# تحميل الإعدادات وتأمين المفاتيح
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'awsan_nfc_global_key_2026_secure')

# إعدادات المدير (Admin)
ADMIN_USER = "awsan"
ADMIN_PASS_HASH = hashlib.sha256("2026".encode()).hexdigest()

# --- قاعدة البيانات والبيانات الأولية ---
def get_db():
    conn = sqlite3.connect('awsan_nfc_2026.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS wallets 
                    (nfc_id TEXT PRIMARY KEY, yer REAL, btc REAL, eth REAL, usdt REAL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                    (tx_id TEXT, vendor TEXT, amount REAL, currency TEXT, timestamp DATETIME)''')
    
    # إدخال بياناتك الشخصية كمحفظة رئيسية
    conn.execute("INSERT OR IGNORE INTO wallets VALUES ('01010305468', 2500000.0, 0.05, 1.2, 5000.0)")
    conn.commit()
    conn.close()

init_db()

# --- محرك معالجة الدفع (الدمج المطلوب) ---
@app.route('/pay', methods=['POST'])
def process_payment():
    """
    بروتوكول معالجة الدفع - ابتكار المهندس أوسان
    بيانات الاختبار المطلوبة مدمجة في هذا المنطق
    """
    data = request.get_json()
    nfc_id = data.get('nfc_id', '01010305468')
    amount = float(data.get('amount', 100.50))
    currency = data.get('currency', 'USDT')
    vendor = data.get('vendor', 'Awsan Tech Store')

    conn = get_db()
    wallet = conn.execute("SELECT * FROM wallets WHERE nfc_id=?", (nfc_id,)).fetchone()
    
    if not wallet or wallet[currency.lower()] < amount:
        return jsonify({"status": "error", "message": "رصيد غير كافٍ أو بطاقة غير معروفة"}), 400

    # تنفيذ الخصم
    new_balance = wallet[currency.lower()] - amount
    conn.execute(f"UPDATE wallets SET {currency.lower()} = ? WHERE nfc_id = ?", (new_balance, nfc_id))
    
    # توثيق العملية برقم مرجعي عالمي
    tx_id = "AWSAN-TX-" + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8].upper()
    conn.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", 
                 (tx_id, vendor, amount, currency, datetime.now()))
    
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "tx_id": tx_id,
        "remaining": new_balance,
        "msg": f"تم دفع {amount} {currency} إلى {vendor}",
        "developer": "Eng. Awsan Sultan"
    })

@app.route('/')
def index():
    return "<h1>Awsan NFC Global 2026 Ready</h1><p>Web3 & Crypto Gateway Active.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
