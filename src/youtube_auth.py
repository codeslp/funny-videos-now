"""
YouTube OAuth 2.0 Setup Helper
Run this ONCE to get your refresh token for automated uploads.

Usage:
  python3 src/youtube_auth.py

Prerequisites:
  1. Go to console.cloud.google.com
  2. Create a new project (or use existing)
  3. Enable "YouTube Data API v3"
  4. Go to Credentials → Create OAuth 2.0 Client ID (Desktop app)
  5. Download the client secret JSON
  6. Add YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET to your .env
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
import webbrowser
import http.server

sys.path.insert(0, os.path.dirname(__file__))
from script_generator import _load_env
_load_env()

CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8090"
SCOPES = "https://www.googleapis.com/auth/youtube.upload"


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Set YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in your .env first.")
        print("   See .env.example for instructions.")
        return

    # Step 1: Open browser for user authorization
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
        f"response_type=code&"
        f"scope={urllib.parse.quote(SCOPES)}&"
        f"access_type=offline&"
        f"prompt=consent"
    )

    print("\n🔐 YouTube OAuth Setup")
    print("=" * 50)
    print("\nOpening your browser for authorization...")
    print("If it doesn't open, go to this URL:\n")
    print(auth_url)
    webbrowser.open(auth_url)

    # Step 2: Capture the authorization code via local server
    auth_code = None

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            auth_code = params.get('code', [None])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Success!</h1><p>You can close this tab.</p>")

        def log_message(self, format, *args):
            pass  # Suppress server logs

    server = http.server.HTTPServer(('localhost', 8090), Handler)
    print("\n⏳ Waiting for authorization...")
    server.handle_request()

    if not auth_code:
        print("❌ No authorization code received.")
        return

    # Step 3: Exchange auth code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }).encode()

    context = ssl._create_unverified_context()
    req = urllib.request.Request(token_url, data=token_data, method='POST')

    try:
        with urllib.request.urlopen(req, context=context) as resp:
            tokens = json.loads(resp.read().decode())
    except Exception as e:
        print(f"❌ Token exchange failed: {e}")
        return

    refresh_token = tokens.get('refresh_token')
    if not refresh_token:
        print("❌ No refresh token in response. Try again with prompt=consent.")
        return

    print("\n✅ SUCCESS! Add this to your .env file:\n")
    print(f"YOUTUBE_REFRESH_TOKEN={refresh_token}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
