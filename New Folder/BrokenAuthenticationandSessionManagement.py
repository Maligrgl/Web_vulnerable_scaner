import requests
from bs4 import BeautifulSoup
import sys

# Hedef web sitesinin URL'sini belirleyin (örnek bir URL kullanmayın)

if len(sys.argv) != 2:
    print("Usage: python3 Sqlinjection.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]


# Oturum açma bilgilerinizi belirleyin
username = "your_username"
password = "your_password"

# Bir requests oturumu oluşturun
session = requests.Session()

# Hedef web sitesinin oturum açma sayfasını alın
response = session.get(target_url)

# Oturum açma sayfasının HTML içeriğini ayrıştırın
soup = BeautifulSoup(response.text, "html.parser")

# Oturum açma sayfasının HTML'sini yazdırarak kontrol edin
print(soup.prettify())

# Oturum açma formunu bulun
form = soup.find("form", {"method": "post"})
if form is None:
    print("Oturum açma formu bulunamadı!")
    sys.exit(1)

# Oturum açma formunun gerekli alanlarını bulun
username_field = form.find("input", {"name": "user"})
password_field = form.find("input", {"name": "pass"})
csrf_token_field = form.find("input", {"name": "csrf_token"})

if username_field is None or password_field is None or csrf_token_field is None:
    print("Gerekli form alanları bulunamadı!")
    sys.exit(1)

# Oturum açma formunun eylem URL'sini bulun
action_url = form["action"]

# Oturum açma formunun verilerini oluşturun
data = {
    username_field["name"]: username,
    password_field["name"]: password,
    csrf_token_field["name"]: csrf_token_field["value"]
}

# Oturum açma formunun verilerini eylem URL'sine gönderin
response = session.post(target_url + action_url, data=data)

# Oturum açma işleminin başarılı olup olmadığını kontrol edin
if response.status_code == 200:
    print("Oturum açma başarılı!")
else:
    print("Oturum açma başarısız!")
    sys.exit(1)

# Oturum açtıktan sonra, hedef web sitesinin diğer sayfalarını kazıyabilirsiniz
profile_url = "https://example.com/profile"
response = session.get(profile_url)

# Profil sayfasının HTML içeriğini ayrıştırın
soup = BeautifulSoup(response.text, "html.parser")

# Profil sayfasından istediğiniz bilgileri çıkarın
name = soup.find("div", {"class": "name"}).text
email = soup.find("div", {"class": "email"}).text
score = soup.find("div", {"class": "score"}).text

# Profil sayfasından çıkarılan bilgileri yazdırın
print(f"Ad: {name}")
print(f"E-posta: {email}")
print(f"Puan: {score}")
