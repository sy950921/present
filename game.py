import sys
import json
from environment import Environment
from ChooseAction import Action

def input (filename="sample splendor request.json"):
    f =open(filename,"r")
    t = json.load(f)
    return t

if __name__ == '__main__':
    # filename = "test_input.json"
    filename = sys.argv[1]
    data = input(filename)
    env = Environment(data)
    action=Action(env)
    action()