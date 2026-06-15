import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os


app = Flask(__name__)

CORS(app)

# Google Sheets Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SHEET_ID = "13OCzn9pQjZ9rrit_kW9igpS0Z-DnRhhMeDgIkc7r-jc"
CREDENTIALS_FILE = "credentials.json"

# Check if credentials file exists
if not os.path.exists(CREDENTIALS_FILE):
    print(f"⚠️  Warning: {CREDENTIALS_FILE} not found in current directory")
    print(f"Current directory: {os.getcwd()}")


def get_sheet():
    """Connect to Google Sheet and return the worksheet"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"{CREDENTIALS_FILE} not found")
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.sheet1  # Get the first sheet
        return worksheet
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        return None


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "✅ Backend is running", "port": 5000}), 200


@app.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submissions and save to Google Sheet"""
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
            except Exception as e:
                print(f"⚠️  Error appending to sheet: {e}\n")
                return jsonify({"success": False, "message": "Failed to save to sheet"}), 500
        else:
            print("⚠️  Warning: Could not connect to Google Sheet\n")
            return jsonify({"success": False, "message": "Failed to connect to sheet"}), 500
        
        return jsonify({"success": True, "message": "Message received and saved"}), 200
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")
        return jsonify({"success": False, "message": "Server error"}), 500


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
    print("=" * 50)
    print(f"✅ Health Check: http://localhost:{port}/")
    print(f"📝 Contact API: http://localhost:{port}/contact (POST)")
    print("=" * 50 + "\n")

    app.run(host="0.0.0.0", port=port, debug=debug)



     