# Terminal 2: paginas na porta 5500 e proxy HTTP para a API da porta 5000.
Set-Location $PSScriptRoot
$env:AGRORISK_BACKEND_URL = "http://127.0.0.1:5000"
python frontend/server.py
