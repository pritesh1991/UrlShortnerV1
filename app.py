from flask import Flask, request, redirect, jsonify, render_template
import redis
import os
import string
import random
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("url")
        if not long_url:
            return render_template("index.html", error="URL is required")
        short_key = generate_short_key()
        r.set(short_key, long_url)
        short_url = f"http://{request.host}/{short_key}"
        return render_template("index.html", short_url=short_url)
    return render_template("index.html")


@app.route("/<short_key>")
def redirect_url(short_key):
    long_url = r.get(short_key)
    if long_url:
        if not long_url.startswith(("http://", "https://")):
            long_url = "http://" + long_url
        return redirect(long_url)
    return jsonify({"error": "Short URL not found"}), 404


@app.route("/all")
def get_all_short_urls():
    keys = r.keys(pattern='*')
    url_mapping = {key: r.get(key) for key in keys}
    return jsonify(url_mapping)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
