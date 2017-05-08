import requests
from requests.compat import urljoin


class StepikAPI:
    """Very basic client for Stepik.org API"""

    def __init__(self):
        self.base_url = 'https://stepik.org:443/api/'

    def get(self, resource, ids, page=1):
        """
        Performs GET request to Stepik API resource
        :param resource: Resource name
        :param ids: Id or list of ids of objects to be requested
        :param page: Page of request
        :return: Parsed JSON response
        """
        url = urljoin(self.base_url, resource)
        response = requests.get(url, params={'ids[]': ids, 'page': page})

        return response.json()
