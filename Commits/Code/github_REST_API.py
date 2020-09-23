from sys import exit

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

    def accessGHEndpoint(self, gh_REST_Endpoint: str = "/") -> requests.Response:
        ghAPIURL = (
            "https://api.github.com/repos/"
            + self.ghUser
            + "/"
            + self.ghRepo
            + gh_REST_Endpoint
        )

        try:
            response = requests.get(url=ghAPIURL, headers=self.ghPAToken)
        except Exception as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        keptResponse = response
        response.close()
        return keptResponse

    def accessGHURL(self, ghURL: str = "https://github.com/") -> requests.Response:
        try:
            response = requests.get(url=ghURL, headers=self.ghPAToken)
        except Exception as error:
            print("Unable to utilize token.\n" + error)
            exit(1)
        keptResponse = response
        response.close()
        return keptResponse
