import os
import csv
import tkinter as tk
from datetime import datetime
from avionicsClasses import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename

root = tk.Tk()

def select_folder():

    root.withdraw()

    folder_path = filedialog.askdirectory()

    return folder_path

def select_save_location():

    root.withdraw()

    save_path = asksaveasfilename(defaultextension='.csv',
                                  initialfile='output.csv',
                                  filetypes=[('CSV Files', '*.csv')])

    return save_path

def count_files(folder_path, extension=None):

    file_list = os.listdir(folder_path)

    if extension:

        file_list = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file)) and file.endswith('.' + extension)]

    else:

        file_list = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file)) and not os.path.splitext(file)[1]]

    return len(file_list)

def write_header_to_csv(file_path):

    column_names = [["Date & Time",

                     "Latitude (degrees)",
                     "Longitude (degrees)",
                     "Altitude-GPS (m)",
                     "Speed (m/s)",
                     "Satellites Connected",
                     "Dilution of Precision",

                     "Altitude-Altimeter (m)",
                     "Temperature (C)",
                     "Pressure (kPa)",
                     "Humidity (%)",
                     "Gas (ohms)",

                     "Acceleration-X (m/s^2)",
                     "Acceleration-Y (m/s^2)",
                     "Acceleration-Z (m/s^2)",

                     "Gyroscopic Velocity-X (m/s)",
                     "Gyroscopic Velocity-Y (m/s)",
                     "Gyroscopic Velocity-Z (m/s)",

                     "Magnetic Field Strength-X (uT)",
                     "Magnetic Field Strength-Y (uT)",
                     "Magnetic Field Strength-Z (uT)",

                     "System Voltage Draw (V)",
                     "System Current Draw (A)",
                     "System Power Draw (W)",

                     "Solar Panel One Voltage Draw (V)",
                     "Solar Panel One Current Draw (A)",
                     "Solar Panel One Power Draw (W)",

                     "Solar Panel One Voltage Draw (V)",
                     "Solar Panel One Current Draw (A)",
                     "Solar Panel One Power Draw (W)",

                     "Solar Panel Three Voltage Draw (V)",
                     "Solar Panel Three Current Draw (A)",
                     "Solar Panel Three Power Draw (W)",

                     "Battery Voltage (V)",
                     "Battery Percentage (%)",

                     "Analog Input A0 (V)",
                     "Analog Input A1 (V)",
                     "Analog Input A2 (V)",
                     "Analog Input A3 (V)",
                     "Analog Input A4 (V)",
                     "Analog Input A5 (V)",
                     "Analog Input A6 (V)"]]

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerows(column_names)

def write_data_to_csv(file_path, converted_data):

    csv_data = [[str(converted_data.TIME),

                 str(converted_data.GPS.Latitude),
                 str(converted_data.GPS.Longitude),
                 str(converted_data.GPS.Altitude),
                 str(converted_data.GPS.Speed),
                 str(converted_data.GPS.Satellites),
                 str(converted_data.GPS.DOP),

                 str(converted_data.ALTIMETER.Altitude),
                 str(converted_data.ALTIMETER.Temperature),
                 str(converted_data.ALTIMETER.Pressure),
                 str(converted_data.ALTIMETER.Humidity),
                 str(converted_data.ALTIMETER.Gas),

                 str(converted_data.ACCELEROMETER.X),
                 str(converted_data.ACCELEROMETER.Y),
                 str(converted_data.ACCELEROMETER.Z),

                 str(converted_data.GYROSCOPE.X),
                 str(converted_data.GYROSCOPE.Y),
                 str(converted_data.GYROSCOPE.Z),

                 str(converted_data.MAGNETOMETER.X),
                 str(converted_data.MAGNETOMETER.Y),
                 str(converted_data.MAGNETOMETER.Z),


                 str(converted_data.POWERDRAW.Voltage),
                 str(converted_data.POWERDRAW.Current),
                 str(converted_data.POWERDRAW.Wattage),

                 str(converted_data.SOLARPANEL.One.Voltage),
                 str(converted_data.SOLARPANEL.One.Current),
                 str(converted_data.SOLARPANEL.One.Wattage),

                 str(converted_data.SOLARPANEL.Two.Voltage),
                 str(converted_data.SOLARPANEL.Two.Current),
                 str(converted_data.SOLARPANEL.Two.Wattage),

                 str(converted_data.SOLARPANEL.Three.Voltage),
                 str(converted_data.SOLARPANEL.Three.Current),
                 str(converted_data.SOLARPANEL.Three.Wattage),

                 str(converted_data.BATTERY.Voltage),
                 str(converted_data.BATTERY.Percentage),

                 str(converted_data.ANALOG.A0),
                 str(converted_data.ANALOG.A1),
                 str(converted_data.ANALOG.A2),
                 str(converted_data.ANALOG.A3),
                 str(converted_data.ANALOG.A3),
                 str(converted_data.ANALOG.A5),
                 str(converted_data.ANALOG.A6)]]

    with open(file_path, 'a', newline='') as csv_file:

        writer = csv.writer(csv_file)
        writer.writerows(csv_data)


