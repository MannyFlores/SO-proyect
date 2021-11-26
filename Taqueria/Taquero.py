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

        # Keep track of rests
        self.isActive = False

        # Number of tacos completed
        self.tacos_done = 0

    # This function returns true if a quesadilla is ready
    # Returns true
    @staticmethod
    def get_quesadilla(quesadillero):
        # Check if quesadillero has quesadillas ready
        if quesadillero.done_quesadillas:
            quesadillero.take_quesadilla()
            return True
        else:
            return False

    # This function takes care of parts
    # part is a dictionary
    def process_part(self, part, quesadillero):
        # Time for each ingredient
        # This times should be the ones defined in the project
        time_cebolla = 1
        time_cilantro = 1
        time_guacamale = 1
        time_salsa = 1
        time_meat = 1

        # Check if taco or quesadilla
        if part['type'] is 'quesadilla':
            # Check if quesadilla is ready
            # if the quesadilla is not ready return false
            # false means the order is not completed
            if not self.get_quesadilla(quesadillero):
                return False

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

            self.tacos_done += 1

        # Update part status
        part['status'] = 'done'

        # Insert finished part in the done list
        self.done_orders.append(part)

        return True
