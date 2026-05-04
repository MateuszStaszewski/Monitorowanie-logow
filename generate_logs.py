import random
import time
from datetime import datetime

ips = ["192.168.1.10", "10.0.0.5", "172.16.0.20", "185.12.34.56", "91.200.12.3"]
methods = ["GET", "POST"]
urls = ["/index.html", "/login", "/admin", "/api/data"]
statuses = [200, 404, 401, 500]

def generate_log():
    ip = random.choice(ips)
    method = random.choice(methods)
    url = random.choice(urls)
    # 200 (OK) występuje najczęściej, 401 (Unauthorized) rzadziej
    status = random.choices(statuses, weights=[70, 10, 15, 5])[0] 
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {random.randint(100, 5000)}'

with open("access.log", "w") as f:
    for _ in range(100): # Wygeneruje 100 wpisów
        log = generate_log()
        f.write(log + "\n")
        time.sleep(0.05) 

print("Plik access.log został pomyślnie wygenerowany!")