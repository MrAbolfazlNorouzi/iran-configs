import requests
import random
import re
import urllib.parse

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
                
                # حذف duplicates و فیلتر کردن
                unique_configs = list(set(vless_configs))
                valid_configs = [cfg for cfg in unique_configs if is_valid_vless(cfg)]
                
                all_configs.extend(valid_configs)
                print(f"Found {len(valid_configs)} valid vless configs from {url}")
                
            else:
                print(f"Failed to fetch {url}, status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error fetching from {url}: {str(e)}")
    
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

def filter_working_configs(configs):
    """فیلتر کردن کانفیگ‌هایی که احتمال کار کردن بیشتری دارند"""
    preferred_configs = []
    other_configs = []
    
    for config in configs:
        # اولویت به کانفیگ‌های reality و tls
        if 'reality' in config or 'tls' in config:
            preferred_configs.append(config)
        else:
            other_configs.append(config)
    
    return preferred_configs + other_configs

def main():
    # لیست منابع کانفیگ (با منابع واقعی جایگزین کن)
    config_urls = [
            "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
            "https://raw.githubusercontent.com/code3-dev/v-data/refs/heads/main/vip",
            "https://raw.githubusercontent.com/10ium/HiN-VPN/refs/heads/main/subscription/base64/vless",
        # اضافه کردن لینک‌های دیگر
    ]
    
    print("Fetching configs from sources...")
    all_configs = fetch_configs_from_urls(config_urls)
    
    print(f"Total unique vless configs found: {len(all_configs)}")
    
    if not all_configs:
        print("No configs found! Using sample configs as fallback.")
        # نمونه کانفیگ‌های پشتیبان براساس نمونه‌های شما
        all_configs = [
            "vless://df0680ca-e43c-498d-ed86-8e196eedd012@185.153.183.211:8880/?type=grpc&encryption=none&flow=#Test-Config-1",
            "vless://e105e56a-5f81-41a2-ab44-bfffc9b00674@45.12.143.191:20329?security=reality&encryption=none&pbk=Lj3MXlg16CTFHtU88acSS-ACfGnwJ_xkU6dC6k8OeDo&fp=chrome&type=tcp&sni=yahoo.com&sid=4602ee9f9f36#Test-Config-2"
        ]
    
    # اولویت‌بندی کانفیگ‌ها
    prioritized_configs = filter_working_configs(all_configs)
    
    # انتخاب حداکثر 30 تا
    selected_configs = prioritized_configs[:30] if len(prioritized_configs) > 30 else prioritized_configs
    
    # اگر هنوز کمتر از 10 تا هست، از بقیه هم انتخاب کن
    if len(selected_configs) < 10:
        remaining = [cfg for cfg in all_configs if cfg not in selected_configs]
        additional = min(30 - len(selected_configs), len(remaining))
        selected_configs.extend(random.sample(remaining, additional))
    
    # ذخیره در فایل
    with open('configs/working-configs.txt', 'w', encoding='utf-8') as f:
        f.write("# Auto-generated vless configs\n")
        f.write("# Updated automatically\n\n")
        
        for i, config in enumerate(selected_configs, 1):
            f.write(f"# Config {i}\n")
            f.write(config + '\n\n')
    
    print(f"Saved {len(selected_configs)} configs to configs/working-configs.txt")
    print("Sample of saved configs:")
    for i, config in enumerate(selected_configs[:3], 1):
        print(f"{i}. {config[:80]}...")

if __name__ == "__main__":
    main()
