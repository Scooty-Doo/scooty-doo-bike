class Light:
    def __init__(self):
        self.color = 'red'

    def set(self, mode):
        if mode == 'maintenance':
            self.red()
        else:
            self.green()

    def green(self):
        self.color = 'green'

    def red(self):
        self.color = 'red'
