import glob2
import os
import pandas as pd

def get_file_data(dir) -> list:
    '''
    This function takes the path to the directory where the folder containing the log files is present and
    processes the text file to separately rip the different values present and make a list of lists
    :param dir: String which gives the base of the path(directory)
    :return: List of lists where each individual list item contains data from one test log file
    '''

    list_of_folders = ['LI5-1834230M', 'LI5-1834871M', 'LI5-1843682M', 'LI5-1834411M', 'LI5-1843681M', 'LI5-1843685M']
    log_data_list = []

    for i in range(len(list_of_folders)):
        base = dir + '/' + list_of_folders[i] + '/' +'PASS' + '/'
        os.chdir(base)
        pattern = '2018*txt'

        for j in glob2.glob(pattern):
            path= os.path.join(base,j)
            log_file = open(path, 'r')

            file_data = log_file.readlines()

            if len(file_data) == 67:
                time = file_data[0][0:19]
                device_id = file_data[0][-13:-1]
                gps_module_status = file_data[11][0:10]
                use_time_gms = file_data[11][-14:-6]
                enable_status = file_data[25][:-1]
                enable_time = file_data[29][-11:-6]
                ttff = file_data[41][7:-4]
                snr1 = file_data[45][-3:-1]
                snr2 = file_data[47][-3:-1]
                snr3 = file_data[49][-3:-1]
                snr4 = file_data[51][-3:-1]
                snr5 = file_data[53][-3:-1]
                snr6 = file_data[55][-3:-1]
                snr7 = file_data[57][-3:-1]
                snr8 = file_data[59][-3:-1]
                gps_signal_status = file_data[63][16:20]
                signal_time = file_data[63][-13:-6]
                total_time = file_data[-1][-9:-1]

                item = [time,device_id,gps_module_status,use_time_gms,enable_status,enable_time,ttff,snr1,snr2,snr3,snr4,snr5,snr6,snr7,snr8,gps_signal_status,signal_time,total_time]

                log_data_list.append(item)

            elif len(file_data) == 69:
                time = file_data[0][0:19]
                device_id = file_data[0][-13:-1]
                gps_module_status = file_data[11][0:10]
                use_time_gms = file_data[11][-14:-6]
                enable_status = file_data[27][:-1]
                enable_time = file_data[31][-11:-6]
                ttff = file_data[43][7:-4]
                snr1 = file_data[47][-3:-1]
                snr2 = file_data[49][-3:-1]
                snr3 = file_data[51][-3:-1]
                snr4 = file_data[53][-3:-1]
                snr5 = file_data[55][-3:-1]
                snr6 = file_data[57][-3:-1]
                snr7 = file_data[59][-3:-1]
                snr8 = file_data[61][-3:-1]
                gps_signal_status = file_data[65][16:20]
                signal_time = file_data[65][-13:-6]
                total_time = file_data[-1][-9:-1]

                item = [time, device_id, gps_module_status, use_time_gms, enable_status, enable_time, ttff, snr1, snr2,
                        snr3, snr4, snr5, snr6, snr7, snr8, gps_signal_status, signal_time, total_time]

                log_data_list.append(item)

            elif len(file_data) == 61:
                time = file_data[0][0:19]
                device_id = file_data[0][-13:-1]
                gps_module_status = file_data[11][0:10]
                use_time_gms = file_data[11][-14:-6]
                enable_status = file_data[27][:-1]
                enable_time = file_data[31][-11:-6]
                ttff = file_data[43][7:-4]
                snr1 = file_data[47][-3:-1]
                snr2 = file_data[49][-3:-1]
                snr3 = file_data[51][-3:-1]
                snr4 = file_data[53][-3:-1]
                snr5 = '0'
                snr6 = '0'
                snr7 = '0'
                snr8 = '0'
                gps_signal_status = file_data[57][16:20]
                signal_time = file_data[57][-13:-6]
                total_time = file_data[-1][-9:-1]

                item = [time, device_id, gps_module_status, use_time_gms, enable_status, enable_time, ttff, snr1, snr2,
                        snr3, snr4, snr5, snr6, snr7, snr8, gps_signal_status, signal_time, total_time]

                log_data_list.append(item)

            else:
                time = file_data[0][0:19]
                device_id = file_data[0][-13:-1]
                gps_module_status = file_data[11][0:10]
                use_time_gms = file_data[11][-14:-6]
                enable_status = file_data[25][:-1]
                enable_time = file_data[29][-11:-6]
                ttff = file_data[41][7:-4]
                snr1 = file_data[45][-3:-1]
                snr2 = file_data[47][-3:-1]
                snr3 = file_data[49][-3:-1]
                snr4 = file_data[51][-3:-1]
                snr5 = '0'
                snr6 = '0'
                snr7 = '0'
                snr8 = '0'
                gps_signal_status = file_data[55][16:20]
                signal_time = file_data[55][-13:-6]
                total_time = file_data[-1][-9:-1]

                item = [time, device_id, gps_module_status, use_time_gms, enable_status, enable_time, ttff, snr1, snr2,
                        snr3, snr4, snr5, snr6, snr7, snr8, gps_signal_status, signal_time, total_time]

                log_data_list.append(item)

    return log_data_list


dir = '/Users/vpb/Desktop/Samsara/GPS Test Data'
log_data = get_file_data(dir)

#Converting the list of lists to a Dataframe
data_frame = pd.DataFrame(log_data, columns=["Time", "Device_id", "Gps_module_status", "Use_time_gms", "Enable_status", "Enable_time", "TTFF", "SNR1", "SNR2",
                        "SNR3", "SNR4", "SNR5", "SNR6", "SNR7", "SNR8", "Gps_signal_status", "Signal_time", "Total_time"])

#Exporting the Dataframe into csv file
data_frame.to_csv('/Users/vpb/Desktop/GPS_Data.csv',sep=',', header=True, index=True)

