import spidev
from gpiozero import DigitalOutputDevice
from time import sleep

class AMT20Encoder:
    _shared_spi = None  # Compartido entre instancias

    def __init__(self, cs_pin=18, spi_bus=0, spi_device=0, max_speed_hz=500000):
        self.cs = DigitalOutputDevice(cs_pin, active_high=False, initial_value=True)
        if AMT20Encoder._shared_spi is None:
            spi = spidev.SpiDev()
            spi.open(spi_bus, spi_device)
            spi.max_speed_hz = max_speed_hz
            spi.mode = 0
            AMT20Encoder._shared_spi = spi
        self.spi = AMT20Encoder._shared_spi

        self.current_position = 0
        self.timeout_limit = 100

        self.NOP = 0x00
        self.RD_POS = 0x10

    def _xfer1(self, byte):
        self.cs.on()                 # Activa CS (activo en bajo -> on() pone 0V)
        data = self.spi.xfer2([byte])
        self.cs.off()                # Desactiva CS
        sleep(0.00001)               # 10 μs entre transferencias
        return data[0]

    def update_position(self):
        timeout_counter = 0
        data = self._xfer1(self.RD_POS)

        # Espera eco de RD_POS
        while data != self.RD_POS and timeout_counter < self.timeout_limit:
            data = self._xfer1(self.NOP)
            timeout_counter += 1

        if timeout_counter < self.timeout_limit:
            msb = self._xfer1(self.NOP) & 0x0F
            lsb = self._xfer1(self.NOP)
            self.current_position = (msb << 8) | lsb
            return self.current_position
        else:
            print("Error obtaining position (timeout).")
            return None

    def get_current_position(self):
        return self.current_position
