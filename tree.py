from __future__ import annotations

from decimal import Decimal
from typing import List

from world import World, Startup, Item, ItemAmount, Building, Recipe
from error_handler import MyCustomError


class Node():
    
    def __init__(self, data: object, child: List[object]=None, 
                 building: Building=None, recipe: Recipe=None) -> None:
        self.building = building
        self.recipe = recipe
        if data == None:
            self.data = []
        else:
            self.data = data
        if child is None:
            self.child = []
        elif isinstance(child, List):
            self.child = child
        else: 
            self.child = [child]
    
    def __str__ (self) -> str:
        text = ''
        count = 0
        for ingredient in self.data:
            if count >= 1:
                pass#text += '\n'
            count += 1
            text += f'{ingredient.amount} {ingredient.item.name}'
        return text
            
    
    def set_child(self, child: object) -> None:
        if isinstance(child, List[Node]):
            self.child = child
        else:
            raise MyCustomError('Object must be a list of nodes')
        
    def add_child(self, child: object) -> None:
        if isinstance(child, Node):
            self.child.append(child)
        else:
            raise MyCustomError('Object must be a Node')
        

class Tree():
    
    def __init__(self, root: Node) -> None:
        self.root = root




            
            

#ApacheMxnetOnAWS diagrams.aws.ml.ApacheMxnetOnAWS