import os


class TokenHandler:
    def __init__(self):
        if os.path.isfile("tokens.txt"):  # Boolean
            pass
        else:
            open(
                "tokens.txt", "w"
            ).close()  # Gaurentees creation of tokens.txt if it is not created

    def write(self, token: str, mode: str = "a+") -> None:
        tokensFile = open("tokens.txt", mode)  # Opens file in appending mode
        tokensFile.writelines(token + "\n")
        tokensFile.close()

    def writelines(self, data: list = None, mode: str = "a+") -> None:
        tokensFile = open("tokens.txt", mode)
        for item in data:
            tokensFile.write(item + "\n")
        tokensFile.close()

    def read(self) -> list:
        tokensFile = open("tokens.txt", "r")  # Opens the file in read mode
        foo = tokensFile.readlines()
        tokensFile.close()
        return [x.replace("\n", "") for x in foo]

    def deleteValue(self, value: str = None) -> None:
        """
        Deletes all instances of a value in the file.
        """
        data = self.read()
        for x in range(len(data)):
            try:
                data.remove(value)
            except ValueError:
                break
        self.writelines(data=data, mode="w")
