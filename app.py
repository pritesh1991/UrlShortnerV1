from flask import Flask, request, redirect, jsonify, render_template, abort
import redis
import os
import string
import secrets
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Allowed URL schemes for security
ALLOWED_SCHEMES = {'http', 'https'}

# Blocked hosts to prevent SSRF attacks
BLOCKED_HOSTS = {'localhost', '127.0.0.1', '0.0.0.0', '::1'}


def is_valid_url(url):
    """Validate URL to prevent security issues."""
    try:
        parsed = urlparse(url)
        # Check if scheme is allowed
        if parsed.scheme.lower() not in ALLOWED_SCHEMES:
            return False
        # Check if host is blocked (prevent SSRF)
        if parsed.hostname and parsed.hostname.lower() in BLOCKED_HOSTS:
            return False
        # Ensure URL has a valid netloc
        if not parsed.netloc:
            return False
        return True
    except Exception:
        return False


def generate_short_key(length=6, max_attempts=10):
    """Generate a cryptographically secure unique short key."""
    characters = string.ascii_letters + string.digits
    for _ in range(max_attempts):
        # Use secrets module for cryptographically strong random
        short_key = ''.join(secrets.choice(characters) for _ in range(length))
        # Check if key already exists to prevent collision
        if not r.exists(short_key):
            return short_key
    # If we couldn't generate a unique key after max_attempts, increase length
    return ''.join(secrets.choice(characters) for _ in range(length + 1))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("url")
        if not long_url:
            return render_template("index.html", error="URL is required")
        
        # Validate URL before storing
        if not is_valid_url(long_url):
            return render_template("index.html", error="Invalid URL. Only HTTP/HTTPS URLs are allowed.")
        
        short_key = generate_short_key()
        r.set(short_key, long_url)
        short_url = f"http://{request.host}/{short_key}"
        return render_template("index.html", short_url=short_url)
    return render_template("index.html")


@app.route("/<short_key>")
def redirect_url(short_key):
    # Sanitize input - only allow alphanumeric characters
    if not short_key.isalnum():
        abort(400)
    
    long_url = r.get(short_key)
    if long_url:
        # Validate URL before redirecting to prevent open redirect attacks
        if not is_valid_url(long_url):
            return jsonify({"error": "Invalid URL stored"}), 500
        
        # Ensure the URL has proper scheme
        if not long_url.startswith(("http://", "https://")):
            long_url = "https://" + long_url
            # Re-validate after adding scheme
            if not is_valid_url(long_url):
                return jsonify({"error": "Invalid URL"}), 500
        
        return redirect(long_url)
    return jsonify({"error": "Short URL not found"}), 404


@app.route("/all")
def get_all_short_urls():
    # Security: Add authentication for admin endpoint
    auth_token = request.headers.get('X-Admin-Token')
    admin_token = os.getenv('ADMIN_TOKEN')
    
    # Only allow access if ADMIN_TOKEN is set and matches
    if not admin_token or auth_token != admin_token:
        return jsonify({"error": "Unauthorized"}), 401
    
    keys = r.keys(pattern='*')
    url_mapping = {key: r.get(key) for key in keys}
    return jsonify(url_mapping)


if __name__ == "__main__":
    # Security: Disable debug mode in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host="0.0.0.0", port=6000, debug=debug_mode)
