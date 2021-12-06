import time


class Chalan:
    def __init__(self):
        self.max_cebolla = 200
        self.max_cilantro = 200
        self.max_guacamole = 100
        self.max_salsa = 150

    def CheckIngredients(self, ingredient_queue):
        while True:

            # Make tortillas
            start_time = time.time()
            tortilla_time = 10
            while time.time() - start_time < tortilla_time:
                time.sleep(5)
                print("Chalan haciendo tortilla")
                ingredient_queue.put("tortilla")

            # Make ingredient packs
            # Make cebolla
            print("Chalan haciendo cebolla")
            time.sleep(10)
            ingredient_queue.put("cebolla")

            print("Chalan haciendo cilantro")
            time.sleep(10)
            ingredient_queue.put("cilantro")

            print("Chalan haciendo guacamole")
            time.sleep(20)
            ingredient_queue.put("guacamole")

            print("Chalan haciendo salsa")
            time.sleep(15)
            ingredient_queue.put("salsa")
