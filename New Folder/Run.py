import subprocess
import sys

# Dosya yollarını burada ekleyeceksiniz
dosya_yollari = {
    "1": "/root/Desktop/New Folder/CommandInjection.py",
    "2": "/root/Desktop/New Folder/FileUpload.py",
    "3": "/root/Desktop/New Folder/Idor.py",
    "4": "/root/Desktop/New Folder/Sqlinjection.py",
    "5": "/root/Desktop/New Folder/Xss.py",
    "6": "/root/Desktop/New Folder/BrokenAuthenticationandSessionManagement.py",
    # Diğer dosya yollarını buraya ekleyin
}

# Saldırı türleri listesi
saldiri_isimleri = [
    "Command Injection",
    "File Upload",
    "IDOR",
    "SQL Injection",
    "Cross-Site Scripting",
    "Broken Authenticationand Session Management"
]

def main():
    # Kullanıcıdan hedef siteyi al
    hedef_site = input("Hedef Site'yi girin: ")
    
    # Saldırı türlerini göster
    print("Mevcut saldırı türleri:")
    for i, isim in enumerate(saldiri_isimleri, 1):
        print(f"{i}. {isim}")

    # Kullanıcıdan saldırı numarasını al
    secim = input("Seçmek istediğiniz saldırının numarasını girin: ")

    # Saldırı dosyasını al
    dosya = dosya_yollari.get(secim)
    if dosya:
        subprocess.run(["python3", dosya, hedef_site])
    else:
        print(f"{secim}. {saldiri_isimleri[int(secim) - 1]} için dosya yolu bulunamadı.")

if __name__ == "__main__":
    main()
