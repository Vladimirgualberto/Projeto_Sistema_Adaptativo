# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
from struct import pack
from random import randint
from time import sleep
from struct import unpack


TOPIC = "area/10/sensor/#"

# fun��o chamada quando a conex�o for realizada, sendo
# ent�o realizada a subscri��o
def on_connect(client, data,flags, rc):
    client.subscribe([(TOPIC, 0)])


# fun��o chamada quando uma nova mensagem do t�pico � gerada
def on_message(client, userdata, msg):
    # decodificando o valor recebido
    v = unpack(">H", msg.payload)[0]

    print (msg.topic + "/" + str(v))


#client = mqtt.Client(client_id='SCADA',
                    # protocol=mqtt.MQTTv31)


# permace em loop, recebendo mensagens


##############
AREA_ID = 10
SENSOR_ID = 5000

# topicos providos por este sensor
tt = "area/%d/sensor/%s/temperatura" % (AREA_ID, SENSOR_ID)
ut = "area/%d/sensor/%s/umidade" % (AREA_ID, SENSOR_ID)

# cria um identificador baseado no id do sensor
client = mqtt.Client(client_id='NODE:%d-%d' % (AREA_ID, SENSOR_ID),
                     protocol=mqtt.MQTTv31)
# estabelece as fun��e de conex�o e mensagens
client.on_connect = on_connect
client.on_message = on_message
# conecta no broker
client.connect("127.0.0.1", 1883)

#########################


client.loop_start()
while True:
    # gera um valor de temperartura aleat�rio
    t = randint(0, 50)
    # codificando o payload como big endian, 2 bytes
    payload = pack(">H", t)
    # envia a publica��o
    client.publish(tt, payload, qos=0)
    print
    tt + "/" + str(t)

    # gera um valor de umidade aleat�rio
    u = randint(0, 100)
    # codificando o payload como big endian, 2 bytes
    payload = pack(">H", u)
    # envia a publica��o
    client.publish(ut, payload, qos=0)
    print
    ut + "/" + str(u)

    sleep(5)

