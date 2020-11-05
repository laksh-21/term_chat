class Chat():
    users   = {"laksh": "12345", "l": "1"}
    rooms   = {"1": "General", "2": "CP"}
    user    = None
    room    = None

    def main(self):
        self.login()
        self.selectRoom()
        while True:
            self.getInput()

    def login(self):
        user_name = input("Enter your username: ")

        if user_name in self.users:
            password = input("Enter your password: ")
            if(password == self.users[user_name]):
                print("You have been logged in!")
                self.user = user_name
            else:
                print("Incorrrect password!")
                self.login()
        else:
            print("This user does not exist.")
            self.login()

    def selectRoom(self):
        print("No. \t Room Name")
        for room in self.rooms:
            print("{} \t {}".format(room, self.rooms[room]))
        choice = input("Select your choice: ")
        if(choice in self.rooms):
            self.room = self.rooms[choice]
            print("Welcome to the {} room!".format(self.room))
        else:
            print("Invalid Choice!")
            self.selectRoom()

    def getInput(self):
        text = input("{}: ".format(self.user))

chat_app = Chat()
chat_app.main()