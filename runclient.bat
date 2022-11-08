@echo off
"%~dp0\sslchat_env\Scripts\python.exe" ".\SSLchat\client.py" "run" "--certBundle" ".\SSLchat\cert.pem" 
pause