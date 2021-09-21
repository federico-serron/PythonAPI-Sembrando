from flask import Flask, request, jsonify
from SalvandoAlimentos.services.auth import authentication
from SalvandoAlimentos.services.products import productService
from SalvandoAlimentos.services.categories import categoryService
from SalvandoAlimentos.services.orders import orderService
from SalvandoAlimentos.services.ratings import ratingService
from SalvandoAlimentos.services.paymethod import paymethodService

app = Flask(__name__)


######################################## USERS ##################################################
# Creating a user
@app.route('/signup', methods=['POST'])
def create_user():
    user_data = request.get_json()
    if 'name' not in user_data:
        return 'El nombre es requerido.', 412
    elif 'email' not in user_data:
        return 'El email es requerido.', 412
    elif 'user_name' not in user_data:
        return 'El nombre de usuario es requerido.', 412
    elif 'password' not in user_data:
        return 'Una contrasena es requerida.', 412
    elif 'address' not in user_data:
        return 'La direccion es requerida.', 412
    else:
        try:
            authentication.create_user(user_data['name'], user_data['email'], user_data['user_name'], user_data['password'],
                                       user_data['address'])
        except Exception:
            return "El usuario ya existe.", 412
        return 'El usuario se ha creado correctamente!', 200


# Listing users
@app.route('/users')
def list_users():
    return jsonify(authentication.obtener_usuarios())


#Listing a user
@app.route('/users/<id_user>')
def list_user(id_user):
    try:
        user = authentication.obtener_usuario(id_user)
        return jsonify(user)
    except Exception:
        return "Usuario no encontrado.", 404


#Update a user
@app.route('/users/<id_user>', methods=['PUT'])
def update_user(id_user):
    user_data = request.get_json()
    if 'name' not in user_data or user_data['name'] == '':
        return "Debe ingresar un nombre para el usuario.", 412
    elif 'password' not in user_data or user_data['password'] == '':
        return "Debe ingresar una password para el usuario.", 412
    else:
        authentication.update_user(id_user, user_data['name'], user_data['password'])
        return "Los valores del usuario se han actualizado correctamente!", 200


# Delete user
@app.route('/users/<id_user>', methods=['DELETE'])
def delete_user(id_user):
    authentication.delete_user(id_user)
    return "El usuario se ha eliminado satisfactoriamente.", 200


# Login
@app.route('/login', methods=['POST'])
def user_login():
    user_data = request.get_json()
    if 'user_name' not in user_data:
        return "Debe ingresar un usuario y/o contrasena", 412
    elif 'password' not in user_data:
        return "Debe ingresar un usuario y/o contrasena", 412
    try:
        id_session = authentication.user_login(user_data['user_name'], user_data['password'])
        return jsonify({"id_session": id_session})
    except Exception:
        return 'USUARIO NO ENCONTRADO', 404



######################################## PRODUCTS ##################################################
# Create a product
@app.route('/products', methods=['POST'])
def create_product():
    product_data = request.get_json()
    if 'title' not in product_data or 'description' not in product_data or 'price' not in product_data:
        return "Debe completar todos los campos", 412
    else:
        productService.create_product(product_data['title'], product_data['description'], product_data['price'],
                                      product_data['expiring_date'], product_data['category_id'],
                                      product_data['image_url'], product_data['available_quant'],
                                      product_data['pickup_time'], product_data['status'])
        return "Se creó el producto satisfactoriamente", 200

    

# Listing all the products
@app.route('/products')
def list_products():
    result = productService.list_products()

    if result == []:
        return "No se encontraron resultados para esta consulta."
    else:
        return jsonify(result)



# Updating a product
@app.route('/products/<id_product>', methods=['PUT'])
def update_product(id_product):
    product_to_update = request.get_json()
    if 'title' not in product_to_update:
        return "Debe ingresar el nuevo titulo", 412
    elif 'description' not in product_to_update:
        return "Debe ingresar la nueva descripcion.", 412
    elif 'price' not in product_to_update:
        return "Debe ingresar el nuevo precio.", 412
    else:
        productService.edit_product(id_product, product_to_update['title'], product_to_update['description'], product_to_update['price'])
        return "Se actualizo el registro correctamente.", 200



# Delete a product
@app.route('/products/<id_product>', methods=['DELETE'])
def delete_product(id_product):
    productService.delete_product(id_product)
    return "El registro se ha eliminado correctamente.", 200




######################################## CATEGORIES ##################################################

# Create category
@app.route('/categories', methods=['POST'])
def create_category():
    category_data = request.get_json()
    if 'name' not in category_data:
        return "Debe ingresar un nombre para la categoria.", 412
    else:
        categoryService.create_category(category_data['name'])
        return "Se ha creado la categoria correcamente!", 200


# List categories
@app.route('/categories', methods=['GET'])
def list_categories():
    return jsonify(categoryService.list_categories())


