# MoreLinks Android App - Build Guide

## Opzione 1: PWA (Consigliato - Funziona Subito!)

1. Apri `android_app/index.html` nel browser Chrome del tuo Android
2. Tocca i 3 punti in alto a destra
3. Seleziona "Aggiungi alla schermata Home"
4. L'app comparirà come un'app nativa!

## Opzione 2: Build APK con Flet

```bash
# 1. Clona il repo
git clone https://github.com/Schumynet/MoreLinks.git
cd MoreLinks/android_flet

# 2. Installa Flet
pip install flet

# 3. Build APK Android
flet build apk --platform android

# Output: dist/morelinks.apk
```

## Opzione 3: Build APK con Capacitor

```bash
# 1. Clona e instala dipendenze
npm install
npx cap sync android

# 2. Build
cd android && ./gradlew assembleDebug
# Output: android/app/build/outputs/apk/debug/app-debug.apk
```

## Opzione 4: Web App su Hosting

Carica `android_app/index.html` su:
- Netlify
- Vercel  
- GitHub Pages
- Qualsiasi hosting statico

## Requisiti per Build APK Locale

- Python 3.11+
- Node.js 18+ (per Capacitor)
- Android SDK / Android Studio
- Java JDK 11+
- 4GB+ RAM

## File APK Pre-compilato

Per richiedere un APK pre-compilato, apri una issue su GitHub.