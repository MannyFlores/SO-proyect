from time import sleep


class Taquero:
    def __init__(self):
        # Number of maximum orders in the main queue
        self.max_queued_orders = 10

        # Number of maximum orders in the sub queue
        self.max_sub_queued_orders = 10

        # Pool of ingredients
        self.ingredients = {
            'cebolla': 100,
            'cilantro': 100,
            'guacamole': 100,
            'salsa': 100
        }

        # Quantity of tortillas
        self.tortillas = 100

        # Taquero queues
        self.main_queue = []
        self.sub_queue = []
        self.done_orders = []

        # Time to process taco
        self.quantum = 1

    def get_quesadilla(self):
        pass

    # This function takes care of parts
    # part is a dictionary
    def process_part(self, part):
        # Time for each ingredient
        time_cebolla = 1
        time_cilantro = 1
        time_guacamale = 1
        time_salsa = 1
        time_meat = 1

        parts_done = 0

        # Check if taco or quesadilla
        if part['type'] is 'quesadilla':
            self.get_quesadilla()

        # Process each taco in the part
        for i in range(1, part):
            # Add Meat
            sleep(time_meat)

            # Check for ingredients in part
            if 'cebolla' in part['ingredients']:
                sleep(time_cebolla)

            if 'cilantro' in part['ingredients']:
                sleep(time_cilantro)

            if 'guacamole' in part['ingredients']:
                sleep(time_guacamale)

            if 'salsa' in part['ingredients']:
                sleep(time_salsa)

            parts_done = i

        # Update status of part
        part['status'] = 'done'

        return part