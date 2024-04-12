import requests
import urllib3

urllib3.disable_warnings()


class ProxyCPAPI:

    def __init__(self, gateway_url):
        self._gateway_url = gateway_url
        self._logged_in = False

    # Function to attempt a login
    def get_login_page(self, username, password):
        # Prepare the login URL and the payload with credentials
        login_url = f"{self._gateway_url}/iserver/auth/status"
        credentials = {
            'username': username,
            'password': password
        }

        # Make a POST request to attempt login
        try:
            response = requests.post(login_url, json=credentials, verify=False)
            response.raise_for_status()  # Raise an error on bad status
            # Check if the response indicates a successful login
            if response.status_code == 200:
                print("Login successful.")
                return response.json()
            else:
                print("Login failed.")
                return response.json()
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def check_cpapi_auth_status(self):
        # Prepare the URL for the status check
        status_url = f"{self._gateway_url}/iserver/auth/status"
        response = requests.get(status_url, verify=False)
        return response
