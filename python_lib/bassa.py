#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Class to encapsulate complete Bassa library functions"""


import re
from errors import InvalidUrl, IncompleteParams, ResponseError
from utils import TimeoutHTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import requests


class Bassa:
    def __init__(self, api_url, total=1, backoff_factor=1, timeout=5):
        """Initializer for a Bassa instance
        Args:
            total (int):    total number of tries for each request
            backoff_factor (int):   It is used to determine the delay between each retry
            follows this formulation {backoff factor} * (2 ** ({number of total retries} - 1))
            timeout (int):  duration in seconds to wait until cancellation
            api_url (str):  URL to the Bassa Server
        Returns:
            None
        """
        retries = Retry(total=total,
                        backoff_factor=backoff_factor,
                        status_forcelist=[429, 500, 502, 503, 504])
        http = requests.Session()
        http.mount("https://",
                   TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
        http.mount("http://",
                   TimeoutHTTPAdapter(max_retries=retries, timeout=timeout))
        self.http = http
        reg = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$',
            re.IGNORECASE)
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
        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)
        if result.status_code == 200:
            self.headers['token'] = result.headers.get('token')
            return self.headers
        else:
            raise ResponseError('API response: {}'.format(result.status_code))

    def add_regular_user_request(self,
                                 user_name=None,
                                 password=None,
                                 email=None):
        """Add user requests with auth level 1
        Args:
            user_name (str):    Name of the user
            password (str):   Password of the user
            email (str): Email ID of the user
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

        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)

    def add_user_request(self,
                         user_name=None,
                         password=None,
                         email=None,
                         auth_level=1):
        """Add user requests with auth level 1 or 0
        Args:
            user_name (str):    Name of the user
            password (str):   Password of the user
            email (str): Email ID of the user
            auth_level (int): Auth level of the user, 0 for admins and 1 for regular users
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

        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)

    def remove_user_request(self, user_name=None):
        """Remove a user request
        Args:
            user_name (str):    Name of the user
         Returns:
            None
        """
        if user_name is None:
            raise IncompleteParams
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint + "/" + user_name

        result = self.http.delete(api_url_complete, headers=self.headers)

    def update_user_request(self,
                            user_name=None,
                            new_user_name=None,
                            password=None,
                            auth_level=None,
                            email=None):
        """Update a user request
        Args:
            user_name (str):    Name of the user to updated
            new_user_name (str): New name for the user
            password (str): New password for the user
            auth_level (int): Auth level for the new user, 0 for admins and 1 for regular users
            email (str): Email ID for the new user
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

        result = self.http.put(api_url_complete,
                               data=params,
                               headers=self.headers)

    def get_user_request(self):
        """Get a user request
         Returns:
            response as json
        """
        endpoint = "/api/user"
        api_url_complete = self.api_url + endpoint

        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def get_user_signup_requests(self):
        """Get all user requests
        Args:
         Returns:
            response as json
        """
        endpoint = "/api/user/requests"
        api_url_complete = self.api_url + endpoint

        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def approve_user_request(self, user_name=None):
        """Approve a user request
        Args:
            user_name (str): Name of the user
         Returns:
            None
        """
        endpoint = "/api/user/approve"
        api_url_complete = self.api_url + endpoint + "/" + user_name
        if user_name is None:
            raise IncompleteParams

            result = self.http.post(api_url_complete, headers=self.headers)

    def get_blocked_users_request(self):
        """Get all blocked user requests 
        Args:
         Returns:
            response as json
        """
        endpoint = "/api/user/blocked"
        api_url_complete = self.api_url + endpoint

        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def block_user_request(self, user_name=None):
        """Block a user request
        Args:
            user_name (str): Name of the user
         Returns:
            None
        """
        endpoint = "/api/user/blocked"
        if user_name is None:
            raise IncompleteParams
        api_url_complete = self.api_url + endpoint + "/" + user_name
        result = self.http.post(api_url_complete, headers=self.headers)

    def unblock_user_request(self, user_name=None):
        """Unblock a user request
        Args:
            user_name (str): Name of the user
         Returns:
            None
        """
        endpoint = "/api/user/blocked"
        if user_name is None:
            raise IncompleteParams
        api_url_complete = self.api_url + endpoint + "/" + user_name
        result = self.http.delete(api_url_complete, headers=self.headers)

    def get_downloads_user_request(self, limit=1):
        """Get downloads user request
        Args:
            limit (int): Number of records to return. limit 1 = 25 records
         Returns:
            response as json
        """
        endpoint = "/api/user/downloads"
        api_url_complete = self.api_url + endpoint + "/" + str(limit)

        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def get_topten_heaviest_users(self):
        """Get top ten user usage
        Args:
         Returns:
            response as json
        """
        endpoint = "/api/user/heavy"
        api_url_complete = self.api_url + endpoint
        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    # Download functions

    def start_download(self, server_key="123456789"):
        """Start downloading files which have been queued
        Args:
             server_key (str): secret server key which you would set in the Bassa Server
        Returns:
            None
        """
        endpoint = "/api/download/start"
        api_url_complete = self.api_url + endpoint
        self.headers['key'] = server_key
        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def kill_download(self, server_key="123456789"):
        """Kill all downloading files 
        Args:
             server_key (str): secret server key which you would set in the Bassa Server
        Returns:
            None
        """
        endpoint = "/api/download/kill"
        api_url_complete = self.api_url + endpoint
        self.headers['key'] = server_key
        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def add_download_request(self, download_link=None):
        """Add a download request
        Args:
            download_link (str): Link to the download the resource
         Returns:
            None
        """
        if download_link is None:
            raise IncompleteParams
        endpoint = "/api/download"
        params = {}
        params['link'] = download_link
        api_url_complete = self.api_url + endpoint
        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)

    def remove_download_request(self, id=None):
        """Remove a download request
        Args:
            id (int): id of the download request 
         Returns:
            None
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + str(id)
        result = self.http.delete(api_url_complete, headers=self.headers)

    def rate_download_request(self, id=None, rate=None):
        """Rate a download request
        Args:
            id (int): id of the download request
            rate (int): rating for the download request
         Returns:
            None
        """
        if id is None or rate is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + str(id)
        params = {}
        params['rate'] = rate

        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)

    def get_downloads_request(self, limit=None):
        """Get all download requests
        Args:
            limit (int): Number of records to return. limit 1 = 25 records
         Returns:
            returns response as json
        """
        if limit is None:
            raise IncompleteParams
        endpoint = "/api/downloads"
        api_url_complete = self.api_url + endpoint + "/" + str(limit)

        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def get_download(self, id=None):
        """Get all download requests
        Args:
            id (int): id of the download
         Returns:
            returns response as json
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/download"
        api_url_complete = self.api_url + endpoint + "/" + str(id)
        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    # File functions

    def start_compression(self, gid_list=None):
        """Start compression of the given files
        Args:
            gid_list (List): list of file identifiers to compress
         Returns:
            returns response
        """
        if gid_list is None:
            raise IncompleteParams
        endpoint = "/api/compress"
        api_url_complete = self.api_url + endpoint
        params = {}
        params['gid'] = gid_list
        result = self.http.post(api_url_complete,
                                data=params,
                                headers=self.headers)

    def get_compression_progress(self, id=None):
        """Get all download requests
        Args:
            id (int): compression id
         Returns:
            returns response as json
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/compression-progress"
        api_url_complete = self.api_url + endpoint + "/" + str(id)
        result = self.http.get(api_url_complete, headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()

    def send_file_from_path(self, id=None):
        """Get all download requests
        Args:
            id (int): id of the file
         Returns:
            returns response as json
        """
        if id is None:
            raise IncompleteParams
        endpoint = "/api/file"
        params = {}
        params['gid'] = id
        api_url_complete = self.api_url + endpoint
        result = self.http.get(api_url_complete,
                               params=params,
                               headers=self.headers)
        if result.status_code == requests.codes.ok:
            return result.json()
