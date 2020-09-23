from datetime import datetime, timedelta
from sqlite3 import Connection, Cursor

import Commits
from Commits.Code.GitHub_REST_API import GitHub_REST_API


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
        """
        Initalizes the class and sets class variables that are to be used only in this class instance.\n
        :param username: The GitHub username.\n
        :param repository: The GitHub repository.\n
        :param token: The personal access token from the user who initiated the program.
        :param tokenList: A list of tokens that will be iterated through.\n
        :param data: The dictionary of data that is returned from the API call.\n
        :param responseHeaders: The dictionary of data that is returned with the API call.\n
        :param cursor: The database cursor.\n
        :param connection: The database connection.
        """
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubTokenList = tokenList
        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = None
        self.gha = None

    def program(self) -> None:
        """
        Calls classes and methods to analyze and interpret data.
        """
        # Gets and stores data from the root api endpoint
        self.set_Data(endpoint="")
        repoConcptionDateTime = datetime.strptime(
            self.data[0]["created_at"].replace("T", " ").replace("Z", ""),
            "%Y-%m-%d %H:%M:%S",
        )

        # Index 0 = Current datetime, Index -1 = conception datetime
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)

        # Gets and stores data from the commits api endpoint
        self.set_Data(endpoint="commits")
        Commits.Logic(
            gha=self.gha,
            data=self.data[0],
            responseHeaders=self.data[1],
            cursor=self.dbCursor,
            connection=self.dbConnection,
        ).parser()

        # Adds all of the datetimes to the SQL database
        # Bewary of changing
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
        """
        Creates a list of datetimes from the repository conception datetime till today's current datetime.\n
        :param rCDT: Repository conception datetime. This is found in the root api call of a repository.
        """
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

    def get_Data(self) -> dict:
        """
        Returns the class variable data.
        """
        return self.data

    def get_DbConnection(self) -> Connection:
        """
        Returns the class variable dbConnection.
        """
        return self.dbConnection

    def get_DbCursor(self) -> Cursor:
        """
        Returns the class variable dbCursor.
        """
        return self.dbCursor

    def get_GitHubRepo(self) -> str:
        """
        Returns the class variable githubRepo.
        """
        return self.githubRepo

    def get_GitHubToken(self) -> str:
        """
        Returns the class variable githubToken.
        """
        return self.githubToken

    def get_GitHubUser(self) -> str:
        """
        Returns the class variable githubUser.
        """
        return self.githubUser

    def set_Data(self, endpoint: str = "/") -> None:
        """
        This method is used to set the most recent GitHub API call into self.data.\n
        This data should be moved into it's own instance before this is called again in order to prevent the data from being overwritten.\n
        :param endpoint: This can be "commits", "issues", "pulls", "", or some other endpoint that is supported by the GitHub API as long as it is accessible with the root url https://api.github.com/{USER}/{REPOSITORY}
        """
        endpoint = endpoint.lower()
        self.gha = GitHubAPI(
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
