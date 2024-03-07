from binance.client import Client 
from telegram import Bot 
import asyncio  

TOKEN = 'tu_token' 
bot = Bot(token=TOKEN) 
chat_id = '@movement_alerts_binance'  
async def enviar_mensaje_a_telegram(mensaje):     
    if mensaje:        
        await bot.send_message(chat_id=chat_id, text=mensaje)     
else:         print("Se intentó enviar un mensaje vacío.")  

variacion = 5  # Variacion en los ultimos 30 minutos en porcentaje 
variacion_100 = 7  # Variacion en los ultimos 30 minutos en porcentaje si tiene menos de 100k de volumen 
variacionfast = 2  # Variacion en los ultimos 2 minutos en porcentaje  

client = Client('','', tld='com')  

async def buscarticks():     
    ticks = []     
    lista_ticks = client.futures_symbol_ticker() # traer todas las monedas de futuros de binace     
    print('Numero de monedas encontradas #' + str(len(lista_ticks)))      
        for tick in lista_ticks:         
            if tick['symbol'][-4:] != 'USDT': # seleccionar todas las monedas en el par USDT             
                continue         
                ticks.append(tick['symbol'])      
                print('Numero de monedas encontradas en el par USDT: #' + str(len(ticks)))      
                return ticks  
async def get_klines(tick):     
    klines = client.futures_klines(symbol=tick, interval=Client.KLINE_INTERVAL_1MINUTE, limit=30)     
    return klines  
async def infoticks(tick):     
    info = client.futures_ticker(symbol=tick)     
    return info  async def human_format(volumen):     
        magnitude = 0     
        while abs(volumen) >= 1000:         
            magnitude += 1         
            volumen /= 1000.0     
        return '%.2f%s' % (volumen, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])  
async def porcentaje_klines(tick, klines, knumber):     
    inicial = float(klines[0][4])     
    final = float(klines[knumber][4])      
# LONG     
if inicial > final:         
    result = round(((inicial - final) / inicial) * 100, 2)         
    if result >= variacion:             
        info = await infoticks(tick)             
        volumen = float(info['quoteVolume'])             
        formatted_volume = await human_format(volumen)  # Aquí aplicas el await para obtener el volumen formateado             
        if volumen > 100000000 or result >= variacion_100:                 
            mensaje = (     
                       f'LONG: {tick}\n'     
                       f'Variacion: {result}%\n'     
                       f'Volumen: {formatted_volume}\n'     
                       f'Precio max: {info["highPrice"]}\n'     
                       f'Precio min: {info["lowPrice"]}\n' 
                       ) 
                       await enviar_mensaje_a_telegram(mensaje)
    
# SHORT     
if final > inicial:         
    result = round(((final - inicial) / inicial) * 100, 2)         
    if result >= variacion:             
        info = await infoticks(tick)             
        volumen = float(info['quoteVolume'])             
        formatted_volume = await human_format(volumen)  # Aquí aplicas el await para obtener el volumen formateado             
        if volumen > 100000000 or result >= variacion_100:                 
            mensaje = (     
                       f'SHORT: {tick}\n'     
                       f'Variacion: {result}%\n'     
                       f'Volumen: {formatted_volume}\n'     
                       f'Precio max: {info["highPrice"]}\n'     
                       f'Precio min: {info["lowPrice"]}\n' 
                       ) 
                       await enviar_mensaje_a_telegram(mensaje)  
# FAST     
if knumber >= 3:         
     inicial = float(klines[knumber-2][4])         
     final = float(klines[knumber][4])         
     if inicial < final:             
         result = round(((final - inicial) / inicial) * 100, 2)             
         if result >= variacionfast:                 
             info = await infoticks(tick)                 
             volumen = float(info['quoteVolume'])                 
             formatted_volume = await human_format(volumen)  # Aquí aplicas el await para obtener el volumen formateado                                
             mensaje = (     
                       f'FAST SHORT!: {tick}\n'     
                       f'Variacion: {result}%\n'     
                       f'Volumen: {formatted_volume}\n'     
                       f'Precio max: {info["highPrice"]}\n'     
                       f'Precio min: {info["lowPrice"]}\n' 
                       ) 
                       await enviar_mensaje_a_telegram(mensaje)
async def main():         
     while True:             
         ticks = await buscarticks()             
         print('Escaneando monedas...')              
             for tick in ticks:                 
                 klines = await get_klines(tick)  # Asegúrate de que get_klines sea compatible con async si hace llamadas a la red                 
                 knumber = len(klines)                 
                 if knumber > 0:                     
                      knumber = knumber - 1                     
                      await porcentaje_klines(tick, klines, knumber)  # Si porcentaje_klines llama a enviar_mensaje_a_telegram, también debe ser async             
                      print('Esperando 30 segundos...')             
                      await asyncio.sleep(30)  # Usa asyncio.sleep para esperas asíncronas  
if __name__ == '__main__':         
    asyncio.run(main())
