__author__ = 'xcbtrader'
# -*- coding: utf-8 -*-
# PROGRAMA PARA AUTOTRADER EN BITCOINS UTILIZANDO LAS APIs DE POLONIEX

import urllib
import requests
import json
import time

class Clase_btc:
	BTC_fecha = time.strftime('%d %b %y')
	BTC_hora = time.strftime('%H:%M:%S')
	BTC_last = 0.0
	BTC_high24hr = 0.0
	BTC_percentChange = 0.0
	BTC_low24hr = 0.0
	BTC_highestBid = 0.0
	BTC_lowestAsk = 0.0
	BTC_baseVolume = 0.0
	
	def actualizar_valores(self):
		err = True
		while err:
			try:
				request = 'https://poloniex.com/public?command=returnTicker'
				response = requests.get(request)
				content = response.json()
				err = False
				
				self.BTC_fecha = time.strftime('%d %b %y')
				self.BTC_hora = time.strftime('%H:%M:%S')
				self.BTC_last = content ['USDT_BTC'] ['last']
				self.BTC_high24hr = content ['USDT_BTC'] ['high24hr']
				self.BTC_percentChange = content ['USDT_BTC'] ['percentChange']
				self.BTC_low24hr = content ['USDT_BTC'] ['low24hr']
				self.BTC_highestBid = content ['USDT_BTC'] ['highestBid']
				self.BTC_lowestAsk = content ['USDT_BTC'] ['lowestAsk']
				self.BTC_baseVolume = content ['USDT_BTC'] ['baseVolume']
			except KeyboardInterrupt:
				exit()
			except:
				print ('### ERROR DE CONEXION - ESPERANDO 10 SEGUNDOS ###')
				err = True
				time.sleep(10)
	def imprimir_valores(self):
		print ('######################################################')
		print ('  FECHA:      ' + self.BTC_fecha + ' -- ' + self.BTC_hora)
		print ('  LAST:       ' + self.BTC_last)
		print ('  HIGH24HR:   ' + self.BTC_high24hr)
		print ('  MOVIMIENTO: ' + self.BTC_percentChange)
		print ('  LOW24HR:    ' + self.BTC_low24hr)
		print ('  HIGHESTBID: ' + self.BTC_highestBid)
		print ('  LOWESTASK:  ' + self.BTC_lowestAsk)
		print ('  BASEVOLUME: ' + self.BTC_baseVolume)
		
def RSI(periodo):
	global datosBTC
	
	final = len(datosBTC)
	if periodo > final:
		print('### ERROR PERIODO RSI INCORRECTO ###')
		return 0
		
	inicio = final - periodo
	incMed = 0.0
	decMed = 0.0
	for d in range (inicio, final):
		incRSI = round((float(datosBTC[d].BTC_last) - float(datosBTC[d-1].BTC_last))/float(datosBTC[d-1].BTC_last),10)
		if incRSI != 0:
			if incRSI > 0:
				incMed = incMed + incRSI
			else:
				decMed = decMed + abs(incRSI)
	incMed = round(incMed/periodo,10)
	decMed = round(decMed/periodo,10)
	if decMed > 0:
		return float(100-(100/(1+(incMed/decMed))))
	else:
		return float(100-(100/(1+incMed)))

def calcular_MinMax(periodo):
	global datosBTC, vMinBTC, vMaxBTC
# CALCULA VALOR MAX Y VALOR MIN DE UN PERIODO. SI PONEMOS 0 COGE TODOS LOS DATOS
	if periodo == 0:
		vMinBTC = round(float(datosBTC[0].BTC_last),10)
		vMaxBTC = round(float(datosBTC[0].BTC_last),10)
		for d in range (1,len(datosBTC)):
			if datosBTC[d].BTC_last > vMaxBTC:
				vMaxBTC = datosBTC[d].BTC_last
			if datosBTC[d].BTC_last < vMinBTC:
				vMinBTC = datosBTC[d].BTC_last
	else:
		final = len(datosBTC)
		inicio = final - periodo
		if inicio < 0:
			print ('### ERROR - PERIODO INCORRECTO ###')
			return
		vMinBTC = round(float(datosBTC[inicio].BTC_last),10)
		vMaxBTC = round(float(datosBTC[inicio].BTC_last),10)
		for d in range (inicio,final):
			if datosBTC[d].BTC_last > vMaxBTC:
				vMaxBTC = datosBTC[d].BTC_last
			if datosBTC[d].BTC_last < vMinBTC:
				vMinBTC = datosBTC[d].BTC_last		
#PROGRAMA PRINCIPAL #################################################
global datosBTC, vMinBTC, vMaxBTC

datosBTC = []

n = 0
lapso = 30
perRSI = 120
vMinBTC = 0.0
vMaxBTC = 0.0

fEstadist = open('./EstPoloniexAPI.txt', 'a')
				
while True:
	btcAct = Clase_btc()
	btcAct.actualizar_valores()
	datosBTC.append(btcAct)
	btcAct.imprimir_valores()
	if n > perRSI:
		Vrsi = RSI(perRSI)
		fEstadist.write(str(btcAct.BTC_fecha) + ';' + str(btcAct.BTC_hora) + ';' + str(btcAct.BTC_last) + ';' + str(Vrsi) + ';' + str(vMinBTC) + ';' + str(vMaxBTC) + '\n')
		print ('  >>RSI' + str(perRSI) + ':     ' + str(Vrsi))
	else:
		print ('  >>RSI:    ####' )
	if n > perRSI:
		calcular_MinMax(perRSI)
		print ('  >>ValMin:   ' + str(vMinBTC))
		print ('  >>ValMax:   ' + str(vMaxBTC))
	else:
		print ('  >>ValMin: ####')
		print ('  >>ValMax: ####')		
	print ('######################################################')
	print ('ESPERANDO ' + str(lapso) + ' SEGUNDOS')
	n +=1
	time.sleep(lapso)

fEstadist.close()
