import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask, Response, request, jsonify


app = Flask(__name__)

# Initialize Firebase Admin SDK
PATH_TO_CERTIFICATE = "certificates/certificate.json"

try:
    cred = credentials.Certificate(PATH_TO_CERTIFICATE)
    firebase_admin.initialize_app(cred)
except FileNotFoundError:
    print("Error: Missing certificate!")
    exit()


@app.route("/new_message", methods=["POST"])
def new_message() -> tuple[Response, int]:
    data = request.get_json()

    # Send message
    messaging.send(
        messaging.Message(
            token=data["token"],
            data=data,
            notification=messaging.Notification(
                title=data["authorName"],
                body=data["messageContent"],
            ),
        )
    )

    return jsonify({"success": True}), 200


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
