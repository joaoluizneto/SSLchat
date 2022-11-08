@echo on
python -m venv sslchat_env
"%~dp0\sslchat_env\Scripts\pip.exe" "install" "-r" ".\requirements.txt"
pause