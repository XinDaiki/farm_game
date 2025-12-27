class Inventory:
    def __init__(self):
        self.items = {"seed":5,"wood":5}

    def use(self,item):
        if self.items.get(item,0)>0:
            self.items[item]-=1
            return True
        return False
