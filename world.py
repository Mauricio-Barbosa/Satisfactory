from __future__ import annotations

from decimal import Decimal
from typing import List

import satisfactory_parser as sp
from error_handler import MyCustomError

class Building:
    
    def __init__(self, classname: str, name: str, slug: str, description: str, 
                 power_consumption: Decimal=None, input_qty: int=None, 
                 output_qty: int=None) -> None:
        self.classname = classname
        self.name = name
        self.slug = slug
        self.description = description
        self.power_consumption = power_consumption
        self.input_qty = input_qty
        self.output_qty = output_qty


class Item:

    def __init__(self, classname: str, name: str, slug: str, 
                 stack_size: Decimal, liquid: bool, sink_points: Decimal, 
                 default_recipe: Recipe=None) -> None:
        self.classname = classname
        self.name = name
        self.slug = slug
        self.stack_size = stack_size
        self.liquid = liquid
        self.sink_points = sink_points
        self.default_recipe = default_recipe
    
    def __str__(self) -> str:
        return 'name = '+self.name+', stack size = '+str(self.stack_size)

    def get_default_recipe(self) -> Recipe:
        return self.default_recipe

    def set_default_recipe(self, recipe) -> None:
        self.default_recipe = recipe


class ItemAmount:
    
    def __init__(self, item: Item, amount: Decimal) -> None:
        self.item = item
        self.amount = amount
    
    def __str__(self) -> str:
        return str(self.amount) + ' ' + self.item.name
    
    def get_amount(self) -> Decimal:
        return self.amount


class Recipe:
    
    def __init__(self, classname: str, name: str, slug: str, 
                 is_alternate: bool, time: Decimal, 
                 ingredients: List[ItemAmount],
                 products: List[ItemAmount], 
                 produced_in: List[Building]) -> None:       
        self.classname = classname
        self.name = name
        self.slug = slug
        self.is_alternate = is_alternate
        self.time = time
        self.ingredients = ingredients
        self.products = products
        self.buildings = produced_in
        
    def __str__(self) -> str:
        
        def concat_itens(items) -> str:
            str_items = ''
            for item in items:
                str_items += str(item.__str__())
                str_items += '\n'
            return str_items
            
        str_ingredients = concat_itens(self.ingredients)
        str_products = concat_itens(self.products)
            
        return f"name: {self.name}, time to build: {self.time},\ningredients:"\
            f"\n{str_ingredients}products:\n{str_products}"
        

class DraftRecipe:
    
    def __init__(self, classname: str, name: str, slug: str, 
                 is_alternate: bool, time: Decimal, ingredients: List[str],
                 products: List[str], produced_in: List[str]) -> None:       
        self.classname = classname
        self.name = name
        self.slug = slug
        self.is_alternate = is_alternate
        self.time = time
        self.ingredients = ingredients
        self.products = products
        self.buildings = produced_in


class ObjectInstantiator:
    
    @staticmethod
    def instantiate_all():
        pass
    
    @staticmethod
    def instantiate_items(items_dict: dict) -> List(Item):
        """ Loops trough itens dict and instantiate objects. """
        items = []
        for key, value in items_dict.items():
            classname = value['className']
            name = value['name']
            slug = value['slug']
            stack_size = value['stackSize']
            liquid = value['liquid']
            sink_points = value['sinkPoints']
            
            instatiated_item = Item(classname, name, slug, stack_size, liquid, 
                                    sink_points)
            items.append(instatiated_item)
        return items

    @staticmethod
    def instantiate_buildings(buildings_dict: dict) -> List(Building):
        """ Loops trough buildings dict and instantiate objects. """
        buildings = []
        for key, value in buildings_dict.items():
            classname = value['className']
            name = value['name']
            slug = value['slug']
            description = value['description']
            power_consumption = 0
            if value.get('metadata') is not None:
                if value['metadata'].get('powerConsumption') is not None:
                    power_consumption = value['metadata']['powerConsumption']
        
            instantiated_building = Building(
                classname = classname, name = name, slug = slug, 
                description = description, 
                power_consumption = power_consumption)
            buildings.append(instantiated_building)
        return buildings

    @staticmethod
    def instantiate_draft_recipes(recipes_dict: dict) -> List(DraftRecipe):
        """ Loops trough recipes dict and instantiate draft objects. 
        Recipes must be later correlated with buildings and itens before used.
        """
        draft_recipes = []
        for key, value in recipes_dict.items():
            classname = value['className']
            name = value['name']
            slug = value['slug']
            is_alternate = value['alternate']
            time = value['time']
            ingredients = value['ingredients']
            products = value['products']
            produced_in = value['producedIn']
        
            instantiated_draft_recipe = DraftRecipe(
                classname = classname, name = name, slug = slug, 
                is_alternate = is_alternate, time = time, 
                ingredients = ingredients, products = products,
                produced_in = produced_in)
            draft_recipes.append(instantiated_draft_recipe)
        return draft_recipes
    
    @staticmethod
    def instantiate_recipes(recipes_dict: dict) -> List(Recipe):
        """ Instantiate recipes from pre-processed recipes list. """
        recipes = []
        for key, value in recipes_dict.items():
            classname = value['classname']
            name = value['name']
            slug = value['slug']
            is_alternate = value['is_alternate']
            time = value['time']
            ingredients = value['ingredients']
            products = value['products']
            buildings = value['produced_in']
            recipes.append(Recipe(classname = classname, name = name, 
                                  slug = slug, is_alternate=is_alternate, 
                                  time=time, ingredients=ingredients, 
                                  products=products, produced_in=buildings))
        return recipes            


