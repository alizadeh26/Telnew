import asyncio
import re
import base64
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# ================== تنظیمات ==================
api_id = 12345678          # ← از my.telegram.org بگیر
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # ← از my.telegram.org بگیر

# لیست کانال‌ها (username بدون @ یا لینک کامل t.me/)
channels = [
    'meli_proxyy',
    'alpha_v2ray_group',
    'vpnplusee_free',
    'BestV2rayConfig',
    'v2rayng_config',
    'freev2rayng',
    'V2rayCollector',
    'Proxy_TG',
    'iran_v2ray',
    # هر کانال دیگه‌ای که می‌خوای اضافه کن
]

limit_per_channel = 40     # تعداد پیام اخیر هر کانال
# ============================================

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start()
    print("✅ لاگین به تلگرام انجام شد")

    configs = set()   # برای حذف خودکار تکراری‌ها

    protocols = ['vless', 'vmess', 'trojan', 'ss', 'ssr']

    for ch in channels:
        try:
            entity = await client.get_entity(ch)
            print(f"📡 در حال خواندن کانال: {entity.title}")

            async for message in client.iter_messages(entity, limit=limit_per_channel):
                if not message.message:
                    continue

                text = message.message

                # استخراج تمام لینک‌های پروتکل
                for proto in protocols:
                    # الگوی دقیق + پشتیبانی از remark (#...)
                    matches = re.findall(
                        rf'(?i){proto}://[^\s#]+(?:#[^\s]+)?',
                        text
                    )
                    for m in matches:
                        cleaned = m.strip().rstrip('.,;!?')
                        if len(cleaned) > 20:   # فیلتر لینک‌های خراب
                            configs.add(cleaned)

        except FloodWaitError as e:
            print(f"⏳ FloodWait: {e.seconds} ثانیه صبر کن")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"⚠️ خطا در کانال {ch}: {e}")

    # ====================== ذخیره ======================
    config_list = sorted(list(configs))

    # فایل معمولی (خط به خط)
    with open('all_configs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(config_list))

    # فایل Base64 (سابسکریپشن یونیورسال)
    b64_content = base64.b64encode('\n'.join(config_list).encode('utf-8')).decode('utf-8')
    with open('sub_base64.txt', 'w', encoding='utf-8') as f:
        f.write(b64_content)

    print(f"\n🎉 تمام! {len(config_list)} کانفیگ جمع‌آوری شد")
    print("📁 all_configs.txt")
    print("📁 sub_base64.txt")

if __name__ == '__main__':
    asyncio.run(main())
