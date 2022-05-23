# pyscript PWA Example

This app shows how using a PWA (Progressive Web App) along with [pyscript](https://pyscript.net)
allows us to create Python-based web applications that install like regular applications and
(mostly) don't suffer from the large file downloads needed for Python's WebAssembly runtime.

![](readme-resources/screenshot.png)

To run the app, just start it as a Flask application (keep the app running for the web weather API).

```bash

python3 -m venv venv
. /venv/bin/activate
pip install -r requirements.txt
flask run

```

Then open 127.0.0.1:5000 and choose "install PWA". See 
[these steps for Chrome](https://www.howtogeek.com/fyi/how-to-install-progressive-web-apps-pwas-in-chrome/), 
google the actions if you are new to this in your browser.

Unfortunately, Mozilla gave up on this feature for Firefox browser.

If you have improvements for the PWA side of things, please open a PR. It's very bare-bones.
