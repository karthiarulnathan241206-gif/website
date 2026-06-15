import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json
from io import StringIO


app = Flask(__name__)

# Configure CORS with specific frontend URL
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://dongle-enterprises.onrender.com",
            "http://localhost:3000",
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Google Sheets Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SHEET_ID = "13OCzn9pQjZ9rrit_kW9igpS0Z-DnRhhMeDgIkc7r-jc"
CREDENTIALS_FILE = "credentials.json"

# Check if credentials exist (file or environment variable)
credentials_available = False
credentials_source = "None"

if os.path.exists(CREDENTIALS_FILE):
    credentials_available = True
    credentials_source = "File"
    print(f"✅ Using credentials from file: {CREDENTIALS_FILE}")
elif os.getenv("GOOGLE_CREDENTIALS_JSON"):
    try:
        test_json = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
        if "type" in test_json and test_json["type"] == "service_account":
            credentials_available = True
            credentials_source = "Environment Variable"
            print(f"✅ Using credentials from environment variable: GOOGLE_CREDENTIALS_JSON")
        else:
            print(f"⚠️  Environment variable exists but is not valid service account credentials")
    except json.JSONDecodeError as e:
        print(f"⚠️  GOOGLE_CREDENTIALS_JSON environment variable is not valid JSON: {e}")
else:
    print(f"❌ Credentials not found!")
    print(f"📝 Please set GOOGLE_CREDENTIALS_JSON environment variable on Render")
    print(f"📝 Instructions: https://dashboard.render.com/ → Your Service → Settings → Environment Variables")


def get_sheet():
    """Connect to Google Sheet and return the worksheet"""
    try:
        creds = None
        
        # Try to load credentials from file first
        if os.path.exists(CREDENTIALS_FILE):
            print("📂 Loading credentials from file...")
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
        # Try to load from environment variable
        elif os.getenv("GOOGLE_CREDENTIALS_JSON"):
            print("🔐 Loading credentials from environment variable...")
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            print(f"📝 Credentials JSON length: {len(creds_json)} characters")
            
            try:
                creds_dict = json.loads(creds_json)
                print(f"✅ JSON parsed successfully. Type: {creds_dict.get('type')}")
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {e}")
                print(f"First 100 chars: {creds_json[:100]}")
                raise
        else:
            raise FileNotFoundError("Credentials not found in file or environment variable")
        
        if creds is None:
            raise ValueError("Failed to create credentials object")
        
        print("🔑 Authorizing with gspread...")
        client = gspread.authorize(creds)
        
        print(f"📊 Opening spreadsheet with ID: {SHEET_ID}")
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.sheet1
        
        print("✅ Successfully connected to Google Sheet!")
        return worksheet
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: Invalid credentials JSON - {e}")
        return None
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {type(e).__name__}: {e}")
        return None


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "✅ Backend is running", 
        "url": "https://donglebackend.onrender.com",
        "credentials": "✅ Available" if credentials_available else "❌ Missing",
        "credentials_source": credentials_source
    }), 200


@app.route("/debug", methods=["GET"])
def debug():
    """Debug endpoint to check credentials status"""
    env_var_exists = bool(os.getenv("GOOGLE_CREDENTIALS_JSON"))
    file_exists = os.path.exists(CREDENTIALS_FILE)
    
    return jsonify({
        "file_exists": file_exists,
        "env_var_exists": env_var_exists,
        "credentials_available": credentials_available,
        "credentials_source": credentials_source,
        "sheet_id": SHEET_ID,
        "cwd": os.getcwd()
    }), 200


@app.route("/contact", methods=["POST", "OPTIONS"])
def contact():
    """Handle contact form submissions and save to Google Sheet"""
    # Handle preflight requests
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
    
    try:
        data = request.json
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Extract form data
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip()
        business_type = data.get("businessType", "").strip()
        message = data.get("message", "").strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Validate required fields
        if not name or not email:
            return jsonify({"success": False, "message": "Name and Email are required"}), 400
        
        # Log to console
        print("\n📝 New Customer Enquiry")
        print("─" * 50)
        print(f"Timestamp: {timestamp}")
        print(f"Name: {name}")
        print(f"Phone: {phone}")
        print(f"Email: {email}")
        print(f"Business Type: {business_type}")
        print(f"Message: {message}")
        print("─" * 50)
        
        # Add to Google Sheet
        worksheet = get_sheet()
        if worksheet:
            try:
                worksheet.append_row([timestamp, name, phone, email, business_type, message])
                print("✅ Data added to Google Sheet successfully\n")
                return jsonify({"success": True, "message": "Message received and saved"}), 200
            except Exception as e:
                print(f"⚠️  Error appending to sheet: {type(e).__name__}: {e}\n")
                return jsonify({"success": False, "message": f"Failed to save to sheet"}), 500
        else:
            print("⚠️  Warning: Could not connect to Google Sheet\n")
            return jsonify({"success": False, "message": "Failed to connect to sheet. Check backend logs."}), 500
        
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}\n")
        return jsonify({"success": False, "message": f"Server error"}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"success": False, "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"success": False, "message": "Internal server error"}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_env = os.environ.get("DEBUG", "false").lower()
    debug = debug_env in ("1", "true", "yes")

    print("=" * 50)
    print("🚀 Starting Backend Server")
    print("=" * 50)
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"📄 Credentials File: {CREDENTIALS_FILE}")
    print(f"📊 Google Sheet ID: {SHEET_ID}")
    print(f"🔐 Credentials Available: {'✅ Yes' if credentials_available else '❌ No'}")
    print(f"📍 Credentials Source: {credentials_source}")
    print("=" * 50)
    print(f"✅ Health Check: https://donglebackend.onrender.com/")
    print(f"🔍 Debug: https://donglebackend.onrender.com/debug")
    print(f"📝 Contact API: https://donglebackend.onrender.com/contact (POST)")
    print("=" * 50 + "\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
