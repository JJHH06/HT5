
#Jose Hurtarte 19707
#Algoritmos y estructura de datos
#Hoja de trabajo 5
#04-03-2020


import simpy
import random
import statistics

# Debe hacer cola (FIFO) en la memoria para entrar al procesador
tiempo_proceso = 5 #intervalo
cant_memoria = 600  #cantidad de memoria RAM
velocidad_procesador = 0.17#velocidad del tiempo de espera por operacion, mientras mas grande mas lento
#0.17 para 6 veces rapido
capacidad_procesador = 1 #numero de procesadores
numero_procesos = 300 #cuantos procesos se van a utilizar, esto se cambia dependiendo de los puntos de la grafica


def processor(env, name, bcs, interval, cpu_speed):
    global TOTAL
    global totales
    totales = list()
    cantMemoriaProceso = random.randint(1, 10)    #Estas son las instrucciones en el loop
    yield env.timeout(random.expovariate(1 / interval))
    necesary_memory = random.randint(1, 10)     #Esta va a ser la memoria que se va a tardar num A.A
    # Request one process
    print('%s is starting at %d' % (name, env.now))
    tiempoInicial = env.now
    
    yield ram.get(necesary_memory)  #se reserva y pide la RAM
    
    isnt_finish = True
    desicion = 1;
    
    #es el ciclo en el que se hacen los procesamientos de las instrucciones
    while isnt_finish:
     
        if cantMemoriaProceso > 0:
            
            with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
                yield req
                print('%s is running at %s' % (name, env.now))
                cantMemoriaProceso = cantMemoriaProceso - 1 #Se procesa una instruccion
                yield env.timeout(cpu_speed) #timeout de la velocidad del procesador
        if cantMemoriaProceso <= 0:
            desicion = 2
                
        if desicion == 2:
            if random.randint(1, 2) == 1: #if con el random para verificar si se va a la espera
                desicion = 3
                print('%s is waiting at %s' % (name, env.now))
            else:
                isnt_finish = False
                ('%s is ready at %s' % (name, env.now))
        if desicion == 3:
            isnt_finish = False
            ('%s is ready at %s' % (name, env.now))  #cuando ya este listo pasa por aca
                
                
    yield ram.put(necesary_memory) #Se devuelve el espacio utilizado en la RAM

        # se hizo release
    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial  #tiempos y calculos para promedio y desviacion
    totales.append(tiempoTotal)
    print ('Total time', tiempoTotal, ' for : ', name)
    
    TOTAL = TOTAL + tiempoTotal

    
    

#random.seed(10)  #se utiliza a veces seed para que no queden muy dispersos los datos al graficar
#aunque no es necesario

env = simpy.Environment()  #crear ambiente de simulacion
bcs = simpy.Resource(env, capacity = capacidad_procesador) #aqui se asigna el valor de procesadores
                                                           # que funcionan a la vez
ram = simpy.Container(env, init=cant_memoria, capacity=cant_memoria) #se asigna la capacidad de la RAM

TOTAL = 0;
# crear los procesos
for i in range(numero_procesos):
    env.process(processor(env, 'Process %d' % i, bcs,tiempo_proceso, velocidad_procesador))

# correr la simulacion
env.run()

print('\nPromedio' , TOTAL/numero_procesos) #promedio de tiempos por todos los procesos
print('Desviacion estandar',statistics.stdev(totales)) #desviacion estandar de los tiempos de cada proceso