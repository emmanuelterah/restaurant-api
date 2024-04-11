# seed.py

from models.pizza import Pizza
from models.restaurant import Restaurant
from models.restaurant_pizza import RestaurantPizza
from models.dbconfig import db

# def seed_data():
#     RestaurantPizza.query.delete()
#     Pizza.query.delete()
#     Restaurant.query.delete()

#     dominion_pizza = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
#     pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
    
#     db.session.add(dominion_pizza)
#     db.session.add(pizza_hut)
    
#     db.session.commit()

#     cheese_pizza = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
#     pepperoni_pizza = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    
#     db.session.add(cheese_pizza)
#     db.session.add(pepperoni_pizza)

#     db.session.commit()

#     db.session.add(RestaurantPizza(price=10, restaurant_id=dominion_pizza.id, pizza_id=cheese_pizza.id))
#     db.session.add(RestaurantPizza(price=12, restaurant_id=pizza_hut.id, pizza_id=pepperoni_pizza.id))

#     db.session.commit()

def seed_data():
    # Check if data already exists and delete it if necessary
    existing_restaurants = Restaurant.query.all()
    existing_pizzas = Pizza.query.all()
    existing_restaurant_pizzas = RestaurantPizza.query.all()

    if existing_restaurant_pizzas:
        RestaurantPizza.query.delete()
    if existing_pizzas:
        Pizza.query.delete()
    if existing_restaurants:
        Restaurant.query.delete()

    # Create new restaurant instances
    dominion_pizza = Restaurant.query.filter_by(name="Dominion Pizza").first()
    if not dominion_pizza:
        dominion_pizza = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
        db.session.add(dominion_pizza)

    pizza_hut = Restaurant.query.filter_by(name="Pizza Hut").first()
    if not pizza_hut:
        pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
        db.session.add(pizza_hut)

    db.session.commit()

    # Create new pizza instances
    cheese_pizza = Pizza.query.filter_by(name="Cheese").first()
    if not cheese_pizza:
        cheese_pizza = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
        db.session.add(cheese_pizza)

    pepperoni_pizza = Pizza.query.filter_by(name="Pepperoni").first()
    if not pepperoni_pizza:
        pepperoni_pizza = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        db.session.add(pepperoni_pizza)

    db.session.commit()

    # Create new restaurant pizza instances
    dominion_cheese_pizza = RestaurantPizza.query.filter_by(restaurant_id=dominion_pizza.id, pizza_id=cheese_pizza.id).first()
    if not dominion_cheese_pizza:
        db.session.add(RestaurantPizza(price=10, restaurant_id=dominion_pizza.id, pizza_id=cheese_pizza.id))

    pizza_hut_pepperoni_pizza = RestaurantPizza.query.filter_by(restaurant_id=pizza_hut.id, pizza_id=pepperoni_pizza.id).first()
    if not pizza_hut_pepperoni_pizza:
        db.session.add(RestaurantPizza(price=12, restaurant_id=pizza_hut.id, pizza_id=pepperoni_pizza.id))

    db.session.commit()

