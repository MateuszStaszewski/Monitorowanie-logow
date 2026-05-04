import re
from collections import Counter

def parse_logs(file_path):
    log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?"\s(?P<status>\d{3})'
    suspicious_ips = []

    try:
        with open(file_path, "r") as f:
            for line in f:
                match = re.search(log_pattern, line)
                if match:
                    ip = match.group('ip')
                    status = match.group('status')
                    
                    if status == '401':
                        suspicious_ips.append(ip)
    except FileNotFoundError:
        return None

    return Counter(suspicious_ips)

if __name__ == "__main__":
    print("Analiza logów w toku...")
    result = parse_logs("access.log")
    
    if result is None:
        print("Nie znaleziono pliku access.log!")
    else:
        print("\n--- RAPORT PODEJRZANYCH AKTYWNOŚCI (STATUS 401) ---")
        for ip, count in result.items():
            print(f"IP: {ip} | Liczba nieudanych logowań: {count}")
            if count > 5:
                print(f"!!! ALARM: Możliwy atak typu Brute-Force z IP: {ip} !!!")