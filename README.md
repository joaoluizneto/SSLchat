# SSL Chat

SSL over TCP over IP chat developed with Python Sockets.

## Installation
Just run install.bat

## Certificate generation
```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -nodes -sha256 -days 365 -subj '/CN=localhost'
```

![image](https://user-images.githubusercontent.com/41850008/200156869-9e530a9a-9719-4e81-9333-20ee080918c2.png)
