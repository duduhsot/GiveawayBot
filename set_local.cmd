powershell -Command "(gc config.py) -replace 'BOT_TOKEN', '5726668567:AAEnt_hRMirItfq2Jrn-srH8OGRz_oVjNOI' | Out-File -encoding ASCII config.py"
powershell -Command "(gc config.py) -replace 'False', 'True'  | Out-File -encoding ASCII config.py"