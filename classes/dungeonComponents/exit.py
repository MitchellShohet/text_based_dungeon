class Exit:
    def __init__(self, exit_number, link=None):
        self.exit_number = exit_number
        self.link = link

    def set_link(self, link):
        self.link = link