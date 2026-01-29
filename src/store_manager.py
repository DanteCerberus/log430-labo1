"""
Store manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.user_view import UserView
from views.product_view import ProductView

if __name__ == '__main__':
    print("===== LE MAGASIN DU COIN =====")
    choice = input("1.Pour utilisateur \n2.Produit ")
    main_menu = 0
    if choice == 1:
        main_menu = UserView()
    else : 
        main_menu = ProductView()

    main_menu.show_options()
