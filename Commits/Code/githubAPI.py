import sys
from http.client import HTTPResponse
from json import dumps, load
from sqlite3 import Connection, Cursor
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class GitHubAPI:
    def __init__(
        self,
        username: str = None,
        repository: str = None,
        token: str = None,
        tokenList: list = None,
    ):
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubTokenList = tokenList
        self.githubAPIURL = None
        self.responseHeaders = None

    def access_GitHubRepoCommits(self) -> dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/commits?state=all")

    def access_GitHubRepoIssues(self) -> dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/issues?state=all")

    def access_GitHubRepoPulls(self) -> dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/pulls?state=all")

    def build_RequestObj(self, url: str = None) -> Request:
        foo = Request(url=url)
        if self.githubToken != None:
            bar = "token " + self.githubToken
            foo.add_header("Authorization", bar)
        return foo

    def access_GitHubAPISpecificEndpoint(self, endpoint: str = "") -> dict:
        self.githubAPIURL = (
            "https://api.github.com/repos/"
            + self.githubUser
            + "/"
            + self.githubRepo
            + endpoint
        )
        request = self.build_RequestObj(url=self.githubAPIURL)
        try:
            foo = urlopen(url=request)
        except HTTPError as error:
            try:
                bar = self.githubTokenList.index(self.githubToken)
                self.set_GitHubToken(self.githubTokenList[bar + 1])
                print("Switching token to: " + self.githubToken)
                self.access_GitHubAPISpecificEndpoint(endpoint=endpoint)
            except IndexError:
                print("Unable to utilize next token: IndexError")
                sys.exit(error)
            except ValueError:
                print("Unable to utilize next token: ValueError")
                sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)

    def access_GitHubAPISpecificURL(self, url: str = None) -> dict:
        self.githubAPIURL = url
        request = self.build_RequestObj(url=self.githubAPIURL)
        try:
            foo = urlopen(url=request)
        except HTTPError as error:
            try:
                bar = self.githubTokenList.index(self.githubToken)
                self.set_GitHubToken(self.githubTokenList[bar + 1])
                print("Switching token to", self.githubTokenList[bar + 1])
                self.access_GitHubAPISpecificEndpoint(url)
            except IndexError:
                print("Unable to utilize next token: IndexError")
                sys.exit(error)
            except ValueError:
                print("Unable to utilize next token: ValueError")
                sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)

    def get_GitHubToken(self) -> str:
        return self.githubToken

    def get_GitHubUser(self) -> str:
        return self.githubUser

    def get_GitHubRepo(self) -> str:
        return self.githubRepo

    def get_GitHubAPIURL(self) -> str:
        return self.githubAPIURL

    def get_ResponseHeaders(self) -> dict:
        return self.responseHeaders

    def set_GitHubUser(self, username: str = None) -> None:
        self.githubUser = username

    def set_GitHubRepo(self, repository: str = None) -> None:
        self.githubRepo = repository

    def set_GitHubAPIURL(self, username: str = None, repository: str = None) -> None:
        self.set_GitHubUser(username=username)
        self.set_GitHubRepo(repository=repository)
        self.githubAPIURL = (
            "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo
        )

    def set_GitHubToken(self, token: str = None) -> None:
        self.githubToken = token

    def set_ResponseHeaders(self, response: HTTPResponse) -> None:
        self.responseHeaders = dict(response.getheaders())
