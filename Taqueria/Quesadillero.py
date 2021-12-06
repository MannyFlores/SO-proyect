import time


class Quesadillero():
    def __init__(self, name="Taquero"):

        self.name = name

        # Number of tacos completed
        self.tacos_done = 1

    def Do_Tacos(self, order_queue, quesadillas_queue):
        while True:

            part = order_queue.get()
            quesadillas_done = 0

            while quesadillas_done < part["quantity"]:

                # Do quesadillas
                # time.sleep(20)
                quesadillas_done += 1
                quesadillas_queue.put(1)