class Node:
    def __init__(self, bs):
        self.path = []
        self.bs4node = bs
        for parent in self.bs4node.parents:
            self.path.append(parent.name)
            self.path.reverse()

    def get_parent(self):
        for parent in self.bs4node.parents:
            if parent and 'class' in parent.attrs:
                return (parent.name, parent.attrs['class'])

    def get_path(self):
        return self.path

    def get_dep(self):
        return len(self.path)
