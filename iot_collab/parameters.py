#Time params
TIMESLOT_DURATION = 3600 # seconds
TRAFFIC_LIGHT_STANDARD_DURATION = 120 #seconds
RED_LIGHT_STANDARD_DURATION = TRAFFIC_LIGHT_STANDARD_DURATION / 2
YELLOW_LIGHT_STANDARD_DURATION = 5 # seconds
GREEN_LIGHT_STANDARD_DURATION = RED_LIGHT_STANDARD_DURATION - YELLOW_LIGHT_STANDARD_DURATION
TIME_THRESHOLD_FOR_FLASHING_LIGHTS = 60
MIN_UNIT_OF_TIME = 5 # seconds
VEHICLE_OUTPUT = 3
MIN_VEHICLE_INPUT_PER_FLASHING_LIGHTS_THRESHOLD = 1

#Params for Crossroad setup
TRAFFIC_LIGHT_Y_ID = 0
FIRST_ROAD_IN_Y_ID = 1
SECOND_ROAD_IN_Y_ID = 3

TRAFFIC_LIGHT_X_ID = 1
FIRST_ROAD_IN_X_ID = 2
SECOND_ROAD_IN_X_ID = 4

FIRST_TIMESLOT_ID = 1
LAST_TIMESLOT_ID = 24

#Params for Policy
MINIMUM_POPULATION_FOR_POLICY_APPLICATION = 10
MIN_POP_POLICY_INCREMENT = 20
DIFFERENCE_THRESHOLD_FOR_POLICY_APPLICATION = 2
DIFF_THRES_INCREMENT = 1
MINIMUM_GREEN_LIGHT_DURATION = 10
POLICY_HARDNESS = 2

#Params for queries
MOTORBIKE_COUNT_WEIGHT = 0.5
CAR_COUNT_WEIGHT = 1
TRUCK_COUNT_WEIGHT = 2.5