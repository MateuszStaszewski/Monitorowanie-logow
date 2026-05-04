import streamlit as st
import re
from collections import Counter
import pandas as pd
import os

st.set_page_config(
    page_title="Monitorowanie logów",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BLOCK_FILE = "blocked_ips.txt"

def load_blocked_ips():
    if not os.path.exists(BLOCK_FILE):
        return set()
    with open(BLOCK_FILE, "r") as f:
        return set(line.strip() for line in f)

def block_ip(ip):
    with open(BLOCK_FILE, "a") as f:
        f.write(ip + "\n")

def unblock_ip(ip):
    if os.path.exists(BLOCK_FILE):
        with open(BLOCK_FILE, "r") as f:
            lines = f.readlines()
        with open(BLOCK_FILE, "w") as f:
            for line in lines:
                if line.strip() != ip:
                    f.write(line)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Inter:wght@400;700&display=swap');

    .stApp {
        background-color: #050a14;
        color: #e0e6ed;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'VT323', monospace;
        color: #00f2fe;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .main-title {
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px #00f2fe;
    }

    .metric-card {
        background-color: #0b1121;
        border: 1px solid #162a4a;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 242, 254, 0.2);
        border-color: #00f2fe;
    }

    .metric-label {
        font-size: 1rem;
        color: #8899ac;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2.5rem;
        font-family: 'VT323', monospace;
        color: #fff;
    }
    
    .value-critical {
        color: #ff3366;
        text-shadow: 0 0 10px #ff3366;
    }

    .alert-box {
        background-color: rgba(255, 51, 102, 0.1);
        border: 1px solid #ff3366;
        color: #ff3366;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .stButton>button {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white;
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        text-transform: uppercase;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 15px #00c6ff;
        transform: scale(1.02);
    }

    .radar-container {
        position: relative;
        width: 100px; height: 100px;
        margin: 0 auto 1rem;
        border-radius: 50%;
        border: 2px solid #162a4a;
        overflow: hidden;
    }
    
    .radar-beam {
        position: absolute;
        top: 50%; left: 50%;
        width: 50%; height: 2px;
        background: linear-gradient(90deg, rgba(0,242,254,1) 0%, rgba(0,242,254,0) 100%);
        transform-origin: left center;
        animation: radar-spin 2s linear infinite;
    }
    
    @keyframes radar-spin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
    st.session_state.total_logs = 0

def parse_logs(file_path):
    log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?"\s(?P<status>\d{3})'
    suspicious_ips = []
    total_logs = 0
    try:
        with open(file_path, "r") as f:
            for line in f:
                total_logs += 1
                match = re.search(log_pattern, line)
                if match and match.group('status') == '401':
                    suspicious_ips.append(match.group('ip'))
    except FileNotFoundError:
        return None, 0
    return Counter(suspicious_ips), total_logs

st.markdown('<h1 class="main-title">🛡️ Monitorowanie logów</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="radar-container">
    <div class="radar-beam"></div>
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #162a4a; font-size: 0.8rem;">SCAN</div>
</div>
""", unsafe_allow_html=True)

if st.button("Uruchom Skanowanie Systemu"):
    st.session_state.scan_results, st.session_state.total_logs = parse_logs("access.log")

if st.session_state.scan_results is not None:
    result = st.session_state.scan_results
    total_count = st.session_state.total_logs
    blocked_list = load_blocked_ips()
    critical_events = sum(1 for ip, count in result.items() if count > 5)
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric-card"><div class="metric-label">Całkowita liczba logów</div><div class="metric-value">{total_count}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card"><div class="metric-label">Wykryte błędy 401</div><div class="metric-value">{sum(result.values())}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card" style="border-color: {"#ff3366" if critical_events > 0 else "#162a4a"}"><div class="metric-label">Krytyczne zagrożenia</div><div class="value-critical metric-value">{critical_events}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_table, col_alerts = st.columns([2, 1])
    
    with col_table:
        st.subheader("Szczegółowa analiza IP (Status 401)")
        
        header_cols = st.columns([3, 1, 1])
        header_cols[0].markdown("**IP ADDRESS**")
        header_cols[1].markdown("**ATTEMPTS**")
        header_cols[2].markdown("**ACTION**")
        st.markdown("---")
        
        for ip, count in result.items():
            row_cols = st.columns([3, 1, 1])
            row_cols[0].write(f"{ip}")
            row_cols[1].write(f"{count}")
            
            if ip in blocked_list:
                if row_cols[2].button("Odblokuj", key=f"btn_{ip}"):
                    unblock_ip(ip)
                    st.rerun()
            else:
                if row_cols[2].button("Blokuj", key=f"btn_{ip}"):
                    block_ip(ip)
                    st.rerun()

    with col_alerts:
        st.subheader("Konsola Alertów")
        alarms_active = False
        for ip, count in result.items():
            if count > 5 and ip not in blocked_list:
                alarms_active = True
                st.markdown(f'<div class="alert-box">⚠️ Brute-Force: {ip} ({count} prób)</div>', unsafe_allow_html=True)
        
        if not alarms_active:
            st.success("Wszystkie parametry w normie. Brak aktywnych zagrożeń.")
else:
    st.info("Kliknij przycisk powyżej, aby przeanalizować plik access.log.")