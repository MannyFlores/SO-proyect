from generator import Generator
from Taqueria.Taquero import Taquero
import multiprocessing


def main():
    order_generator = Generator()

    orden_queue = multiprocessing.Queue()

    # Generate 10 random orders
    for i in range(1, 15):
        order = order_generator.generate_order()
        # print(order)
        for part in order['orden']:
            orden_queue.put(part)

    Asada = Taquero()
    
    p = multiprocessing.Process(target=Asada.Do_Tacos, args=(orden_queue, ))
    p.start()
    p.join()
    
    
if __name__ == '__main__':
    main()
