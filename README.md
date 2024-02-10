To start the webserver:
```
poetry install
poetry run python src/data_collector.py
```
Then you need to set up ngrok so we can connect from torbrowser, ```ngrok http 8080```. Replace the ngrok with yours in the interceptor.js.

Install tampermonkey, or just put the js code from requests_interceptor.js into devtools manually.

DEMO VIDEO: https://vimeo.com/911844203
