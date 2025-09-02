import requests
import random
import re
import time
from datetime import datetime

def fetch_configs_from_urls(url_list):
    """Fetch configs from multiple URLs"""
    all_configs = []
    
    for url in url_list:
        try:
            print(f"Fetching from: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                # پیدا کردن تمام کانفیگ‌های vless با regex بهبود یافته
                vless_pattern = r'vless://[a-zA-Z0-9-@.:?=&%#/_]+'
                vless_configs = re.findall(vless_pattern, response.text)
                
                # همچنین خط به خط بررسی کنیم
                lines = response.text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('vless://'):
                        # حذف کاراکترهای اضافی در انتها
                        clean_line = re.sub(r'[`<>"\'{}|\\^]', '', line)
                        if clean_line not in vless_configs:
                            vless_configs.append(clean_line)
                
                # فقط کانفیگ‌های معتبر رو اضافه کن (بدون حذف duplicates الان)
                valid_configs = [cfg for cfg in vless_configs if is_valid_vless(cfg)]
                all_configs.extend(valid_configs)
                
                print(f"Found {len(valid_configs)} vless configs from {url}")
                
            else:
                print(f"Failed to fetch {url}, status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error fetching from {url}: {str(e)}")
        
        # تاخیر کوتاه بین درخواست‌ها
        time.sleep(1)
    
    return all_configs

def is_valid_vless(config):
    """Check if a vless config is valid"""
    try:
        if not config.startswith('vless://'):
            return False
        
        # بررسی وجود UUID و آدرس سرور
        if '@' not in config:
            return False
        
        # بررسی ساختار کلی
        parts = config.split('vless://')[1].split('@')
        if len(parts) < 2:
            return False
        
        uuid_part = parts[0]
        # UUID می‌تواند با ed یا e6 شروع شود (مشاهده شده در نمونه‌ها)
        if len(uuid_part) < 30:  # حداقل طول UUID
            return False
        
        return True
        
    except:
        return False

def main():
    # لیست منابع کانفیگ
    config_urls = [
            "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
            "https://raw.githubusercontent.com/code3-dev/v-data/refs/heads/main/vip",
            "https://raw.githubusercontent.com/10ium/HiN-VPN/refs/heads/main/subscription/base64/vless",
        # اضافه کردن لینک‌های دیگر
    ]
    
    print("Fetching configs from sources...")
    all_configs = fetch_configs_from_urls(config_urls)
    
    print(f"Total vless configs found: {len(all_configs)}")
    
    if not all_configs:
        print("No configs found! Using sample configs as fallback.")
        # نمونه کانفیگ‌های پشتیبان
        all_configs = [
            "vless://df0680ca-e43c-498d-ed86-8e196eedd012@185.153.183.211:8880/?type=grpc&encryption=none&flow=#Test-Config-1",
            "vless://e105e56a-5f81-41a2-ab44-bfffc9b00674@45.12.143.191:20329?security=reality&encryption=none&pbk=Lj3MXlg16CTFHtU88acSS-ACfGnwJ_xkU6dC6k8OeDo&fp=chrome&type=tcp&sni=yahoo.com&sid=4602ee9f9f36#Test-Config-2",
            "vless://bfc78cd8-5951-4803-8d6c-4cedef8cd420@95.164.85.109:59374/?type=tcp&encryption=none&flow=&sni=yahoo.com&fp=chrome&security=reality&pbk=ZsswZuBV8bEGQWFrpShCilSytnDUj0kwHFhTSLXzOwc&sid=d21e7c#Test-Config-3",
            "vless://8672bdcd-e331-464d-9ed8-93a242ca7d2e@89.44.197.77:15946?path=%2F&security=none&encryption=none&type=ws#Test-Config-4",
            "vless://e4824193-4f54-453b-d037-88368e85ef0e@45.82.251.80:8880?encryption=none&security=none&type=grpc#Test-Config-5"
        ]
    
    # حذف duplicates (بعد از اینکه همه رو گرفتیم)
    unique_configs = list(set(all_configs))
    print(f"Unique vless configs: {len(unique_configs)}")
    
    # همیشه لیست کاملاً تصادفی جدید ایجاد کن - حتی اگر منابع تغییر نکرده باشن
    random.shuffle(unique_configs)
    
    # انتخاب 30 تا تصادفی (یا کمتر اگر تعداد کم باشه)
    selected_count = min(30, len(unique_configs))
    selected_configs = unique_configs[:selected_count]
    
    # ذخیره در فایل
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('configs/working-configs.txt', 'w', encoding='utf-8') as f:
        f.write("# Auto-generated vless configs\n")
        f.write(f"# Last update: {current_time}\n")
        f.write(f"# Total available: {len(unique_configs)}\n")
        f.write(f"# Randomly selected: {len(selected_configs)}\n\n")
        
        for i, config in enumerate(selected_configs, 1):
            f.write(f"# Config {i}\n")
            f.write(config + '\n\n')
    
    print(f"Saved {len(selected_configs)} randomly selected configs to configs/working-configs.txt")
    print(f"Update time: {current_time}")

if __name__ == "__main__":
    main()
