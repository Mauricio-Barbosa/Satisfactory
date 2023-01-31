import json

file_dir = 'C:/Users/mauri/OneDrive/Documentos/Estudos/Python/Satisfactory/source/data.json'
keys = ['buildings', 'generators', 'items', 'miners', 'recipes', 'resources', 'schematics']


def parse_file(file_dir):
    parsed_data=''
    with open(file_dir) as json_data:
        parsed_data = json.load(json_data)
    return parsed_data

def get_items():
    return parse_file(file_dir)["items"]

def get_buildings():
    return parse_file(file_dir)["buildings"]

def get_recipes():
    return parse_file(file_dir)["recipes"]


a = get_items()

# =============================================================================
# a=get_itens()
# 
# 
# for key, value in a.items():
#     print(value["name"])
#     print('################')
# =============================================================================
# =============================================================================
#     name = item['name']
#     slug = item['slug']
#     stack_size = item['stackSize']
#     liquid = item['liquid']
#     sink_points = item['sinkPoints']
# =============================================================================
