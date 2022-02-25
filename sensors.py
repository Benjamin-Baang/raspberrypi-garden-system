#import libraries
import time
import smbus
import time
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08
V_MAX = 9.6
V_MIN = 6.9

def get_temperature_and_humidity():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])

    time.sleep(0.5)

    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    # Convert the data
    temp = data[0] * 256 + data[1]
    #cTemp = -45 + (175 * temp / 65535.0)
   # fTemp = -49 + (315 * temp / 65535.0)
    cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    fTemp = cTemp * 1.8 + 32
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0 
    return fTemp, humidity  


def get_soil_moisture():
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)
    
    ADC_Value = ADC.ADS1263_GetChannelValue(0)    # get ADC1 value
    # if(ADC_Value>>31 ==1):
    #     print("ADC1 IN%d = -%lf" %(0, (REF*2 - ADC_Value * REF / 0x80000000)))
    # else:
    #     print("ADC1 IN%d = %lf" %(1, (ADC_Value * REF / 0x7fffffff)))   # 32bit
    # print("\33[11A")
    adc = (REF*2 - ADC_Value * REF / 0x80000000);
    adc = ((((adc - V_MAX) / (V_MAX - V_MIN)) + 1) * 10) if (adc >= V_MIN) else 0;
    return adc;


def read_data():
    temp, humidity = get_temperature_and_humidity()    
    moisture = get_soil_moisture()

    # Output data to screen
#    print ("Temperature in Celsius is : %.2f C" %cTemp)
    # print ("Temperature in Fahrenheit is : %.2f F" %temp)
    # print ("Relative Humidity is : %.2f %%RH" %humidity)
    # print ("Soil Moisture is: %.2f" %moisture)
    time.sleep(1)

    return round(temp,2), round(humidity,2), round(moisture,2)
