from display import DisplayManager
import time

disp = DisplayManager()

# Persian text with Unicode escape
# متن فارسی با Unicode escape
txt = "\u0633\u0644\u0627\u0645 \u062F\u0646\u06CC\u0627 12345"

disp.draw_text(txt, font_size=28, x=20, y=20,
               box_w=250, box_h=60,
               with_box=True, fg=(0,0,0), mirror=True)

disp.update_display()
time.sleep(5)
disp.close()
