class Repartidor:
    def __init__(self, asada_suadero_1, asada_suadero_2, adobada, quesadillas, cabeza_tripa):

        self.Tripa_Cabeza = cabeza_tripa
        self.Asada_Suadero_1 = asada_suadero_1
        self.Asada_Suadero_2 = asada_suadero_2
        self.Adobada = adobada
        self.Quesadillero = quesadillas

    def Repartir(self, order_queue, incomplete_order_queue):
        while True:
            order = order_queue.get()

            order["status"] = "In Progress"

            for part in order["orden"]:
                if part["type"] == "quesadilla":
                    self.Quesadillero.put(part)

                if part["meat"] == "asada" or part["meat"] == "suadero":
                    # Asignar orden al taquero que tenga menos tacos en su queue
                    if self.Asada_Suadero_2.qsize() > self.Asada_Suadero_1.qsize():
                        self.Asada_Suadero_1.put(part)
                    else:
                        self.Asada_Suadero_2.put(part)
                elif part["meat"] == "adobada":
                    self.Adobada.put(part)
                elif part["meat"] == "tripa" or part["meat"] == "cabeza":
                    self.Tripa_Cabeza.put(part)

            # Pasar copia de orden al armador
            incomplete_order_queue.put(order)