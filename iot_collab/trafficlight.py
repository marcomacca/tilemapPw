class TrafficLightAxis:
    def __init__(self, tl_id, road_id1, road_id2):
        self.tl_id = tl_id 
        self.road_id1 = road_id1 # id strada (1 di 2)
        self.road_id2 = road_id2 # id strada (2 di 2)
        self.population1 = 0
        self.population2 = 0
        self.light_status = 'RED'
        self.car_input1 = 0
        self.car_input2 = 0
        self.sum_of_green_duration = 0
        self.num_of_green = 0
        self.avg_green_duration = 0
    
    def lightSwitch(self):
        if self.light_status == 'RED':
            light_status = 'GREEN'
        elif light_status == 'GREEN':
            light_status = 'YELLOW'
        elif light_status == 'YELLOW':
            light_status = 'RED'

def resetDataForTimeslot(TrafficLightAxis1, TrafficLightAxis2):
    TrafficLightAxis1.sum_of_green_duration = 0
    TrafficLightAxis1.num_of_green = 0
    TrafficLightAxis1.avg_green_duration = 0
    TrafficLightAxis2.sum_of_green_duration = 0
    TrafficLightAxis2.num_of_green = 0
    TrafficLightAxis2.avg_green_duration = 0


