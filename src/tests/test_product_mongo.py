from daos.product_dao_mongo import ProductDAOMongo
from models.product import Product

dao = ProductDAOMongo()
    
def test_product_select():
    user_list = dao.select_all()
    assert len(user_list) >= 3

def test_product_insert():
    prd = Product(None, 'Test', 'testBrand', 19.11)
    dao.insert(prd)
    prod_list = dao.select_all()
    prods = [p.name for p in prod_list]
    assert prd.name in prods


def test_product_update():
    prd = Product(None, 'Testicular', 'testimonialBrand', 12.55)
    assigned_id = dao.insert(prd)

    corrected_name = 'Testimonial'
    prd.prod_id = assigned_id
    prd.name = corrected_name
    dao.update(prd)

    prod_list = dao.select_all()
    prods = [p.name for p in prod_list]
    assert corrected_name in prods
     # cleanup
    dao.delete(assigned_id)

def test_product_delete():
    prd = Product(None, 'Testament', 'TestamentBrand',88.55)
    assigned_id = dao.insert(prd)
    dao.delete(assigned_id)

    new_dao = ProductDAOMongo()
    prod_list = new_dao.select_all()
    prods = [p.name for p in prod_list]
    assert prd.name not in prods