from generator import Generator
from Taqueria.Taquero import Taquero
from Taqueria.Repartidor import Repartidor
import multiprocessing


def main():
    order_generator = Generator()

    # Main Queue
    orden_queue = multiprocessing.Queue()

    # Generate Random orders
    for i in range(1, 50):
        orden_queue.put(order_generator.generate_order())

    # Sub Queues
    asada_suadero_1_queue = multiprocessing.Queue()
    asada_suadero_2_queue = multiprocessing.Queue()
    adobada_queue = multiprocessing.Queue()
    quesadillas_queue = multiprocessing.Queue()
    cabeza_tripa_queue = multiprocessing.Queue()

    # Create Repartidor
    repartidor = Repartidor(asada_suadero_1_queue, asada_suadero_2_queue, adobada_queue, quesadillas_queue, cabeza_tripa_queue)
    repartidor_processes = multiprocessing.Process(target=repartidor.Repartir, args=(orden_queue,))
    repartidor_processes.start()

    # Asada 1
    taquero_asada = Taquero(name="Asada_1", meat="Asada-Suadero")
    asada_1 = multiprocessing.Process(target=taquero_asada.Do_Tacos, args=(repartidor.Asada_Suadero_1, ))
    asada_1.start()

    # Asada 2
    taquero_asada_2 = Taquero(name="Asada_2", meat="Asada-Suadero")
    asada_2 = multiprocessing.Process(target=taquero_asada_2.Do_Tacos, args=(repartidor.Asada_Suadero_2,))
    asada_2.start()

    # Adobada
    taquero_adobada = Taquero(name="Adobada", meat="Adobada")
    adobada = multiprocessing.Process(target=taquero_adobada.Do_Tacos, args=(repartidor.Adobada, ))
    adobada.start()

    # Cabeza Tripa
    taquero_cabeza = Taquero(name="Cabeza_Tripa", meat="Cabeza_Tripa")
    cabeza = multiprocessing.Process(target=taquero_cabeza.Do_Tacos, args=(repartidor.Tripa_Cabeza,))
    cabeza.start()


    
if __name__ == '__main__':
    main()
