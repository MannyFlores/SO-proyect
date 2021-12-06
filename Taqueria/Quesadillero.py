import time


class Quesadillero:
    def __init__(self, name="Taquero"):
        self.name = name

    def Do_Tacos(self, order_queue, quesadillas_queue):
        while True:

            part = order_queue.get()

            for i in range(0, part["quantity"]):
                time.sleep(1)
                quesadillas_queue.put(1)