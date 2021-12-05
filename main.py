from generator import Generator
from Taqueria.Taquero import Taquero
from Taqueria.Repartidor import Repartidor
import multiprocessing


def main():
    order_generator = Generator()

    # Main Queue
    orden_queue = multiprocessing.Queue()

    for i in range(1, 5):
        orden_queue.put(order_generator.generate_order())

    # Sub Queues
    asada_suadero_1 = multiprocessing.Queue()
    asada_suadero_2 = multiprocessing.Queue()
    adobada = multiprocessing.Queue()
    quesadillas = multiprocessing.Queue()
    cabeza_tripa = multiprocessing.Queue()

    # Create Repartidor
    repartidor = Repartidor(asada_suadero_1, asada_suadero_2, adobada, quesadillas, cabeza_tripa)
    repartidor_processes = multiprocessing.Process(target=repartidor.Repartir, args=(orden_queue,))
    repartidor_processes.start()

    taquero_asada = Taquero(name="Asada_1", meat="Asada")
    asada_1 = multiprocessing.Process(target=taquero_asada.Do_Tacos, args=(repartidor.Asada_Suadero_1, ))
    asada_1.start()

    taquero_asada_2 = Taquero(name="Asada_2", meat="Asada")
    asada_2 = multiprocessing.Process(target=taquero_asada_2.Do_Tacos, args=(repartidor.Asada_Suadero_2,))
    asada_2.start()



    
if __name__ == '__main__':
    main()
