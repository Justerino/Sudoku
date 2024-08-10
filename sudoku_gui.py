import tkinter as tk
from sudoku_board import SudokuBoard
import time

class SudokuGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Sudoku')
        self.window.resizable(False, False)

        self.board = SudokuBoard()

        # Set the background color of the main window and add padding around the grid
        self.window.configure(bg='steelblue')
        self.frame = tk.Frame(self.window, bg='black', padx=20, pady=20)  # Adjusted padding
        self.frame.grid(row=0, column=0)

        self.entries = []
        self.create_grid()

        # Initialize the pencil mode variable here
        self.is_pencil_mode = tk.BooleanVar(value=False)

        # Adjust button frame to accommodate the new number pad layout
        self.button_frame = tk.Frame(self.window, bg='steelblue', padx=10, pady=10)
        self.button_frame.grid(row=0, column=1, sticky='n')

        self.create_buttons()

        self.window.bind("<Button-1>", self.on_global_click)

        self.selected_row = None
        self.selected_col = None

    # --- Grid Setup Methods ---
    def create_grid(self):
        for i in range(9):
            row_entries = []
            for j in range(9):
                top_pad = 5 if i % 3 == 0 and i != 0 else 1
                left_pad = 5 if j % 3 == 0 and j != 0 else 1

                text_widget = tk.Text(self.frame, bg='lemon chiffon', width=4, height=2, padx=10, pady=10,
                                      font=('Arial', 24), wrap='none', insertontime=False)
                text_widget.grid(row=i, column=j, padx=(left_pad, 1), pady=(top_pad, 1))

                self.configure_text_widget(text_widget)

                text_widget.bind('<Button-1>', lambda e, row=i, col=j: self.on_cell_select(row, col))
                text_widget.bind('<KeyPress>', lambda e, row=i, col=j: self.on_key_press(e, row, col))

                row_entries.append(text_widget)
            self.entries.append(row_entries)

    def configure_text_widget(self, text_widget):
        text_widget.tag_configure("center", justify='center')
        text_widget.insert("1.0", "")
        text_widget.tag_add("center", "1.0", "end")

    # --- Button and Input Handling Methods ---
    def create_buttons(self):
        button_width = 10
        button_height = 2
        num_button_width = 5

        difficulties = {'Easy': 'palegreen', 'Medium': 'light goldenrod', 'Hard': 'salmon'}

        # Difficulty buttons
        for i, (difficulty, color) in enumerate(difficulties.items()):
            tk.Button(self.button_frame, bg=color, text=difficulty, width=button_width, height=button_height,
                      command=lambda d=difficulty: self.generate_puzzle(d)).grid(row=i, column=0, columnspan=3, padx=5,
                                                                                 pady=5)

        # Pencil Mode toggle button
        pencil_button = tk.Checkbutton(self.button_frame, text="Pencil Mode", variable=self.is_pencil_mode)
        pencil_button.grid(row=len(difficulties), column=0, columnspan=3, padx=5, pady=5)

        # Arrange number pad buttons in a 3x3 grid like a standard keypad
        numbers = [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3]
        ]

        for i, row in enumerate(numbers):
            for j, num in enumerate(row):
                tk.Button(self.button_frame, text=str(num), width=num_button_width, height=button_height,
                          command=lambda n=num: self.on_num_pad_click(n)).grid(row=i + len(difficulties) + 1, column=j,
                                                                               padx=2, pady=2)

    def on_num_pad_click(self, num):
        self.handle_input(num)

    def on_key_press(self, event, row, col):
        if event.char.isdigit() and 1 <= int(event.char) <= 9:
            self.selected_row = row
            self.selected_col = col

            event.widget.delete("1.0", tk.END)
            self.handle_input(int(event.char))

            return "break"

    def handle_input(self, num):
        if self.selected_row is not None and self.selected_col is not None:
            text_widget = self.entries[self.selected_row][self.selected_col]

            if self.is_pencil_mode.get():
                self.add_pencil_marks(text_widget, num)
            else:
                self.set_pen_value(text_widget, num)
                self.on_cell_change(self.selected_row, self.selected_col, None)

            text_widget.tag_add("center", "1.0", "end")
            self.update_highlights()

    def add_pencil_marks(self, text_widget, num):
        current_text = text_widget.get("1.0", tk.END).strip()
        pencil_marks = current_text.split()

        if len(pencil_marks) < 3 and str(num) not in pencil_marks:
            new_text = current_text + " " + str(num) if current_text else str(num)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", new_text)
            text_widget.tag_add("pencil", "1.0", tk.END)
            text_widget.tag_config("pencil", foreground="grey", font=("Arial", 24))

    def set_pen_value(self, text_widget, num):
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", str(num))
        text_widget.tag_add("pen", "1.0", tk.END)
        text_widget.tag_config("pen", foreground="black", font=("Arial", 48))

    # --- Highlighting Methods ---
    def on_cell_select(self, row, col):
        self.selected_row = row
        self.selected_col = col
        self.update_highlights()

    def update_highlights(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(bg='lemon chiffon')

        if self.selected_row is not None and self.selected_col is not None:
            self.highlight_related_cells()

    def highlight_related_cells(self):
        selected_value = self.board.get_value(self.selected_row, self.selected_col)

        if selected_value is not None:
            for i in range(9):
                for j in range(9):
                    if self.board.get_value(i, j) == selected_value:
                        self.entries[i][j].config(bg='lightgreen')

        self.entries[self.selected_row][self.selected_col].config(bg='lightblue')

        for i in range(9):
            if i != self.selected_row:
                self.entries[i][self.selected_col].config(bg='lightyellow')
            if i != self.selected_col:
                self.entries[self.selected_row][i].config(bg='lightyellow')

        start_row, start_col = 3 * (self.selected_row // 3), 3 * (self.selected_col // 3)
        for i in range(3):
            for j in range(3):
                r, c = start_row + i, start_col + j
                if r != self.selected_row and c != self.selected_col:
                    self.entries[r][c].config(bg='lightyellow')

    # --- Puzzle Management Methods ---
    def generate_puzzle(self, difficulty):
        seed = int(time.time() * 1000)
        print(f"Generating puzzle with seed: {seed}")
        self.board.generate_puzzle(difficulty, seed)
        self.update_gui()

    def update_gui(self):
        for i in range(9):
            for j in range(9):
                text_widget = self.entries[i][j]
                cell_value = self.board.get_value(i, j)
                text_widget.delete("1.0", tk.END)

                if cell_value is not None:
                    text_widget.insert("1.0", str(cell_value))
                    text_widget.tag_add("pen", "1.0", tk.END)
                    text_widget.tag_config("pen", foreground="black", font=("Arial", 48))
                    text_widget.tag_add("center", "1.0", "end")

    # --- Global Click Binding ---
    def on_global_click(self, event):
        widget = event.widget
        if widget not in [self.entries[i][j] for i in range(9) for j in range(9)] and not isinstance(widget, tk.Button):
            self.selected_row = None
            self.selected_col = None
            self.update_highlights()

    def on_cell_change(self, row, col, event):
        value = self.entries[row][col].get("1.0", tk.END).strip()

        if value.isdigit():
            num = int(value)
            current_value = self.board.get_value(row, col)
            self.board.set_value(row, col, None)

            if self.board.is_valid(row, col, num):
                self.board.set_value(row, col, num)
                self.entries[row][col].config(bg='lemon chiffon')
            else:
                self.entries[row][col].config(bg='firebrick')
                self.window.after(200, lambda: self.clear_invalid_entry(row, col))

            if self.board.get_value(row, col) is None:
                self.board.set_value(row, col, current_value)
        else:
            self.entries[row][col].delete("1.0", tk.END)

        self.entries[row][col].tag_add("center", "1.0", "end")
        self.update_highlights()

    def clear_invalid_entry(self, row, col):
        self.entries[row][col].delete("1.0", tk.END)
        self.entries[row][col].config(bg='firebrick')

    # --- Running the Game ---
    def run(self):
        self.window.mainloop()
