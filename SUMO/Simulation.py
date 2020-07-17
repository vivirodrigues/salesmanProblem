class Vehicles:

	def add1(traci):
		traci.route.add("trip", ['3to4', '4to5', '5to6', '6to7', '7to8', '8to9', '9to10', '10to11', '11to12', '12to13', '13to14', '14to15', '15to16', '16to17', '17to18', '18to19', '19to20', '20to21', '21to22', '22to25'])
		traci.vehicle.add("caminhao", "trip")
		traci.vehicle.setParameter("caminhao","carFollowModel","KraussPS")
		traci.vehicle.setVehicleClass("caminhao","truck")
		traci.vehicle.setShapeClass("caminhao","truck")
		traci.vehicle.setEmissionClass("caminhao","HBEFA3/HDV")
		traci.vehicle.setMaxSpeed("caminhao",2.2) # aprox 8 km/h 
		print(traci.vehicle.getAccel("caminhao"))
		print(traci.vehicle.getVehicleClass("caminhao"))	
		print(traci.vehicle.getEmissionClass("caminhao"))		

		traci.vehicle.add("carrinheiro", "trip")		
		traci.vehicle.setVehicleClass("carrinheiro","pedestrian")
		traci.vehicle.setShapeClass("carrinheiro","pedestrian")
		traci.vehicle.setMaxSpeed("carrinheiro",1) # aprox 4 km/h
		traci.vehicle.setEmissionClass("carrinheiro","Zero")
		
		return True

	