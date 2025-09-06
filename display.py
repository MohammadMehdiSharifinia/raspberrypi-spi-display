#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DisplayManager: مدیریت نمایشگر ILI9341 با پشتیبانی کامل از فارسی
- بکگراند و متن روی یک فریم ترکیب می‌شوند.
- متن فارسی و اعداد فارسی به‌درستی نمایش داده می‌شوند.
- قابلیت فلیپ افقی (mirror).
- امکان رسم متن در هر جای صفحه با یا بدون بکگراند.
"""

import logging
from PIL import Image, ImageDraw, ImageFont, ImageOps

# تلاش برای وارد کردن کتابخانه‌های فارسی‌ساز
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_FARSI = True
except ImportError:
    HAS_FARSI = False

from Background import (
    ILI9341, prepare_image_for_display,
    DEFAULT_DISPLAY_WIDTH, DEFAULT_DISPLAY_HEIGHT,
    GPIO_DC, GPIO_RST, GPIO_BL,
    SPI_BUS, SPI_DEVICE, SPI_SPEED, DEFAULT_MADCTL
)

log = logging.getLogger("display")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# مسیر فونت فارسی
FONT_PATH = "/home/raspberrypi/IRANYekanLight.ttf"

# --- تبدیل اعداد انگلیسی به فارسی ---
def eng_to_farsi_numbers(text: str) -> str:
    digits_map = {str(i): chr(0x06F0 + i) for i in range(10)}  # Persian digits U+06F0..U+06F9
    return ''.join(digits_map.get(ch, ch) for ch in text)


class DisplayManager:
    def __init__(self):
        # فقط یک‌بار نمایشگر راه‌اندازی می‌شود
        self.dev = ILI9341(
            spi_bus=SPI_BUS,
            spi_device=SPI_DEVICE,
            spi_speed=SPI_SPEED,
            madctl=DEFAULT_MADCTL,
            gpio_dc=GPIO_DC,
            gpio_rst=GPIO_RST,
            gpio_bl=GPIO_BL
        )
        self.disp_w = DEFAULT_DISPLAY_WIDTH
        self.disp_h = DEFAULT_DISPLAY_HEIGHT
        self.current_img = Image.new("RGB", (self.disp_w, self.disp_h), (0, 0, 0))

    # ---------- Utilities ----------
    def _get_font(self, size: int):
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except Exception as e:
            log.error("Font not found or invalid: %s", e)
            return ImageFont.load_default()

    def _prepare_text(self, text: str) -> str:
        """تبدیل اعداد انگلیسی به فارسی + شکل‌دهی متن فارسی (در صورت وجود کتابخانه‌ها)"""
        text = eng_to_farsi_numbers(text)
        if HAS_FARSI:
            try:
                reshaped = arabic_reshaper.reshape(text)   # اتصال حروف فارسی
                return get_display(reshaped)              # راست‌به‌چپ شدن متن
            except Exception as e:
                log.warning("Arabic shaping failed: %s", e)
                return text
        else:
            log.warning("arabic_reshaper/python-bidi not installed, showing raw text")
            return text

    # ---------- API ----------
    def show_background(self, path: str, fit: str = "cover", mirror: bool = True):
        """بکگراند را بارگذاری می‌کند"""
        img = Image.open(path)
        img = prepare_image_for_display(img, self.disp_w, self.disp_h, fit)
        if mirror:
            img = ImageOps.mirror(img)
        self.current_img = img

    def clear(self, color=(0, 0, 0)):
        """پاک کردن کل صفحه با یک رنگ ثابت"""
        self.current_img = Image.new("RGB", (self.disp_w, self.disp_h), color)

    def draw_text(
        self,
        text: str,
        font_size: int = 20,
        bottom_offset: int = 72,
        fg=(0, 0, 0),
        bg=(255, 255, 255),
        box_w: int = 290,
        box_h: int = 40,
        mirror: bool = True,
        x: int = None,
        y: int = None,
        with_box: bool = True
    ):
        """
        متن/عدد را روی فریم فعلی قرار می‌دهد.
        - اگر with_box=True → متن داخل باکس رنگی (bg).
        - اگر with_box=False → متن بدون باکگراند (فقط متن).
        """
        text = self._prepare_text(text)
        font = self._get_font(font_size)

        if x is None:
            x = (self.disp_w - box_w) // 2
        if y is None:
            y1 = self.disp_h - 1 - bottom_offset
            y = y1 - box_h + 1
            if y < 0:
                y = 0

        # ایجاد تصویر موقت برای متن
        if with_box:
            box_img = Image.new("RGB", (box_w, box_h), bg)
        else:
            box_img = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(box_img)

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = max(0, (box_w - tw) // 2)
        ty = max(0, (box_h - th) // 2)
        draw.text((tx, ty), text, font=font, fill=fg)

        if mirror:
            box_img = ImageOps.mirror(box_img)

        # Paste روی تصویر اصلی
        if with_box:
            self.current_img.paste(box_img, (x, y))
        else:
            self.current_img.paste(box_img, (x, y), box_img)

    def update_display(self, mirror_frame: bool = False):
        """ارسال فریم به نمایشگر"""
        img = self.current_img
        if mirror_frame:
            img = ImageOps.mirror(img)
        self.dev.display_image(img, self.disp_w, self.disp_h)

    def close(self):
        """بستن ارتباط با SPI"""
        self.dev.close()