# Update category
@app.route('/categories/<id_category>', methods=['PUT'])
def update_category(id_category):
    new_data = request.get_json()
    if 'name' not in new_data:
        return "Debe ingresar el nuevo nombre de la categoria.", 412
    categoryService.update_category(id_category, new_data['name'])
    return "La categoria se ha cambiado correcamente!", 200



# Delete category
@app.route('/categories/<id_category>', methods=['DELETE'])
def delete_category(id_category):
    categoryService.delete_category(id_category)
    return "La categoria se ha eliminado correcamente.", 200


######################################## ORDERS ##################################################

# Create order
@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.get_json()
    if 'id' not in order_data:
        return "Debe especificar que usuario hizo la orden", 412
    elif 'products' not in order_data:
        return "Debe ingresar el/los productos a comprar.", 412
    elif 'payment_method' not in order_data:
        return "Debe ingresar un metodo de pago.", 412
    elif 'pickup_time' not in order_data:
        return "Debe especificar un horario para retirar el producto.", 412
    else:
        orderService.create_order(order_data['id'], order_data['products'], order_data['payment_method'], order_data['pickup_time'])
        return "La orden se ha creado satisfactoriamente.", 200


# List all the orders
@app.route('/orders')
def list_orders():
    list_order_data = request.get_json()
    return jsonify(orderService.list_orders())


# List all the orders of a specific user
@app.route('/orders/<id_user>')
def list_user_orders(id_user):
    result = orderService.list_user_orders(id_user)
    if not len(result) == 0:
        return jsonify(result)
    else:
        return "El usuario especificado no tiene ninguna orden activa.", 412


# Delete order
@app.route('/orders/<id_order>', methods=['DELETE'])
def delete_order(id_order):
    orderService.delete_order(id_order)
    return "La order seleccionada se la eliminado con exito.", 200



######################################## RATINGS ##################################################

#Create rating
@app.route('/ratings', methods=['POST'])
def create_rating():
    rating_data = request.get_json()
    if 'user_id' not in rating_data:
        return "Debe ingresar un usuario.", 412
    if 'product_id' not in rating_data:
        return "Debe ingresar a que producto pertenece la calaficacion.", 412
    if 'rating' not in rating_data:
        return "Debe ingresar una calificacion del 1 al 5", 412
    if int(rating_data['rating']) > 5 or int(rating_data['rating'] < 0):
        return "La calificacion debe estar entre 0 y 5.", 412
    ratingService.create_rating(rating_data['user_id'], rating_data['product_id'], rating_data['rating'], rating_data['comment'])
    return "Su calificacion se ha guardado correctamente!", 200



# List ratings
@app.route('/ratings')
def list_ratings():
    return jsonify(ratingService.list_ratings())


# Update rating
@app.route('/ratings/<id_rating>', methods=['PUT'])
def update_rating(id_rating):
    rating_data = request.get_json()
    if 'rating' not in rating_data:
        return "Debe ingresar una calificacion.", 412
    if 'comment' not in rating_data:
        return "Debe ingresar un comentario.", 412
    if int(rating_data['rating']) < 0 and int(rating_data['rating']) > 5:
        return "La calificacion debe ser entre 0 y 5.", 412
    try:
        ratingService.update_rating(id_rating, rating_data['rating'], rating_data['comment'])
        return "La calificacion se ha modificado correctamente!", 200
    except:
        return "No existe el comentario a modificar.", 404


# Delete rating
@app.route('/ratings/<id_rating>', methods=['DELETE'])
def delete_rating(id_rating):
    ratingService.delete_rating(id_rating)
    return "La calificacion se ha eliminado correctamente.", 200


######################################## PAYMENT METHODS ##################################################

# Create paymethod
@app.route('/paymethods', methods=['POST'])
def create_paymethod():
    paymethod_data = request.get_json()
    if 'name' not in paymethod_data:
        return "Debe ingresar el nombre del metodo de pago.", 412
    paymethodService.create_paymethod(paymethod_data['name'])
    return "El nuevo metodo de pago se ha agregado satisfactoriamente!", 200


# List paymethods
@app.route('/paymethods')
def list_paymethod():
    result = paymethodService.list_paymethod()
    return jsonify(result)


# Update paymethods
@app.route('/paymethods/<id_paymethod>', methods=['PUT'])
def update_paymethod(id_paymethod):
    paymethod_data = request.get_json()
    if 'name' not in paymethod_data:
        return "Debe especificar el nuevo nombre.", 412
    paymethodService.update_paymethod(id_paymethod, paymethod_data['name'])
    return "El metodo de pago se ha actualizado correctamente!", 200


# Delete paymethod
@app.route('/paymethods/<id_paymethod>', methods=['DELETE'])
def delete_paymethod(id_paymethod):
    paymethodService.delete_paymethod(id_paymethod)
    return "El metodo de pago se ha eliminado correctamente.", 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)


