from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app)



@app.route("/contact", methods=["POST"])
def contact():
    

    data = request.json


    print("New Customer Enquiry")
    print("--------------------")
    print("Name:", data.get("name"))
    print("Phone:", data.get("phone"))
    print("Email:", data.get("email"))
    print("Business:", data.get("businessType"))
    print("Message:", data.get("message"))


    return jsonify({

        "success": True,
        "message": "Message Received"

    })




if __name__ == "__main__":

    app.run(port=5000, debug=True)