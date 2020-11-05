"""
Copyright (C) 2020-2050
    -   Marina Prieto Pech
    -   Sergio Silvestre Pavón
    -   Josue Carlos Zenteno Yave
"""
import json
from src.Maze import Maze
from src.InconsiSpector import InconsiSpector
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from src.ImageManager import ImageManager


class JSONManager:
    ###########################---Attributes---############################
    file_path = str()
    input_file = str()
    input_json = json

    ###########################---Constructor---###########################
    def __init__(self):
        pass

    ###########################---Main Methods---##########################
    @staticmethod
    def generate_json(maze, rows, columns):
        # Creating a Dictionary for the Maze class
        maze_dict = {"rows": rows, "cols": columns, "max_n": 4, "mov": [[-1, 0], [0, 1], [1, 0], [0, -1]],
                     "id_mov": ["N", "E", "S", "O"], "cells": {}}

        # Filling the Cells key for the Maze dictionary with auxiliary dictionaries (one per cell per row)
        for i in range(rows):
            for j in range(columns):
                cell_dict_aux = {"(" + str(i) + ", " + str(j) + ")": {"value": 0, "neighbors": [maze.body[i][j].NESO[0],
                                                                                                maze.body[i][j].NESO[1],
                                                                                                maze.body[i][j].NESO[2],
                                                                                                maze.body[i][j].NESO[
                                                                                                    3]]}}
                maze_dict["cells"].update(cell_dict_aux)

        # Saving the JSON file
        with open("Lab_" + str(rows) + "_" + str(columns) + ".json", "w") as outfile:
            json.dump(maze_dict, outfile, indent=4)

    def read_json(self):
        #Checking if the input file is correct or not
        if not self.is_valid_json():
            self.notify_error("File_Type")
        else:
            self.input_file = open(self.file_path)
            self.input_json = json.load(self.input_file)

    def generate_image(self):
        inspector = InconsiSpector()
        #Generating a temporal maze which will store the information about the maze read in the json file
        temp_maze = self.generate_temp_maze()
        #Lookig for inconsistencies
        found, kind_error = inspector.find_inconsistencies(temp_maze)
        if not found:
            #Using the corresponding method
            ImageManager.generate_image(temp_maze, temp_maze.rows, temp_maze.columns)
        else:
            print("Error found: "+kind_error)

    def generate_temp_maze(self):
        maze = Maze(self.input_json["rows"], self.input_json["cols"])
        #Assigning the NESO values to the corresponding cells of the maze
        for i in range(self.input_json["rows"]):
            for j in range(self.input_json["cols"]):
                maze.body[i][j].NESO = self.input_json["cells"]["(" + str(i) + ", " + str(j) + ")"]["neighbors"]
        return maze

    def is_valid_json(self):
        #Checking if the file is a JSON file
        if self.file_path[-4:] == "json":
            return True
        return False

    def ask_for_file(self):
        # Hiding the tk GUI
        Tk().withdraw()
        # show an "Open" dialog box and return the path to the selected file
        filename = askopenfilename()
        self.file_path = filename

    @staticmethod
    def notify_error(kind):
        # List of errors that we will notify
        if kind == "File_Type":
            print("Wrong file type, please select a json file")

    # NUEVO (preguntar si también generar)
    def read_problem_json(self):
        # select the problem json
        self.read_json()
        initial_state = self.input_json["INITIAL"]
        goal_state = self.input_json["OBJETIVE"]
        maze_json = self.input_json["MAZE"]
        # select and check the maze jason
        self.read_json()
        file_path_divided = self.file_path.split('/')

        while True:
            if self.file_path[-1] != maze_json:
                print("You don't select the corresponding maze")
            else:
                # self.generate_temp_maze()
                self.generate_image()