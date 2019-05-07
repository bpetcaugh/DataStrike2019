class Log():
    def __init__(self, filen):
        self.filename = "./logs/" + filen
        self.initialize_file()

    def initialize_file(self):
        with open(self.filename, "w") as myFile:
            myFile.write("DATASTRIKE2019\n")

    def add_to_file(self, line):
        with open(self.filename, "a") as myFile:
            myFile.write(line)       

