# 🛠️ LOREM_DDoS

![Banner Jaringan](https://example.com/banner-jaringan.jpg) <!-- Ganti dengan banner Anda -->

**Tools analisis jaringan canggih** dengan dukungan multi-platform dan antarmuka interaktif.

## 🌍 Kompatibilitas Lengkap

### ✔️ Platform yang Didukung Penuh
| Sistem Operasi       | Scan Port | Serangan DDoS | Sniffing Paket  | Tes API  | Catatan                   |
|----------------------|-----------|---------------|-----------------|----------|---------------------------|
| **Linux**            | ✅ Penuh  | ✅           | ✅ Paket mentah | ✅      | Performa terbaik          |
| **macOS**            | ✅ Penuh  | ✅           | ⚠️ Terbatas     | ✅      | Butuh libpcap             |
| **Windows WSL2**     | ✅ Penuh  | ✅           | ⚠️ Sebagian     | ✅      | Tidak support raw socket  |
| **Termux (Android)** | ✅        | ⚠️           | ❌              | ✅      | Akses jaringan terbatas   |
| **ChromeOS**         | ✅        | ⚠️           | ❌              | ✅      | Mode Linux container      |

### ☁️ Dukungan Cloud & Virtual
| Lingkungan        | Dukungan  | Keterbatasan                 |
|-------------------|-----------|------------------------------|
| AWS EC2           | ⚠️       | Sniffing tidak bekerja        |
| Google Cloud      | ⚠️       | Pembatasan request            |
| Docker            | ✅       | Gunakan `--net=host`          |
| VirtualBox/VMware | ✅ Penuh | Mode bridged direkomendasikan |

### 📱 Perangkat Mobile & Khusus
| Perangkat        | Tingkat Dukungan | Kebutuhan                 |
|------------------|------------------|---------------------------|
| Raspberry Pi     | ✅ Penuh         | Pendingin disarankan      |
| Orange Pi        | ✅ Penuh         | Tersedia versi ARM64      |
| Android (Termux) | ⚠️ Dasar         | Tidak bisa capture paket  |
| iPad (iSH)       | ⚠️ Terbatas      | Lingkungan Alpine Linux   |

## 📥 Instalasi Universal

```bash
# Untuk Linux/macOS/WSL
curl -sSL https://install.example.com/tool-jaringan | bash

# Windows (via WSL)
wsl --install -d Ubuntu
sudo apt update && sudo apt install python3-pip libpcap-dev
```

## 💪 Fitur Adaptif

Tool ini secara cerdas menyesuaikan diri:

1. **Mode Low-Power** - Otomatis mengurangi thread di perangkat lemah
2. **Deteksi Cloud** - Menonaktifkan fitur terlarang di VPS
3. **Mekanisme Cadangan** - Metode alternatif ketika root tidak tersedia

## ⚡ Performa Berbagai Perangkat

| Perangkat         | Port/detik | Request DDoS/detik |
|-------------------|------------|--------------------|
| PC High-end       | 5,000+     | 50,000+            |
| MacBook M1        | 3,200      | 28,000             |
| Raspberry Pi 4    | 800        | 5,000              |
| Android (Termux)  | 150        | 1,200              |

## ⚠️ Perhatian Hukum

**PENTING**: Tool ini otomatis:
- Menonaktifkan fitur terlarang di yurisdiksi tertentu
- Membatasi capture paket di jaringan perusahaan
- Mencegah serangan ke domain .gov/.mil

## 🔍 Tips Ahli

1. **Untuk perangkat lemah**:
   ```bash
   python3 main.py --low-power
   ```

2. **Di lingkungan terbatas**:
   ```bash
   python3 main.py --stealth --timeout 5
   ```

3. **Cek kompatibilitas**:
   ```bash
   python3 main.py --diagnose

   ```

---

### **🔒 Hak Akses (Privileges)**
|                           | `sudo python3`                     | `python3`                          |
|---------------------------|------------------------------------|------------------------------------|
| **Level Akses**           | Root (superuser)                   | User biasa                         |
| **Port Dibawah 1024**     | ✅ Bisa akses                      | ❌ Tidak bisa akses               |
| **Raw Socket/Packet**     | ✅ Full capability                 | ❌ Terbatas                       |
| **File System**           | ✅ Baca/tulis semua file           | ❌ Hanya file user yang boleh     |

---

### **🛠️ Dampak pada Fitur Tool**
| Fitur                  | Dengan `sudo`                     | Tanpa `sudo`                       |
|------------------------|-----------------------------------|------------------------------------|
| **Port Scanning**      | ✅ Scan semua port (1-65535)      | ⚠️ Hanya port >1024 efektif       |
| **DDoS Attack**        | ✅ Maximum power                  | ⚠️ Mungkin gagal di port rendah   |
| **Packet Sniffing**    | ✅ Capture semua paket            | ❌ Tidak bekerja                  |
| **API Testing**        | ✅ Normal                         | ✅ Normal                         |
| **Traceroute**         | ✅ Akurat                         | ⚠️ Tidak akurat                   |

---

### **🖥️ Cara Mengoperasikan **
```bash
# disarankan memakai environtment python dengan cara
python3 -m venv venv
source venv/bin/activate

# Install persyaratan
pip install -r requirements.txt

# Update proxy:
python3 proxy_scraper.py

```
### Dua cara mengoperasikan tool ini:
Jalankan tanpa akses root
```bash
# Tanpa akses root
python3 main.py
```
Atau jalankan dengan akses root
```bash
# Akses root
sudo python3 main.py
```

---

### **⚡ Performance Impact**
|                          | `sudo python3`                     | `python3`                          |
|--------------------------|------------------------------------|------------------------------------|
| **Kecepatan**            | ⚠️ Sedikit lebih lambat            | ✅ Lebih cepat                    |
| **Stabilitas**           | ❌ Risiko crash tinggi             | ✅ Lebih stabil                   |
| **Logging**              | ✅ Log sistem penuh                | ⚠️ Hanya log aplikasi             |

---

### **🔐 Security Considerations**
|                          | `sudo`                             | Non-`sudo`                         |
|--------------------------|------------------------------------|------------------------------------|
| **Risiko Keamanan**      | ❌ Tinggi (remote code execution)  | ✅ Rendah                         |
| **Audit Trail**          | ✅ Tercatat di /var/log/auth.log   | ❌ Tidak tercatat khusus          |
| **System Protection**    | ❌ Bisa modifikasi sistem          | ✅ Hanya user space               |

---

### **💡 Rekomendasi Penggunaan**
1. **Pakai `sudo` hanya untuk:**
   - Packet sniffing
   - Scan port bawah 1024
   - Serangan DDoS ke port sistem

2. **Hindari `sudo` ketika:**
   - Testing API biasa
   - Scan port tinggi (>1024)
   - Di lingkungan tidak tepercaya

3. **Alternatif lebih aman:**
   ```bash
   # Beri hak spesifik tanpa full root
   sudo setcap cap_net_raw+eip $(which python3)
   python3 main.py  # Bisa sniffing tanpa sudo
   ```

---

---

**Terakhir Diuji Pada**:  
- Ubuntu 22.04 LTS  
- Windows 11 WSL2  
- macOS Ventura 13.4  
- Termux v0.118 (Android 13)
- Kali Linux


**SUPPORT ME BY**:    
[![SAWER ME!](https://saweria.co/dronxploit)]
**FOLLOW ME ON**:    
[![FOLLOW ME!](https://instagram.com/dronxploit)]

**Contriubtor**
[![CONTRIBUTOR](https://github.com/palacita135)]
