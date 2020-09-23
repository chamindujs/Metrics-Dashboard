from datetime import datetime, timedelta
from sqlite3 import Connection, Cursor
from sys import exit

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

        try:
            if ghUser is None:
                raise ValueError
            if ghRepo is None:
                raise ValueError
            if ghPAToken is None:
                raise ValueError
            if connection is None:
                raise ValueError
            if cursor is None:
                raise ValueError

        except ValueError:
            exit("Insufficent arguements passed into logic.py")

        self.githubUser = ghUser
        self.githubRepo = ghRepo
        self.githubToken = ghPAToken

        self.cursor = cursor
        self.connection = connection

    def program(self) -> None:

        self.set_Data(endpoint="")
        repoConcptionDateTime = datetime.strptime(
            self.data[0]["created_at"].replace("T", " ").replace("Z", ""),
            "%Y-%m-%d %H:%M:%S",
        )
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)

        self.set_Data(endpoint="commits")
        Commits.Logic(
            gha=self.gh_REST_API,
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
        self.gh_REST_API = GitHub_REST_API(
            ghUser=self.githubUser,
            ghRepo=self.githubRepo,
            ghPAToken=self.githubToken,
        )
        self.data = self.__accessGHEndpoint__(
            gh_REST_API=self.gh_REST_API, gh_REST_Endpoint=endpoint
        )

    def __accessGHEndpoint__(
        self, gh_REST_API: GitHub_REST_API, gh_REST_Endpoint
    ) -> tuple:
        ghResponse = gh_REST_API.accessGHEndpoint(gh_REST_Endpoint)

        return (ghResponse.json(), ghResponse.headers)


if __name__ == "__main__":
    exit("logic.py is meant to be imported as a module.")
else:
    pass
