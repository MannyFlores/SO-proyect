class Armador:
    def __init__(self):
        self.done_orders = []
        self.incomplete_orders = []
        self.done_parts = []

    def CheckForOrders(self, done_parts_queue, incomplete_order_queue):
        while True:

            while not incomplete_order_queue.empty():
                self.incomplete_orders.append(incomplete_order_queue.get())

            part = done_parts_queue.get()

            found = False

            # Search for part in incomplete orders
            for order in self.incomplete_orders:
                for incomplete_part in order["orden"]:
                    if part["part_id"] == incomplete_part["part_id"]:
                        incomplete_part["status"] = 'done'
                        found = True

            for order in self.incomplete_orders:
                isdone = True
                for incomplete_part in order["orden"]:
                    if incomplete_part["status"] != "done":
                        isdone = False

                if isdone:
                    print(order)
                    self.incomplete_orders.remove(order)


            if not found:
                done_parts_queue.put(part)
