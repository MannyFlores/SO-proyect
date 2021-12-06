import random
import datetime
import pprint


# This script generates random mock orders to test the scheduling algorithm
import time


class Generator:
    def __init__(self):
        self.taco_meat = ['asada', 'adobada', 'suadero', 'cabeza', 'tripa']
        self.ingredients = ['cebolla', 'cilantro', 'salsa', 'guacamole']
        self.type = ['taco', 'quesadilla']
        self.order_count = 1
        self.max_parts = 5

    # This function generates a part from the order
    # returns a dictionary
    def generate_taco(self, part_num):
        # ['asada', 'adobada', 'suadero', 'cabeza', 'tripa']
        meat = random.choice(self.taco_meat)

        random.seed(time.time())

        # Picks random ingredients ['cebolla', 'cilantro', 'salsa', 'guacamole']
        ingredients = []
        for ingredient in self.ingredients:
            if random.randint(0, 1) == 1:
                ingredients.append(ingredient)

        # number of tacos 1 - 100
        quantity = random.randint(1, 5)

        # Picks a random type ['taco', 'quesadilla']
        taco_type = random.choice(self.type)

        return {
            'part_id': f'{self.order_count}-{part_num}',
            'type': taco_type,
            'meat': meat,
            'status': 'open',
            'quantity': quantity,
            'ingredients': ingredients
        }

    # This function generates an order based on the sample json
    # returns a dictionary
    def generate_order(self):

        # Generate taco orders
        orden = []
        for i in range(1, random.randint(2, self.max_parts)):
            orden.append(self.generate_taco(part_num=i))

        out = {
            'datetime': str(datetime.datetime.now()),
            'request_id': self.order_count,
            'status': 'open',
            'orden': orden
        }

        self.order_count += 1

        # pprint.pprint(out)
        return out
