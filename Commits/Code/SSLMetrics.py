import sys
from sqlite3 import Connection, Cursor  # Need these for determining type

import Master
import sqlite_database
from TokenHandler import TokenHandler


class SSLMetrics:
    def __init__(self) -> None:
        self.args = sys.argv[1:]
        self.githubURL = None
        self.githubUser = None
        self.githubRepo = None
        self.githubToken = None
        self.githubTokenList = None
        self.dbCursor = None
        self.dbConnection = None
        self.th = TokenHandler()

    def parseArgs(self) -> None:

        if len(self.args) > 2:
            sys.exit("Too Many Args")
        try:
            self.githubURL = self.args[0]
        except IndexError:
            sys.exit("No URL Arg")
        try:
            self.githubToken = self.args[1]
            self.th.write(token=self.githubToken)
            self.githubTokenList = self.th.read()
        except IndexError:
            self.githubTokenList = self.th.read()
            try:
                self.githubToken = self.githubTokenList[0]
            except IndexError:
                pass

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
sys.exit(0)
