import os
# --- 🛠️ 1. OPENGL / WINDOWS GRAPHICS EMULATOR YAMASI ---
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2' 
os.environ['KIVY_BCKEND'] = 'sdl2'

import kivy
from kivy.config import Config
Config.set('graphics', 'width', '1100')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', True) 

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.storage.jsonstore import JsonStore
import json

class MVDSAcademyMobilePlayer(App):
    def build(self):
        self.title = "MVDS ACADEMY"
        
        # 📂 %100 INTERNETSİZ DOĞRUDAN MASAÜSTÜ VERİ BAĞLANTISI (B PLAN KANADI)
        self.desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.veri_dosyasi = os.path.join(self.desktop_dir, "mvds_live_data.json")
        self.user_dosyasi = os.path.join(self.desktop_dir, "mvds_user_status.json")

        self.joined_count = 0
        self.store = JsonStore(self.user_dosyasi)
        self.has_joined_this_event = self.store.exists('status') and self.store.get('status')['has_joined']

        # Esnek Layout Sistemi
        self.layout = FloatLayout()

        # --- 🖼️ ŞABLON ARKA PLAN (Sıfıra Sıfır Kilitli) ---
        if os.path.exists("arka_plan.png"):
            self.bg_img = Image(source="arka_plan.png", allow_stretch=True, keep_ratio=False,
                                size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
            self.layout.add_widget(self.bg_img)

        # Üst Sabit Başlık (Çizgi başlangıcına hizalı)
        self.lbl_main_title = Label(
            text="MVDS ACADEMY", font_size='26sp', bold=True, italic=True,
            halign='left', valign='middle', text_size=(300, None),
            size_hint=(0.27, 0.1), pos_hint={'x': 0.035, 'y': 0.82}
        )
        self.layout.add_widget(self.lbl_main_title)

        # --- SOL PANEL: İKİ SATIRLI DUYURU METİNLERİ (Siyah kutuların tam içi, büyük puntolar) ---
        text_1 = "WELCOME TO THE OFFICIAL MVDS ACADEMY CLAN CAMPUS.\nTEAM UP WITH YOUR LEGENDARY CREW MEMBERS RIGHT NOW!"
        self.lbl_w1 = Label(
            text=text_1, font_size='16sp', italic=True, bold=True,
            halign='center', valign='middle', text_size=(490, None),
            size_hint=(0.45, 0.18), pos_hint={'x': 0.02, 'y': 0.58}
        )
        self.layout.add_widget(self.lbl_w1)

        text_2 = "CHECK ALL AVAILABLE LIVE EVENTS ON THE RIGHT PANEL\nAND DOMINATE THE ASPHALT HIGHWAYS TO WIN TOP RACES!"
        self.lbl_w2 = Label(
            text=text_2, font_size='16sp', italic=True, bold=True,
            halign='center', valign='middle', text_size=(490, None),
            size_hint=(0.45, 0.18), pos_hint={'x': 0.02, 'y': 0.35}
        )
        self.layout.add_widget(self.lbl_w2)

        # --- SAĞ PANEL: CANLI ETKİNLİK ALANLARI ---
        self.lbl_title = Label(
            text="NOW LIVE: LOADING...", font_size='18sp', bold=True, italic=True,
            halign='left', valign='middle', text_size=(500, None),
            size_hint=(0.45, 0.07), pos_hint={'x': 0.51, 'y': 0.69}
        )
        self.layout.add_widget(self.lbl_title)

        # Canlı Araba Resim Alanı
        self.lbl_img = AsyncImage(
            source="", allow_stretch=True, keep_ratio=False,
            size_hint=(0.454, 0.28), pos_hint={'x': 0.51, 'y': 0.38}
        )
        self.layout.add_widget(self.lbl_img)

        # SAYAÇ KONUMU: Beyaz kutunun sağ üst köşesindeki boş alan
        self.lbl_count = Label(
            text="JOINED PLAYER COUNT: 0", font_size='14sp', bold=True, italic=True,
            color=(1, 0.6, 0, 1), halign='right', valign='middle', text_size=(500, None),
            size_hint=(0.454, 0.05), pos_hint={'x': 0.51, 'y': 0.69}
        )
        self.layout.add_widget(self.lbl_count)

        # Kıpkırmızı JOIN EVENT Butonu
        self.btn_join = Button(
            text="JOIN EVENT", font_size='14sp', bold=True, italic=True,
            background_normal='', background_color=(0.7, 0, 0, 1),
            size_hint=(0.454, 0.07), pos_hint={'x': 0.51, 'y': 0.20}
        )
        self.btn_join.bind(on_press=self.click_join_mobile_pure_offline)
        self.layout.add_widget(self.btn_join)

        # Yeşil Quit Butonu
        self.btn_quit = Button(
            text="Quit", font_size='16sp', bold=True, italic=True,
            background_normal='', background_color=(0, 0.48, 0, 1),
            size_hint=(0.282, 0.09), pos_hint={'x': 0.708, 'y': 0.03}
        )
        self.btn_quit.bind(on_press=lambda x: self.stop())
        self.layout.add_widget(self.btn_quit)

        # 🚀 AÇILIŞTA TEK SEFERLİK REFRESH MOTORU: Girer girmez dosyayı tokatlar
        self.pure_offline_refresh()

        return self.layout

    def pure_offline_refresh(self):
        """Ağ/Server aramadan, girer girmez masaüstündeki JSON verisini sıfırdan okur."""
        if os.path.exists(self.veri_dosyasi):
            try:
                with open(self.veri_dosyasi, "r", encoding="utf-8") as f:
                    result = json.load(f)
                
                event_name = result.get("event_name", "NO LIVE EVENT")
                self.joined_count = result.get("joined_count", 0)

                if event_name in ["NO ACTIVE EVENT YET", "NO LIVE EVENT"]:
                    self.lbl_title.text = "NOW LIVE: NO ACTIVE EVENT YET"
                    self.btn_join.disabled = True
                    self.btn_join.background_color = (0.3, 0.3, 0.3, 1)
                    self.store.put('status', has_joined=False)
                    self.has_joined_this_event = False
                    self.lbl_img.source = ""
                else:
                    self.lbl_title.text = f"NOW LIVE: {event_name.upper()}"
                    if self.joined_count == 0:
                        self.store.put('status', has_joined=False)
                        self.has_joined_this_event = False

                    if self.has_joined_this_event:
                        self.btn_join.disabled = True
                        self.btn_join.background_color = (0.3, 0.3, 0.3, 1)
                    else:
                        self.btn_join.disabled = False
                        self.btn_join.background_color = (0.7, 0, 0, 1)

                    # Resmi de direkt masaüstü klasöründen lokal çeker
                    local_image_path = os.path.join(self.desktop_dir, "live_event_image.png")
                    if os.path.exists(local_image_path):
                        self.lbl_img.source = local_image_path

                self.lbl_count.text = f"JOINED PLAYER COUNT: {self.joined_count}"
            except: pass
        else:
            self.lbl_title.text = "NOW LIVE: NO ACTIVE EVENT YET"
            self.btn_join.disabled = True
            self.btn_join.background_color = (0.3, 0.3, 0.3, 1)
            self.lbl_img.source = ""

    def click_join_mobile_pure_offline(self, instance):
        if self.has_joined_this_event: return
        self.has_joined_this_event = True
        self.store.put('status', has_joined=True)
        
        self.joined_count += 1
        self.lbl_count.text = f"JOINED PLAYER COUNT: {self.joined_count}"
        self.btn_join.disabled = True
        self.btn_join.background_color = (0.3, 0.3, 0.3, 1)
        
        # Sayacı anında masaüstündeki ortak JSON dosyasına yazar
        if os.path.exists(self.veri_dosyasi):
            try:
                with open(self.veri_dosyasi, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["joined_count"] = self.joined_count
                with open(self.veri_dosyasi, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except: pass

if __name__ == "__main__":
    MVDSAcademyMobilePlayer().run()
