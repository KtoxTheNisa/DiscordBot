# Discord Level Bot 🤖

2. sınıf İleri Programlama dersi projesi.

## Özellikler
- ✅ XP/Level Sistemi
- ✅ Ekonomi (BotCoin)
- ✅ Oyunlar (Kelime, Düello)
- ✅ Sosyal (Evlilik, Rep)
- ✅ Yönetim (Rol Panelleri, Kick, Ban)

## Teknolojiler
- Python 3.10+
- Discord.py (Async)
- SQLite (aiosqlite)
- PIL (Resim işleme)

## Kurulum

### 1. Gereksinimleri yükle
```bash
pip install -r requirements.txt
```

### 2. .env dosyası oluştur
```env
TOKEN=your_token_here
OWNER_ID=your_id
CLIENT_SECRET=your_secret
SECRET_KEY=random_key
```

### 3. Botu çalıştır
```bash
python main.py
```

## Komutlar

### XP/Level
- `!profile [@kullanıcı]` - Profil göster
- `!stat` - XP sıralaması
- `!levelver @kullanıcı 10` - (Admin) Level ver

### Ekonomi
- `!borsa` - BotCoin fiyatı
- `!coinal 5` - 5 BotCoin al
- `!günlük` - Günlük ödül
- `!soygun` - Risk-reward oyunu

## Mimari
```
bot/
├── main.py              # Ana bot
├── config.py            # Ayarlar
├── database.py          # Veritabanı yönetimi
├── cogs/
│   ├── stats.py         # XP/Level
│   ├── ekonomi.py       # Para sistemi
│   ├── oyun.py          # Oyunlar
│   ├── sosyal.py        # Sosyal özellikler
│   └── yonetim.py       # Admin komutları
└── data/
    └── database.db      # SQLite DB
```

## Veritabanı Şeması

### users tablosu
| Alan | Tür | Açıklama |
|------|-----|----------|
| server_id | INTEGER | Sunucu ID |
| user_id | INTEGER | Kullanıcı ID |
| level | INTEGER | Seviye |
| xp | INTEGER | Deneyim puanı |
| botcoin | INTEGER | Para |
| message | INTEGER | Mesaj sayısı |

## Lisans
MIT License

## İletişim
- Discord: @username
- Email: email@example.com