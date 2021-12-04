import time


class Taquero():
    def __init__(self):

        # Number of maximum orders in the main queue
        self.max_queued_orders = 10

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
        self.process_sub_queue = []

        # Time to process taco
        self.quantum = 2

        # Keep track of rests
        self.isActive = False

        # Mock numbers, the time is defined in the project
        self.rest_time_max = 100
        self.rest_time = 0
        self.active_time = 0
        self.active_time_max = 100

        # Number of tacos completed
        self.tacos_done = 0

        self.time_cebolla = 1
        self.time_cilantro = 1
        self.time_guacamole = 1
        self.time_salsa = 1
        self.time_meat = 1

    def Do_Tacos(self, order_queue):
        # Take parts if the main queue is not full and the taqueria queue has items.
        while not order_queue.empty() and len(self.main_queue) < self.max_queued_orders:
            part = order_queue.get()
            part["done_ingredients"] = []
            part["tacos_done"] = 0
            self.main_queue.append(part)

        while len(self.main_queue) > 0:
            # Do taco
            for part in self.main_queue:
                print(f"{part['part_id']}: In progress")
                start_time = time.time()
                change = False
                while part["tacos_done"] < part["quantity"]:

                    # Add meat
                    if "meat" not in part["done_ingredients"]:
                        time.sleep(self.time_meat)
                        print(f"{part['part_id']}: Added Meat")
                        part["done_ingredients"].append("meat")
                    if time.time() - start_time >= self.quantum: break

                    if "cebolla" not in part["done_ingredients"]:
                        time.sleep(self.time_cebolla)
                        print(f"{part['part_id']}: Added Cebolla")
                        part["done_ingredients"].append("cebolla")
                    if time.time() - start_time >= self.quantum: break

                    if "cilantro" not in part["done_ingredients"]:
                        time.sleep(self.time_cilantro)
                        print(f"{part['part_id']}: Added Cilantro")
                        part["done_ingredients"].append("cilantro")
                    if time.time() - start_time >= self.quantum: break

                    if "guacamole" not in part["done_ingredients"]:
                        time.sleep(self.time_guacamole)
                        print(f"{part['part_id']}: Added Guacamole")
                        part["done_ingredients"].append("guacamole")
                    if time.time() - start_time >= self.quantum: break

                    if "salsa" not in part["done_ingredients"]:
                        time.sleep(self.time_salsa)
                        print(f"{part['part_id']}: Added Salsa")
                        part["done_ingredients"].append("salsa")
                    if time.time() - start_time >= self.quantum: break

                    part["tacos_done"] += 1

                if part["tacos_done"] == part["quantity"]:

                    print(f"{part['part_id']}: Done")
                    self.done_orders.append(part)
                    self.main_queue.remove(part)
                else:
                    print(f"{part['part_id']}: Suspended")
