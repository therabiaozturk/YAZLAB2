
# Drone Tabanlı Teslimat Sisteminde Rota Planlaması 🚁🧠

Bu proje, **Python** dili ile geliştirilmiş, şehir içi **drone teslimatlarını** optimize etmeye yönelik bir rota planlama sistemidir. Sistem; **Genetik Algoritmalar** ve **Kısıt Tatmin Problemi (CSP)** tekniklerini birleştirerek teslimat noktaları arasında en verimli güzergahı bulmayı amaçlamaktadır. 

## 🔍 Amaç

- Teslimat noktaları arasında **optimal rotayı** hesaplamak  
- **Uçuşa yasak bölgelerden** kaçınmak  
- Kullanıcı dostu bir **arayüzle** rotayı görselleştirmek  
- Gerçek zamanlı kararlar ve esnek yapı sağlamak

## 🛠 Kullanılan Teknolojiler

- **Python 3.11**
- **Tkinter** – Arayüz
- **Matplotlib** – Görselleştirme
- **NumPy** – Sayısal hesaplamalar
- **OOP** – Nesne tabanlı yapı

## 📁 Proje Yapısı

```
YAZLAB2/
├── main.py              # Uygulama giriş noktası
├── genetik.py           # Genetik algoritma uygulaması
├── csp.py               # Kısıt Tatmin Problemi çözümü
├── drone.py             # Drone sınıfı
├── teslimat.py          # Teslimat mantığı
├── noflyzone.py         # Uçuşa yasak bölgeler
├── arayuz.py            # Tkinter GUI
├── gorsel.py            # Harita ve rota çizimi
└── utils.py             # Yardımcı fonksiyonlar
```

## 🧠 Algoritmalar

### Genetik Algoritma
- Bireyler = Rotalar
- Fitness = Toplam mesafe + yasak bölge cezası
- Çaprazlama ve mutasyon ile gelişim sağlanır

### Kısıt Tatmin Problemi (CSP)
- Teslimatlar sıralanırken kısıtlar uygulanır
- No-fly zone, zaman, kapasite gibi sınırlamalar gözetilir

## 🖼 Arayüz Özellikleri

- Teslimat noktalarını harita üzerinden ekleme
- No-fly zone'ları çizme
- “Rota Hesapla” butonuyla işlemi başlatma
- Dinamik rota görselleştirmesi

## 🚀 Başlatma

Proje kök dizininde şu komutla çalıştırabilirsiniz:

```bash
python main.py
```

## 📊 Test Senaryoları

| Nokta Sayısı | Yasak Bölge | Ortalama Süre | Başarı |
|--------------|-------------|----------------|--------|
| 5            | 1           | 3.4 sn         | ✅     |
| 10           | 2           | 5.8 sn         | ✅     |
| 20           | 3           | 9.2 sn         | ✅     |

## 📌 Anahtar Kelimeler

**Drone, optimizasyon, genetik, kısıt, haritalama**

## 📄 Lisans

Bu proje akademik kullanım için geliştirilmiştir.
