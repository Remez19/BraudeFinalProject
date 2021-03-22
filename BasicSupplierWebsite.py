import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



class SupplierWebsite:

    def __init__(self, pageLink, insertQuery):
        self.pageLink = pageLink
        self.insertQuery = insertQuery
        self.resultVegList = []

    def connectionChecker(self, link):
        try:
            session = requests.Session()
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session.get(link)
        except Exception:
            print("Connection Failure")
            return None
