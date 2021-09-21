from datetime import datetime
from SalvandoAlimentos.data.models import rating as rating_model

def _set_date_time():
    # dd/mm/YY H:M:S
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def _rating_exists(id):
    comment = rating_model._rating_exists(id)
    return not len(comment) == 0



# CREATE
def create_rating(id_user, product_id, rating, comment):
    date = _set_date_time()
    rating_model.create_rating(id_user, product_id, rating, comment, date)


# LIST
def list_ratings():
    return rating_model.list_ratings()


# UPDATE
def update_rating(id_comment, rating, comment):
    date = _set_date_time()
    rating_model.update_rating(id_comment, rating, comment, date)

# DELETE
def delete_rating(id_rating):
    rating_model.delete_rating(id_rating)