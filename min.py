from display import DisplayManager
import jdatetime
import time


# ساخت شیء نمایشگر
disp = DisplayManager()

# نمایش بکگراند
image_path = "/home/raspberrypi/home.jpg"
disp.show_background(image_path, mirror=True)

# دریافت تاریخ شمسی
date_str = jdatetime.datetime.now().strftime("%Y/%m/%d")

# ابعاد و مختصات برای تاریخ
box_w, box_h = 140, 45
x = 45
y = -5

# نوشتن تاریخ روی بکگراند
disp.draw_text(date_str,
               font_size=24,
               x=x, y=y,
               box_w=box_w, box_h=box_h,
               with_box=False,   # بدون بکگراند سفید
               fg=(255,255,255),       # رنگ مشکی
               mirror=True)

# ارسال به نمایشگر
disp.update_display()

# بستن ارتباط
disp.close()