def decodeData(packet):
    
    data = AVIONICSDATA(None, None, None, None, None, None, None, None, None, None)
    
    # Date & Time
    if (int.from_bytes(packet[0:2], "big", signed=True)) != 0:
    
        data.TIME = datetime(int.from_bytes(packet[0:2], "big", signed=True),
                             int.from_bytes(packet[2:3], "big", signed=True),
                             int.from_bytes(packet[3:4], "big", signed=True),
                             int.from_bytes(packet[4:5], "big", signed=True),
                             int.from_bytes(packet[5:6], "big", signed=True),
                             int.from_bytes(packet[6:7], "big", signed=True))
    
    else:
    
        data.TIME = int.from_bytes(packet[0:7], "big", signed=True)
    
    # GPS
    data.GPS = GPS((int.from_bytes(packet[7:11], "big", signed=True))/10000000,
                   (int.from_bytes(packet[11:15], "big", signed=True))/10000000,
                   (int.from_bytes(packet[15:19], "big", signed=True))/100,
                   (int.from_bytes(packet[19:22], "big", signed=True))/100,
                   (int.from_bytes(packet[22:23], "big", signed=True)),
                   (int.from_bytes(packet[23:25], "big", signed=True))/100)
    
    # Altimeter
    data.ALTIMETER = ALTIMETER((int.from_bytes(packet[25:29], "big", signed=True))/100,
                               (int.from_bytes(packet[29:31], "big", signed=True))/100,
                               (int.from_bytes(packet[31:34], "big", signed=True))/100,
                               (int.from_bytes(packet[34:36], "big", signed=True))/100,
                               (int.from_bytes(packet[36:38], "big", signed=True))/100)
    
    # Accelerometer
    data.ACCELEROMETER = ACCELEROMETER((int.from_bytes(packet[38:40], "big", signed=True))/100,
                                       (int.from_bytes(packet[40:42], "big", signed=True))/100,
                                       (int.from_bytes(packet[42:44], "big", signed=True))/100)
    
    # Gyroscope
    data.GYROSCOPE = GYROSCOPE((int.from_bytes(packet[44:46], "big", signed=True))/100,
                               (int.from_bytes(packet[46:48], "big", signed=True))/100,
                               (int.from_bytes(packet[48:50], "big", signed=True))/100)
    
    # Magnetometer
    data.MAGNETOMETER = MAGNETOMETER((int.from_bytes(packet[50:52], "big", signed=True)) / 100,
                                     (int.from_bytes(packet[52:54], "big", signed=True)) / 100,
                                     (int.from_bytes(packet[54:56], "big", signed=True)) / 100)
    
    # Power Draw
    data.POWERDRAW = POWER((int.from_bytes(packet[56:58], "big", signed=True))/1000,
                           (int.from_bytes(packet[58:60], "big", signed=True))/1000,
                           (int.from_bytes(packet[60:62], "big", signed=True))/1000)
    
    # Solar Panel
    data.SOLARPANEL = SOLARPANEL(POWER((int.from_bytes(packet[62:64], "big", signed=True))/1000,
                                       (int.from_bytes(packet[64:66], "big", signed=True))/1000,
                                       (int.from_bytes(packet[66:68], "big", signed=True))/1000),
                                 POWER((int.from_bytes(packet[68:70], "big", signed=True))/1000,
                                       (int.from_bytes(packet[70:72], "big", signed=True))/1000,
                                       (int.from_bytes(packet[72:74], "big", signed=True))/1000),
                                 POWER((int.from_bytes(packet[74:76], "big", signed=True))/1000,
                                       (int.from_bytes(packet[76:78], "big", signed=True))/1000,
                                       (int.from_bytes(packet[78:80], "big", signed=True))/1000))
    
    #  Battery
    data.BATTERY = BATTERY(((int.from_bytes(packet[80:82], "big", signed=True))/100),
                           ((int.from_bytes(packet[82:84], "big", signed=True))/100))
    
    #  Analog
    data.ANALOG = ANALOG(((int.from_bytes(packet[84:86], "big", signed=True))/100),
                         ((int.from_bytes(packet[86:88], "big", signed=True))/100),
                         ((int.from_bytes(packet[88:90], "big", signed=True))/100),
                         ((int.from_bytes(packet[90:92], "big", signed=True))/100),
                         ((int.from_bytes(packet[92:94], "big", signed=True))/100),
                         ((int.from_bytes(packet[94:96], "big", signed=True))/100),
                         ((int.from_bytes(packet[96:98], "big", signed=True))/100))

    return data

searchPath = select_folder()
savePath = select_save_location()

write_header_to_csv(savePath)

for i in range(count_files(searchPath)):

    try:

        with open(os.path.join(searchPath, str(i)), 'rb') as single_file:

            raw_data = single_file.read()
            compiled_data = decodeData(raw_data)

            write_data_to_csv(savePath, compiled_data)

            print("\n" + "="*150 + "\n" + str(compiled_data) + "\n" + "="*150 + "\n")

    except:

        pass
