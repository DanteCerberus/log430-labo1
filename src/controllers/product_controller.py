"""
User controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from daos.product_dao_mongo import ProductDAOMongo

class ProductController:
    def __init__(self):
        self.dao = ProductDAOMongo()

    def list_product(self):
        """ List all users """
        return self.dao.select_all()
        
    def create_product(self, user):
        """ Create a new user based on user inputs """
        self.dao.insert(user)

    def shutdown(self):
        """ Close database connection """
        self.dao.close()
