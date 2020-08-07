#-------------------------------------------
# sudoku solver based on tkinter library
# 2020, by Giuseppe Campanella with <3
#-------------------------------------------

import copy
import random
import tkinter as tk
from tkinter import messagebox


class Sudoku():
    def __init__(self, sudoku_game, entries):
        self.sudoku_game = sudoku_game
        self.sudoku_solution = copy.deepcopy(sudoku_game)
        self.entries = entries
        self.unic_solution = False
        self.multiple_solutions = False
        self.print_sudoku()

    def print_matrix(self, m2=False):
        if(m2):
            m = self.sudoku_game
        else:
            m = self.sudoku_solution
        cnt = 0
        print()
        for i in range(0, 9):
            for j in range(0, 9):
                if(j != 0 and j%3 == 0):
                    print("|", end='')
                print(m[i][j], end=' ')
            print()
            cnt += 1
            if(cnt != 9 and cnt % 3 == 0):
                for j in range(0, 9*2 + 1):
                    print("_", end='')
                print()
        print()

    # check if the value is valid in the row, column and square
    def check_value(self, v, x, y):
        for i in range(0, 9):
            if(i!=y and self.sudoku_solution[x][i] == v):
                return False

        for i in range(0, 9):
            if(i!=x and self.sudoku_solution[i][y] == v):
                return False

        # check the square
        x0, y0 = (x//3)*3, (y//3)*3
        for i in range(x0,x0 + 3):
            for j in range(y0,y0 + 3):
                if(i!=x and j!=y and self.sudoku_solution[i][j] == v):
                    return False

        return True

    # shuffle values when I request a random sudoku
    def solve(self, only_one_solution=True):
        values = list(range(1,10))
        random.shuffle(values)
        while True:
            for i in range(0,9):
                for j in range(0,9):
                    if(self.sudoku_solution[i][j] == 0):
                        for val in values:
                            if(self.check_value(val, i, j)):
                                self._val = self.sudoku_solution[i][j] = val
                                self._x = i
                                self._y = j
                                if(self.solve(only_one_solution=only_one_solution)):
                                    return True
                                # backtrack
                                self.sudoku_solution[i][j] = 0
                        # if the final call of the function returns False with
                        # unic_solution == False it means there is no solution
                        return False
            # found a solution
            if(only_one_solution):
                return True
            else:
                # if I want more solutions for the sudoku, return False
                # return False

                # check if there are multiple solutions
                if(self.unic_solution):
                    # if the final call of the function returns True with
                    # unic_solution == True it means there are multiple solutions
                    self.multiple_solutions = True
                    return True
                else:
                    # if the final call of the function returns False with
                    # unic_solution == True it means there is only one solution
                    self.unic_solution = True
                    return False

    def print_sudoku(self, solution=False):
        if(not solution):
            m = self.sudoku_game
        else:
            m = self.sudoku_solution
        for i in range(0,9):
            for j in range(0,9):
                val = m[i][j]
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                if(val == 0):
                    val = ""
                entry.insert(0, val)

    def solve_sudoku(self, message=True, only_one_solution=True):
        self.check_input()
        if(self.valid_input):
            self.unic_solution = False
            self.multiple_solutions = False
            is_solvable = self.solve(only_one_solution=only_one_solution)
            if(is_solvable):
                self.print_sudoku(solution=True)
            else:
                if(message):
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
                self.sudoku_solution[i][j] = val

    def clear_window(self):
        for i in range(0,9):
            for j in range(0,9):
                self.sudoku_solution[i][j] = 0
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, "")
                entry.config({"background" : "white"})

    # check if the input given is valid or not
    def check_input_sudoku(self, show_red_bg = True):
        self.valid_input = True
        for i in range(0,9):
            for j in range(0,9):
                if(self.sudoku_solution[i][j] != 0):
                    valid = self.check_value(self.sudoku_solution[i][j], i, j)
                    if(not valid):
                        self.valid_input = False
                        if(show_red_bg):
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

    # with a recursive function values from sudoku solution are removed
    # for each value removed an attempt is made to find a solution
    # if there are multiple solution, the recursion ends with the matrix from
    # the previous step as a sudoku game for the player
    def remove_value_recursively(self):
        while(self.find_perfect_sudoku):
            x, y = random.randint(0, 8), random.randint(0, 8)

            if(self.sudoku_solution[x][y] != 0):
                prev_value = self.sudoku_solution[x][y]
                self.sudoku_solution[x][y] = 0
                self.entries[x][y].delete(0, tk.END)

                self.unic_solution = False
                self.multiple_solutions = False
                is_solvable = self.solve(only_one_solution=False)

                # there is no solution for this sudoku
                if(not is_solvable and not self.unic_solution):
                    print("there is no solution for this sudoku")
                    self.find_perfect_sudoku = False
                    self.sudoku_game = copy.deepcopy(self.sudoku_solution)
                    return False

                # if exists only one solution the value can be removed
                if(self.unic_solution and not self.multiple_solutions):
                    self.sudoku_game = copy.deepcopy(self.sudoku_solution)
                    self.remove_value_recursively()
                else:
                    # exit from recursion
                    self.find_perfect_sudoku = False
                    return False

    def create_random_sudoku(self):
        self.clear_window()
        self.solve()

        self.find_perfect_sudoku = True
        self.sudoku_game = copy.deepcopy(self.sudoku_solution)
        self.remove_value_recursively()

        # m = sudoku solution, m2 = sudoku game
        print("m")
        self.print_matrix()
        print("m2")
        self.print_matrix(m2=True)

        self.print_sudoku()


def main():

    # sudoku test
    sudoku_game = [[5,3,0,0,7,0,0,0,0],
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

    sudoku = Sudoku(sudoku_game, entries)

    frame = tk.Frame(root)
    frame.pack(side="top")

    check_button = tk.Button(frame, text="Check input", width=9, command=lambda:sudoku.check_input(messageinfo=True))
    check_button.pack(side="left")

    solve_button = tk.Button(frame, bg="green", text="Solve", width=7, command=lambda:sudoku.solve_sudoku())
    solve_button.pack(side="left")

    clear_button = tk.Button(frame, text="Clear", width=7, command=lambda:sudoku.clear_window())
    clear_button.pack(side="right")

    rand_button = tk.Button(frame, text="Randomize", width=7, command=lambda:sudoku.create_random_sudoku())
    rand_button.pack(side="right")

    root.mainloop()

if __name__ == "__main__":
    main()
