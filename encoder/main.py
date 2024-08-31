import time

def main():
    # Instancia el encoder
    encoder = AMT20Encoder(cs_pin=18)  # Asegúrate de ajustar el pin CS si es necesario

    try:
        while True:
            # Actualiza la posición y obtén el valor actual
            position = encoder.update_position()

            if position is not None:
                print(f"Current position: {position}")

            # Aquí también puedes acceder directamente al atributo `current_position`
            #print(f"Accessed directly: {encoder.get_current_position()}")

            # Espera 250 ms antes de la siguiente lectura
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()