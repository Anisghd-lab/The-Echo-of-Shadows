Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Compilation L'Écho des Ombres - Android Release " -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

# 1. Nettoyage des processus
Get-Process java,dart -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500

# 2. Récupération des dépendances
Write-Host "`n[1/3] flutter pub get..." -ForegroundColor Yellow
flutter pub get

# 3. Exécution des tests unitaires
Write-Host "`n[2/3] flutter test..." -ForegroundColor Yellow
flutter test

# 4. Compilation Release APK
Write-Host "`n[3/3] flutter build apk --release..." -ForegroundColor Yellow
flutter build apk --release --target-platform android-arm64,android-arm --no-tree-shake-icons

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=================================================" -ForegroundColor Green
    Write-Host "  SUCCÈS : APK L'ÉCHO DES OMBRES GÉNÉRÉ AVEC SUCCÈS !" -ForegroundColor Green
    Write-Host "  Fichier : build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor White
    Write-Host "=================================================" -ForegroundColor Green
} else {
    Write-Host "`n[!] La compilation a rencontré une erreur." -ForegroundColor Red
}
