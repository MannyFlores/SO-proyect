import time
import logging, sys


class Taquero():
    def __init__(self, name, meat, quesadillero):

        # Number of maximum orders in the main queue
        self.max_queued_orders = 10

        self.name = name

        self.quesadillero = quesadillero

        # Pool of ingredients
        self.ingredients = {
            'cebolla': 200,
            'cilantro': 200,
            'guacamole': 100,
            'salsa': 150
        }

        # Quantity of tortillas
        self.tortillas = 50

        # Taquero queues
        self.main_queue = []

        # Time to process taco
        self.quantum = 2

        # Keep track of rests
        self.isActive = False

        # Number of tacos completed
        self.tacos_done = 1

        # Parts finished
        self.done_orders = []

        # How many ingredients until refill
        self.ingredient_threshold = 10

        self.time_cebolla = 0.5
        self.time_cilantro = 0.5
        self.time_guacamole = 0.5
        self.time_salsa = 0.5
        self.time_meat = 1

        self.needIngredients = False

        self.fan_time = 0
        self.fan = False

        self.rest_time = 0

    def check_ingredients(self):
        if self.ingredients["cebolla"] < self.ingredient_threshold:
            self.needIngredients = True
        if self.ingredients["cilantro"] < self.ingredient_threshold:
            self.needIngredients = True
        if self.ingredients["guacamole"] < self.ingredient_threshold:
            self.needIngredients = True
        if self.ingredients["salsa"] < self.ingredient_threshold:
            self.needIngredients = True
        if self.tortillas < self.ingredient_threshold:
            self.needIngredients = True

    def Do_Tacos(self, order_queue, quesadillas_done, done_part_queue):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        while True:
            # Take parts if the main queue is not full and the taqueria queue has items.
            while not order_queue.empty() and len(self.main_queue) < self.max_queued_orders and self.isActive:
                # Take a part from the queue
                part = order_queue.get()
                # Keep track of ingredients done in the part
                part["done_ingredients"] = []
                # Keep track of how many tacos are done in the part
                part["tacos_done"] = 0
                part["quesadillas_done"] = 0

                print(f"{self.name} Refilling queue with part: {part['part_id']}")
                # Add to the main queue
                self.main_queue.append(part)

            # Work on main queue
            while self.isActive:

                # Check if needs rest
                if self.tacos_done % 1000 == 0:
                    logging.debug(f"{self.name} Descansando")
                    self.rest_time = time.time()
                    self.isActive = False
                    break

                # Check if needs fan
                if self.tacos_done % 600 == 0:
                    logging.debug(f"{self.name} Ventilador Prendido")
                    self.fan_time = time.time()
                    self.fan = True

                # Round robin
                for part in self.main_queue:
                    logging.debug(f"{self.name} {part['part_id']}: In progress")
                    start_time = time.time()

                    while part["tacos_done"] < part["quantity"]:

                        # Check for tortillas
                        if self.tortillas == 0:
                            break

                        # Add meat
                        if "meat" not in part["done_ingredients"]:
                            time.sleep(self.time_meat)
                            logging.debug(f"{self.name} {part['part_id']}: Added Meat")
                            part["done_ingredients"].append("meat")
                        if time.time() - start_time >= self.quantum: break

                        if "cebolla" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_cebolla)
                            logging.debug(f"{self.name} {part['part_id']}: Added Cebolla")
                            part["done_ingredients"].append("cebolla")
                        if time.time() - start_time >= self.quantum: break

                        if "cilantro" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_cilantro)
                            logging.debug(f"{self.name} {part['part_id']}: Added Cilantro")
                            part["done_ingredients"].append("cilantro")
                        if time.time() - start_time >= self.quantum: break

                        if "guacamole" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_guacamole)
                            logging.debug(f"{self.name} {part['part_id']}: Added Guacamole")
                            part["done_ingredients"].append("guacamole")
                        if time.time() - start_time >= self.quantum: break

                        if "salsa" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_salsa)
                            logging.debug(f"{self.name} {part['part_id']}: Added Salsa")
                            part["done_ingredients"].append("salsa")
                        if time.time() - start_time >= self.quantum: break

                        part["tacos_done"] += 1
                        part["done_ingredients"] = []
                        self.tacos_done += 1

                    if part["tacos_done"] == part["quantity"]:
                        logging.debug(f"{self.name} {part['part_id']}: Done")
                        part["status"] = 'done'
                        done_part_queue.put(part)
                        self.main_queue.remove(part)
                    else:
                        logging.debug(f"{self.name} {part['part_id']}: Suspended")

            if self.fan and time.time() - self.fan_time >= 60:
                logging.debug(f"{self.name} Ventilador Apagado")
                self.fan = False

            if not self.isActive and time.time() - self.rest_time >= 30:
                logging.debug(f"{self.name}  Activo")
                self.isActive = True
