# **README.txt**

## **Descripción**

Este script está diseñado para asignar direcciones IP estáticas a dispositivos de una red (Desktop, Server, Wireless) a través de un servidor DHCP basado en el archivo de configuración `dhcpd.conf`. El script lee un archivo de entrada con una lista de dispositivos y MACs, y luego asigna direcciones IP en rangos específicos, verificando que no haya conflictos con las IPs ya asignadas en el archivo de configuración DHCP existente.

Además, realiza copias de seguridad de los archivos de configuración antes de actualizarlos, y reinicia el servicio DHCP para aplicar los cambios.

## **Requisitos**

- **Python 3.x**: Asegúrate de tener instalado Python 3.x.
- **Dependencias**: El script usa las librerías estándar de Python:
  - `sys`
  - `datetime`
  - `os`

- **Acceso sudo**: El script requiere permisos de superusuario para interactuar con el servicio `isc-dhcp-server` (para detener, iniciar y verificar el estado del servicio).

## **Archivos requeridos**

- `dhcpd.conf`: Archivo de configuración actual del servidor DHCP.
- `plantilladhcpconf.txt`: Plantilla de configuración DHCP.
- `securitydhcpdconf.txt`: Copia de seguridad del archivo `dhcpd.conf` antes de realizar cambios.
- Archivos de grupos:
  - `grupodesktop.txt`
  - `gruposerver.txt`
  - `grupowireless.txt`
  - Copias de seguridad para cada grupo: `scgrupodesktop.txt`, `scgruposerver.txt`, `scgrupowireless.txt`.
  
## **Archivos de entrada**

El script requiere un archivo de entrada con la lista de dispositivos, con la siguiente estructura en cada línea:
hostname;mac_address;device_type


- `hostname`: Nombre del dispositivo.
- `mac_address`: Dirección MAC del dispositivo.
- `device_type`: Tipo de dispositivo: `Desktop`, `Server` o `Wireless`.

Este archivo debe pasarse como argumento cuando se ejecuta el script.

Ejemplo de archivo de entrada (`ips.txt`):
PC1;00:1A:2B:3C:4D:5E;Desktop Server1;00:1A:2B:3C:4D:5F;Server 
WiFiDevice1;00:1A:2B:3C:4D:60;Wireless


## **Uso**

1. **Ejecuta el script desde la terminal** pasando el archivo con la lista de dispositivos como argumento:
python script.py ips.txt


- **ips.txt**: Archivo que contiene la lista de dispositivos a asignar direcciones IP.

2. El script asignará direcciones IP estáticas a los dispositivos listados y actualizará los grupos `Desktop`, `Server` y `Wireless` en el archivo `dhcpd.conf`.

3. El script hará una copia de seguridad del archivo `dhcpd.conf` y los archivos de grupo antes de realizar cualquier cambio.

4. Después de actualizar el archivo de configuración, el servicio DHCP se detendrá y se reiniciará automáticamente.

5. El script realizará un `ping` a todas las IPs asignadas para verificar si están activas.

## **Comandos usados en el script**

- `sudo systemctl stop isc-dhcp-server`: Detiene el servicio `isc-dhcp-server`.
- `sudo systemctl start isc-dhcp-server`: Inicia el servicio `isc-dhcp-server`.
- `sudo systemctl status isc-dhcp-server`: Verifica el estado del servicio `isc-dhcp-server`.

## **Ejemplo de ejecución**


$ python script.py ips.txt has iniciado el script en fecha = 2024-11-06 10:00:00 se han añadido 3 ips fijas al servidor has finalizado de ejecutar el script en fecha = 2024-11-06 10:05:00


## **Posibles errores**

- Si no se proporciona el archivo de entrada como argumento, el script mostrará el siguiente error:

ERROR, TIENE QUE INTRODUCIR 2 ARGUMENTOS


- Si hay un problema con el servicio DHCP (por ejemplo, permisos insuficientes), es posible que se requiera ejecutar el script como superusuario.

## **Consideraciones**

- Asegúrate de tener suficiente espacio en los rangos de IPs configurados (`192.169.x.x` para `Desktop`, `192.168.x.x` para `Server`, y `192.170.x.x` para `Wireless`).
- El script intenta manejar conflictos de direcciones IP verificando que las direcciones ya asignadas no se dupliquen.
- Los nombres de los dispositivos se procesan para eliminar caracteres especiales que puedan causar problemas con el servidor DHCP.

## **Licencia**

Este script es de uso libre y se distribuye bajo MIT. Modifícalo y úsalo según tus necesidades.
