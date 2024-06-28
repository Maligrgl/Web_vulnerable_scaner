import requests
import random
import string
import os
import sys

# Test edilecek web sitesinin URL'sini tanımla
if len(sys.argv) != 2:
    print("Usage: python3 Sqlinjection.py <target_url>")
    sys.exit(1)

target_url = sys.argv[1]

# Dosya yükleme işlevinin parametrelerini tanımla
upload_param = "file"
submit_param = "submit"

# Test edilecek dosya türlerini ve uzantılarını tanımla
file_types = ["text", "image", "audio", "video", "executable", "script", "archive"]
file_extensions = [".txt", ".jpg", ".mp3", ".mp4", ".exe", ".php", ".zip"]

# Test edilecek dosya boyutlarını tanımla (bayt cinsinden)
file_sizes = [1024, 2048, 4096, 8192, 16384, 32768, 65536]

# Test sonuçlarını saklamak için bir liste oluştur
test_results = []

# Her dosya türü için bir döngü başlat
for file_type in file_types:
    # Her dosya boyutu için bir döngü başlat
    for file_size in file_sizes:
        # Rastgele bir dosya adı oluştur
        file_name = "".join(random.choice(string.ascii_letters) for _ in range(10))
        
        # Dosya türüne uygun bir dosya uzantısı ekle
        file_name += file_extensions[file_types.index(file_type)]
        
        # Dosya türüne uygun bir dosya içeriği oluştur
        file_content = os.urandom(file_size)
        
        # Dosyayı geçici olarak kaydet
        with open(file_name, "wb") as f:
            f.write(file_content)
        
        # Dosyayı web sitesine yükle
        files = {upload_param: (file_name, file_content)}
        data = {submit_param: "Upload"}
        response = requests.post(target_url, files=files, data=data)
        
        # Yanıtı analiz et
        if response.status_code == 200:
            # Yanıt başarılı ise
            if file_type == "script" and file_name in response.text:
                # Dosya türü script ise ve dosya adı yanıtta görünüyorsa
                # Zafiyet tespit edildi
                test_result = (file_name, file_size, file_type, "Vulnerable")
            else:
                # Dosya türü script değilse veya dosya adı yanıtta görünmüyorsa
                # Zafiyet tespit edilmedi
                test_result = (file_name, file_size, file_type, "Safe")
        else:
            # Yanıt başarısız ise
            # Zafiyet tespit edilemedi
            test_result = (file_name, file_size, file_type, "Unknown")
        
        # Test sonucunu listeye ekle
        test_results.append(test_result)
        
        # Dosyayı sil
        os.remove(file_name)

# Test sonuçlarını rapor et
print("FILE UPLOAD ZAFİYETİ TEST RAPORU")
print("Dosya Adı\tDosya Boyutu\tDosya Türü\tSonuç")
for test_result in test_results:
    print("\t".join(str(x) for x in test_result))
