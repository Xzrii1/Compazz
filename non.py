import math
import smbus
import time
import datetime
import threading

# Initialize the I2C bus
bus = smbus.SMBus(1)

# Define the HMC5883L register addresses
HMC5883L_ADDRESS = 0x1E
HMC5883L_REGISTER_X_MSB = 0x03
HMC5883L_REGISTER_Y_MSB = 0x05
HMC5883L_REGISTER_Z_MSB = 0x07

# Define the magnetometer scale factor
SCALE_FACTOR = 0.92

# Define the wind speed sensor pin (assuming an analog input)
WIND_SPEED_PIN = 0

# Define the wave height sensor pin (assuming an analog input)
WAVE_HEIGHT_PIN = 1

# Define the air temperature sensor pin (assuming an analog input)
AIR_TEMP_PIN = 2

def read_magnetometer():
    # Read the magnetometer data
    x_ms = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_X_MSB)
    x_ls = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_X_MSB + 1)
    y_ms = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_Y_MSB)
    y_ls = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_Y_MSB + 1)
    z_ms = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_Z_MSB)
    z_ls = bus.read_byte_data(HMC5883L_ADDRESS, HMC5883L_REGISTER_Z_MSB + 1)

    # Convert the data to signed 16-bit integers
    x = (x_ms << 8) | x_ls
    y = (y_ms << 8) | y_ls
    z = (z_ms << 8) | z_ls

    # Apply the scale factor
    x *= SCALE_FACTOR
    y *= SCALE_FACTOR
    z *= SCALE_FACTOR

    return x, y, z

def calculate_heading(x, y):
    # Calculate the compass heading
    heading = math.atan2(y, x) * 180 / math.pi
    return heading

def read_wind_speed():
    # Read the wind speed sensor value (assuming an analog input)
    wind_speed_value = analog_read(WIND_SPEED_PIN)
    # Convert the value to wind speed (m/s)
    wind_speed = wind_speed_value * 3.33  # adjust this value based on your sensor's specifications
    return wind_speed

def read_wave_height():
    # Read the wave height sensor value (assuming an analog input)
    wave_height_value = analog_read(WAVE_HEIGHT_PIN)
    # Convert the value to wave height (m)
    wave_height = wave_height_value * 0.5  # adjust this value based on your sensor's specifications
    return wave_height

def read_air_temperature():
    # Read the air temperature sensor value (assuming an analog input)
    air_temp_value = analog_read(AIR_TEMP_PIN)
    # Convert the value to air temperature (°C)
    air_temp = air_temp_value * 0.1  # adjust this value based on your sensor's specifications
    return air_temp

def display_clock():
    # Get the current time in WIB
    current_time = datetime.datetime.now() + datetime.timedelta(hours=7)  # adjust for WIB
    return current_time.strftime("%H:%M:%S")

def update_display():
    while True:
        # Read the magnetometer data
        x, y, z = read_magnetometer()

        # Calculate the compass heading
        heading = calculate_heading(x, y)

        # Read the wind speed
        wind_speed = read_wind_speed()

        # Read the wave height
        wave_height = read_wave_height()

        # Read the air temperature
        air_temp = read_air_temperature()

        # Display the compass heading, wind speed, wave height, air temperature, and clock
        print("Compass Heading: {:.2f} degrees".format(heading))
        print("Wind Speed: {:.2f} m/s".format(wind_speed))
        print("Wave Height: {:.2f} m".format(wave_height))
        print("Air Temperature: {:.2f} °C".format(air_temp))
        print("Time: {}".format(display_clock()))

        # Wait for 1 second before taking the next reading
        time.sleep(1)

# Create a thread for updating the display
display_thread = threading.Thread(target=update_display)
display_thread.daemon = True
display_thread.start()

while True:
    # Keep the main thread running to prevent the program from exiting
    time.sleep(1)