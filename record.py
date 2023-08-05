# Copyright 2023 Timothy Lowther. All Rights Reserved.

import machine, onewire, ds18x20, time
 
# Setup
ds_pin = machine.Pin(22)
 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
 
roms = ds_sensor.scan()
 
print('Found DS devices: ', roms)

# Settings
time_between_readings_s = 30
time_to_record_for_s = 60 * 60 # 60 Mins
auto_stop = True

# Timing
start_time = time.time()
print("Starting At " + str(start_time))

# Data Recording
data = {}

# Loop
record = True
while record:
    time_elapsed = time.time() - start_time
        
    # Check If Should End
    if time_elapsed > time_to_record_for_s:
        record = False
        break

    ds_sensor.convert_temp()
 
    sensor_read_time_ms = 750
    time.sleep_ms(sensor_read_time_ms)

    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        print("Temp after " + str(time_elapsed) + " seconds is " + str(temp))

        # Push Data To Dictionary
        data[time_elapsed] = temp
        
    sleep_time_after_reading = (time_between_readings_s * 1000) - sensor_read_time_ms
    time.sleep_ms(sleep_time_after_reading)


print(data)


