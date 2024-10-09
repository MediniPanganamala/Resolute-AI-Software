from flask import Flask, request, jsonify
from functools import wraps
import json
import hashlib
import logging
import os

app = Flask(__name__)


logging.basicConfig(filename='license_system.log', level=logging.INFO)


user_roles_db = {
    "admin_user": {"role": "admin", "password": "admin_pass"},
    "regular_user": {"role": "user", "password": "user_pass"}
}


licenses_db = {
    "VALID_LICENSE_KEY": {"status": "valid", "usage_count": 0},
    "EXPIRED_LICENSE_KEY": {"status": "expired", "usage_count": 0}
}


def check_auth(username, password):
    user = user_roles_db.get(username)
    return user and user['password'] == password

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Unauthorized access"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/validate', methods=['POST'])
@requires_auth
def validate_license():
    data = request.get_json()
    license_key = data.get('license_key')

    if not data or 'license_key' not in data:
        logging.warning(f"Invalid request received: {data}")
        return jsonify({"error": "Invalid request"}), 400
    
    if license_key in licenses_db:
        licenses_db[license_key]['usage_count'] += 1  
        status = licenses_db[license_key]['status']
        logging.info(f"License validation requested for: {license_key}, status: {status}")
        return jsonify({"status": status, "usage_count": licenses_db[license_key]['usage_count']})
    else:
        logging.info(f"License validation failed for: {license_key}")
        return jsonify({"status": "invalid"}), 404

@app.route('/revoke', methods=['POST'])
@requires_auth
def revoke_license():
    data = request.get_json()
    username = request.authorization.username  

    if user_roles_db[username]['role'] != "admin":
        return jsonify({"error": "Unauthorized action"}), 403  n
    
    license_key = data.get('license_key')

    if not data or 'license_key' not in data:
        logging.warning(f"Invalid revoke request received: {data}")
        return jsonify({"error": "Invalid request"}), 400

    if license_key in licenses_db:
        licenses_db[license_key]['status'] = 'revoked'
        logging.info(f"License revoked for: {license_key}")
        return jsonify({"status": "revoked"}), 200
    else:
        logging.info(f"Revocation failed for: {license_key}")
        return jsonify({"status": "invalid"}), 404

@app.route('/activate', methods=['POST'])
@requires_auth
def activate_license():
    data = request.get_json()
    
    if not data or 'license_key' not in data:
        logging.warning(f"Invalid activation request received: {data}")
        return jsonify({"error": "Invalid request"}), 400
    
    license_key = data['license_key']
    
    licenses_db[license_key] = {"status": "valid", "usage_count": 0}
    logging.info(f"License activated: {license_key}")
    return jsonify({"status": "activated"}), 201

if __name__ == "__main__":
    app.run(debug=True)
