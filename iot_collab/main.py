# coding: utf-8

import pyodbc
from connector import queryForVehicles, writeTrafficLightPolicy
from trafficlight import *
from parameters import *

PROJECT_TO_QUERY = 3 # 1, 2, 3 or 4

def setTLParamsForTimeslot(TrafficLightAxis_y, TrafficLightAxis_x, timeslot_id):
    roady1_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_y.tl_id, TrafficLightAxis_y.road_id1, timeslot_id)
    roady2_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_y.tl_id, TrafficLightAxis_y.road_id2, timeslot_id)

    roadx1_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_x.tl_id, TrafficLightAxis_x.road_id1, timeslot_id)
    roadx2_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_x.tl_id, TrafficLightAxis_x.road_id2, timeslot_id)

    TrafficLightAxis_y.car_input1 = round(roady1_params[3] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)
    TrafficLightAxis_y.car_input2 = round(roady2_params[3] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)

    TrafficLightAxis_x.car_input1 = round(roadx1_params[3] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)
    TrafficLightAxis_x.car_input1 = round(roadx2_params[3] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)

    TrafficLightAxis_y.sum_of_green_duration = 0
    TrafficLightAxis_y.num_of_green = 0

    TrafficLightAxis_x.sum_of_green_duration = 0
    TrafficLightAxis_x.num_of_green = 0


def setFlashingTrafficLights(TrafficLightAxis1, TrafficLightAxis2, timeslot_id):
    avg_green_duration_1 = 0
    avg_green_duration_2 = 0
    writeTrafficLightPolicy(TrafficLightAxis1, PROJECT_TO_QUERY, timeslot_id, avg_green_duration_1)
    writeTrafficLightPolicy(TrafficLightAxis2, PROJECT_TO_QUERY, timeslot_id, avg_green_duration_2)


def main():
    # create the 2 traffic_light axis 
    tl_y = TrafficLightAxis(TRAFFIC_LIGHT_Y_ID, FIRST_ROAD_IN_Y_ID, SECOND_ROAD_IN_Y_ID)
    tl_x = TrafficLightAxis(TRAFFIC_LIGHT_X_ID, FIRST_ROAD_IN_X_ID, SECOND_ROAD_IN_X_ID)

    tl_y.light_status = 'GREEN'

    for i in range(FIRST_TIMESLOT_ID, LAST_TIMESLOT_ID + 1):
        timeslot_remaining_time = TIMESLOT_DURATION
        
        # check if there's less than 1 car per minute coming from every direction
        setTLParamsForTimeslot(tl_y, tl_x, i)
        if tl_y.car_input1 * 12 < 1 \
        & tl_y.car_input2 * 12 < 1 \
        & tl_x.car_input1 * 12 < 1 \
        & tl_x.car_input2 * 12 < 1:
            setFlashingTrafficLights(tl_y, tl_x, i)
            break
        
        while timeslot_remaining_time > 0:
            green_remaining_time = GREEN_LIGHT_STANDARD_DURATION

            while green_remaining_time > 0:
                print()
                # ...


        avg_green_duration_y = round(tl_y.sum_of_green_duration / tl_y.num_of_green)
        avg_green_duration_x = round(tl_x.sum_of_green_duration / tl_x.num_of_green)

        writeTrafficLightPolicy(tl_y, PROJECT_TO_QUERY, i, avg_green_duration_y)
        writeTrafficLightPolicy(tl_x, PROJECT_TO_QUERY, i, avg_green_duration_x)
    







        
               


main()
