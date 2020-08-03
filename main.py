#-------------------------------------------
# sudoku solver based on tkinter library
# 2020, by Giuseppe Campanella with <3
#-------------------------------------------

import tkinter as tk
from tkinter import messagebox

class Sudoku():
    def __init__(self, m, entries):
        self.m = m
        self.entries = entries
        self.print_solution()

    def print_matrix(self):
        cnt = 0
        print()
        for i in range(0, 9):
            for j in range(0, 9):
                if(j != 0 and j%3 == 0):
                    print("|", end='')
                print(self.m[i][j], end=' ')
            print()
            cnt += 1
            if(cnt != 9 and cnt % 3 == 0):
                for j in range(0, 9*2 + 1):
                    print("_", end='')
                print()
        print()

    def check_possibile_value(self, v, x, y):
        for i in range(0, 9):
            if(self.m[x][i] == v):
                return False

        for i in range(0, 9):
            if(self.m[i][y] == v):
                return False

        # check the square
        x0, y0 = (x//3)*3, (y//3)*3
        for i in range(x0,x0 + 3):
            for j in range(y0,y0 + 3):
                if(self.m[i][j] == v):
                    return False

        return True

    def check_value(self, v, x, y):
        for i in range(0, 9):
            if(i!=y and self.m[x][i] == v):
                return False

        for i in range(0, 9):
            if(i!=x and self.m[i][y] == v):
                return False

        # check the square
        x0, y0 = (x//3)*3, (y//3)*3
        for i in range(x0,x0 + 3):
            for j in range(y0,y0 + 3):
                if(i!=x and j!=y and self.m[i][j] == v):
                    return False

        return True

    def solve(self):
        for i in range(0,9):
            for j in range(0,9):
                if(self.m[i][j] == 0):
                    for val in range(1, 10):
                        if(self.check_possibile_value(val, i, j)):
                            self.m[i][j] = val
                            if(self.solve()):
                                return True
                            # backtrack
                            self.m[i][j] = 0
                    return False
        # found a solution
        return True

    def print_solution(self):
        for i in range(0,9):
            for j in range(0,9):
                val = self.m[i][j]
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                if(val == 0):
                    val = ""
                entry.insert(0, val)

    def solve_sudoku(self):
        self.check_input()
        if(self.valid_input):
            is_solvable = self.solve()
            if(is_solvable):
                self.print_solution()
            else:
                messagebox.showwarning("Warning", "This input did not led to a solution. Try another input.")

    def read_sudoku_from_window(self):
        for i in range(0,9):
            for j in range(0,9):
                entry = self.entries[i][j]
                entry.config({"background" : "white"})
                val = entry.get()
                if(len(val) == 0):
                    val = 0
                else:
                    val = int(val)
                if(val < 1 or val > 9):
                    val = 0
                self.m[i][j] = val

    def clear_window(self):
        for i in range(0,9):
            for j in range(0,9):
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, "")
                entry.config({"background" : "white"})

    def check_input_sudoku(self):
        self.valid_input = True
        for i in range(0,9):
            for j in range(0,9):
                if(self.m[i][j] != 0):
                    valid = self.check_value(self.m[i][j], i, j)
                    if(not valid):
                        self.valid_input = False
                        self.change_color_bg_entries(i, j)

    def check_input(self, messageinfo=False):
        self.read_sudoku_from_window()
        self.check_input_sudoku()
        if(not self.valid_input):
            self.print_error_message()
        if(messageinfo and self.valid_input):
            messagebox.showinfo("Info", "This input does not contain errors.")

    def print_error_message(self):
        messagebox.showerror("Error", "This input contains errors.")

    def change_color_bg_entries(self, x, y):
        self.entries[x][y].config({"background" : "red"})

def main():

    # sudoku test
    m = [[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]]

    root = tk.Tk()
    root.title("sudoku solver")
    root.resizable(0,0)

    large_font = ('Times New Roman', 30)

    entries = []

    # I've could done this better, maybe next time...
    for i in range(0,9):
        r_entries = []
        # black row every 3 rows
        if(i!=0 and i%3 == 0):
            r_frame = tk.Frame(root, height=5, bg="black")
            r_frame.pack(side="top", fill="x")

        r_frame = tk.Frame(root)
        r_frame.pack(side="top")
        for j in range(0,9):
            # black column every 3 columns
            if(j!=0 and j%3 == 0):
                c_frame = tk.Frame(r_frame, width=5, bg="black")
                c_frame.pack(side="left", fill="y")

            c_frame = tk.Frame(r_frame)
            c_frame.pack(side="left")
            entry = tk.Entry(c_frame, width=2, font=large_font)
            entry.grid(row=i, column=j)
            r_entries.append(entry)
        entries.append(r_entries)

    sudoku = Sudoku(m, entries)

    frame = tk.Frame(root)
    frame.pack(side="top")

    check_button = tk.Button(frame, text="Check input", width=9, command=lambda:sudoku.check_input(messageinfo=True))
    check_button.pack(side="left")

    solve_button = tk.Button(frame, bg="green", text="Solve", width=7, command=lambda:sudoku.solve_sudoku())
    solve_button.pack(side="left")

    clear_button = tk.Button(frame, text="Clear", width=7, command=lambda:sudoku.clear_window())
    clear_button.pack(side="right")

    root.mainloop()

if __name__ == "__main__":
    main()
