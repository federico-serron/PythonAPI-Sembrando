from SalvandoAlimentos.data.data_base import BaseDeDatos

# CREATE NEW PRODUCT
def create_product(title, description, price, expiring_date, category_id, image_url, available_quant, pickup_time,
                   status):
    create_product_sql = f""" INSERT INTO products(title, description, price, expiring_date, category_id, image_url, 
    available_quant, pickup_time, status) 
    VALUES ('{title}', '{description}', '{price}', '{expiring_date}', '{category_id}', '{image_url}', '{available_quant}', '{pickup_time}', '{status}') 
    """

    bd = BaseDeDatos()
    bd.ejecutar_sql(create_product_sql)


# LIST ALL THE PRODUCTS
def list_products():
    list_products_sql = """
        SELECT * FROM products WHERE status=1
    """

    bd = BaseDeDatos()
    bd._crear_conexion()
    cursor = bd.conexion.cursor()
    cursor.execute(list_products_sql)

    query_result = [ dict(line) for line in [ zip([ column[0] for column in cursor.description ], row) for row in cursor.fetchall() ] ]

    bd._cerrar_conexion()

    return query_result


# EDIT A PRODUCT
def edit_product(id, title, description, price):
    edit_product_sql = f"""
        UPDATE products SET title='{title}', description='{description}', price={price} WHERE id={id}
    """

    bd = BaseDeDatos()
    bd.ejecutar_sql(edit_product_sql)


# DELETE A PRODUCT
def delete_product(id):
    delete_product_sql = f'DELETE FROM products WHERE id={id}'

    bd = BaseDeDatos()
    bd.ejecutar_sql(delete_product_sql)