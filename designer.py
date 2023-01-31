from __future__ import annotations

from decimal import Decimal
from typing import List
import math
from diagrams import Diagram
from diagrams.aws.ml import ApacheMxnetOnAWS as cube
from diagrams.aws.enablement import ManagedServices as building_icon

from world import World, Startup, Item, ItemAmount, Building, Recipe
from error_handler import MyCustomError
from tree import Tree, Node


def first(iterable, default=None, key=None):
    if key is None:
        for el in iterable:
            if el:
                return el
    else:
        for el in iterable:
            if key(el):
                return el
    return default


class TreeBuilder:
    
    @staticmethod
    def disassemble_1_level(item_amounts: List[ItemAmount], recipe: Recipe=None
                            ) -> List[ItemAmount]:
        dissassembled_ingredients = []
        
        for item_amount in item_amounts:
            
            amount_param = item_amount.amount
            used_recipe = item_amount.item.default_recipe
            amount_produced = first(
                x.amount for x in used_recipe.products
                if x.item.classname == item_amount.item.classname)
            
            for ingredient in used_recipe.ingredients:
                amount_required = (
                    (ingredient.amount*amount_param)/amount_produced)
                item_required = ingredient.item
                dissassembled_ingredients.append(
                    ItemAmount(item_required, amount_required))

        return dissassembled_ingredients
            

    def disassemble_to_root_building(self, item_amounts: List[ItemAmount]
                                     ) -> List[object]:
        root_recipe = item_amounts[0].item.default_recipe
        root_node = Node(data = item_amounts, 
                         building = root_recipe.buildings[0],
                         recipe = root_recipe)
        item_tree = Tree(root_node)

        def recursive_disassemble(self, node: Node) -> Node:
            if node.data is None:
                return
            for item_amount in node.data:
                if item_amount.item.default_recipe is None:
                    continue
                
                decomposition = TreeBuilder.disassemble_1_level([item_amount])
                
                for ingredient in decomposition:
                    ingredient_recipe = ingredient.item.default_recipe
                    if ingredient_recipe is not None:
                        building = ingredient_recipe.buildings[0]
                    else:
                        building = None
                    node.add_child(Node(data = [ingredient], 
                                        building = building, 
                                        recipe=ingredient_recipe))
                
                for ingredient_it_amnt in node.child:
                    recursive_disassemble(self, ingredient_it_amnt)

        recursive_disassemble(self, root_node)
        return item_tree
    
    def tree_to_node_list(self, tree: Tree) -> List:
        node_list = []
        def recursion(node: Node):
            node_list.append(node)
            if node.child is None:
                return
            for child in node.child:
                recursion(child)
        recursion(tree.root)
        return node_list

    def tree_to_node_compact(self, tree: Tree) -> List:
        
        zip_list = []
        node_list = self.tree_to_node_list(tree)
        
        def search_zip(self, recipe_classname):
            for r_itemamount in zip_list:
                if r_itemamount.recipe is None:
                    return None
                if node.recipe.classname == recipe_classname:
                    return node
            return None
            
        
        for node in node_list:
            pass
            #if search_zip(self, )
            

class CalcUtils:

    @staticmethod
    def __decimal_places(number: Decimal) -> Decimal:
        if(isinstance(number, Decimal)):
            return abs(Decimal(number).normalize().as_tuple().exponent)
        return 0
    
    @staticmethod
    def __lcm_int(numbers: List(int)) -> int:
        return math.lcm(*numbers)
    
    @staticmethod
    def __lcm_decimal(numbers: List(Decimal)) -> int:
        max_decimal_places = abs(max(
            CalcUtils.__decimal_places(number) for number in numbers))
        integers = (
            int(number * (10**max_decimal_places)) for number in numbers)
        integers = list(integers)
        lcm = CalcUtils.__lcm_int(integers)
        lcm = lcm // 10**max_decimal_places
        return lcm
        
    
    @staticmethod
    def lcm(numbers: List()) -> int:
        """ Cálculo de lcm capaz de lidar com números decimais """
                              
        if not(all((isinstance(x, int) or isinstance(x, Decimal)) for x in 
                   numbers)):
            raise MyCustomError('Only integers and decimals allowed in lcm.')
        
        lcm = 0
        if(any(isinstance(x, Decimal)) for x in numbers):
            lcm = CalcUtils.__lcm_decimal(numbers)
        else:
            lcm = CalcUtils.__lcm_int(numbers)
             
        return lcm
   
    
class Search:
    
    @staticmethod
    def print_recipe_by_product(world: World, product_name: str) -> None:
        for recipe in world.recipes:
            for product in recipe.products:
                if(product_name == product.item.name):
                    print(recipe)

    @staticmethod
    def find_item_by_name(world: World, product_name: str) -> None:
        for item in world.items:
            if(product_name == item.name):
                return item
        return None


class TreeVisualization():
    
    def __init__(self, tree: Tree) -> None:
        self.tree = tree
    
    def draw_simple_only_ingredients(self):
        root = self.tree.root
        root_name = root.__str__()
        diagram_name = f'Recipe for producing {root.__str__()}.'
        with Diagram(name = diagram_name, direction = 'BT'):
            def recursion(viz_item, node):
                for item in node.child:
                    #node_items.append(item)
                    new_viz_item = cube(label = item.__str__())#'1')
                    viz_item << new_viz_item
                    if item.child is not None:
                        recursion(new_viz_item, item)
                return viz_item
                
            
            
            viz = cube(root_name)
            viz = recursion(viz, self.tree.root)
            #viz >> viz2
            #cube(root_name).connect(cube, recursion(cube, self.tree.root))
            
    def draw_simple(self):
        root = self.tree.root
        root_name = root.__str__()
        diagram_name = f'Recipe for producing {root.__str__()}.'
        with Diagram(name = diagram_name, direction = 'BT'):
            def recursion(viz_item, node):
                
                if node.building is not None:
                    new_viz_building = building_icon(
                        label = node.building.name)
                    viz_item << new_viz_building
                
                for item in node.child:
                    new_viz_item = cube(label = item.__str__())
                    if(node.building is not None):
                        new_viz_building << new_viz_item
                    else:
                        print("tava None")
                        viz_item << new_viz_item
                    if item.child is not None:
                        recursion(new_viz_item, item)
                return viz_item
            
            viz = cube(root_name)
            viz = recursion(viz, self.tree.root)
            
        
