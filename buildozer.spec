# 📂 1. Doğru klasöre geç ve eski kalıntıları tamamen temizle
%cd /content
!rm -rf buildozer.spec buildozer.spec*

# ⚙️ 2. Dosya yüklemeyle uğraşmıyoruz, spec dosyasını direkt burada sıfırdan yazdırıyoruz
with open("buildozer.spec", "w", encoding="utf-8") as f:
    f.write("""[app]
title = MVDS ACADEMY
package.name = mvdsac
package.domain = com.mstwnted
source.dir = .
source.include_exts = py,png,json
version = 1.10a
requirements = python3,kivy,pillow
orientation = landscape
fullscreen = 1
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/arka_plan.png

[buildozer]
log_level = 2
warn_on_root = 1
""")

print("Sihirli Dosya Doğrulandı! buildozer.spec başarıyla sıfırdan yazıldı.")

# 🛠️ 3. Bağımlılıkları Kur ve Derlemeyi Başlat
!pip install --upgrade buildozer cython pillow requests
!sudo apt-get install -y scons libssl-dev libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav libgstreamer-plugins-base1.0-dev libasound2-dev libgwenhywfar-dev libitpp-dev libvlc-dev libvlccore-dev vlc-data autoconf automake libtool pkg-config zlib1g-dev python3-dev libffi-dev libgmp-dev
!sudo apt-get install -y openjdk-17-jdk
!sudo update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java

# 🚀 4. APK Paketlemeyi Fırlat
!yes | buildozer android release
