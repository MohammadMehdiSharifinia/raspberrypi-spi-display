# Raspberry Pi ILI9341 Display Manager
# مدیریت نمایشگر ILI9341 رزبری‌پای

این پروژه یک کلاس ساده به نام **DisplayManager** فراهم می‌کند برای کار با نمایشگر ILI9341 روی Raspberry Pi.  
با این کلاس می‌توانید تصویر بکگراند و متن فارسی (با اعداد فارسی) را روی نمایشگر نشان دهید.  

This project provides a simple **DisplayManager** class to work with an ILI9341 LCD on Raspberry Pi.  
It supports showing background images and Persian text (with Persian digits) on the screen.  

---

## ✨ Features | امکانات
- Display background image | نمایش بکگراند
- Show Persian text and numbers | نمایش متن و عدد فارسی
- Automatic English→Persian digit conversion | تبدیل خودکار اعداد انگلیسی به فارسی
- Optional background box for text | متن با یا بدون بکگراند
- Horizontal flip (mirror) | فلیپ افقی

---

## 🛠 Requirements | پیش‌نیازها
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-spidev python3-rpi.gpio
pip3 install arabic-reshaper python-bidi jdatetime
