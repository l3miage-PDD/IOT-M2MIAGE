# Lecture de deux capteurs du shield IKS01A3 et affichage sur le port serie de l'USB USER
# "Casting" RF des mesures avec la radio BLE du STM32WB55 
# Materiel : 
#  - Une carte NUCLEO-WB55
#  - Un shield X-NUCLEO IKS01A3


from machine import I2C

from time import sleep_ms, time # Pour gérér les temporisations et l'horodatage
import ble_sensor # Pour implémenter le protocole GATT pour Blue-ST
import bluetooth # Classes "primitives du BLE" 
# (voir https://docs.micropython.org/en/latest/library/ubluetooth.html)



varef = 3.3
RESOLUTION = const(4096)

# Quantum de l'ADC
quantum = varef / (RESOLUTION -1)

# Initialisation de l'ADC sur la broche A0
adc_A0 = pyb.ADC(pyb.Pin( 'A0' ))

# Initialisations pour calcul de la moyenne
Nb_Mesures = 500
Inv_Nb_Mesures = 1 / Nb_Mesures


# Instance de la classe BLE
ble = bluetooth.BLE()
ble_device = ble_sensor.BLESensor(ble)

while True:
	somme_tension = 0
	moyenne_tension = 0
	
	# Calcul de la moyenne de la tension aux bornes du potentiomètre

	for i in range(Nb_Mesures): # On fait Nb_Mesures conversions de la tension d'entrée
		
		# Lit la conversion de l'ADC (un nombre entre 0 et 4095 proportionnel à la tension d'entrée)
		valeur_numerique = adc_A0.read()
		
		# On calcule à présent la tension (valeur analogique) 
		tension = valeur_numerique * quantum

		# On l'ajoute à la valeur calculée à l'itération précédente
		somme_tension = somme_tension + tension

		# Temporisation pendant 1 ms
		sleep_ms(1)
	
	# On divise par Nb_Mesures pour calculer la moyenne de la tension du potentiomètre
	moyenne_tension = somme_tension * Inv_Nb_Mesures 
	
	# Affichage de la tension moyenne sur le port série de l'USB USER
	print( "La valeur moyenne de la consommation est de : %.2f W" %moyenne_tension)

	# Preparation des donnees pour envoi en BLE.
	# Le protocole Blue-ST code les temperatures, pressions et humidites sous forme de nombres entiers.
	# Donc on multiplie les différentes mesures par 10 ou par 100 pour conserver des decimales avant
	# d'arrondir a  l'entier le plus proche.
	# Par exemple si temp = 18.45�C => on envoie ble_temp = 184. 
	ble_tens = int(moyenne_tension*10)
	timestamp = time()

	# Envoie des donn�es en BLE 
	ble_device.set_data_env(timestamp, ble_tens, True) 

	sleep_ms(5000)
