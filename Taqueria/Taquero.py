from time import sleep
from multiprocessing import Process


class Taquero:
    def __init__(self):

        # Log steps
        # TODO: implement logging
        self.verbose = False

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
        # Mock numbers, the time is defined in the project
        self.rest_time_max = 100
        self.rest_time = 0
        self.active_time = 0
        self.active_time_max = 100

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
    # quesadillero is an object
    # chalan is an object
    # returns True if the order is completed
    # returns False if the order cannot be completed
    def process_part(self, part, quesadillero):
        # Time for each ingredient
        # This times should be the ones defined in the project
        time_cebolla = 1
        time_cilantro = 1
        time_guacamole = 1
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
                # Check if there is available ingredients
                # if not the order is put on hold
                if self.ingredients['cebolla'] > 0:
                    sleep(time_cebolla)
                else:
                    return False

            if 'cilantro' in part['ingredients']:
                # Check if there is available ingredients
                # if not the order is put on hold
                if self.ingredients['cebolla'] > 0:
                    sleep(time_cebolla)
                else:
                    return False

            if 'guacamole' in part['ingredients']:
                # Check if there is available ingredients
                # if not the order is put on hold
                if self.ingredients['cebolla'] > 0:
                    sleep(time_cebolla)
                else:
                    return False

            if 'salsa' in part['ingredients']:
                # Check if there is available ingredients
                # if not the order is put on hold
                if self.ingredients['cebolla'] > 0:
                    sleep(time_cebolla)
                else:
                    return False

            self.tacos_done += 1

        # Update part status
        part['status'] = 'done'

        # Insert finished part in the done list
        self.done_orders.append(part)

        return True

    # This function handles incoming orders and calls the auxiliary necessary functions
    def handle_orders(self, order_queue, quesadillero, chalan):
        # Work if the order queue has orders and the Taquero is not resting
        while order_queue and self.active_time < self.active_time_max:
            # Get an order from the order queue
            self.main_queue.append(order_queue.get())

            # Pass order to the sub queue if its not full
            # The sub queue holds process for each part
            if len(self.sub_queue) < self.max_sub_queued_orders:
                # Create a process with a part from the main queue
                p = Process(target=self.process_part, args=(self.main_queue.pop()))
                p.start()
                p.join()
                self.sub_queue.append(p)

            # Work on the sub queue
            # The parts are going to be worked on using round robin
            # The time each part of the order is worked on is defined by self.quantum
            # TODO: implement round robin for self.sub_queue

            # The chalan needs to check if an order was not completed
            # If the order is not completed, check the ingredient pool
            # The chalan should be another process, this so the Taquero can work in other parts
            # TODO: implement chalan ingredient checks
