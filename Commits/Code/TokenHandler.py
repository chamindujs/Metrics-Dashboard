import os


class TokenHandler:
    def __init__(self):
        if os.path.isfile("tokens.txt"):  # Boolean
            pass
        else:
            open(
                "tokens.txt", "w"
            ).close()  # Gaurentees creation of tokens.txt if it is not created

    def write(self, token: str) -> None:
        with open("tokens.txt", "a+") as tokensFile:  # Opens file in appending mode
            tokensFile.write(token + "\n")
            tokensFile.close()

    def read(self) -> list:
        with open("tokens.txt", "r") as tokensFile:  # Opens the file in read mode
            fileLines = tokensFile.readlines()
            tokensFile.close()
        return [line.replace("\n", "") for line in fileLines]
