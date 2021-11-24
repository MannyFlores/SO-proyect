from generator import Generator


def main():
    order_generator = Generator()

    # Generate 10 random orders
    for i in range(1, 11):
        order_generator.generate_order()


if __name__ == '__main__':
    main()
