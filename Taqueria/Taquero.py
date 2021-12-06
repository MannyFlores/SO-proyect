import logging
import sys
import time


class Taquero:
    def __init__(self, name, meat, quesadillero):

        # Number of maximum orders in the main queue
        self.max_queued_orders = 5

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
        self.ingredient_threshold = 0

        self.time_cebolla = 0.5
        self.time_cilantro = 0.5
        self.time_guacamole = 0.5
        self.time_salsa = 0.5
        self.time_meat = 1

        self.needIngredients = False

        self.fan_time = 0
        self.fan = False

        self.rest_time = 0

    def check_ingredients(self, ingredient_queue):
        if self.ingredients["cebolla"]  <= self.ingredient_threshold:
            found = False
            logging.debug(f"{self.name}, esperando cebolla")
            while not found:
                ingredient = ingredient_queue.get()
                if ingredient == "cebolla":
                    self.ingredients["cebolla"] = 200
                    found = True

        if self.ingredients["cilantro"] <= self.ingredient_threshold:
            found = False
            logging.debug(f"{self.name}, esperando cilantro")
            while not found:
                ingredient = ingredient_queue.get()
                if ingredient == "cilantro":
                    self.ingredients["cilantro"] = 200
                    found = True

        if self.ingredients["guacamole"]  <= self.ingredient_threshold:
            found = False
            logging.debug(f"{self.name}, esperando guacamole")
            while not found:
                ingredient = ingredient_queue.get()
                if ingredient == "guacamole":
                    self.ingredients["guacamole"] = 100
                    found = True

        if self.ingredients["salsa"] <= self.ingredient_threshold:
            found = False
            logging.debug(f"{self.name}, esperando salsa")
            while not found:
                ingredient = ingredient_queue.get()
                if ingredient == "salsa":
                    self.ingredients["salsa"] = 150
                    found = True

        if self.tortillas <= self.ingredient_threshold:
            found = False
            logging.debug(f"{self.name}, esperando tortillas")
            while not found:
                ingredient = ingredient_queue.get()
                if ingredient == "salsa":
                    self.tortillas = 50
                    found = True

    def Do_Tacos(self, order_queue, quesadillas_done, done_part_queue, ingredient_queue):
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
            while self.isActive and len(self.main_queue) != 0:

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

                    self.check_ingredients(ingredient_queue)

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

                        if "cebolla" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0 and "cebolla" in part["ingredients"]:
                            time.sleep(self.time_cebolla)
                            logging.debug(f"{self.name} {part['part_id']}: Added Cebolla")
                            part["done_ingredients"].append("cebolla")
                            self.ingredients["cebolla"] -= 1
                        if time.time() - start_time >= self.quantum: break

                        if "cilantro" not in part["done_ingredients"] and self.ingredients["cilantro"] > 0 and "cilantro" in part["ingredients"]:
                            time.sleep(self.time_cilantro)
                            logging.debug(f"{self.name} {part['part_id']}: Added Cilantro")
                            part["done_ingredients"].append("cilantro")
                            self.ingredients["cilantro"] -= 1
                        if time.time() - start_time >= self.quantum: break

                        if "guacamole" not in part["done_ingredients"] and self.ingredients["guacamole"] > 0 and "guacamole" in part["ingredients"]:
                            time.sleep(self.time_guacamole)
                            logging.debug(f"{self.name} {part['part_id']}: Added Guacamole")
                            part["done_ingredients"].append("guacamole")
                            self.ingredients["guacamole"] -= 1
                        if time.time() - start_time >= self.quantum: break

                        if "salsa" not in part["done_ingredients"] and self.ingredients["salsa"] > 0 and "salsa" in part["ingredients"]:
                            time.sleep(self.time_salsa)
                            logging.debug(f"{self.name} {part['part_id']}: Added Salsa")
                            part["done_ingredients"].append("salsa")
                            self.ingredients["salsa"] -= 1
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
