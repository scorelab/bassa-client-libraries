import unittest
from errors import InvalidUrl, IncompleteParams, ResponseError
from bassa import Bassa

import time

import logging
import sys


class TestBassaPythonLib(unittest.TestCase):

    client = Bassa(api_url="http://localhost:5000")
    INVALID_URL = "hppts://localhost:5000"
    VALID_URL = "http://localhost:5000"
    TEST_USERS = [["rand", "pass", "rand@scorelab.org"],
                  ["Mehant", "secretpass", "kmehant@scorelab.org"],
                  ["MehantAdmin", "secretpass", "kmehant@scorelab.org"],
                  ["Mehant2", "secretpass2", "kmehant2@scorelab.org"],
                  ["blockeduser", "blockedpass", "blockedemail@scorelab.org"]]
    DOWNLOAD_LINK = "http://www.scorelab.org/assets/img/score.jpg"

    def test_url(self):
        """Test input URL"""
        self.assertRaises(InvalidUrl, Bassa, self.INVALID_URL)

    def test_login(self):
        """Test user login"""
        result = self.client.login(
            user_name=self.TEST_USERS[0][0], password=self.TEST_USERS[0][1])
        time.sleep(10)

    def test_add_regular_user_request(self):
        """Test adding a regular user request"""
        self.client.add_regular_user_request(
            user_name=self.TEST_USERS[1][0], password=self.TEST_USERS[1][1], email=self.TEST_USERS[1][2])
        time.sleep(10)

    def test_add_user_request(self):
        """Test adding a user request"""
        self.client.add_user_request(
            user_name=self.TEST_USERS[2][0], password=self.TEST_USERS[2][1], email=self.TEST_USERS[2][2])
        time.sleep(10)

    def test_remove_user_request(self):
        """Test removing a user request"""
        self.client.remove_user_request(user_name=self.TEST_USERS[1][0])
        time.sleep(10)

    def test_update_user_request(self):
        """Test updating a user request"""
        self.client.update_user_request(user_name=self.TEST_USERS[2][0], new_user_name="Mehant",
                                        password="newsecretpass", auth_level=0, email="kmehant@gmail.com")
        time.sleep(10)

#    def test_get_user_signup_requests(self):
#        """Test getting all user requests"""
#        result = self.client.get_user_signup_requests()
#        print(result)
#        time.sleep(10)

    def test_approve_user_request(self):
        """Test approving a user request"""
        self.client.add_user_request(
            user_name=self.TEST_USERS[3][0], password=self.TEST_USERS[3][1], email=self.TEST_USERS[3][2])
        self.client.approve_user_request(user_name=self.TEST_USERS[3][0])
        time.sleep(10)

    def test_block_user_request(self):
        """Test blocking a user request"""
        self.client.add_regular_user_request(
            user_name=self.TEST_USERS[4][0], password=self.TEST_USERS[4][1], email=self.TEST_USERS[4][2])
        self.client.block_user_request(user_name=self.TEST_USERS[4][0])
        time.sleep(10)

#    def test_get_blocked_users_request(self):
#        """Test getting blocked user requests"""
#        result = self.client.get_blocked_users_request()
#        print(result)
#        time.sleep(10)

    def test_unblock_user_request(self):
        """Test unblocking a user request"""
        self.client.unblock_user_request(user_name=self.TEST_USERS[4][0])
        time.sleep(10)

    def test_add_download_request(self):
        """Test adding a download request"""
        self.client.add_download_request(download_link=self.DOWNLOAD_LINK)
        time.sleep(10)

#    def test_get_topten_heaviest_users(self):
#        """Test getting top ten heaviest users"""
#        result = self.client.get_topten_heaviest_users()
#        print(result)
#        time.sleep(10)

#    def test_get_downloads_request(self):
#        """Test getting all download requests"""
#        result = self.client.get_downloads_request(limit=1)
#        print(result)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("BassaPythonClientLibrary").setLevel(logging.ERROR)
    unittest.main()
