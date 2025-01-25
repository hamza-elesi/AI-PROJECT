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
        # Initialize the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, self.scopes)

        # Use one of the redirect URIs configured in your JSON
        flow.redirect_uri = "http://localhost"  # Matches redirect_uris in your client_secret.json

        # Run the local server for authentication
        credentials = flow.run_local_server(port=8080)
        logging.info("Authentication successful.")
        return build(self.service_name, self.version, credentials=credentials)


class GetData(GoogleOAuth):
    def __init__(self, client_secret_file, domain):
        """
        Get all keywords from Google Search Console (last 16 months).
        :param client_secret_file: OAuth JSON file path.
        :param domain: Google Search Console resource name (site URL).
        """
        self.SCOPES = ['https://www.googleapis.com/auth/webmasters']
        self.CLIENT_SECRET = client_secret_file
        self.SERVICE_NAME = 'searchconsole'
        self.VERSION = 'v1'
        self.domain = domain

        # Initialize authentication
        super().__init__(self.CLIENT_SECRET, self.SCOPES, self.SERVICE_NAME, self.VERSION)
        self.service = self.auth()

    def execute_request(self, start_row, start_date, end_date, dimensions, report_type, aggregate_by):
        """
        Executes a searchAnalytics.query request.
        :param start_row: Start row for paginated results.
        :param start_date: Start date in YYYY-MM-DD format.
        :param end_date: End date in YYYY-MM-DD format.
        :param dimensions: List of dimensions (e.g., ['query', 'page']).
        :param report_type: Report type ('web', 'discover', or 'googleNews').
        :param aggregate_by: Aggregation type ('auto', 'byProperty', 'byPage').
        :return: API response as a dictionary.
        """
        params = {
            'type': report_type,
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'aggregationType': aggregate_by,
            'dataState': 'all',
            'rowLimit': 25000,
            'startRow': start_row,
        }

        try:
            response = self.service.searchanalytics().query(siteUrl=self.domain, body=params).execute()
            return response
        except Exception as err:
            logging.error(f"Error executing request: {err}")
            return None

    def worker(self, start_date, end_date, dimensions, report_type='web', aggregate_by='auto'):
        """
        Retrieve all search analytics data for the given parameters.
        :param start_date: Start date in YYYY-MM-DD format.
        :param end_date: End date in YYYY-MM-DD format.
        :param dimensions: List of dimensions (e.g., ['query', 'page']).
        :param report_type: Report type ('web', 'discover', or 'googleNews').
        :param aggregate_by: Aggregation type ('auto', 'byProperty', 'byPage').
        :return: Combined results from all pages of the query.
        """
        start_row = 0
        result = []
        while True:
            response = self.execute_request(
                start_row, start_date, end_date, dimensions, report_type, aggregate_by
            )
            if response and 'rows' in response:
                result.extend(response['rows'])

                if len(response['rows']) == 25000:
                    start_row += 25000
                else:
                    logging.info(f"Retrieved {start_row + len(response['rows'])} rows in total.")
                    break
            else:
                logging.warning("No more data or an error occurred.")
                break

        return result


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Path to your client_secret.json file
    CLIENT_SECRET_FILE = "secret.json"  # Replace with the actual path to your JSON
    DOMAIN = "https://www.example.com"  # Replace with your verified site URL

    # Initialize the data fetcher
    gsc_data_fetcher = GetData(CLIENT_SECRET_FILE, DOMAIN)

    # Parameters
    START_DATE = "2025-01-01"
    END_DATE = "2025-01-02"
    DIMENSIONS = ['query', 'page']

    # Fetch data
    data = gsc_data_fetcher.worker(START_DATE, END_DATE, DIMENSIONS)
    print(data)
