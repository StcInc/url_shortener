import redis
from flask import Flask, request, render_template, redirect

import configuration as config

BASE = "0123456789abcdefghijklmnopqrstuvwxyz"

app = Flask(__name__)

redis_connection = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)

def num_to_link(num):
    digits = []
    while num > 0:
        remainder = num % len(BASE)
        digits.append(remainder)
        num = num // len(BASE)
    n = len(digits)
    b = len(BASE)
    return "".join(BASE[digits[n - i - 1] % b] for i in range(n))


def previously_shortened(url):
    return redis_connection.hget(config.REDIS_ORIG_TO_SHORT, url)


def get_short_url(url):
    shortened = previously_shortened(url)
    if shortened:
        return config.BASE_URL + "/" + shortened.decode("utf-8")
    else:
        num = redis_connection.hlen(config.REDIS_SHORT_TO_ORIG) + 1  # to avoid ''
        short_url =  num_to_link(num)
        redis_connection.hset(config.REDIS_SHORT_TO_ORIG, short_url, url)
        redis_connection.hset(config.REDIS_ORIG_TO_SHORT, url, short_url)
        return config.BASE_URL + "/" + short_url


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def status(path):
    if path:
        url = redis_connection.hget(config.REDIS_SHORT_TO_ORIG, path)
        if url:
            return redirect(url, code=302)
        else:
            return redirect("/", code=302)

    return render_template(
        "index.html",
        url=path
    )


@app.route('/', methods=['POST'])
def shorten_url():
    url= request.form['url']
    short_url = get_short_url(url)

    return render_template(
        "index.html",
        url=url,
        short_url=short_url
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
