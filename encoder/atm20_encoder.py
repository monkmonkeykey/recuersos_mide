import spidev
from gpiozero import DigitalOutputDevice
from time import sleep

class AMT20Encoder:
    def __init__(self, cs_pin=18, spi_bus=0, spi_device=0, max_speed_hz=500000):
        self.cs = DigitalOutputDevice(cs_pin, active_high=False, initial_value=True)
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0
        self.current_position = 0
        self.timeout_limit = 100

        # Definición de comandos SPI
        self.NOP = 0x00
        self.RD_POS = 0x10

    def spi_write(self, send_byte):
        self.cs.on()  # Activa CS
        data = self.spi.xfer2([send_byte])
        self.cs.off()  # Desactiva CS
        sleep(0.00001)  # 10 microsegundos de retardo
        return data[0]

    def update_position(self):
        timeout_counter = 0
        data = self.spi_write(self.RD_POS)

        while data != self.RD_POS and timeout_counter < self.timeout_limit:
            data = self.spi_write(self.NOP)
            timeout_counter += 1

        if timeout_counter < self.timeout_limit:
            self.current_position = (self.spi_write(self.NOP) & 0x0F) << 8
            self.current_position |= self.spi_write(self.NOP)
            return self.current_position
        else:
            print("Error obtaining position.")
            print("Reset the program to restart.")
            return None

    def get_current_position(self):
        return self.current_position
