import requests
import random

def main():
    # اینجا لینک‌های کانفیگ رو اضافه کن
    config_urls = [
            "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
            "https://raw.githubusercontent.com/code3-dev/v-data/refs/heads/main/vip",
            "https://raw.githubusercontent.com/10ium/HiN-VPN/refs/heads/main/subscription/base64/vless",
        # لینک‌های دیگه رو اینجا اضافه کن
    ]
    
    all_configs = []
    
    for url in config_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                configs = response.text.split('\n')
                vless_configs = [cfg.strip() for cfg in configs 
                               if cfg.strip().startswith('vless://')]
                all_configs.extend(vless_configs)
        except:
            pass
    
    # انتخاب 30 تا تصادفی
    selected = random.sample(all_configs, min(30, len(all_configs)))
    
    # ذخیره در فایل
    with open('configs/working-configs.txt', 'w') as f:
        for config in selected:
            f.write(config + '\n')

if __name__ == "__main__":
    main()
