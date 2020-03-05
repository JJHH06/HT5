import simpy
import random
import statistics

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador
tiempo_proceso = 5 #intervalo
cant_memoria = 100  #cantidad de memoria RAM
velocidad_procesador = 0.17 #velocidad del tiempo de espera por operacion, mientras mas grande mas lento
#0.17 para 6 veces rapido
capacidad_procesador = 1 #numero de procesadores
numero_procesos = 200 #cuantos procesos se van a utilizar, esto se cambia dependiendo de los puntos de la grafica

#Procesadores habilitados para realizar el calculo
# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria


def processor(env, name, bcs, interval, cpu_speed):
    global TOTAL
    global totales
    totales = list()
    cantMemoriaProceso = random.randint(1, 10)    #Estas son las instrucciones en el loop
    yield env.timeout(random.expovariate(1 / interval))
    necesary_memory = random.randint(1, 10)     #Esta va a ser la memoria que se va a tardar num A.A
    # Request one of its charging spots
    print('%s is starting at %d' % (name, env.now))
    tiempoInicial = env.now
    
    yield ram.get(necesary_memory)
    
    isnt_finish = True
    desicion = 1;
    
    while isnt_finish:
      #  if random.randint(1, 2) == 1:
       #     yield env.timeout(cpu_speed)
        if cantMemoriaProceso > 0:
            
            with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
                yield req
                print('%s is running at %s' % (name, env.now))
                cantMemoriaProceso = cantMemoriaProceso - 1
                yield env.timeout(cpu_speed)
        if cantMemoriaProceso <= 0:
            desicion = 2
                
        if desicion == 2:
            if random.randint(1, 2) == 1:
                desicion = 3
                print('%s is waiting at %s' % (name, env.now))
            else:
                isnt_finish = False
                ('%s is ready at %s' % (name, env.now))
        if desicion == 3:
            isnt_finish = False
            ('%s is ready at %s' % (name, env.now))
                
                
    yield ram.put(necesary_memory) 
               # print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial
    totales.append(tiempoTotal)
    print ('Total time', tiempoTotal, ' for : ', name)
    
    TOTAL = TOTAL + tiempoTotal

    
    

#random.seed(10)  #se utiliza esta seed para que no queden muy dispersos los datos al graficar
env = simpy.Environment()  #crear ambiente de simulacion
bcs = simpy.Resource(env, capacity = capacidad_procesador) #aqui se asigna el valor de procesadores
                                                           # que funcionan a la vez
ram = simpy.Container(env, init=cant_memoria, capacity=cant_memoria)

TOTAL = 0;
# crear los procesos
for i in range(numero_procesos):
    env.process(processor(env, 'Process %d' % i, bcs,tiempo_proceso, velocidad_procesador))

# correr la simulacion
env.run()

print('\nPromedio' , TOTAL/numero_procesos)
print('Desviacion estandar',statistics.stdev(totales))