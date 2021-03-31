import math
import time
try:
    import RPi.GPIO as GPIO
except:
    print("Could not find RPi.GPIO. Try installing the RPi module")
import busio
import adafruit_adxl34x

NUM_BITS = 8
MAX_MAGNITUDE = 2.0  # Maximum number representable and starting position for creating output.
# The numeric representation for the most significant bit would be MAX_MAGNITUDE/2,
# The next most significant bit would be MAX_MAGNITUDE/4,
# The next would be MAX_MAGNITUDE/8 and so on.

def main():
    import board  # Weird import location due to startup error on coding computer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    last_accel_magnitude = 0
    print("Outputting accelerometer data...")
    AccelerometerClass.setup_gpio()
    try:
        while True:
            start_time_ns = time.time()
            for i in range(10000):
                x, y, z = accelerometer.acceleration
                accel_magnitude = math.sqrt(x ** 2 + y ** 2 + z ** 2)
                # TODO: Maybe add compensation for delta time
                jerk = abs(accel_magnitude - last_accel_magnitude)
                bin_array = AccelerometerClass.floating_point_to_fixed_point_bin_array(jerk)
                AccelerometerClass.output_gpio_data(bin_array)
                last_accel_magnitude = accel_magnitude
            end_time_ns = time.time()
            loop_time = (start_time_ns - end_time_ns) / 10000
            print("The average time to output is " + str(loop_time) + " seconds")
    except:
        AccelerometerClass.cleanup_pins()

class AccelerometerClass:
    PINS_BOARD = [11, 13, 15, 29, 31, 33, 35, 37]
    PINS_BCM = [0, 2, 3, 21, 22, 23, 24]
    PIN_NUMBERS = [0, 2, 3, 21, 22, 23, 24]

    ACK_BOARD = 36
    ACK_BCM = 27
    ACK = ACK_BCM

    SEND_READY_BOARD = 38
    SEND_READY_BCM = 28
    SEND_READY = SEND_READY_BCM

    OFFPIN_IN_BOARD = 40
    OFFPIN_IN_BCM = 29
    OFFPIN_IN = OFFPIN_IN_BCM


    @staticmethod
    def floating_point_to_fixed_point_bin_array(float_in):
        """

        :param float_in: Any floating point number less than MAX_MAGNITUDE
        :return: Binary array representing a fixed point integer with NUM_DECIMAL_PLACES number of binary decimal places.
        """
        if float_in > MAX_MAGNITUDE:
            return [True, True, True, True, True, True, True, True]
        bin_array = [False, False, False, False, False, False, False, False]
        comparison_num = MAX_MAGNITUDE / 2
        running_float = float_in
        for i in range(0, NUM_BITS):
            if running_float >= comparison_num:
                bin_array[i] = True
                running_float -= comparison_num
            comparison_num /= 2
        return bin_array

    @staticmethod
    def gpio_pinnout_check():
        AccelerometerClass.setup_gpio()
        print("The pins should light up in sequential order. (LSB to MSB)")
        print("The SEND_READY pin will stay high.")
        print("Press ctrl-C to continue")
        GPIO.output(AccelerometerClass.SEND_READY, GPIO.HIGH)
        try:
            while True:
                for pin_number in AccelerometerClass.PIN_NUMBERS:
                    GPIO.output(pin_number, GPIO.HIGH)
                    time.sleep(1.0)  # Wait one second before setting high the next output
                    GPIO.output(pin_number, GPIO.LOW)
        finally:
            AccelerometerClass.cleanup_pins()

    @staticmethod
    def cleanup_pins():
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[0], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[1], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[2], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[3], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[4], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[5], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[6], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[7], GPIO.OUT)
        GPIO.setup(AccelerometerClass.SEND_READY, GPIO.OUT)
        GPIO.cleanup()

    @staticmethod
    def output_gpio_data(bin_array):
        """
        This function assumes bin_array is NUM_BITS long.
        :param bin_array: A NUM_BITS long array of bits
        :return:
        """
        for i in range(NUM_BITS):
            GPIO.output(AccelerometerClass.PIN_NUMBERS[i], bin_array[i])

    @staticmethod
    def setup_gpio():
        # GPIO.setwarnings(False)
        if GPIO.getmode() == GPIO.BCM:
            AccelerometerClass.PIN_NUMBERS = AccelerometerClass.PINS_BCM

            AccelerometerClass.ACK = AccelerometerClass.ACK_BCM
            AccelerometerClass.SEND_READY = AccelerometerClass.SEND_READY_BCM
            AccelerometerClass.OFFPIN_IN = AccelerometerClass.OFFPIN_IN_BCM
        elif GPIO.getmode() == GPIO.BOARD:
            AccelerometerClass.PIN_NUMBERS = AccelerometerClass.PINS_BOARD

            AccelerometerClass.ACK = AccelerometerClass.ACK_BOARD
            AccelerometerClass.SEND_READY = AccelerometerClass.SEND_READY_BOARD
            AccelerometerClass.OFFPIN_IN = AccelerometerClass.OFFPIN_IN_BOARD
        else:
            GPIO.setmode(GPIO.BOARD)
            AccelerometerClass.PIN_NUMBERS = AccelerometerClass.PINS_BOARD

            AccelerometerClass.ACK = AccelerometerClass.ACK_BOARD
            AccelerometerClass.SEND_READY = AccelerometerClass.SEND_READY_BOARD
            AccelerometerClass.OFFPIN_IN = AccelerometerClass.OFFPIN_IN_BOARD
        # Setup output GPIO pins
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[0], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[1], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[2], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[3], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[4], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[5], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[6], GPIO.OUT)
        GPIO.setup(AccelerometerClass.PIN_NUMBERS[7], GPIO.OUT)
        GPIO.setup(AccelerometerClass.SEND_READY, GPIO.OUT)

        # Set all GPIO pins low to start
        GPIO.output(AccelerometerClass.PIN_NUMBERS[0], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[1], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[2], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[3], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[4], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[5], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[6], GPIO.LOW)
        GPIO.output(AccelerometerClass.PIN_NUMBERS[7], GPIO.LOW)
        GPIO.output(AccelerometerClass.SEND_READY, GPIO.LOW)

        # Setup input GPIO pins
        GPIO.setup(AccelerometerClass.ACK, GPIO.IN)
        GPIO.setup(AccelerometerClass.OFFPIN_IN, GPIO.IN)


if __name__ == "__main__":
    # execute only if run as a script
    main()
