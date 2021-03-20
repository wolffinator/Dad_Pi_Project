import math
import time
import busio
import adafruit_adxl34x

NUM_BITS = 8
MAX_MAGNITUDE = 2.0  # Should be the max value represented by a fixed point number with NUM_DECIMAL_PLACES.


def main():
    import board  # Weird import location due to startup error on coding computer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    last_accel_magnitude = 0
    while True:
        x, y, z = accelerometer.acceleration
        accel_magnitude = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        # TODO: Maybe add compensation for delta time
        jerk = accel_magnitude - last_accel_magnitude
        bin_array = floating_point_to_fixed_point_bin_array(jerk)

        last_accel_magnitude = accel_magnitude


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

if __name__ == "__main__":
    # execute only if run as a script
    main()
