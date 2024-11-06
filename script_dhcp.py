import sys, datetime, os
print('has iniciado el script en fecha = ' + str(datetime.datetime.now()))

archivo_ips = sys.argv[1]
dhcpconf = 'dhcpd.conf'
plantilla = 'plantilladhcpconf.txt'
security = 'securitydhcpdconf.txt'
grupodesktop = 'grupodesktop.txt'
scgrupodesktop = 'scgrupodesktop.txt'
gruposerver = 'gruposerver.txt'
scgruposerver = 'scgruposerver.txt'
grupowireless = 'grupowireless.txt'
scgrupowireless = 'scgrupowireless.txt'
segmentoservers = "192.168."
segmentotrabajo = "192.169."
segmentowireless = "192.170."
ipes = []
desktop = []
server = []
wireless = []
nombrehost = []
octeto3server = 0
octeto4server = 2
octeto3trabajo = 0
octeto4trabajo = 2
octeto3wireless = 0
octeto4wireless = 2
contador = 0
ide = 1

with open(archivo_ips, "r") as ips, open(dhcpconf, "r") as dhcp:
    contenidodhcp = dhcp.read() #guardo el contenido del fichero en una variable para su uso más adelante
    for linea in ips:
        device = linea.split(";") #ira leyendo el codigo linea a linea y cada vez que haya una nueva linea se almacenara un array en device, aplastando al de la anterior linea, usando como separador el ;
        while device[0] in contenidodhcp: #compruebo que el equipo no esta ya metido, y si lo esta, le añado un numero que lo distinga
            device[0] += str(ide)
            ide += 1
        if device[1] not in contenidodhcp: #compruevo que la mac no está ya en el fichero
            if device[2] == "Desktop\n" or device[2] == "Desktop": 
                device[2] = "Desktop" #como la función split saca los elementos que estan a final de linea y en mitad de fichero con \n hago esto para que no aparezca
                while segmentotrabajo + str(octeto3trabajo) + "." + str(octeto4trabajo) in contenidodhcp: #si la ip se encuenta dentro del fichero pasa a la siguiente ip y vuelve a comprobar
                    if octeto4trabajo < 255 and octeto3trabajo <= 149:
                        octeto4trabajo += 1
                    elif octeto4trabajo == 254:
                        octeto3trabajo += 1
                        octeto4trabajo = 1
                if segmentotrabajo + str(octeto3trabajo) + "." + str(octeto4trabajo) not in contenidodhcp: #una vez que la ip se sabe que no esta asignada ya, la ensambla en una unica variable, e introduce los datos del dispositivo y la ip que se le asociara en un array
                    ipdesktop  = segmentotrabajo + str(octeto3trabajo) + "." + str(octeto4trabajo)
                    desktop.append([device[0], device[1], device[2], ipdesktop])
                    contador += 1 #cuenta el número de registros
                    if octeto4trabajo < 255 and octeto3trabajo <= 149:
                        octeto4trabajo += 1
                    elif octeto4trabajo == 254:
                        octeto3trabajo += 1
                        octeto4trabajo = 1
                        
            elif device[2] == "Server\n" or device[2] == "Server":
                device[2] = "Server"
                while segmentoservers + str(octeto3server) + "." + str(octeto4server) in contenidodhcp:
                    if octeto4server < 255 and octeto4server <= 149:
                        octeto4server += 1
                    elif octeto4server == 254:
                        octeto3server += 1
                        octeto3server = 1
                if segmentoservers + str(octeto3server) + "." + str(octeto4server) not in contenidodhcp:
                    ipserver  = segmentoservers + str(octeto3server) + "." + str(octeto4server)
                    server.append([device[0], device[1], device[2], ipserver])
                    contador += 1
                    if octeto4server < 255 and octeto4server <= 149:
                        octeto4server += 1
                    elif octeto4server == 254:
                        octeto3server += 1
                        octeto3server = 1
                        
            elif device[2] == "Wireless\n" or device[2] == "Wireless":
                device[2] = "Wireless"
                while segmentowireless + str(octeto3wireless) + "." + str(octeto4wireless) in contenidodhcp:
                    if octeto4wireless < 255 and octeto4wireless <= 149:
                        octeto4wireless += 1
                    elif octeto4wireless == 254:
                        octeto3wireless += 1
                        octeto3wireless = 1
                if segmentowireless + str(octeto3wireless) + "." + str(octeto4wireless) not in contenidodhcp:
                    ipwireless  = segmentowireless + str(octeto3wireless) + "." + str(octeto4wireless)
                    wireless.append([device[0], device[1], device[2], ipwireless])
                    contador += 1
                    if octeto4wireless < 255 and octeto4wireless <= 149:
                        octeto4wireless += 1
                    elif octeto4wireless == 254:
                        octeto3wireless += 1
                        octeto3wireless = 1

ips.close()
dhcp.close()

