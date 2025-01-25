import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleOAuth:
    def __init__(self, client_secret_file, scopes, service_name, version):
        """
        Base class for authenticating with Google APIs.
        :param client_secret_file: Path to the OAuth client secret JSON file.
        :param scopes: List of API scopes.
        :param service_name: Name of the Google API service (e.g., 'searchconsole').
        :param version: Version of the API (e.g., 'v1').
        """
        self.client_secret_file = client_secret_file
        self.scopes = scopes
        self.service_name = service_name
        self.version = version

    def auth(self):
        """
        Authenticate and return a Google API service client.
        :return: Authenticated service object.
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secret_file, self.scopes
        )

        # Explicitly set the redirect URI
        flow.redirect_uri = "http://localhost/"
        credentials = flow.run_local_server(port=8080)

        service = build(self.service_name, self.version, credentials=credentials)
        return service


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    CLIENT_SECRET_FILE = "secret.json"  # Replace with your JSON file
    SCOPES = ['https://www.googleapis.com/auth/webmasters']
    SERVICE_NAME = 'searchconsole'
    VERSION = 'v1'

    oauth = GoogleOAuth(CLIENT_SECRET_FILE, SCOPES, SERVICE_NAME, VERSION)
    service = oauth.auth()

    print("Authentication successful!")
