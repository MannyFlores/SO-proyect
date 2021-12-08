import datetime
import time


class Armador:
    def __init__(self):
        self.done_orders = []
        self.incomplete_orders = []
        self.done_parts = []
        self.out_time = 0
        self.out_average = 0

    def CheckForOrders(self, done_parts_queue, incomplete_order_queue):
        start_time = time.time()
        while True:
            try:
                current_time = time.time() - start_time
                throughput = len(self.done_orders) / (current_time / 60)
                print(f" Orders Per Minute: {throughput}")
                print(f" Avarge turnaround time: {self.out_time}")
            except:
                print(f" Orders Per Minute: 0 ")

            # Mientras el repartidor siga mandando ordenes, guarda una copia en self.incomplete_orders
            while not incomplete_order_queue.empty():
                self.incomplete_orders.append(incomplete_order_queue.get())

            # part es una parte de la queue
            part = done_parts_queue.get()

            found = False

            # Search for part in incomplete orders
            for order in self.incomplete_orders:
                for incomplete_part in order["orden"]:
                    if part["part_id"] == incomplete_part["part_id"]:
                        incomplete_part["status"] = 'done'
                        found = True

            # Revisar que este completa la orden
            for order in self.incomplete_orders:
                isdone = True
                for incomplete_part in order["orden"]:
                    if incomplete_part["status"] != "done":
                        isdone = False

                if isdone:
                    print(order)
                    self.done_orders.append(order)

                    arrival = datetime.datetime.strptime(order['datetime'], "%Y-%m-%d %H:%M:%S.%f")
                    out = datetime.datetime.now()

                    time_out = out - arrival

                    self.out_time = time_out.total_seconds()
                    self.out_average = self.out_time / len(self.done_orders)

                    self.incomplete_orders.remove(order)

            if not found:
                done_parts_queue.put(part)

                # turnaround time
