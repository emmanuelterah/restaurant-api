# seed.py

from models.pizza import Pizza
from models.restaurant import Restaurant
from models.restaurant_pizza import RestaurantPizza
from models.dbconfig import db

def seed_data():
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    dominion_pizza = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
    
    db.session.add(dominion_pizza)
    db.session.add(pizza_hut)
    
    db.session.commit()

    cheese_pizza = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni_pizza = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    
    db.session.add(cheese_pizza)
    db.session.add(pepperoni_pizza)

    db.session.commit()

    db.session.add(RestaurantPizza(price=10, restaurant_id=dominion_pizza.id, pizza_id=cheese_pizza.id))
    db.session.add(RestaurantPizza(price=12, restaurant_id=pizza_hut.id, pizza_id=pepperoni_pizza.id))

    db.session.commit()
