from __future__ import division
import os
import sys
import subprocess
import signal
import socket
import threading
import time
from optparse import OptionParser
import ConsumptionModel as cM
import json
from decimal import Decimal, ROUND_HALF_UP
#import fuzzy
import math

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")

sys.path.append(os.path.join('/home/-/sumo-1.5.0/tools'))

import traci

class UnusedPortLock:
    lock = threading.Lock()

    def __init__(self):
        self.acquired = False

    def __enter__(self):
        self.acquire()

    def __exit__(self):
        self.release()

    def acquire(self):
        if not self.acquired:
            UnusedPortLock.lock.acquire()
            self.acquired = True

    def release(self):
        if self.acquired:
            UnusedPortLock.lock.release()
            self.acquired = False

def find_unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()
    return port

def terminate_sumo(sumo):
    if sumo.returncode == None:
        os.kill(sumo.pid, signal.SIGILL)
        #time.sleep(0.5)
        if sumo.returncode == None:
            os.kill(sumo.pid, signal.SIGKILL)
            #time.sleep(1)
            if sumo.returncode == None:
                time.sleep(0.5)

def calculate_real_fuel(speed,accel,slope):
        modelo = cM.ModelConsumption(speed, accel, slope)
        consumption = modelo.run()
        instant_fuel = consumption
           
        return instant_fuel

def calculate_real_fuel2(speed,accel,slope):
    modelo = cM.ModelConsumption(speed, accel, slope)
    consuption = modelo.run()
    p = 0.2 # Percentage increase in consumption [0,1]
    maxSlope = 25
    maxSpeed = 30
    factor_Slope = math.exp(slope)/math.exp(maxSlope)
    factor_Speed = math.exp(speed)/math.exp(maxSpeed)
    factor_RPM = factor_Speed*factor_Speed*p
    instant_fuel = consuption + consuption*factor_RPM
   
    return instant_fuel

def run(network, begin, end, interval, rota, file):

    speedList = []
    fuelList = []
    pdfSpeed = [0] * 110
    pdfFuel = [0] * 30
    co2Emission = []
    
    total = 0

    step = 1
    consumption = 0
    totalConsumption = 0
    #f_2 = fuzzy.Algorithm()
    
    dados = []

    #adition = Simulation.Vehicles.add1(traci)     
    traci.route.add("trip", rota)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
    traci.vehicle.setMaxSpeed("caminhao",28) # aprox 8 km/h 
    
    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:   
        
        speedI = traci.vehicle.getSpeed("caminhao")

        if speedI < -100:
            speedI = float(0)
        
        speed = speedI * 3.6 # m/s para km/h                
        
        num = Decimal(float(speed)).quantize(0, ROUND_HALF_UP)
        
        pdfSpeed[int(num)] += 1

        speedList.append(speed)

        #traci.vehicle.setSpeed("caminhao",speed)
        angle = traci.vehicle.getSlope("caminhao")
        acceleration = traci.vehicle.getAcceleration("caminhao")
        
        consumption = calculate_real_fuel2(speedI,acceleration,angle)
                

        if consumption < 0:
            consumption = float(0)        
        num = Decimal(float(consumption)).quantize(0, ROUND_HALF_UP)
        
        pdfFuel[int(num)] += 1
        total += 1

        fuelList.append(consumption)

        totalConsumption += consumption

        co2 = traci.vehicle.getCO2Emission("caminhao")
        co2Emission.append(co2)

        x, y, z = traci.vehicle.getPosition3D("caminhao")
        dados.append({"x":x, "y":y, "z":z, "angle":angle})

        traci.simulationStep()                          
        vehicles = traci.simulation.getEndingTeleportIDList()
        
        for vehicle in vehicles:
            traci.vehicle.remove(vehicle, reason=4)    

        step += 1
    
    dicionarioFuel = {}
    dicionarioSpeed = {}
    dicionarioFuelList = {}
    dicionarioSpeedList = {}
    dicionarioMap = {}
    dicionarioCO2 = {}
    # dicionario i:pdfSpeed[i]
    for i in range(len(pdfSpeed)):
        pdfSpeed[i] = (pdfSpeed[i]/total) * 100
        sett = {i:pdfSpeed[i]}
        dicionarioSpeed.update(sett)
        
    for i in range(len(pdfFuel)):
        pdfFuel[i] = (pdfFuel[i]/total) * 100        
        sett = {i:pdfFuel[i]}
        dicionarioFuel.update(sett)

    for i in range(1,len(fuelList)):        
        sett = {i:fuelList[i]}
        dicionarioFuelList.update(sett)

    for i in range(1,len(speedList)):        
        sett = {i:speedList[i]}
        dicionarioSpeedList.update(sett)

    for i in range(1,len(dados)):        
        sett = {i:dados[i]}
        dicionarioMap.update(sett)

    for i in range(1,len(co2Emission)):        
        sett = {i:co2Emission[i]}
        dicionarioCO2.update(sett)

    traci.close()
    sys.stdout.flush()
    #writeJson(dicionarioFuelList,'fuel'+ file)
    #writeJson(dicionarioSpeedList,'speed' + file)
    #writeJson(dicionarioCO2,'CO2' + file)
    #writeJson1(dicionarioFuel,'pdfFuel' + file)
    #writeJson1(dicionarioSpeed,'pdfSpeed' + file)
    writeJson1(dicionarioMap,'map' + file)
    return totalConsumption
        
def start_simulation(sumo, scenario, network, begin, end, interval, output, rota, file):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        consumption = run(network, begin, end, interval,rota, file)        
    except Exception as e:
        #print(e)        
        raise
    finally:
        #print("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

    return consumption

def writeJson(content,fileName):
    with open('results/rotas5/'+fileName+'.json', 'w') as json_file:
        json.dump(content, json_file,separators=(',', ':'),ensure_ascii=False, sort_keys=True, indent=4)

def writeJson1(content,fileName):    
    with open('results/PDF/'+fileName+'.json', 'w') as json_file:
        json.dump(content, json_file,separators=(',', ':'),ensure_ascii=False, sort_keys=True, indent=4)

def main(rota, file):

    parser = OptionParser()
    parser.add_option("-c", "--command", dest="command", default="sumo", help="The command used to run SUMO [default: %default]", metavar="COMMAND")
    parser.add_option("-s", "--scenario", dest="scenario", default="SUMO/map.sumocfg", help="A SUMO configuration file [default: %default]", metavar="FILE")
    parser.add_option("-n", "--network", dest="network", default="SUMO/map.net.xml", help="A SUMO network definition file [default: %default]", metavar="FILE")    
    parser.add_option("-b", "--begin", dest="begin", type="int", default=0, action="store", help="The simulation time (s) at which the re-routing begins [default: %default]", metavar="BEGIN")
    parser.add_option("-e", "--end", dest="end", type="int", default=600, action="store", help="The simulation time (s) at which the re-routing ends [default: %default]", metavar="END")
    parser.add_option("-i", "--interval", dest="interval", type="int", default=1, action="store", help="The interval (s) of classification [default: %default]", metavar="INTERVAL")    
    parser.add_option("-o", "--full-output", dest="output", default="SUMO/output.xml", help="The XML file at which the output must be written [default: %default]", metavar="FILE")


    (options, args) = parser.parse_args()
    
    consumption = start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.output, rota, file)
    return consumption

if __name__ == "__main__":
    main()