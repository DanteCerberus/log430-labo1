"""
User view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from models.product import Product
from controllers.product_controller import ProductController

class ProductView:
    @staticmethod
    def show_options():
        """ Show menu with operation options which can be selected by the user """
        controller = ProductController()
        while True:
            print("\n1. Montrer la liste de produit\n2. Ajouter un produit\n3. Quitter l'appli")
            choice = input("Choisissez une option: ")

            if choice == '1':
                product = controller.list_product()
                ProductView.show_products(product)
            elif choice == '2':
                name, brand, price = ProductView.get_inputs()
                product = Product(None, name, brand, price)
                controller.create_product(product)
            elif choice == '3':
                controller.shutdown()
                break
            else:
                print("Cette option n'existe pas.")

    @staticmethod
    def show_products(products):
        """ List users """
        print("\n".join(f"{product.prod_id}: {product.name} {product.brand}{product.price}" for product in products))

    @staticmethod
    def get_inputs():
        """ Prompt product for inputs necessary to add a new product """
        name = input("Nom du produit : ").strip()
        brand = input("Marque du produit: ").strip()
        prix = input("Prix du produit: ").strip()
        return name, brand, prix