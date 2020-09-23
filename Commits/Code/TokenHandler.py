import os


class TokenHandler:
    def __init__(self):
        if os.path.isfile("tokens.txt"):
            pass
        else:
            open("tokens.txt", "w").close()

    def write(self, token: str) -> None:
        with open("tokens.txt", "a+") as tokensFile:
            tokensFile.write(token + "\n")
            tokensFile.close()

    def read(self) -> list:
        with open("tokens.txt", "r") as tokensFile:
            fileLines = tokensFile.readlines()
            tokensFile.close()
        return [line.replace("\n", "") for line in fileLines]
