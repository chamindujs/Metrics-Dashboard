from sys import argv, exit
from sqlite3 import Connection, Cursor

from Commits.Code.DBConnection import DBConnection
import Commits.Code.Main
from Commits.Code.TokenHandler import TokenHandler


class SSLMetrics:
    def __init__(self) -> None:

        argvAmount = len(argv)

        if argvAmount > 2:
            exit("No GitHub Personal Access Token arguement.")

        if argvAmount > 3:
            exit("Too many arguements.")

        try:
            if argv[1].find("github.com/") == -1:
                raise LookupError

            self.splitGHURL = argv[1].split("/")

            if len(self.splitGHURL) > 5:
                raise LookupError

        except IndexError:
            exit("No GitHub URL arguement.")

        except LookupError:
            exit("Invalid GitHub URL arguement.")

    def run(self) -> None:
        connection, cursor = DBConnection(ghRepo=self.splitGHURL[-1]).dbConnect()

        Master.Logic(
            username=self.splitGHURL[-2],
            repository=self.splitGHURL[-1],
            token=argv[2],
            cursor=self.dbCursor,
            connection=self.dbConnection,
        ).program()


s = SSLMetrics()
s.parseArgs()
s.stripURL()
s.launch()
exit(0)
