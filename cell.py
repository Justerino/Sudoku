class Cell:
    def __init__(self, value=None):
        self.value = value
        self.pencil_marks = []
        self.is_fixed = False

    def set_value(self, value):
        if not self.is_fixed:
            self.value = value

    def clear(self):
        if not self.is_fixed:
            self.value = None

    def add_pencil_mark(self, value):
        if value not in self.pencil_marks:
            self.pencil_marks.append(value)

    def remove_pencil_mark(self, value):
        if value in self.pencil_marks:
            self.pencil_marks.remove(value)