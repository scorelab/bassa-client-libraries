import re
from errors import InvalidUrl, IncompleteParams, ResponseError
import requests


class Bassa:

    def __init__(self, api_url):
        """Initializer for a Bassa instance
        Args:
            api_url (str):    URL to the Bassa Server
        Returns:
            None
        """
        reg = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(reg, api_url) is not None:
            self.api_url = api_url
        else:
            raise InvalidUrl
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    # User functions

    def login(self, user_name=None, password=None):
        """Login to the Bassa Server
        Args:
            user_name (str):    Name of the user
            password (str):   Password of the user
        Returns:
            None
        """
        endpoint = "/api/login"
        api_url_complete = self.api_url + endpoint
        params = {}
        if user_name is None or password is None:
            raise IncompleteParams
        params['user_name'] = user_name
        params['password'] = password
        result = requests.post(
            api_url_complete, data=params, headers=self.headers)
        if result.status_code == 200:
            self.headers['token'] = result.headers['token']
        else:
            raise ResponseError('API response: {}'.format(result.status_code))

    def add_regular_user_request(self, user_name=None, password=None, email=None, retries=1):
        """Add user requests with auth level 1
        Args:
            user_name (str):    Name of the user
            password (str):   Password of the user
            email (str): Email ID of the user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        endpoint = "/api/regularuser"
        api_url_complete = self.api_url + endpoint
        params = {}
        if user_name is None or password is None or email is None:
            raise IncompleteParams
        params['user_name'] = user_name
        params['password'] = password
        params['email'] = email
        while retries != -1:
            result = requests.post(
                api_url_complete, data=params, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def add_user_request(self, user_name=None, password=None, email=None, auth_level=1, retries=1):
        """Add user requests with auth level 1 or 0
        Args:
            user_name (str):    Name of the user
            password (str):   Password of the user
            email (str): Email ID of the user
            auth_level (int): Auth level of the user, 0 for admins and 1 for regular users
            retires (int): number of retries upon failure
        Returns:
            None
        """
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint
        params = {}
        if user_name is None or password is None or email is None:
            raise IncompleteParams
        params['user_name'] = user_name
        params['password'] = password
        params['email'] = email
        params['auth'] = auth_level
        while retries != -1:
            result = requests.post(
                api_url_complete, data=params, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def remove_user_request(self, user_name=None, retries=1):
        """Remove a user request
        Args:
            user_name (str):    Name of the user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        if user_name is None:
            raise IncompleteParams
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint + "/" + user_name
        while retries != -1:
            result = requests.delete(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def update_user_request(self, user_name=None, new_user_name=None, password=None, auth_level=None, email=None, retries=1):
        """Update a user request
        Args:
            user_name (str):    Name of the user to updated
            new_user_name (str): New name for the user
            password (str): New password for the user
            auth_level (int): Auth level for the new user, 0 for admins and 1 for regular users
            email (str): Email ID for the new user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        if user_name is None or new_user_name is None or password is None or auth_level is None or email is None:
            raise IncompleteParams
        params = {}
        params['user_name'] = new_user_name
        params['password'] = password
        params['auth_level'] = auth_level
        params['email'] = email
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint + "/" + user_name
        while retries != -1:
            result = requests.put(
                api_url_complete, data=params, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def get_user_request(self, retries=1):
        """Get a user request
            retires (int): number of retries upon failure
        Returns:
            response as json
        """
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    def get_user_signup_requests(self, retries=1):
        """Get all user requests
        Args:
            retires (int): number of retries upon failure
        Returns:
            response as json
        """
        endpoint = "/api/user/requests"
        api_url_complete = self.api_url + endpoint
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    def approve_user_request(self, user_name=None, retries=1):
        """Approve a user request
        Args:
            user_name (str): Name of the user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        endpoint = "/api/user/approve"
        api_url_complete = self.api_url + endpoint + "/" + user_name
        if user_name is None:
            raise IncompleteParams
        while retries != -1:
            result = requests.post(
                api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def get_blocked_users_request(self, retries=1):
        """Get all blocked user requests 
        Args:
            retires (int): number of retries upon failure
        Returns:
            response as json
        """
        endpoint = "/api/user/blocked"
        api_url_complete = self.api_url + endpoint
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    def block_user_request(self, user_name=None, retries=1):
        """Block a user request
        Args:
            user_name (str): Name of the user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        endpoint = "/api/user/blocked"
        if user_name is None:
            raise IncompleteParams
        api_url_complete = self.api_url + endpoint + "/" + user_name
        while retries != -1:
            result = requests.post(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def unblock_user_request(self, user_name=None, retries=1):
        """Unblock a user request
        Args:
            user_name (str): Name of the user
            retires (int): number of retries upon failure
        Returns:
            None
        """
        endpoint = "/api/user/blocked"
        if user_name is None:
            raise IncompleteParams
        api_url_complete = self.api_url + endpoint + "/" + user_name
        while retries != -1:
            result = requests.delete(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def get_downloads_user_request(self, limit=1, retries=1):
        """Get downloads user request
        Args:
            limit (int): Number of records to return. limit 1 = 25 records
            retires (int): number of retries upon failure
        Returns:
            response as json
        """
        endpoint = "/api/user/downloads"
        api_url_complete = self.api_url + endpoint + "/" + limit
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    def get_topten_heaviest_users(self, retries=1):
        """Get top ten user usage
        Args:
            retires (int): number of retries upon failure
        Returns:
            response as json
        """
        endpoint = "/api/user/heavy"
        api_url_complete = self.api_url + endpoint
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    # Download functions

    def start_download(self, retries=1, server_key=123456789):
        """Start downloading files which have been queued
        Args:
            retires (int): number of retries upon failure
            server_key (str): secret server key which you would set in the Bassa Server
        Returns:
            None
        """
        endpoint = "/api/download/start"
        api_url_complete = self.api_url + endpoint
        self.headers['key'] = server_key
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def kill_download(self, retries=1, server_key=123456789):
        """Kill all downloading files 
        Args:
            retires (int): number of retries upon failure
            server_key (str): secret server key which you would set in the Bassa Server
        Returns:
            None
        """
        endpoint = "/api/download/kill"
        api_url_complete = self.api_url + endpoint
        self.headers['key'] = server_key
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def add_download_request(self, download_link=None, retries=1):
        """Add a download request
        Args:
            download_link (str): Link to the download the resource
            retires (int): number of retries upon failure
        Returns:
            None
        """
        if download_link is None:
            raise IncompleteParams
        endpoint = "/api/download"
        params = {}
        params['link'] = download_link
        api_url_complete = self.api_url + endpoint
        while retries != -1:
            result = requests.post(
                api_url_complete, data=params, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def remove_download_request(self, id=None, retries=1):
        """Remove a download request
        Args:
            id (int): id of the download request 
            retires (int): number of retries upon failure
        Returns:
            None
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + id
        while retries != -1:
            result = requests.delete(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def rate_download_request(self, id=None, rate=None, retries=1):
        """Rate a download request
        Args:
            id (int): id of the download request
            rate (int): rating for the download request
            retires (int): number of retries upon failure
        Returns:
            None
        """
        if id is None or rate is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + id
        params = {}
        params['rate'] = rate
        while retries != -1:
            result = requests.post(
                api_url_complete, data=params, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
            elif int(result.status_code/100) == 5:
                continue

    def get_downloads_request(self, limit=None, retries=1):
        """Get all download requests
        Args:
            limit (int): Number of records to return. limit 1 = 25 records
            retires (int): number of retries upon failure
        Returns:
            returns response as json
        """
        if limit is None:
            raise IncompleteParams
        endpoint = "/api/downloads"
        api_url_complete = self.api_url + endpoint + "/" + limit
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result.json()
            elif int(result.status_code/100) == 5:
                continue

    def get_download(self, id=None, retries=1):
        """Get all download requests
        Args:
            limit (int): Number of records to return. limit 1 = 25 records
            retires (int): number of retries upon failure
        Returns:
            returns response
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + id
        while retries != -1:
            result = requests.get(api_url_complete, headers=self.headers)
            retries = retries-1
            if int(result.status_code/100) in [3, 4]:
                retries = 0
                raise ResponseError(
                    'API response: {}'.format(result.status_code))
            elif int(result.status_code/100) == 2:
                retries = 0
                return result
            elif int(result.status_code/100) == 5:
                continue
