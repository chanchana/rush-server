import sys
from route import update, get, get_from_id
import database as db


argv = sys.argv

function = argv[1]
param = argv[2:]
# update dvalue 
# [group name] [map name]
if function == 'dvalue':
    update(param[0], param[1])

# test route 
# [group name] [map name] [item id list string]
elif function == 'route':
    pass

# test route from ALPHA0 map by node name 
# [item list string (sep by ';')]
elif function == 'alphan':
    items = param[0].split(';')
    get('Bottom Market', 'Bottom Market', items)

# test route from ALPHA0 map by item id 
# [item id list string (sep by ';')]
elif function == 'alpha':
    items = param[0].split(';')
    get_from_id('Bottom Market', 'Bottom Market', items)

# import database from file
# [filename]
elif function == 'db_import':
    db.import_from(param[0])

# get all available category
elif function == 'db_category':
    db.get_category()

# get item by item id 
# [item id]
elif function == 'db_get':
    db.get_from_id(param[0])

# get item node name by item id 
# [item id]
elif function == 'db_get_node':
    db.get_node_from_id(param[0])

# show all item in database
elif function == 'db_show':
    db.show_all()