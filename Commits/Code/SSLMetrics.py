from sys import argv, exit
from sqlite3 import Connection, Cursor

from db_connection import DBConnection
from logic import Logic
from token_handler import TokenHandler


class SSLMetrics:
    def __init__(self) -> None:

        argvAmount = len(argv)

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

        Logic(
            ghUser=self.splitGHURL[-2],
            ghRepo=self.splitGHURL[-1],
            ghPAToken=argv[2],
            connection=connection,
            cursor=cursor,
        ).program()


if __name__ == "__main__":
    SSLMetrics().run()
else:
    exit("SSLMetrics.py is meant to be ran as a standalone script.")
