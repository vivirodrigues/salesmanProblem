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
import fuzzy

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

def run(network, begin, end, interval, rota):

    step = 1
    consumption = 0
    f_2 = fuzzy.Algorithm()
    
    #adition = Simulation.Vehicles.add1(traci) 
    traci.route.add("trip", rota)
    traci.vehicle.add("caminhao", "trip")
    traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
    traci.vehicle.setVehicleClass("caminhao","truck")
    traci.vehicle.setShapeClass("caminhao","truck")
    traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
    traci.vehicle.setMaxSpeed("caminhao",28) # aprox 8 km/h 
    #print(traci.vehicle.getAccel("caminhao"))
    #print(traci.vehicle.getVehicleClass("caminhao"))    
    #print(traci.vehicle.getEmissionClass("caminhao")) 
    
    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:   
        
        angle = traci.vehicle.getSlope("caminhao")
        speedI = traci.vehicle.getSpeed("caminhao")
        if angle == float(0):
            angle = 0.1
        elif angle < float(-50):
            angle = 0.1
        if speedI < -10:
            speedI = float(0)
        
        #print("Angle",angle," speed",speedI) 

        speed = f_2.findSpeed(angle, speedI)

        traci.vehicle.setSpeed("caminhao",speed)
        angle = traci.vehicle.getSlope("caminhao")
        acceleration = traci.vehicle.getAcceleration("caminhao")
        
        consumption += calculate_real_fuel(speed,acceleration,angle)         

        traci.simulationStep()                          
        vehicles = traci.simulation.getEndingTeleportIDList()
        
        for vehicle in vehicles:
            traci.vehicle.remove(vehicle, reason=4)    

        step += 1
    
    #time.sleep(10)    
    #print("Simulation finished")
    traci.close()
    sys.stdout.flush()
    #time.sleep(10)
    return consumption
        
def start_simulation(sumo, scenario, network, begin, end, interval, output, rota):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen([sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port", str(remote_port), "--duration-log.statistics","--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)    
    unused_port_lock.release()


    try:
        traci.init(remote_port)            
        consumption = run(network, begin, end, interval,rota)        
    except Exception as e:
        #print(e)        
        raise
    finally:
        #print("Terminating SUMO")  
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

    return consumption
        
def main(rota):

    parser = OptionParser()
    parser.add_option("-c", "--command", dest="command", default="sumo", help="The command used to run SUMO [default: %default]", metavar="COMMAND")
    parser.add_option("-s", "--scenario", dest="scenario", default="SUMO2/map.sumocfg", help="A SUMO configuration file [default: %default]", metavar="FILE")
    parser.add_option("-n", "--network", dest="network", default="SUMO2/map.net.xml", help="A SUMO network definition file [default: %default]", metavar="FILE")    
    parser.add_option("-b", "--begin", dest="begin", type="int", default=0, action="store", help="The simulation time (s) at which the re-routing begins [default: %default]", metavar="BEGIN")
    parser.add_option("-e", "--end", dest="end", type="int", default=600, action="store", help="The simulation time (s) at which the re-routing ends [default: %default]", metavar="END")
    parser.add_option("-i", "--interval", dest="interval", type="int", default=1, action="store", help="The interval (s) of classification [default: %default]", metavar="INTERVAL")    
    parser.add_option("-o", "--full-output", dest="output", default="SUMO2/output1.xml", help="The XML file at which the output must be written [default: %default]", metavar="FILE")


    (options, args) = parser.parse_args()
    
    consumption = start_simulation(options.command, options.scenario, options.network, options.begin, options.end, options.interval, options.output, rota)
    return consumption

if __name__ == "__main__":
    main()