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

        # Parts finished
        self.done_orders = []

        # How many ingredients until refill
        self.ingredient_threshold = 10

        self.fan_time = 0
        self.fan = False

        self.rest_time = 0

    def Do_Tacos(self, order_queue):
        while True:
            # Take parts if the main queue is not full and the taqueria queue has items.
            while not order_queue.empty() and len(self.main_queue) < self.max_queued_orders and self.isActive:
                # Take a part from the queue
                part = order_queue.get()
                part["tacos_done"] = 0
                print(f"{self.name} Refilling queue with part: {part['part_id']}")
                # Add to the main queue
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

                        # Make Quesadillas
                        time.sleep(1.5)

                        part["tacos_done"] += 1
                        self.tacos_done += 1

                    if part["tacos_done"] == part["quantity"]:
                        print(f"{self.name} {part['part_id']}: Done")
                        self.done_orders.append(part)
                        self.main_queue.remove(part)
                    else:
                        print(f"{self.name} {part['part_id']}: Suspended")

            if self.fan and time.time() - self.fan_time >= 60:
                print(f"{self.name} Ventilador Apagado")
                self.fan = False

            if not self.isActive and time.time() - self.rest_time >= 30:
                print(f"{self.name}  Activo")
                self.isActive = True
