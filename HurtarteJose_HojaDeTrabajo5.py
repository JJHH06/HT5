import simpy
import random

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador
tiempo_proceso = 10
# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria


def car(env, name, bcs, driving_time, charge_duration, interval):
    global TOTAL
    cantMemoriaProceso = random.randint(1, 10)
    yield env.timeout(random.expovariate(1 / interval))

    # Request one of its charging spots
    print('%s is starting at %d' % (name, env.now))
    tiempoInicial = env.now
    
    with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial
    print ('tiempo total', tiempoTotal, ' para carro: ', name)
    TOTAL = TOTAL + tiempoTotal
        
    
    
#
random.seed(10)
env = simpy.Environment()  #crear ambiente de simulacion
bcs = simpy.Resource(env, capacity=1) #el cargador de bateria soporta 2 carros
                                      #a la vez
TOTAL = 0;
# crear los carros
for i in range(5):
    tiempoConducir = random.randint(1,5)
    tCarga = random.randint(1,5)
    env.process(car(env, 'Process %d' % i, bcs, tiempoConducir, tCarga,tiempo_proceso))

# correr la simulacion
env.run()
print('promedio' , TOTAL/5)