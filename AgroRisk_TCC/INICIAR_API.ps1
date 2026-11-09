# Terminal 1: roda SOMENTE a API, porta 5000. Deixe este terminal aberto.
Set-Location "$PSScriptRoot\backend"
$env:AGRORISK_API_ONLY = "1"
$env:FLASK_DEBUG = "False"
python app.py
