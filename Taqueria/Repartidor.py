class Repartidor():
    def __init__(self, asada_suadero_1, asada_suadero_2, adobada, quesadillas, cabeza_tripa):

        self.Tripa_Cabeza = cabeza_tripa
        self.Asada_Suadero_1 = asada_suadero_1
        self.Asada_Suadero_2 = asada_suadero_2
        self.Adobada = adobada
        self.Quesadillero = quesadillas

    def Repartir(self, order_queue):
        while True:
            order = order_queue.get()

            order["status"] = "In Progress"

            for part in order["orden"]:
                if part["meat"] == "asada" or part["meat"] == "suadero":
                    # Check queue lengths of taqueros
                    if self.Asada_Suadero_2.qsize() > self.Asada_Suadero_1.qsize():
                        self.Asada_Suadero_1.put(part)
                    else:
                        self.Asada_Suadero_2.put(part)

                if part["meat"] == "adobada":
                    self.Adobada.put(part)

                if part["meat"] == "tripa" or part["meat"] == "cabeza":
                    self.Tripa_Cabeza.put(part)

