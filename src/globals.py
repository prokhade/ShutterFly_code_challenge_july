import os


def init():
    PATH = 'C:/Users/Prateek/Desktop/IUB/Interviews/ShutterFly/ShutterFly-code-challenge-new'
    INPUT = 'input'
    OUTPUT = 'output'
    SRC = 'src'
    global input_path
    input_path = os.path.join(PATH, INPUT)
    global src_path
    src_path = os.path.join(PATH, SRC)
    global output_path
    output_path = os.path.join(PATH, OUTPUT)
    global end_week
    end_week = None

