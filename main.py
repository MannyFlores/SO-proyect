import time

from generator import Generator
from Taqueria.Taquero import Taquero
from Taqueria.Repartidor import Repartidor
from Taqueria.Quesadillero import Quesadillero
from Taqueria.Armador import Armador
from Taqueria.Chalan import Chalan
import multiprocessing


def main():
    order_generator = Generator()

    # Main Queue
    orden_queue = multiprocessing.Queue()

    # Sub Queues
    asada_suadero_1_queue = multiprocessing.Queue()
    asada_suadero_2_queue = multiprocessing.Queue()
    adobada_queue = multiprocessing.Queue()
    quesadillas_queue = multiprocessing.Queue()
    cabeza_tripa_queue = multiprocessing.Queue()

    # Quesadillas Terminadas queue
    quesadillas_terminadas = multiprocessing.Queue()

    # Todos los taqueros ponen sus parte terminada aqui
    done_part_queue = multiprocessing.Queue()

    # Ordenes incompletas - el repartidor manda una copia de la orden al armador por esta queue
    incomplete_order_queue = multiprocessing.Queue()

    # Queues de ingredientes - los chalanes mandan paquetes de ingredientes por estas queues
    ingrediente_queue_1 = multiprocessing.Queue()
    ingrediente_queue_2 = multiprocessing.Queue()

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
    asada_1 = multiprocessing.Process(target=taquero_asada.Do_Tacos, args=(repartidor.Asada_Suadero_1, quesadillas_terminadas, done_part_queue, ingrediente_queue_1, ))
    asada_1.start()

    # Asada 2
    taquero_asada_2 = Taquero(name="Asada_2", meat="Asada-Suadero", quesadillero=quesadillero)
    asada_2 = multiprocessing.Process(target=taquero_asada_2.Do_Tacos, args=(repartidor.Asada_Suadero_2, quesadillas_terminadas, done_part_queue, ingrediente_queue_1,))
    asada_2.start()

    # Adobada
    taquero_adobada = Taquero(name="Adobada", meat="Adobada", quesadillero=quesadillero)
    adobada = multiprocessing.Process(target=taquero_adobada.Do_Tacos, args=(repartidor.Adobada, quesadillas_terminadas, done_part_queue, ingrediente_queue_2, ))
    adobada.start()

    # Cabeza Tripa
    taquero_cabeza = Taquero(name="Cabeza_Tripa", meat="Cabeza_Tripa", quesadillero=quesadillero)
    cabeza = multiprocessing.Process(target=taquero_cabeza.Do_Tacos, args=(repartidor.Tripa_Cabeza, quesadillas_terminadas, done_part_queue, ingrediente_queue_2, ))
    cabeza.start()

    # Chalanes
    chalan_1 = Chalan()
    chalan_1_process = multiprocessing.Process(target=chalan_1.CheckIngredients, args=(ingrediente_queue_1, ))
    chalan_1_process.start()

    chalan_2 = Chalan()
    chalan_2_process = multiprocessing.Process(target=chalan_2.CheckIngredients, args=(ingrediente_queue_2, ))
    chalan_2_process.start()

    while True:
        start_time = time.time()
        while time.time() - start_time < 1:
            orden_queue.put(order_generator.generate_order())
    
if __name__ == '__main__':
    main()
