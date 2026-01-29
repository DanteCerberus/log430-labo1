"""
Product model
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

class Product:
    def __init__(self, prod_id, name, brand, price):
        self.prod_id=prod_id
        self.name=name
        self.brand=brand
        self.price=price