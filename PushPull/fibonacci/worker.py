import sys
import time
import zmq

context = zmq.Context()

work = context.socket(zmq.PULL)
work.connect("tcp://localhost:5557")

# Socket para enviar mensajes a 
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

#Definimos Fibonacci
def fib(n):
    if n == 0:
        return 0
    elif n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# Procesar tareas para siempre
while True:
    s = work.recv()

    #Hago la tarea
    f = fib(int(s))

    # Simple progress indicator for the viewer
    # Indicador de progreso simple para el espectador
    sys.stdout.write('.')
    sys.stdout.flush()

    # Do the work
    #time.sleep(int(s)*0.001)
    print(s,f)

    #Envio la respuesta
    # Send results to sink (Envio los resultados para sink)
    
    sink.send_string(u'%i' % f)
