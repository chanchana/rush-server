from flask import Flask, jsonify, render_template, request, redirect, send_from_directory
from flask_cors import CORS
from get_data import get_map_list, get_map_data, get_route, get_map_point
import database as db

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/stores')
def all_stores():
    data = get_map_list()
    return jsonify({'map':data})

@app.route('/stores/str')
def all_stores_str():
    data = get_map_list()
    names = ''
    for d in data:
        names += d['group']+'-'+d['name']+';'
    return names

@app.route('/stores/<string:group>/<string:name>')
def get_store_data(group, name):
    data = db.get_all()
    category = db.get_category()
    return jsonify({'data':data, 'category':category})

@app.route('/stores/mappoint/<string:group>/<string:name>')
def get_store_map_point(group, name):
    data = get_map_point(group, name)
    return jsonify(data)

@app.route('/stores/mapimage/<string:group>/<string:name>')
def get_store_map_image(group, name):
    return send_from_directory(f'map/data/{group}/', f'{name}.gif')

@app.route('/stores/<string:group>/<string:name>/route/<string:items>')
def fastest_route(group, name, items):
    order, data = get_route(group, name, items)
    if not data:
        return 'Item not in the list'
    return jsonify({'path' : data, 'order' : order})

##### DEMO #####

@app.route('/demo', methods=['GET', 'POST'])
def demo_start():
    if request.method == 'POST':
        select = str(request.form['select'])
        group, name = select.split(';')
        return redirect('/demo/map/{}/{}'.format(group, name))

    else:
        stores = get_map_list()
        return render_template('start_page.html', stores=stores)

@app.route('/demo/map/<string:group>/<string:name>', methods=['GET', 'POST'])
def demo_select(group, name):
    if request.method == 'POST':
        select = list(request.form.getlist('items'))
        items = ';'.join(select)
        return redirect('/demo/map/{}/{}/route/{}'.format(group, name, items))

    else:
        items = get_map_data(group, name)
        menu = {}
        print(items)
        valid = [item for item in items if items[item] != 'START' and items[item] != 'LINK' and items[item] != 'Cashier' and items[item] != 'GATE']
        for v in valid:
            menu[v] = items[v]
        print('BREAK')
        print(items)
        return render_template('select_page.html', items=menu)

@app.route('/demo/map/<string:group>/<string:name>/route/<string:items>')
def demo_route(group, name, items):
    path = get_route(group, name, items)
    data = get_map_data(group, name)
    point = get_map_point(group, name)
    item = items.split(';') + ['START', 'END']
    return render_template('map.html', path=path, data=data, point=point, item=item)

app.run(host='178.128.24.70', port=8000)


