import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime

channels = ['filembad', 'Farah_VPN', 'persianvpnhub']
max_per_channel = 500
max_pages = 200

# رجکس دقیق برای گرفتن کانفیگ‌ها
regex = re.compile(r'(?i)(?:vless|vmess|trojan|ss|ssr)://[^\s<>"\']+')

def scrape_channel(channel):
    configs = []
    seen = set()
    url = f'https://t.me/s/{channel}'
    
    for _ in range(max_pages):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                break
                
            soup = BeautifulSoup(r.text, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message')
            
            if not messages:
                break
                
            for msg in messages:
                text = msg.get_text(separator=' ', strip=True)
                matches = regex.findall(text)
                
                for config in matches:
                    if config not in seen:
                        seen.add(config)
                        configs.append(config)
                        
                if len(configs) >= max_per_channel:
                    return configs[:max_per_channel]
            
            # صفحه بعدی (pagination)
            last_msg = messages[-1]
            date_a = last_msg.find('a', class_='tgme_widget_message_date')
            if date_a and date_a.get('href'):
                post_id = date_a['href'].split('/')[-1]
                url = f'https://t.me/s/{channel}?before={post_id}'
            else:
                break
                
        except Exception as e:
            print(f"Error in {channel}: {e}")
            break
            
    return configs[:max_per_channel]

# =============== چک زمان آپدیت ===============
last_file = 'last_update.txt'
if os.path.exists(last_file):
    with open(last_file) as f:
        last = float(f.read().strip())
    if time.time() - last < 6000:   # ۱۰۰ دقیقه = ۶۰۰۰ ثانیه
        print("هنوز ۱۰۰ دقیقه نشده. رد شد.")
        exit(0)

# =============== اسکریپ کردن ===============
print("شروع اسکریپ از کانال‌ها...")
all_configs = set()

for ch in channels:
    print(f"در حال اسکریپ {ch} ...")
    ch_confs = scrape_channel(ch)
    print(f"   → {len(ch_confs)} کانفیگ جدید")
    all_configs.update(ch_confs)

all_list = list(all_configs)
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

header = f"""# 🚀 Persian VPN Subscription
# Updated: {timestamp}
# Total: {len(all_list)} unique configs
# Channels: {', '.join(channels)}
# Auto-update every ~100 minutes via GitHub Actions

"""

content = header + '\n'.join(all_list)

with open('subscription.txt', 'w', encoding='utf-8') as f:
    f.write(content)

# نسخه base64
import base64
b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
with open('subscription_base64.txt', 'w', encoding='utf-8') as f:
    f.write(b64)

# ذخیره زمان آخرین آپدیت
with open(last_file, 'w') as f:
    f.write(str(time.time()))

print(f"✅ تمام شد! {len(all_list)} کانفیگ یونیک ذخیره شد.")
