class User:
    def __init__(self, client_socket, address):
        self.user_name = None
        self.client_socket = client_socket
        self.address = address
        self.active = True
    
    def __repr__(self):
        print("Name: {}\nSocket: {}\nAddress: {}".format(self.user_name, self.client_socket, self.address))
    
    def set_user_name(self, user_name):
        self.user_name = user_name
    