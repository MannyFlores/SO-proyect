from generator import Generator
from Taqueria.Taquero import Taquero
from Taqueria.Repartidor import Repartidor
from Taqueria.Quesadillero import Quesadillero
from Taqueria.Armador import Armador
import multiprocessing


def main():
    order_generator = Generator()

    # Main Queue
    orden_queue = multiprocessing.Queue()

    # Generate Random orders
    for i in range(1, 10):
        orden = order_generator.generate_order()
        print(orden)
        orden_queue.put(orden)

    # Sub Queues
    asada_suadero_1_queue = multiprocessing.Queue()
    asada_suadero_2_queue = multiprocessing.Queue()
    adobada_queue = multiprocessing.Queue()
    quesadillas_queue = multiprocessing.Queue()
    cabeza_tripa_queue = multiprocessing.Queue()

    # Quesadillas Terminadas queue
    quesadillas_terminadas = multiprocessing.Queue()

    # Ordenes terminadas queue
    done_part_queue = multiprocessing.Queue()

    # Ordenes incompletas
    incomplete_order_queue = multiprocessing.Queue()

    # Create Repartidor
    repartidor = Repartidor(asada_suadero_1_queue, asada_suadero_2_queue, adobada_queue, quesadillas_queue, cabeza_tripa_queue)
    repartidor_processes = multiprocessing.Process(target=repartidor.Repartir, args=(orden_queue, incomplete_order_queue, ))
    repartidor_processes.start()

    # Create Armador
    armador = Armador()
    armador_process = multiprocessing.Process(target=armador.CheckForOrders, args=(done_part_queue, incomplete_order_queue, ))
    armador_process.start()

    # Quesadillero
    quesadillero = Quesadillero(name="Quesadillero")
    quesadillero_process = multiprocessing.Process(target=quesadillero.Do_Tacos, args=(repartidor.Quesadillero, quesadillas_terminadas, ))
    quesadillero_process.start()

    # Asada 1
    taquero_asada = Taquero(name="Asada_1", meat="Asada-Suadero", quesadillero=quesadillero)
    asada_1 = multiprocessing.Process(target=taquero_asada.Do_Tacos, args=(repartidor.Asada_Suadero_1, quesadillas_terminadas, done_part_queue, ))
    asada_1.start()

    # Asada 2
    taquero_asada_2 = Taquero(name="Asada_2", meat="Asada-Suadero", quesadillero=quesadillero)
    asada_2 = multiprocessing.Process(target=taquero_asada_2.Do_Tacos, args=(repartidor.Asada_Suadero_2, quesadillas_terminadas, done_part_queue, ))
    asada_2.start()

    # Adobada
    taquero_adobada = Taquero(name="Adobada", meat="Adobada", quesadillero=quesadillero)
    adobada = multiprocessing.Process(target=taquero_adobada.Do_Tacos, args=(repartidor.Adobada, quesadillas_terminadas, done_part_queue, ))
    adobada.start()

    # Cabeza Tripa
    taquero_cabeza = Taquero(name="Cabeza_Tripa", meat="Cabeza_Tripa", quesadillero=quesadillero)
    cabeza = multiprocessing.Process(target=taquero_cabeza.Do_Tacos, args=(repartidor.Tripa_Cabeza, quesadillas_terminadas, done_part_queue, ))
    cabeza.start()

    
if __name__ == '__main__':
    main()
