from sys import exit
from urllib.error import HTTPError

import requests


class GitHub_REST_API:
    def __init__(
        self,
        ghUser: str = None,
        ghRepo: str = None,
        ghPAToken: str = None,
    ):
        self.ghUser = ghUser
        self.ghRepo = ghRepo
        self.ghPAToken = {"Authorization": "token " + ghPAToken}

    def accessGHEndpoint(self, ghEndpoint: str = "/") -> requests.Response:
        ghAPIURL = (
            "https://api.github.com/repos/"
            + self.ghUser
            + "/"
            + self.ghRepo
            + ghEndpoint
        )

        try:
            response = requests.get(url=ghAPIURL, headers=self.githubToken)
        except HTTPError as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        keptResponse = response
        response.close()
        return keptResponse

    def accessGHURL(self, ghURL: str = "https://github.com/") -> requests.Response:
        try:
            response = requests.get(url=ghURL, headers=self.githubToken)
        except HTTPError as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        keptResponse = response
        response.close()
        return keptResponse
