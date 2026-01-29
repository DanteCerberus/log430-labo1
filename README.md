# Labo 01 – Client/Serveur, Persistence (DAO/RDBS/NoSQL)
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann.

## 🎯 Objectifs d’apprentissage

- Apprendre à créer une application **client-serveur** simple.
- Comprendre et mettre en œuvre la structure **MVC avec DAO** pour bien séparer les responsabilités.
- Comprendre les avantages et les inconvénients des bases de données relationnelles (ex. MySQL) par rapport aux bases « NoSQL » ou orientées à documents (ex. MongoDB).

--- 

## ⚙️ Setup
Dans ce laboratoire, vous développerez une application de gestion des utilisateurs et des articles pour un petit magasin. Il ne s'agit pas d'une application commerciale complète, mais elle offre une structure de base qui nous permettra d’expérimenter une architecture Client–Serveur sous une forme simplifiée.

> ⚠️ IMPORTANT : Avant de commencer le setup et les activités, veuillez lire la documentation architecturale dans le répertoire `/docs/arc42/docs.pdf`.

### 1. Clonez le dépôt

```bash
git clone git@github.com:DanteCerberus/log430-labo1.git
cd log430-labo1
```

### 2. Créez un fichier .env
Créez un fichier `.env` basé sur `.env.example`. Dans le fichier `.env`, utilisez les mêmes identifiants que ceux mentionnés dans `docker-compose.yml`.

> ⚠️ IMPORTANT : Si vous executez l'application sur votre ordinateur, utilisez les valeurs `localhost` ou `127.0.0.1` sur les variables `MYSQL_HOST` et `MONGODB_HOST`. Si vous executez l'application sur **Docker**, conservez les valeurs indiqués dans le fichier `.env.example.`. Dans un conteneur Docker, vous devez **toujours** indiquer le nom (hostname) d'un service dans `docker-compose.yml` et non `localhost`.

### 3. Créez un réseau Docker
Éxecutez dans votre terminal:
```bash
docker network create labo01-network
```

### 4. Préparer l’environnement de développement
Suivez les mêmes étapes que dans le labo 0. 

### 5. Lancez l’application 
Suivez les mêmes étapes que dans le labo 0, mais utilisez `store_manager.py` au lieu de `calculator.py`.
```bash
python src/store_manager.py
```

---

## 🧪 Activités pratiques

### 1. DAO MySQL

Le fichier `UserDAO` (dans `dao/user_dao.py`) contient déjà les méthodes `select_all()` et `insert(user)`.

Complétez cette DAO en y ajoutant :
   - `update(user)` – pour modifier un utilisateur existant.
   - `delete(user_id)` – pour supprimer un utilisateur.

> 💡 **Question 1** : Quelles commandes avez-vous utilisées pour effectuer les opérations UPDATE et DELETE dans MySQL ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.


Un mélange des deux. conn pour gérer la connection, cursor pour gérer la requête sql. 

    def update(self, user):
        """ Update given user in MySQL """
        self.cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (user.name, user.email, user.id))
        self.conn.commit()
        

    def delete(self, user_id):
        """ Delete user from MySQL with given user ID """
        self.cursor.execute(
            "DELETE FROM users WHERE id =%s",
            [user_id]
        )
        self.conn.commit()

#### Remarque : types de DAO
Il existe plusieurs manières d’implémenter une DAO. Par exemple, nous pourrions placer les opérations de base de données directement dans la classe Model. Dans notre cas, nous conservons la DAO et le Model séparés, comme décrit dans les ouvrages suivants : 
- 📘 Documenting Software Architectures: Views and Beyond, Clements et al., 2010, p. 97.
- 📕 Core J2EE Patterns: Best Practices and Design Strategies, Alur et al., 2001, p. 252.

### 2. DAO MongoDB

Créez une nouvelle DAO `UserDAOMongo` dans un fichier `dao/user_dao_mongo.py`.

Implémentez les mêmes méthodes :
   - `select_all()`
   - `insert(user)`
   - `update(user)`
   - `delete(user_id)`

Modifiez la méthode `__init__` pour vous connecter à MongoDB au lieu de MySQL. Utilisez la bibliothéque `pymongo` et la variable d'environnement `MONGODB_HOST`.

