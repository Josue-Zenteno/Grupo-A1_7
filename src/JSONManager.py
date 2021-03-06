"""
Copyright (C) 2020-2050
    -   Marina Prieto Pech
    -   Sergio Silvestre Pavón
    -   Josue Carlos Zenteno Yave
"""
import json
from Maze import Maze
from tkinter import Tk
from ImageManager import ImageManager
from InconsiSpector import InconsiSpector
from tkinter.filedialog import askopenfilename

class JSONManager:
    ###########################---Attributes---############################
    file_path = str()
    input_file = str()
    input_json = json

    ###########################---Constructor---###########################
    def __init__(self):
        self.image_manager = ImageManager()
        pass

    ###########################---Main Methods---##########################
    @staticmethod
    def generate_maze_json(maze, rows, columns):
        # Creating a Dictionary for the Maze class
        maze_dict = {"rows": rows, "cols": columns, "max_n": 4, 
                     "mov": [[-1, 0], [0, 1], [1, 0], [0, -1]],
                     "id_mov": ["N", "E", "S", "O"], "cells": {}}

        # Filling the Cells key for the Maze dictionary with auxiliary dictionaries (one per cell per row)
        for i in range(rows):
            for j in range(columns):
                cell_dict_aux = {"(" + str(i) + ", " + str(j) + ")": 
                    {
                    "value": maze.body[i][j].value, 
                    "neighbors": [maze.body[i][j].NESO[0],maze.body[i][j].NESO[1],maze.body[i][j].NESO[2],maze.body[i][j].NESO[3]]
                    }
                }

                maze_dict["cells"].update(cell_dict_aux)

        # Saving the JSON file
        with open("problem_" + str(rows) + "x" + str(columns) + "_maze.json", "w") as outfile:
            json.dump(maze_dict, outfile, indent=4)

    def generate_problem_json(self, rows, columns):
        # select the initial state
        initial_state_row, initial_state_column = self.ask_for_initial_state(rows, columns)
        # select the objective state
        objective_state_row, objective_state_column = self.ask_for_goal_state(rows, columns)

        # create the dictionary to export the info into a json format
        problem_dict = {"INITIAL": "("+ initial_state_row +", "+ initial_state_column +")",
                        "OBJETIVE": "("+ objective_state_row +", "+ objective_state_column +")",
                        "MAZE": "problem_" + str(rows) + "x" + str(columns) + "_maze.json"}

        with open("problem_" + str(rows) + "x" + str(columns) + ".json", "w") as outfile:
            json.dump(problem_dict, outfile)

    def read_problem_json(self):
        # select the problem json
        print("Select the problem json.")
        self.ask_for_file()
        self.read_json()
        str_initial_state = self.input_json["INITIAL"]
        str_goal_state = self.input_json["OBJETIVE"]
        maze_json = self.input_json["MAZE"]
        
        # select and check the maze jason
        print("Select the maze json.")
        while True:
            self.ask_for_file()
            self.read_json()
            file_path_divided = self.file_path.split('/')

            if file_path_divided[-1] != maze_json:
                print("You didn't select the corresponding maze")
                raise Exception("")
            else:
                self.generate_image()
                problem_maze = self.generate_temp_maze()
                break
        
        initial_state, goal_state = self.parse_values(str_initial_state,str_goal_state)

        return initial_state, goal_state, problem_maze

    def generate_image(self):
        inspector = InconsiSpector()
        #Generating a temporal maze which will store the information about the maze read in the json file
        temp_maze = self.generate_temp_maze()
        #Lookig for inconsistencies
        found, kind_error = inspector.find_inconsistencies(temp_maze)
        if not found:
            #Using the corresponding method
            self.image_manager.generate_image(temp_maze, temp_maze.rows, temp_maze.columns)
            temp_maze.body.clear()
        else:
            print("Error found: "+ kind_error)

    #########################---Auxiliary Methods---#######################
    def read_json(self):
        #Checking if the input file is correct or not
        if self.is_valid_json():
            self.input_file = open(self.file_path)
            self.input_json = json.load(self.input_file)

    @staticmethod
    def ask_for_initial_state(rows, columns):
        while True:
            initial_state_row = input("\nIntroduce initial state row: ")
            initial_state_column = input("Introduce initial state column: ")
            
            if initial_state_row.isdigit() and initial_state_column.isdigit():
                if rows-1 >= int(initial_state_row) >= 0 and columns - 1 >= int(initial_state_column) >= 0:
                    break
                else:
                    print("\nPosition out of the bounds of the maze. Please introduce a valid position")
            else:
                print("\nPlease introduce a valid size (<number>, <number>) \n")

        return initial_state_row, initial_state_column

    @staticmethod
    def ask_for_goal_state(rows, columns):
        while True:
            objective_state_row = input("\nIntroduce objective state row: ")
            objective_state_column = input("Introduce objective state column: ")
            if objective_state_row.isdigit() and objective_state_column.isdigit():
                if rows-1 >= int(objective_state_row) >= 0 and columns - 1 >= int(objective_state_column) >= 0:
                    break
                else:
                    print("\nPosition out of the bounds of the maze. Please introduce a valid position\n")
            else:
                print("\nPlease introduce a valid size (<number>, <number>) \n")
            
        return objective_state_row, objective_state_column

    def ask_for_file(self):
        # Hiding the tk GUI
        Tk().withdraw()
        # show an "Open" dialog box and return the path to the selected file
        filename = askopenfilename()
        self.file_path = filename

    def generate_temp_maze(self):
        maze = Maze(self.input_json["rows"], self.input_json["cols"])
        #Assigning the NESO values to the corresponding cells of the maze
        for i in range(self.input_json["rows"]):
            for j in range(self.input_json["cols"]):
                maze.body[i][j].NESO = self.input_json["cells"]["(" + str(i) + ", " + str(j) + ")"]["neighbors"]
                maze.body[i][j].value = self.input_json["cells"]["(" + str(i) + ", " + str(j) + ")"]["value"]
        return maze

    @staticmethod
    def parse_values(str_initial_state,str_goal_state):
        initial, objetive = "", ""

        for i in str_initial_state:
            if i.isdigit():
                initial += i
            elif i == ',' :
                initial += i
            elif i == ')':
                break

        for i in str_goal_state:
            if i.isdigit():
                objetive += i
            elif i == ',' :
                objetive += i
            elif i == ')':
                break
         
        initial = initial.split(',')
        objetive = objetive.split(',')
        
        initial_state = (int(initial[0]),int(initial[1]))
        goal_state = (int(objetive[0]),int(objetive[1]))

        return initial_state, goal_state

    def is_valid_json(self):
        #Checking if the file is a JSON file
        if self.file_path[-4:] == "json":
            return True
        return False