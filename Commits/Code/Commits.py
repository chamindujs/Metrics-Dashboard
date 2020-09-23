from datetime import datetime
from sqlite3 import Connection, Cursor

from githubAPI import GitHubAPI


class Logic:
    def __init__(
        self,
        gha: GitHubAPI = None,
        data: dict = None,
        responseHeaders: tuple = None,
        cursor: Cursor = None,
        connection: Connection = None,
    ):
        self.gha = gha
        self.data = data
        self.responseHeaders = responseHeaders
        self.dbCursor = cursor
        self.dbConnection = connection

    def parser(self) -> None:
        while True:
            for x in range(len(self.data)):

                author = "NA"
                author_date = "NA"
                committer = "NA"
                committer_date = "NA"
                message = "NA"
                comment_count = "NA"
                commits_url = "NA"
                comments_url = "NA"

                try:
                    author = self.data[x]["commit"]["author"]["name"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    committer = self.data[x]["commit"]["committer"]["name"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    message = self.data[x]["commit"]["message"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    comment_count = self.data[x]["commit"]["comment_count"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    commits_url = self.data[x]["commit"]["url"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    comments_url = self.data[x]["comments_url"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    author_date = (
                        self.data[x]["commit"]["author"]["date"]
                        .replace("T", " ")
                        .replace("Z", " ")
                    )
                    author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    committer_date = (
                        self.data[x]["commit"]["committer"]["date"]
                        .replace("T", " ")
                        .replace("Z", " ")
                    )
                    committer_date = datetime.strptime(
                        committer_date, "%Y-%m-%d %H:%M:%S "
                    )
                except KeyError:
                    pass
                except AttributeError:
                    pass

                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(
                    sql,
                    (
                        str(author),
                        str(author_date),
                        str(committer_date),
                        str(committer),
                        str(commits_url),
                        str(message),
                        str(comment_count),
                        str(comments_url),
                    ),
                )
                self.dbConnection.commit()

            try:
                foo = self.responseHeaders["Link"]
                if 'rel="next"' not in foo:
                    break

                else:
                    bar = foo.split(",")

                    for x in bar:
                        if 'rel="next"' in x:
                            url = x[x.find("<") + 1 : x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()
            except KeyError:
                print(self.responseHeaders)
                break
            break
