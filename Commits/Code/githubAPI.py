from sys import exit
from urllib.error import HTTPError
import requests


class GitHubAPI:
    def __init__(
        self,
        ghUser: str = None,
        ghRepo: str = None,
        ghPAToken: str = None,
    ):
        self.githubUser = ghUser
        self.githubRepo = ghRepo
        self.githubToken = {"Authorization": "token " + ghPAToken}
        self.responseHeaders = {}

    def accessGHEndpoint(self, ghEndpoint: str = "/") -> dict:
        ghAPIURL = (
            "https://api.github.com/repos/"
            + self.githubUser
            + "/"
            + self.githubRepo
            + ghEndpoint
        )

        try:
            response = requests.get(url=ghAPIURL, headers=self.githubToken)
        except HTTPError as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        self.set_ResponseHeaders(response=response.headers)
        return response.json()

    def accessGHURL(self, ghURL: str = None) -> dict:
        try:
            response = requests.get(url=ghURL, headers=self.githubToken)
        except HTTPError as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        self.set_ResponseHeaders(response=response.headers)
        return response.json()

    def set_ResponseHeaders(self, response: dict) -> None:
        self.responseHeaders = response
