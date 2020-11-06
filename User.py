class User:
    def __init__(self, client_socket, address):
        self.user_name = None
        self.client_socket = client_socket
        self.address = address
        self.active = True
    
    def set_user_name(self, user_name):
        self.user_name = user_name
    