class Crafting:
    recipes = {"plank":{"wood":2}}

    def craft(self,item,inv):
        if item not in self.recipes: return False
        for k,v in self.recipes[item].items():
            if inv.items.get(k,0)<v: return False
        for k,v in self.recipes[item].items():
            inv.items[k]-=v
        inv.items[item]=inv.items.get(item,0)+1
        return True