class Binder:
    
    default_recipe_exclusions = [
        'Recipe_UnpackageOilResidue_C', 'Recipe_UnpackageOil_C',
        'Recipe_UnpackageNitrogen_C', 'Recipe_UnpackageOil_C', 'Water']
    item_recipe_exclusion = ['Desc_Water_C']
    
    @staticmethod
    def bind_recipes(items: List[Item], buildings: List[Building],
                 draft_recipes: List[DraftRecipe]):
        recipes_list = []
        if items is None or buildings is None:
            raise MyCustomError("""Itens and buildings must be instantiated 
                                first.""")  
        for recipe in draft_recipes:
            
            binded_ingredients = Binder.search_ingredients(
                recipe.ingredients, items)
            binded_products = Binder.search_products(
                recipe.products, items)
            binded_buildings = Binder.search_buildings(
                recipe.buildings, buildings)
            
            recipes_list.append(
                Recipe(classname = recipe.classname, name = recipe.name, 
                       slug = recipe.slug, is_alternate = recipe.is_alternate, 
                       time = recipe.time, ingredients = binded_ingredients, 
                       products = binded_products, 
                       produced_in = binded_buildings)
                )
            
        return recipes_list

    @staticmethod
    def bind_default_recipes(items: List[Item], recipes: List[Recipe]
                             ) -> List[Item]:
        
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
        
        temp_items = items
        for item in temp_items:
            item.default_recipe = first(
                recipe for recipe in recipes for product in recipe.products 
                if item.classname == product.item.classname 
                and recipe.is_alternate == False
                and recipe.classname not in Binder.default_recipe_exclusions
                and 'Unpackage' not in recipe.classname
                and item.classname not in Binder.item_recipe_exclusion)
        binded_items = temp_items
        return binded_items

    @staticmethod
    def search_buildings(buildings_str: List[str], 
                        buildings: List[Building]) -> List[Building]:
        found_buildings = []
        
        #[x for x in buildings if x.classname == building_name]  
        #[x for x in buildings if x.classname in buildings_str] 
        
        for building_name in buildings_str:
            for building in buildings:
                if building.classname == building_name:
                    found_buildings.append(building)
                    break
                
        return found_buildings

    @staticmethod
    def search_ingredients(ingredients_str: List[str],
                           items: List[Item]) -> List[ItemAmount]:
        found_item_amounts = []
                
        for ingredient in ingredients_str:
            for item in items:
                if item.classname == ingredient['item']:
                    found_item_amounts.append(
                        ItemAmount(item, ingredient['amount']))
        
        return found_item_amounts

    @staticmethod
    def search_products(products_str: List[str],
                           items: List[Item]) -> List[ItemAmount]:
        found_item_amounts = []
                
        for product in products_str:
            for item in items:
                if item.classname == product['item']:
                    found_item_amounts.append(
                        ItemAmount(item, product['amount']))
        
        return found_item_amounts


class World:
    
    def __init__(self, name, recipes=None, items=None, buildings=None):
        self.name = name
        self.recipes = recipes
        self.items = items
        self.buildings = buildings


class ProductionInstance:
    
    def __init__(self, recipe, input_items: List[ItemAmount], 
                 output_items: List[ItemAmount]):
        self.recipe = recipe
        self.input_items = input_items
        self.output_items = output_items
        

class Startup:
    
    @staticmethod
    def setup_world(name: str) -> World:
        obj_inst = ObjectInstantiator()
        items = obj_inst.instantiate_items(sp.get_items())
        buildings = obj_inst.instantiate_buildings(sp.get_buildings())
        draft_recipes = obj_inst.instantiate_draft_recipes(sp.get_recipes())
        
        binder = Binder()
        recipes = binder.bind_recipes(items, buildings, draft_recipes)
        items = binder.bind_default_recipes(items, recipes)
        
        world = World(name = name, recipes = recipes, items = items, 
                      buildings = buildings)
        return world
        

# =============================================================================
# my_world = Startup.setup_world(name = 'My world')
# search = Search()
# search.print_recipe_by_product(world=my_world, product_name='Iron Plate')
# 
# 
# 
# math_utils = CalcUtils()
# print(math_utils.lcm([4, 6, Decimal('9.111')]))
# print(math.lcm(4000, 6000, 9111))
# 
# time_lcm = timeit.timeit(stmt='math_utils._CalcUtils__lcm_decimal([2, 600, 1355])', globals=globals(), number=1)
# time_math = timeit.timeit(stmt='math.lcm(4, 6, 5)', globals=globals(), number=1)
# 
# 
# =============================================================================
