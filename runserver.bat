@echo off
"%~dp0\sslchat_env\Scripts\python.exe" ".\SSLchat\server.py" "run" "--key" ".\SSLchat\key.pem" "--cert" ".\SSLchat\cert.pem" "--numCli" "5"
pause