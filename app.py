from flask import Flask, request, redirect, jsonify
import redis
import os
import string
import random


app = Flask(__name__)
app.config['SERVER_NAME'] = 'b949-49-205-33-36.ngrok-free.app'

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    long_url = data["url"]
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    short_key = generate_short_key()
    r.set(short_key, long_url)

    short_url = f"http://{request.host}/{short_key}"
    return jsonify({"short_url": f"{short_url}"}), 201


@app.route("/<short_key>", methods=["GET"])
def redirect_url(short_key):
    long_url = r.get(short_key)
    if long_url:
        # Ensure the URL has a scheme
        if not long_url.startswith("http://") and not long_url.startswith("https://"):
            long_url = "http://" + long_url
        return redirect(long_url)

    return jsonify({"error": "Short URL not found"}), 404


@app.route("/all", methods=["GET"])
def get_all_short_urls():
    keys = r.keys(pattern='*')
    url_mapping = {key: r.get(key) for key in keys}
    return jsonify(url_mapping)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
