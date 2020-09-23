from datetime import datetime, timedelta
from sqlite3 import Connection, Cursor

from commits import Commits
from github_REST_API import GitHub_REST_API


class Logic:
    def __init__(
        self,
        ghUser: str = None,
        ghRepo: str = None,
        ghPAToken: str = None,
        connection: Connection = None,
        cursor: Cursor = None,
    ) -> None:

        self.githubUser = ghUser
        self.githubRepo = ghRepo
        self.githubToken = ghPAToken

        self.cursor = cursor
        self.connection = connection

        self.data = None
        self.gh_REST_API = None

    def program(self) -> None:

        self.set_Data(endpoint="")
        repoConcptionDateTime = datetime.strptime(
            self.data[0]["created_at"].replace("T", " ").replace("Z", ""),
            "%Y-%m-%d %H:%M:%S",
        )
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)

        self.set_Data(endpoint="commits")
        Commits.Logic(
            gha=gh_REST_API,
            data=self.data[0],
            responseHeaders=self.data[1],
            cursor=self.cursor,
            connection=self.connection,
        ).parser()

        for foo in datetimeList:

            date = datetime.strptime(foo[:10], "%Y-%m-%d")

            date = str(date)

            self.cursor.execute(
                "SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('"
                + date
                + "');"
            )
            rows = self.cursor.fetchall()
            commits = rows[0][0]

            sql = "INSERT INTO MASTER (date, commits) VALUES (?,?) ON CONFLICT(date) DO UPDATE SET commits = (?);"
            self.cursor.execute(sql, (date, str(commits), str(commits)))

            self.connection.commit()

    def generate_DateTimeList(self, rCDT: datetime) -> list:
        foo = []
        today = datetime.today()
        if rCDT.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            foo.append(str(today))
        else:
            foo.append(str(today))
            while today > rCDT:
                today = today - timedelta(days=1)
                foo.append(str(today))
        return foo

    def set_Data(self, endpoint: str = "/") -> None:
        endpoint = endpoint.lower()
        gh_REST_API = GitHub_REST_API(
            username=self.githubUser,
            repository=self.githubRepo,
            token=self.githubToken,
        )
        if endpoint == "commits":
            self.data = [
                gh_REST_API.access_GitHubRepoCommits(),
                gh_REST_API.get_ResponseHeaders(),
            ]
        elif endpoint == "issues":
            self.data = [
                gh_REST_API.access_GitHubRepoIssues(),
                gh_REST_API.get_ResponseHeaders(),
            ]
        elif endpoint == "pulls":
            self.data = [
                gh_REST_API.access_GitHubRepoPulls(),
                gh_REST_API.get_ResponseHeaders(),
            ]
        elif endpoint == "":
            self.data = [
                gh_REST_API.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                gh_REST_API.get_ResponseHeaders(),
            ]
        elif endpoint[0] == "/":
            self.data = [
                gh_REST_API.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                gh_REST_API.get_ResponseHeaders(),
            ]
        else:
            self.data = [
                gh_REST_API.access_GitHubAPISpecificURL(url=endpoint),
                gh_REST_API.get_ResponseHeaders(),
            ]