#realizo copias de seguridad de los 3 grupos (unicamente si ) y del fichero de configuración dhcp por si acaso hubiera algún error en la lista de dispositivos poder dar marcha atras y ya ejecutar el script con la lista buena
if contador != 0:    
    with open (grupodesktop, "r") as gd, open (scgrupodesktop, "a") as scgd:
        contenidogd = gd.read()
        scgd.write(contenidogd)
    gd.close()
    scgd.close()

    with open (gruposerver, "r") as gs, open (scgruposerver, "a") as scgs:
        contenidogs = gs.read()
        scgs.write(contenidogd)
    gs.close()
    scgs.close()

    with open (grupowireless, "r") as gw, open (scgrupowireless, "a") as scgw:
        contenidogw = gw.read()
        scgw.write(contenidogw)
    gw.close()
    scgw.close()

    with open (dhcpconf, "r") as dhcp1:
        copiaseguridad = dhcp1.read()
    dhcp1.close()

    with open(security, "w") as seguridaddhcp:
        seguridaddhcp.write(copiaseguridad)
    seguridaddhcp.close()  

#actualizo los grupos con los nuevos dispositivos
with open (grupodesktop, "a") as gd, open (gruposerver, "a") as gs, open (grupowireless, "a") as gw:
    ide = 1
    for equipo in server:
        if equipo[0] in nombrehost: #compruebo que en el fichero de ips, si hay 2 dispositivo con igual nombre se diferencien
            equipo[0] += str(ide)
            ide += 1
        nombrehost.append(equipo[0])
        equipo[0] = equipo[0].replace(" ", "") #elimino del nombre cualquier caracter especial que pueda fastidiar el servidor dhcp
        equipo[0] = equipo[0].replace("/", "")
        equipo[0] = equipo[0].replace("\\", "")
        equipo[0] = equipo[0].replace("(", "")
        equipo[0] = equipo[0].replace(")", "")
        gs.write("\n\thost " + equipo[0] + "{\n" + "\t\thardware ethernet " + equipo[1] + ";\n" + "\t\tfixed-address " + equipo[3] + ";\n" + "\t}\n")
        ipes.append(equipo[3]) #añado las ips tambien en una unica variable para luego poder comprobar que esta activa o no
    for equipo in desktop:
        ide = 1
        if equipo[0] in nombrehost:
            equipo[0] += (ide)
            ide += 1
        nombrehost.append(equipo[0])
        equipo[0] = equipo[0].replace(" ", "")
        equipo[0] = equipo[0].replace("/", "")
        equipo[0] = equipo[0].replace("\\", "")
        equipo[0] = equipo[0].replace("(", "")
        equipo[0] = equipo[0].replace(")", "")
        gd.write("\n\thost " + equipo[0] + "{\n" + "\t\thardware ethernet " + equipo[1] + ";\n" + "\t\tfixed-address " + equipo[3] + ";\n" + "\t}\n")
        ipes.append(equipo[3])
        contador += 1
    for equipo in wireless:
        ide = 1
        if equipo[0] in nombrehost:
            equipo[0] += str(ide)
            ide += 1
        nombrehost.append(equipo[0])
        equipo[0] = equipo[0].replace(" ", "")
        equipo[0] = equipo[0].replace("/", "")
        equipo[0] = equipo[0].replace("\\", "")
        equipo[0] = equipo[0].replace("(", "")
        equipo[0] = equipo[0].replace(")", "")
        gw.write("\n\thost " + equipo[0] + "{\n" + "\t\thardware ethernet " + equipo[1] + ";\n" + "\t\tfixed-address " + equipo[3] + ";\n" + "\t}\n")
        ipes.append(equipo[3])
        contador += 1
gs.close()
gd.close()
gw.close()

#saco el contenido de los 3 grupos y los almaceno en variables
with open (grupowireless, "r") as gw:
    contenidogw = gw.read()
gw.close()
with open (gruposerver, "r") as gs:
    contenidogs = gs.read()
gs.close()
with open (grupodesktop, "r") as gd:
    contenidogd = gd.read()
gd.close()


#sobreescribo el fichero de configuración con la plantilla agregandole los 3 grupos ya actualizados al final
with open (dhcpconf, "w") as dhcp, open(plantilla, "r") as plantilladhcp:
    contenidoplantilla = plantilladhcp.read()
    dhcp.write(contenidoplantilla + '\n')
    dhcp.write("group server {\n")
    dhcp.write('\toption domain-name "server";\n')
    dhcp.write(contenidogs)
    dhcp.write("}\n")
    dhcp.write("group wireless {\n")
    dhcp.write('\toption domain-name "wireless";\n')
    dhcp.write(contenidogw)
    dhcp.write("}\n")
    dhcp.write("group desktop {\n")
    dhcp.write('\toption domain-name "desktop";\n')
    dhcp.write(contenidogd)
    dhcp.write("}\n")
dhcp.close()
plantilladhcp.close()               

#hago la llamada de parada y encendido del servidor dhcp unicamente si se han añadido registros
if contador != 0:  
    print(os.popen('sudo systemctl stop isc-dhcp-server').read()) 
    print(os.popen('sudo systemctl start isc-dhcp-server').read())
print(os.popen('sudo systemctl status isc-dhcp-server').read())
#hago el ping
for ips in ipes:
    pregunta = os.system('ping -c 1 ' + ips + ' > /dev/null 2>&1')
    if pregunta == 0:
        print(ips + ' is up')
    else:
        print(ips + ' is down')
if len(sys.argv) != 2:
    print("ERROR, TIENE QUE INTTRODUCIR 2 ARGUMENTOS")
    sys.exit(1)
print('se han añadido ' + str(contador) + ' ips fijas al servidor')
print('has finalizado de ejecutar el script en fecha = ' + str(datetime.datetime.now()))