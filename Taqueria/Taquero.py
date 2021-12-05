import time


class Taquero():
    def __init__(self, name="Taquero", meat="Asada"):

        # Number of maximum orders in the main queue
        self.max_queued_orders = 5

        self.name = name

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

        self.done_orders = []

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

    def Do_Tacos(self, order_queue):
        while True:
            # Take parts if the main queue is not full and the taqueria queue has items.
            while not order_queue.empty() and len(self.main_queue) < self.max_queued_orders and self.isActive:
                part = order_queue.get()
                part["done_ingredients"] = []
                part["tacos_done"] = 0
                print(f"{self.name} Refilling queue with part: {part['part_id']}")
                self.main_queue.append(part)

            while len(self.main_queue) > 0 and self.isActive:
                # Check if needs rest
                if self.tacos_done % 1000 == 0:
                    print(f"{self.name} Descansando")
                    self.rest_time = time.time()
                    self.isActive = False

                # Check if needs fan
                if self.tacos_done % 600 == 0:
                    print(f"{self.name} Ventilador Prendido")
                    self.fan_time = time.time()
                    self.fan = True


                for part in self.main_queue:
                    print(f"{self.name} {part['part_id']}: In progress")
                    start_time = time.time()
                    change = False
                    while part["tacos_done"] < part["quantity"]:

                        # Check for tortillas
                        if self.tortillas == 0:
                            break

                        # Add meat
                        if "meat" not in part["done_ingredients"]:
                            time.sleep(self.time_meat)
                            print(f"{self.name} {part['part_id']}: Added Meat")
                            part["done_ingredients"].append("meat")
                        if time.time() - start_time >= self.quantum: break

                        if "cebolla" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_cebolla)
                            print(f"{self.name} {part['part_id']}: Added Cebolla")
                            part["done_ingredients"].append("cebolla")
                        if time.time() - start_time >= self.quantum: break

                        if "cilantro" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_cilantro)
                            print(f"{self.name} {part['part_id']}: Added Cilantro")
                            part["done_ingredients"].append("cilantro")
                        if time.time() - start_time >= self.quantum: break

                        if "guacamole" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_guacamole)
                            print(f"{self.name} {part['part_id']}: Added Guacamole")
                            part["done_ingredients"].append("guacamole")
                        if time.time() - start_time >= self.quantum: break

                        if "salsa" not in part["done_ingredients"] and self.ingredients["cebolla"] > 0:
                            time.sleep(self.time_salsa)
                            print(f"{self.name} {part['part_id']}: Added Salsa")
                            part["done_ingredients"].append("salsa")
                        if time.time() - start_time >= self.quantum: break

                        part["tacos_done"] += 1
                        self.tacos_done += 1

                    if part["tacos_done"] == part["quantity"]:
                        print(f"{self.name} {part['part_id']}: Done")
                        self.done_orders.append(part)
                        self.main_queue.remove(part)
                    else:
                        print(f"{self.name} {part['part_id']}: Suspended")

            print(f"{self.name} Done with main queue, Refilling")

            if self.fan and time.time() - self.fan_time >= 60:
                print(f"{self.name} Ventilador Apagado")
                self.fan = False

            if not self.isActive and time.time() - self.rest_time >= 30:
                print(f"{self.name}  Activo")
                self.isActive = True