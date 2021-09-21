from SalvandoAlimentos.data.models import product as product_model


def create_product(title, description, price, expiring_date, category_id, image_url, available_quant, pickup_time, status):
    product_model.create_product(title, description, price, expiring_date, category_id, image_url, available_quant,
                                 pickup_time, status)

def list_products():
    return product_model.list_products()


def edit_product(id, title, description, price):
    product_model.edit_product(id, title, description, price)


def delete_product(id):
    product_model.delete_product(id)

