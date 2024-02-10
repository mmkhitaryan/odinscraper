To start the webserver:
```
poetry install
poetry run python data_collector.py
```
Then you need to set up ngrok so we can connect from torbrowser, ```ngrok http 8080```. Replace the ngrok with yours in the interceptor.js.
