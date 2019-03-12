import pymongo
import csv

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
rushdb = myclient['rushdb']
item_tb = rushdb['item_tb']

# import database from csv file 
def import_from(filename):
    ''' import databse from CSV file'''
    
    # delete old atabase
    item_tb.delete_many({})
    with open('testdata.csv', 'r') as f:
        data = csv.DictReader(f)
        data = [dict(row) for row in data]
        print(f'importing :{len(data)} items')
        print(item_tb.insert_many(data))

# get all items
def get_all(mapid='ALPHA'):
    items = item_tb.find({}, {'_id': 0})
    return list(items)

# get all items
def get_all_from_category(category, mapid='ALPHA'):
    items = item_tb.find({'Category':category}, {'_id': 0})
    return list(items)


# get all category from map
def get_category(mapid='ALPHA'):
    items = get_all()
    categories = []
    for item in items:
        categories.append(item['Category'])
    categories = list(set(categories))
    print(categories)
    return categories

# get item node
def get_from_id(item_id, mapid='ALPHA0'):
    ''' get item node name '''

    item = item_tb.find_one({'Store':mapid, 'ID':item_id})
    print(item)
    return item

# get item information
def get_node_from_id(item_id,  mapid='ALPHA0'):
    ''' get item row in database '''

    item = item_tb.find_one({'Store':mapid, 'ID':item_id})
    if item : print(item['Node'])
    return item['Node'] if item else None

# show all item in database
def show_all():
    ''' print all item in databse '''

    items = item_tb.find({})
    for row in items:
        print(row)
            