Modifiez `test_user.py` pour utiliser `UserDAOMongo` en lieu de `UserDAO`, puis relancez les tests. Une implémentation correcte doit produire les mêmes résultats, en considérant que quelques ajustements mineurs dans les tests peuvent être nécessaires pour assurer l’interchangeabilité des DAO.

> 💡 **Question 2** : Quelles commandes avez-vous utilisées pour effectuer les opérations dans MongoDB ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.

conn -> MongoClient
cursor -> une collection de la base de données

"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            env_path = ".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MYSQL_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD") 
            self.client = MongoClient(
                f"mongodb://{db_user}:{db_pass}@{db_host}:27017"
            )
            db = self.client[db_name]
            self.collection = db["users"] 
            
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MySQL """
        rows = self.collection.find()
        return [
        User(
            user_id=row.get("id"),
            name=row.get("name"),
            email=row.get("email")
        )
        for row in rows
        ]

    def insert(self, user):
        """ Insert given user into MySQL """
        return self.collection.insert_one({"name" :user.name, "email" : user.email}).inserted_id

    def update(self, user):
        """ Update given user in MySQL """
        self.collection.find_one_and_update(
            {"_id" : user.id}, 
            {"$set":{"name" : user.name,"email" : user.email}}
            )
        

    def delete(self, user_id):
        """ Delete user from MySQL with given user ID """
        self.collection.find_one_and_delete({"_id" : user_id})
        
        

    def delete_all(self): #optional
        """ Empty users table in MySQL """
        self.collection.delete_many( {})
        
        
        
    def close(self):
        self.client.close()


### 3. Nouvelle table : Products
Insérez le code SQL pour créer la table `products` dans `db-init/init.sql`. Ce fichier sera executé a chaque fois qu'on démarre la conteneur.
```sql
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    brand VARCHAR(20) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

Ensuite, vous devez arrêter, reconstruire et redémarrer le conteneur Docker.
```bash
docker compose down -v 
docker compose build
docker compose up -d
```

Créez un nouvel Model, View, Controller et DAO pour `Product`. Utilisez une structure MVC similaire à `User`. Ajoutez les options `Montrer la liste d'items` et `Ajouter un item` dans `product_view.py`. Vous pouvez également ajouter une option de `Supprimer un item` au menu (facultatif). Si vous voulez, créez une classe `View` séparée uniquement pour imprimer toutes les options de menu. Veuillez utiliser les diagrammes UML disponibles dans le dossier `docs/views` comme référence pour l’implémentation.

N'oubliez pas la création des tests pour valider `ProductDAO`. Le fichier de test est dans le répertoire `src/tests/test_product.py`. Vous pouvez utilizer `src/tests/test_user.py` comme référence de test.

> 💡 **Question 3** : Comment avez-vous implémenté votre `product_view.py` ? Est-ce qu’il importe directement la `ProductDAO` ? Veuillez inclure le code pour illustrer votre réponse.

Le code est essentiellment le même que celui de user avec quelque modidification pour le model Product. Il appel le controlleur qui lui appel la ProductDAO

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


> 💡 **Question 4** : Si nous devions créer une application permettant d’associer des achats d'articles aux utilisateurs (`Users` → `Products`), comment structurerions-nous les données dans MySQL par rapport à MongoDB ?

Pour MySQL, il faudrait faire une ou plusieurs table intermédiaire. Les tables peuvent être facture qui contiendrait l'utilisateur et listeItem qui contiendrait une référence du numéro facture, de l'identifiant des produits ainsi que la quantité de chacun.

MongoDB pourrait contenir une table qui contiendrait l'identifiant de l'utilisateur ainsi que la sous-liste des produits de chancun.


### ✅ Correction des activités

Des tests unitaires sont inclus dans le dépôt. Pour les exécuter :

```bash
pytest
```

Pour exécuter un fichier de test spécifique (par exemple, `test_user.py`)  :

```bash
pytest ./src/tests/test_user.py
```

Si tous les tests `User` et `Product` passent ✅, vos implémentations sont correctes.

---

## 📦 Livrables

- Code compressé en `.zip` contenant **l'ensemble du code source** du projet Labo 01.
- Rapport `.pdf` répondant aux 4 questions presentées dans ce fichier. Il est **obligatoire** d'ajouter du code ou des sorties de terminal pour illustrer chacune de vos réponses.

