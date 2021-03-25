import math
import time
import RPi.GPIO as GPIO
import busio
import adafruit_adxl34x

NUM_BITS = 8
MAX_MAGNITUDE = 2.0  # Maximum number representable and starting position for creating output.
# The numeric representation for the most significant bit would be MAX_MAGNITUDE/2,
# The next most significant bit would be MAX_MAGNITUDE/4,
# The next would be MAX_MAGNITUDE/8 and so on.

BIT1 = 11
BIT2 = 13
BIT3 = 15
BIT4 = 29
BIT5 = 31
BIT6 = 33
BIT7 = 35
BIT8 = 37

PIN_NUMBERS = [BIT1, BIT2, BIT3, BIT4, BIT5, BIT6, BIT7, BIT8]

ACK_IN = 36
SEND_READY = 38
OFFPIN_IN = 40


def main():
    import board  # Weird import location due to startup error on coding computer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    last_accel_magnitude = 0
    print("Outputting accelerometer data...")

    while True:
        start_time_ns = time.time_ns()
        for i in range(10000):
            x, y, z = accelerometer.acceleration
            accel_magnitude = math.sqrt(x ** 2 + y ** 2 + z ** 2)
            # TODO: Maybe add compensation for delta time
            jerk = abs(accel_magnitude - last_accel_magnitude)
            bin_array = floating_point_to_fixed_point_bin_array(jerk)
            output_gpio_data(bin_array)
            last_accel_magnitude = accel_magnitude
        end_time_ns = time.time_ns()
        loop_time = (start_time_ns - end_time_ns) / 10000
        print("The average time to output is " + str(loop_time) + " nanoseconds")


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


def setup_gpio():
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # We are accessing GPIOs according to their physical board location
    # Setup output GPIO pins
    GPIO.setup(BIT1, GPIO.OUT)
    GPIO.setup(BIT2, GPIO.OUT)
    GPIO.setup(BIT3, GPIO.OUT)
    GPIO.setup(BIT4, GPIO.OUT)
    GPIO.setup(BIT5, GPIO.OUT)
    GPIO.setup(BIT6, GPIO.OUT)
    GPIO.setup(BIT7, GPIO.OUT)
    GPIO.setup(BIT8, GPIO.OUT)
    GPIO.setup(SEND_READY, GPIO.OUT)

    # Set all GPIO pins low to start
    GPIO.output(BIT1, GPIO.LOW)
    GPIO.output(BIT2, GPIO.LOW)
    GPIO.output(BIT3, GPIO.LOW)
    GPIO.output(BIT4, GPIO.LOW)
    GPIO.output(BIT5, GPIO.LOW)
    GPIO.output(BIT6, GPIO.LOW)
    GPIO.output(BIT7, GPIO.LOW)
    GPIO.output(BIT8, GPIO.LOW)
    GPIO.output(SEND_READY, GPIO.LOW)

    # Setup input GPIO pins
    GPIO.setup(ACK_IN, GPIO.IN)
    GPIO.setup(OFFPIN_IN, GPIO.IN)


def gpio_pinnout_check():
    setup_gpio()
    print("The pins should light up in sequential order. (LSB to MSB)")
    print("The SEND_READY pin will stay high.")
    print("Press ctrl-C to continue")
    GPIO.output(SEND_READY, GPIO.HIGH)
    try:
        while True:
            for pin_number in PIN_NUMBERS:
                GPIO.output(pin_number, GPIO.HIGH)
                time.sleep(1.0)  # Wait one second before setting high the next output
                GPIO.output(pin_number, GPIO.LOW)
    finally:
        cleanup_pins()


def cleanup_pins():
    GPIO.output(BIT1, GPIO.LOW)
    GPIO.output(BIT2, GPIO.LOW)
    GPIO.output(BIT3, GPIO.LOW)
    GPIO.output(BIT4, GPIO.LOW)
    GPIO.output(BIT5, GPIO.LOW)
    GPIO.output(BIT6, GPIO.LOW)
    GPIO.output(BIT7, GPIO.LOW)
    GPIO.output(BIT8, GPIO.LOW)
    GPIO.output(SEND_READY, GPIO.LOW)
    GPIO.cleanup()


def output_gpio_data(bin_array):
    """
    This function assumes bin_array is NUM_BITS long.
    :param bin_array: A NUM_BITS long array of bits
    :return:
    """
    for i in range(NUM_BITS):
        GPIO.output(PIN_NUMBERS[i], bin_array[i])


if __name__ == "__main__":
    # execute only if run as a script
    main()
