import json

class TreeNode:
    def __init__(self, question : str, options : dict[str, 'TreeNode'],parent : 'TreeNode' = None):
        self.question = question
        self.options = options
        self.parent = parent

    def AddOption(self, option : str, node : 'TreeNode'):
        self.options[option] = node

    def GetOptions(self):
        return self.options

    def __str__(self):
        return self.question

class Tree:
    def __init__(self, firstQuestion : str):
        self.root = TreeNode(firstQuestion, {})
        self.currentNode = self.root
    
    def AppendQuestion(self, question : str):
        self.currentNode.AddOption(question, TreeNode(question, {}, self.currentNode))

    def DeleteQuestion(self, option : str):
        del self.currentNode.options[option]

    def Reset(self):
        self.currentNode = self.root

    def GetQuestion(self) -> str:
        return self.currentNode.question
    
    def ListOptions(self) -> list[str]:
        return list(self.currentNode.options.keys())

    def GoBack(self):
        if self.currentNode.parent is not None:
            self.currentNode = self.currentNode.parent
    
    def ChooseOption(self, option : str):
        if option in self.currentNode.options:
            self.currentNode = self.currentNode.options[option]
            return True
        return False

    def __str__(self) -> str:
        return self._build_tree_string(self.root, "", "")[:-1]

    def _build_tree_string(self, node:TreeNode,children_prefix, is_last=True):
        result = ""
        if node.parent is None:
            result += f"{node.question}\n"
        elif is_last:
            result += f"{children_prefix}└── {node.question}\n"
        else:
            result += f"{children_prefix}├── {node.question}\n"

        if len(node.options) > 0:
            for i, (option, child_node) in enumerate(node.options.items()):
                if i == len(node.options) - 1:
                    if node.parent is None:
                        result += self._build_tree_string(child_node, "", True)
                    else:
                        result += self._build_tree_string(child_node, children_prefix + "│   ", True)
                else:
                    if node.parent is None:
                        result += self._build_tree_string(child_node, "", False)
                    else:
                        result += self._build_tree_string(child_node, children_prefix + "│   ", False)
                    
        return result
    

def parse_json_to_tree(json_str):
    data = json.loads(json_str)
    root_question = data['question']
    tree = Tree(root_question)
    build_tree_from_json(tree.root, data['options'], tree.root)
    return tree

def build_tree_from_json(node, options, parent):
    for option, option_data in options.items():
        question = option_data['question']
        new_node = TreeNode(question, {}, parent)
        node.AddOption(option, new_node)
        if 'options' in option_data:
            build_tree_from_json(new_node, option_data['options'], new_node)