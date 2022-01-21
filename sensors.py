#import libraries
import time
import smbus
import time
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08


def read_data():
	bus = smbus.SMBus(1)
	bus.write_i2c_block_data(0x44, 0x2C, [0x06])

	time.sleep(0.5)

	data = bus.read_i2c_block_data(0x44, 0x00, 6)
	# Convert the data
	temp = data[0] * 256 + data[1]
	#cTemp = -45 + (175 * temp / 65535.0)
	fTemp = -49 + (315 * temp / 65535.0)
	humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

	ADC = ADS263.ADS1263()
	if (ADC.ADS1263if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1)):
		exit()
	ADC.ADS1263_SetMode(0)
	
	ADC_Value = ADC.ADS1263_GetAll()    # get ADC1 value
	if(ADC_Value[0]>>31 ==1):
		print("ADC1 IN%d = -%lf" %(0, (REF*2 - ADC_Value[0] * REF / 0x80000000)))
	else:
		print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
	print("\33[11A")
	adc = (REF*2 - ADC_Value[i] * REF / 0x80000000);

	# Output data to screen
	print ("Temperature in Celsius is : %.2f C" %cTemp)
	print ("Temperature in Fahrenheit is : %.2f F" %fTemp)
	print ("Relative Humidity is : %.2f %%RH" %humidity)
	time.sleep(1)

	return fTemp, humidity, adc
