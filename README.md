# sol_klik

Streamlit tabanlı otomatik tıklama aracı.

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
streamlit run app.py
```

Tetikleyici tuşu seçip **AYARLA**'ya bastıktan sonra uygulama açık kalırken
başka bir pencerede seçilen tuşlara basarak sol veya sağ tıklamayı saniyede 15 kez
başlatıp durdurabilirsiniz. Ayrıca belirlediğiniz durdurma tuşu uygulamayı
sonlandırır. İsteğe bağlı olarak duraklatma tuşu ile tetikleyicileri geçici olarak
devre dışı bırakabilir ve tek tuş yerine `ctrl+p` gibi kombinasyonlar atayabilirsiniz.

## Paketleme

Arkadaşınızın herhangi bir kurulum yapmadan çalıştırabileceği tek dosyalık bir sürüm oluşturmak için:

```bash
pip install -r requirements.txt
python build.py
```

Bu komutlar çalıştırıldığında `dist/sol_klik` (Windows'ta `dist/sol_klik.exe`) dosyası oluşur.
Bu dosyayı hedef işletim sistemiyle aynı platformda paketlemeli ve karşı tarafa göndererek sadece çift tıklayarak çalıştırmasını sağlayabilirsiniz.

Windows'ta doğrudan PyInstaller komutu kullanmak isterseniz:

```powershell
pyinstaller app.py --onefile --name PoyrazClicker `
  --collect-metadata streamlit --collect-data streamlit `
  --hidden-import streamlit.web.cli `
  --add-data "app.py;app.py" `
  --console
```
