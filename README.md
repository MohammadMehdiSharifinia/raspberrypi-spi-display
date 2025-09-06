# Raspberry Pi ILI9341 Display Manager (Persian Support)
# مدیریت نمایشگر ILI9341 رزبری‌پای با پشتیبانی فارسی

---
## 📝 How to write Persian text | چطور فارسی بنویسیم

- All Python files must be saved as **UTF-8**.  
  همه فایل‌های پایتون باید با **UTF-8** ذخیره شوند.  

- At the top of each `.py` file, add:  
  بالای هر فایل `.py` این خط را بگذارید:
  ```python
  # -*- coding: utf-8 -*-

## ✨ Features | امکانات
- Show full background image | نمایش تصویر بکگراند
- Draw text and numbers (with Persian/Arabic support) | نمایش متن و عدد فارسی
- Automatic English→Persian digits conversion | تبدیل خودکار اعداد انگلیسی به فارسی
- Proper Persian text shaping (with `arabic-reshaper` + `python-bidi`)  
  پشتیبانی از اتصال حروف و نمایش راست‌به‌چپ
- Optional background box for text | نمایش متن با یا بدون بکگراند
- Horizontal flip (Mirror) | فلیپ افقی تصویر و متن

---

## 🛠 Requirements | پیش‌نیازها

### Hardware | سخت‌افزار
- Raspberry Pi (recommended 3/4) | رزبری‌پای (مدل ۳ یا ۴ پیشنهاد می‌شود)
- ILI9341 LCD connected via SPI | نمایشگر ILI9341 با ارتباط SPI

### Software | نرم‌افزار
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-spidev python3-rpi.gpio
pip3 install arabic-reshaper python-bidi jdatetime
