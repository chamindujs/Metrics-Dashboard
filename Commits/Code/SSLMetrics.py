from sys import argv, exit
from sqlite3 import Connection, Cursor

import Commits.Code.DBConnection
import Commits.Code.Main
from Commits.Code.TokenHandler import TokenHandler


class SSLMetrics:
    def __init__(self) -> None:

        if len(argv) > 3:
            exit("Too many arguements.")

        try:
            self.ghURL = argv[1]
        except IndexError:
            exit("No URL arguement.")

        try:
            self.ghPAToken = argv[2]
        except IndexError:
            exit("No GitHub Personal Access Token arguement")

        self.githubUser = None
        self.githubRepo = None
        self.dbCursor = None
        self.dbConnection = None

    def stripURL(self) -> None:

        if self.githubURL.find("github.com/") == -1:
            sys.exit("Invalid URL Arg")

        foo = self.githubURL.split("/")

        if len(foo) > 5:
            sys.exit("Invalid URL Arg")

        self.githubUser = foo[-2]
        self.githubRepo = foo[-1]

    def launch(self) -> None:
        self.dbCursor, self.dbConnection = sqlite_database.open_connection(
            self.githubRepo
        )
        Master.Logic(
            username=self.githubUser,
            repository=self.githubRepo,
            token=self.githubToken,
            tokenList=self.githubTokenList,
            cursor=self.dbCursor,
            connection=self.dbConnection,
        ).program()


s = SSLMetrics()
s.parseArgs()
s.stripURL()
s.launch()
exit(0)
