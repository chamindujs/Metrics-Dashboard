import os
import sqlite3
from time import time


class DBConnection:
    def __init__(self, directory: str = "/metrics", ghRepo: str = "temporary"):

        count = 0
        fileExists = True
        directoryExists = False

        self.filePath = None

        dbFilePath = (
            lambda path, num: path
            + r"/"
            + ghRepo
            + "_"
            + str(int(time()))
            + "_"
            + str(num)
            + ".db"
        )

        while directory is False:
            if os.path.isdir(directory):
                directoryExists = True
            else:
                os.mkdir(directory)

        while fileExists is True:
            if os.path.isfile(dbFilePath(directory, count)):
                count += 1
            else:
                self.filePath = dbFilePath(directory, count)
                fileExists = False

    def open_connection(repo_name):
        try:
            connection = sqlite3.connect("/metrics/" + str(repo_name) + ".db")
        except sqlite3.OperationalError:
            connection = sqlite3.connect("/metrics/" + str(repo_name) + ".db")

        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS COMMITS (author VARCHAR(3000), author_date VARCHAR(3000), committer VARCHAR(3000), committer_date VARCHAR(3000), commits_url VARCHAR(3000), message VARCHAR(30000), comment_count VARCHAR(3000), comments_url VARCHAR(3000));"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS MASTER(date DATE, commits INT(3000), issues INT(3000), defect_density INT(3000), issue_spoilage_avg INT(3000), issue_spoilage_max INT(3000), issue_spoilage_min INT(3000), lines_of_code INT(300), num_of_chars INT(300), PRIMARY KEY (date));"
        )

        connection.commit()

        return cursor, connection
