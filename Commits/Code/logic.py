from datetime import datetime, timedelta
from sqlite3 import Connection, Cursor

from commits import Commits
from github_REST_API import GitHub_REST_API


class Logic:
    def __init__(
        self,
        username: str = None,
        repository: str = None,
        token: str = None,
        tokenList: list = None,
        cursor: Cursor = None,
        connection: Connection = None,
    ) -> None:
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubTokenList = tokenList
        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = None
        self.gha = None

    def program(self) -> None:

        self.set_Data(endpoint="")
        repoConcptionDateTime = datetime.strptime(
            self.data[0]["created_at"].replace("T", " ").replace("Z", ""),
            "%Y-%m-%d %H:%M:%S",
        )
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)

        self.set_Data(endpoint="commits")
        Commits.Logic(
            gha=self.gha,
            data=self.data[0],
            responseHeaders=self.data[1],
            cursor=self.dbCursor,
            connection=self.dbConnection,
        ).parser()

        for foo in datetimeList:

            date = datetime.strptime(foo[:10], "%Y-%m-%d")

            date = str(date)

            self.dbCursor.execute(
                "SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('"
                + date
                + "');"
            )
            rows = self.dbCursor.fetchall()
            commits = rows[0][0]

            sql = "INSERT INTO MASTER (date, commits) VALUES (?,?) ON CONFLICT(date) DO UPDATE SET commits = (?);"
            self.dbCursor.execute(sql, (date, str(commits), str(commits)))

            self.dbConnection.commit()

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
        self.gha = GitHub_REST_API(
            username=self.githubUser,
            repository=self.githubRepo,
            token=self.githubToken,
            tokenList=self.githubTokenList,
        )
        if endpoint == "commits":
            self.data = [
                self.gha.access_GitHubRepoCommits(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "issues":
            self.data = [
                self.gha.access_GitHubRepoIssues(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "pulls":
            self.data = [
                self.gha.access_GitHubRepoPulls(),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint == "":
            self.data = [
                self.gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
        elif endpoint[0] == "/":
            self.data = [
                self.gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
        else:
            self.data = [
                self.gha.access_GitHubAPISpecificURL(url=endpoint),
                self.gha.get_ResponseHeaders(),
            ]
