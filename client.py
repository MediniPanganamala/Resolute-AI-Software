import requests

BASE_URL = "http://127.0.0.1:5000"  
def validate_license(license_key):
    url = f"{BASE_URL}/validate"
    data = {
        "license_key": license_key
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()

        if response.status_code == 200:
            if result['status'] == 'valid':
                print("License is valid!")
            else:
                print("License is invalid or expired.")
        else:
            print(f"Error: {result.get('error', 'Unknown error occurred')}")
    except Exception as e:
        print(f"Error: {e}")

def activate_license(license_key):
    url = f"{BASE_URL}/activate"
    data = {
        "license_key": license_key
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()

        if response.status_code == 201:
            print(f"License activated: {result['status']}")
        else:
            print(f"Error: {result.get('error', 'Activation failed')}")
    except Exception as e:
        print(f"Error: {e}")

def revoke_license(username, license_key):
    url = f"{BASE_URL}/revoke"
    data = {
        "username": username,
        "license_key": license_key
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        if response.status_code == 200:
            print(f"License revoked: {result['status']}")
        else:
            print(f"Error: {result.get('error', 'Revocation failed')}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\nLicense Management Client")
        print("1. Validate License")
        print("2. Activate License")
        print("3. Revoke License")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            license_key = input("Enter the license key to validate: ")
            validate_license(license_key)

        elif choice == '2':
            license_key = input("Enter the new license key to activate: ")
            activate_license(license_key)

        elif choice == '3':
            username = input("Enter your username (admin): ")
            license_key = input("Enter the license key to revoke: ")
            revoke_license(username, license_key)

        elif choice == '4':
            print("Exiting the client.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
