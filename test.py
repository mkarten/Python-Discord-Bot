from tree import *
import jsonpickle

def test ():

    json_str = open("tree.json", "r").read()
    tr = parse_json_to_tree(json_str)
    print(tr)




if __name__ == "__main__":
    test()