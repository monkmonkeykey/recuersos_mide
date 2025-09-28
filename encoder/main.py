import time
from atm20_encoder import AMT20Encoder

def main():
    # Define los tres CS en pines distintos
    encA = AMT20Encoder(cs_pin=18)  # Encoder A
    encB = AMT20Encoder(cs_pin=23)  # Encoder B
    encC = AMT20Encoder(cs_pin=24)  # Encoder C

    try:
        while True:
            posA = encA.update_position()
            posB = encB.update_position()
            posC = encC.update_position()

            if None not in (posA, posB, posC):
                print(f"A: {posA:4d}  B: {posB:4d}  C: {posC:4d}")
            else:
                # Si alguno falló, indícalo para depurar cableado/ruido/CS
                print(f"A: {posA}  B: {posB}  C: {posC}")

            # Ritmo de muestreo: ~50 ms por ciclo (20 Hz conjunto)
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Program stopped by user")

if __name__ == "__main__":
    main()
