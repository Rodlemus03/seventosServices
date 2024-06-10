from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Ruta para el CRUD de clientes
CLIENTES_FILE = 'clientes.json'

def load_clientes():
    if not os.path.exists(CLIENTES_FILE):
        return []
    with open(CLIENTES_FILE, 'r') as file:
        return json.load(file)

def save_clientes(clientes):
    with open(CLIENTES_FILE, 'w') as file:
        json.dump(clientes, file, indent=4)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/clientes')
def listar_clientes():
    clientes = load_clientes()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        clientes = load_clientes()
        cliente = {
            'id': len(clientes) + 1,
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'telefono': request.form['telefono'],
            'direccion': request.form['direccion'],
        }
        clientes.append(cliente)
        save_clientes(clientes)
        return redirect(url_for('listar_clientes'))
    return render_template('nuevo_cliente.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    clientes = load_clientes()
    cliente = next((c for c in clientes if c['id'] == id), None)
    if cliente is None:
        return 'Cliente no encontrado', 404
    if request.method == 'POST':
        cliente['nombre'] = request.form['nombre']
        cliente['apellido'] = request.form['apellido']
        cliente['telefono'] = request.form['telefono']
        cliente['direccion'] = request.form['direccion']
        cliente['email'] = request.form['email']
        save_clientes(clientes)
        return redirect(url_for('listar_clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/clientes/borrar/<int:id>')
def borrar_cliente(id):
    clientes = load_clientes()
    clientes = [c for c in clientes if c['id'] != id]
    save_clientes(clientes)
    return redirect(url_for('listar_clientes'))


# Ruta para el CRUD de inventario
INVENTARIO_FILE = 'inventario.json'

def load_inventario():
    if not os.path.exists(INVENTARIO_FILE):
        return []
    with open(INVENTARIO_FILE, 'r') as file:
        return json.load(file)

def save_inventario(inventario):
    with open(INVENTARIO_FILE, 'w') as file:
        json.dump(inventario, file, indent=4)

@app.route('/inventario')
def listar_inventario():
    inventario = load_inventario()
    return render_template('inventario.html', inventario=inventario)

@app.route('/inventario/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        inventario = load_inventario()
        producto = {
            'id': len(inventario) + 1,
            'nombre_producto': request.form['nombre_producto'],
            'marca': request.form['marca'],
            'valor': float(request.form['valor']),
            'precio': float(request.form['precio']),
            'stock': int(request.form['stock'])
        }
        inventario.append(producto)
        save_inventario(inventario)
        return redirect(url_for('listar_inventario'))
    return render_template('nuevo_producto.html')

@app.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    inventario = load_inventario()
    producto = next((p for p in inventario if p['id'] == id), None)
    if producto is None:
        return 'Producto no encontrado', 404
    if request.method == 'POST':
        producto['nombre_producto'] = request.form['nombre_producto']
        producto['marca'] = request.form['marca']
        producto['valor'] = float(request.form['valor'])
        producto['precio'] = float(request.form['precio'])
        producto['stock'] = int(request.form['stock'])
        save_inventario(inventario)
        return redirect(url_for('listar_inventario'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/inventario/borrar/<int:id>')
def borrar_producto(id):
    inventario = load_inventario()
    inventario = [p for p in inventario if p['id'] != id]
    save_inventario(inventario)
    return redirect(url_for('listar_inventario'))
# Ruta para la página de pedidos

@app.route('/tabla_pedidos', methods=['GET', 'POST'])
def obtener_pedidos():
    # Leer los datos de los pedidos desde el archivo JSON
    with open('pedidos.json', 'r') as file:
        pedidos = json.load(file)
    
    # Leer los datos de los clientes desde el archivo JSON
    with open('clientes.json', 'r') as file:
        clientes = json.load(file)

    # Mapear los IDs de cliente en los pedidos a sus respectivos nombres de cliente
    for pedido in pedidos:
        cliente_id = pedido['cliente']
        for cliente in clientes:
            if cliente['id'] == cliente_id:
                pedido['cliente'] = cliente['nombre']
                break

    # Pasar los datos a la plantilla
    return render_template('tabla_pedidos.html', pedidos=pedidos)

@app.route('/eliminar_pedido', methods=['POST'])
def eliminar_pedido():
    if request.method == 'POST':
        # Obtener el ID del pedido a eliminar desde el formulario
        id_pedido = int(request.form['id_pedido'])

        # Leer los pedidos desde el archivo JSON
        with open('pedidos.json', 'r') as file:
            pedidos = json.load(file)

        # Eliminar el pedido con el ID especificado
        pedidos = [pedido for pedido in pedidos if pedido['id'] != id_pedido]

        # Escribir los pedidos actualizados de vuelta al archivo JSON
        with open('pedidos.json', 'w') as file:
            json.dump(pedidos, file, indent=4)

        # Redirigir a la página de la lista de pedidos
        return redirect('/tabla_pedidos')

@app.route('/pedidos', methods=['GET', 'POST'])
def nuevo_pedido():
    clientes = load_clientes()
    productos=load_inventario()
    if request.method == 'POST':
        cliente_id = int(request.form['cliente'])
        # Aquí puedes procesar el resto de los datos del pedido
        # por ejemplo, guardarlos en una base de datos
        return redirect(url_for('menu'))  # Redirige a la página de menú después de guardar el pedido
    return render_template('pedidos.html', clientes=clientes,productos=productos)
# Ruta para registrar el pedido
# Función para cargar los pedidos desde el archivo JSON
def load_pedidos():
    try:
        with open('pedidos.json', 'r') as file:
            pedidos = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        pedidos = []  # Si el archivo no existe o está vacío, retorna una lista vacía
    return pedidos

# Función para guardar el pedido en el archivo JSON
def guardar_pedido(pedido):
    pedidos = load_pedidos()
    pedidos.append(pedido)
    with open('pedidos.json', 'w') as file:
        json.dump(pedidos, file, indent=4)


# Ruta para registrar un nuevo pedido
@app.route('/registrar_pedido', methods=['POST'])
def registrar_pedido():
    if request.method == 'POST':
        # Obtener el ID del cliente y el total del formulario
        cliente_id = int(request.form['cliente'])
        total = float(request.form['total'])
        fecha_recoger=request.form['fecha_recoger']
        # Inicializar una lista para almacenar los detalles del pedido
        detalles_pedido = []

        # Obtener los detalles de cada producto en el carrito
        for key, value in request.form.items():
            if key.startswith('producto_'):
                producto_id = int(key.split('_')[1])
                cantidad = int(value)
                detalles_pedido.append({'id_producto': producto_id, 'cantidad': cantidad})

        # Obtener la fecha actual
        fecha_pedido = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Crear el objeto de pedido
        pedido = {
            'id': len(load_pedidos()) + 1,  # Obtener el próximo ID de pedido
            'cliente': cliente_id,
            'detalles_pedido': detalles_pedido,
            'total': total,
            'fecha_pedido': fecha_pedido,
            'fecha_recoger': fecha_recoger  # Puedes ajustar esto según sea necesario
        }

        # Guardar el pedido en el archivo JSON
        guardar_pedido(pedido)

        # Redirigir a alguna página después de registrar el pedido
        return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
