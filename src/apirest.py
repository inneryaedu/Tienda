from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Tienda'
mysql = MySQL(app)

#Renderizar la vista de la ruta inicial
@app.route('/')
def productos():
    return render_template('productos.html')

class ProductosResource(Resource):
    contador=0
    def get(self):
        # Obtener todos los productos de la base de datos
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Productos")
            productos = cur.fetchall()
            cur.close()
            return {'productos':productos},200

    def post(self):
        # Agregar un nuevo producto a la base de datos
        nombre = request.json['nombre']
        precio = request.json['precio']
        descripcion = request.json['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Productos (nombre, precio, descripcion) VALUES (%s, %s, %s)",
                    (nombre, precio, descripcion))
        mysql.connection.commit()
        cur.close()

        return {'message': 'Producto agregado correctamente'}, 201

api.add_resource(ProductosResource, '/productos')

if __name__ == '__main__':
    app.run(debug=True)