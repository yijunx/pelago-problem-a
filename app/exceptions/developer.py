class DeveloperDoesNotExist(Exception):
    def __init__(self, name: str):
        self.message = f"Developer with name {name} does not exist"
        self.http_code = 404
    

class DeveloperAlreadyExist(Exception):
    def __init__(self, name: str):
        self.message = f"Developer with name {name} already exist"
        self.http_code = 404