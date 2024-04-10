from flask import Flask, jsonify, request, make_response
from sqlalchemy.exc import IntegrityError
from models.pizza import Pizza
from models.restaurant import Restaurant
from models.restaurant_pizza import RestaurantPizza
from models.dbconfig import db
from flask_cors import CORS
import os

def create_app():
    # define routes , request hooks , define is helper methods associated to the routes 
    # create the flask app 
    app = Flask(__name__)
    # allow CORS FOR ALL ROUTES 
    CORS(app)
    app.config.from_object('config.Config')

    @app.route("/", methods=['GET'])
    def home():
        return 'Karibu to the Pizza Restaurant API! 🍕 For a list of restaurants, visit /restaurants. For a list of pizzas go to /pizzas'

    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        output = []
        for restaurant in restaurants:
            output.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address
            })
        return jsonify(output)

    @app.route('/restaurants/<int:id>', methods=['GET'])
    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            pizzas = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in restaurant.pizzas]
            return jsonify({
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'pizzas': pizzas
            })
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'error': 'Restaurant not found'}), 404

    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        output = []
        for pizza in pizzas:
            output.append({
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            })
        return jsonify(output)
    
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.json
        try:
            # Extract data from request
            price = float(data.get('price'))
            pizza_id = int(data.get('pizza_id'))
            restaurant_id = int(data.get('restaurant_id'))

            # Validate input
            if not (price and 1 <= price <= 30 and pizza_id and restaurant_id):
                return jsonify({"errors": ["Invalid input data"]}), 400

            # Check if pizza and restaurant exist
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)
            if not (pizza and restaurant):
                return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

            # Create restaurant pizza
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Return the created pizza details
            return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 201
        except ValueError:
            return jsonify({"errors": ["Invalid price or IDs"]}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"errors": ["Database integrity error"]}), 400

    return app
