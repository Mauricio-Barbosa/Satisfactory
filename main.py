from world import World, Startup, Item, ItemAmount, Building, Recipe
from designer import TreeBuilder, Search, TreeVisualization


world = Startup().setup_world('my world')
item = Search().find_item_by_name(world, 'Fused Modular Frame')

item_amount = []
item_amount.append(ItemAmount(item, 3))
x = TreeBuilder().disassemble_to_root_building(item_amount)
node_list = TreeBuilder().tree_to_node_list(x)

TreeVisualization(x).draw_simple()