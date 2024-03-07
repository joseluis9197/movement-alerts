### Movement Alerts (Alertas de Movimiento)

Este script fue desarrollado para detectar movimientos del mercado de criptomonedas en futuros de binance, con este script usted podra tener en vivo y en directo una alerta cuando un crypto activo este teniendo un movimiento inusal tanto al alza o la baja.

**Como usar el script**
- Descargar python [Aqui](https://www.python.org/ "Aqui")
- Descargar y modificar el Archivo, lo puedes modificar con sublime text, o cualquier otro editor de codigo bajo lso parametros que tu quieras.
```python
variacion = 5  # Variacion en los ultimos 30 minutos en porcentaje
variacion_100 = 7  # Variacion en los ultimos 30 minutos en porcentaje si tiene menos de 100k de volumen
variacionfast = 2  # Variacion en los ultimos 2 minutos en porcentaje
```
- Antes de ejecutar el Script deberas instalar la libreria de Python de Binance `pip install python-binance`
- Una vez guardado el archivo debes ejecutarlo desde una terminal de windows o de tu sistema operativo que uses con el siguiente comando.
`python script.py`

#### Contact
- Twitter: [https://twitter.com/ElGafasTrading](https://twitter.com/ElGafasTrading "https://twitter.com/ElGafasTrading")
- Instagram: [https://www.instagram.com/elgafastrading/](https://www.instagram.com/elgafastrading/ "https://www.instagram.com/elgafastrading/")
- Youtube: [https://www.youtube.com/@ElGafasTrading](https://www.youtube.com/@ElGafasTrading "https://www.youtube.com/@ElGafasTrading")

**Configuración Inicial:**

Se importan las librerías necesarias (pip install python-telegram-bot) y se configuran las credenciales del bot de Telegram y los parámetros para filtrar las variaciones de precio en diferentes escenarios.
Conexión a Binance y Telegram: Se inicializan los clientes para las APIs de Binance y Telegram.

**Obtención de Datos de Binance:**

buscarticks: Obtiene todos los símbolos de futuros de Binance y filtra aquellos que terminen en 'USDT'.
get_klines: Obtiene las líneas de precio (klines) para un símbolo dado, en intervalos de 1 minuto, limitado a los últimos 30 minutos.
infoticks: Obtiene información de mercado para un símbolo dado.
human_format: Formatea números grandes a un formato más legible (K, M, G, etc.).

**Análisis y Alertas:**

porcentaje_klines: Calcula la variación porcentual en el precio entre el primer y el último minuto de las klines obtenidas. Dependiendo de la variación y del volumen, decide si envía una alerta de LONG, SHORT o FAST SHORT a través de Telegram.

enviar_mensaje_a_telegram: Función asíncrona para enviar mensajes al canal de Telegram configurado.

**Función Principal (main):**
Se ejecuta en un bucle infinito, buscando nuevos datos cada 30 segundos y analizando cada símbolo obtenido para determinar si se cumplen las condiciones para enviar alguna alerta.
