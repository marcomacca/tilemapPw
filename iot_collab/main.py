# coding: utf-8

import pyodbc
from connector import queryForVehicles, writeTrafficLightPolicy
from trafficlight import *
from parameters import *
from random import randrange

PROJECT_TO_QUERY = 3 # 1, 2, 3 or 4

def setTLParamsForTimeslot(TrafficLightAxis_y, TrafficLightAxis_x, timeslot_id):
    roady1_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_y.tl_id, TrafficLightAxis_y.road_id1, timeslot_id)
    roady2_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_y.tl_id, TrafficLightAxis_y.road_id2, timeslot_id)

    roadx1_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_x.tl_id, TrafficLightAxis_x.road_id1, timeslot_id)
    roadx2_params = queryForVehicles(PROJECT_TO_QUERY, TrafficLightAxis_x.tl_id, TrafficLightAxis_x.road_id2, timeslot_id)

    TrafficLightAxis_y.car_input1 = round(roady1_params[4] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)
    TrafficLightAxis_y.car_input2 = round(roady2_params[4] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)

    TrafficLightAxis_x.car_input1 = round(roadx1_params[4] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)
    TrafficLightAxis_x.car_input2 = round(roadx2_params[4] / TIMESLOT_DURATION * MIN_UNIT_OF_TIME)

    TrafficLightAxis_y.sum_of_green_duration = 0
    TrafficLightAxis_y.num_of_green = 0

    TrafficLightAxis_x.sum_of_green_duration = 0
    TrafficLightAxis_x.num_of_green = 0

def setFlashingTrafficLights(TrafficLightAxis1, TrafficLightAxis2, timeslot_id):
    writeTrafficLightPolicy(TrafficLightAxis1, PROJECT_TO_QUERY, timeslot_id)
    writeTrafficLightPolicy(TrafficLightAxis2, PROJECT_TO_QUERY, timeslot_id)

def trafficLightPolicy(TrafficLightAxis_waiting, TrafficLightAxis_active, green_remaining_time, axis_pop_diff_check, minimum_pop_length):
    axis_population_waiting = TrafficLightAxis_waiting.population1 + TrafficLightAxis_waiting.population2
    axis_population_active = TrafficLightAxis_active.population1 + TrafficLightAxis_active.population2
    if axis_population_waiting >= minimum_pop_length \
    and axis_population_waiting >= axis_population_active * axis_pop_diff_check:
        green_remaining_time = green_remaining_time / POLICY_HARDNESS
        minimum_pop_length += MIN_POP_POLICY_INCREMENT
        axis_pop_diff_check += DIFF_THRES_INCREMENT
    return green_remaining_time

def trafficLightGreenLifeCycle(TrafficLightAxis1, TrafficLightAxis2, green_remaining_time, green_elapsed_time):
    green_duration_check = green_remaining_time
    green_elapsed_check = green_elapsed_time
    if green_duration_check < MIN_UNIT_OF_TIME:
        # add self.car_input in every queue
        TrafficLightAxis1.population1 += round(TrafficLightAxis1.car_input1 * green_remaining_time / MIN_UNIT_OF_TIME) 
        TrafficLightAxis1.population2 += round(TrafficLightAxis1.car_input2 * green_remaining_time / MIN_UNIT_OF_TIME)
        TrafficLightAxis2.population1 += round(TrafficLightAxis2.car_input1 * green_remaining_time / MIN_UNIT_OF_TIME)
        TrafficLightAxis2.population2 += round(TrafficLightAxis2.car_input2 * green_remaining_time / MIN_UNIT_OF_TIME)
        # take out VEHICLE_OUTPUT in the queues that have GREEN light
        TrafficLightAxis1.population1 -= round(VEHICLE_OUTPUT * green_remaining_time / MIN_UNIT_OF_TIME)
        if TrafficLightAxis1.population1 < 0:
            TrafficLightAxis1.population1 = 0
        TrafficLightAxis1.population2 -= round(VEHICLE_OUTPUT * green_remaining_time / MIN_UNIT_OF_TIME)
        if TrafficLightAxis1.population2 < 0:
            TrafficLightAxis1.population2 = 0
        green_elapsed_check += green_duration_check
        green_duration_check -= green_duration_check
        if green_duration_check == 0:
            print("traffic light " + str(TrafficLightAxis1.tl_id) + " is now YELLOW")
            #end of green life cycle
            TrafficLightAxis1.sum_of_green_duration += green_elapsed_check
            TrafficLightAxis1.num_of_green += 1
            TrafficLightAxis1.lightSwitch()
            if TrafficLightAxis1.light_status == 'YELLOW':
                # More cars keep coming, but...
                TrafficLightAxis1.population1 += round(TrafficLightAxis1.car_input1 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis1.population2 += round(TrafficLightAxis1.car_input2 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis2.population1 += round(TrafficLightAxis2.car_input1 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis2.population2 += round(TrafficLightAxis2.car_input2 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                # someone "has" to stop at the YELLOW light, right?
                TrafficLightAxis1.population1 -= randrange(1, round(VEHICLE_OUTPUT * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME))
                TrafficLightAxis1.population2 -= randrange(1, round(VEHICLE_OUTPUT * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME))
                TrafficLightAxis1.lightSwitch()
                print("traffic light " + str(TrafficLightAxis1.tl_id) + " is now RED")
                TrafficLightAxis2.lightSwitch()
                print("traffic light " + str(TrafficLightAxis2.tl_id) + " is now GREEN")
    else:
        # add self.car_input in every queue
        TrafficLightAxis1.population1 += TrafficLightAxis1.car_input1
        TrafficLightAxis1.population2 += TrafficLightAxis1.car_input2
        TrafficLightAxis2.population1 += TrafficLightAxis2.car_input1
        TrafficLightAxis2.population2 += TrafficLightAxis2.car_input2
        # take out VEHICLE_OUTPUT in the queues that have GREEN light
        TrafficLightAxis1.population1 -= VEHICLE_OUTPUT
        TrafficLightAxis1.population2 -= VEHICLE_OUTPUT
        if TrafficLightAxis1.population1 < 0:
            TrafficLightAxis1.population1 = 0
        if TrafficLightAxis1.population2 < 0:
            TrafficLightAxis1.population2 = 0
        green_duration_check -= MIN_UNIT_OF_TIME
        green_elapsed_check += MIN_UNIT_OF_TIME
        if green_duration_check == 0:
            #end of green life cycle
            TrafficLightAxis1.sum_of_green_duration += green_elapsed_check
            TrafficLightAxis1.num_of_green += 1
            TrafficLightAxis1.lightSwitch()
            if TrafficLightAxis1.light_status == 'YELLOW':
                # More cars keep coming, but...
                TrafficLightAxis1.population1 += round(TrafficLightAxis1.car_input1 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis1.population2 += round(TrafficLightAxis1.car_input2 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis2.population1 += round(TrafficLightAxis2.car_input1 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                TrafficLightAxis2.population2 += round(TrafficLightAxis2.car_input2 * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME)
                # someone "has" to stop at the YELLOW light, right?
                TrafficLightAxis1.population1 -= randrange(1, round(VEHICLE_OUTPUT * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME))
                TrafficLightAxis1.population2 -= randrange(1, round(VEHICLE_OUTPUT * YELLOW_LIGHT_STANDARD_DURATION / MIN_UNIT_OF_TIME))
                if TrafficLightAxis1.population1 < 0:
                    TrafficLightAxis1.population1 = 0
                if TrafficLightAxis1.population2 < 0:
                    TrafficLightAxis1.population2 = 0
                TrafficLightAxis1.lightSwitch()
                TrafficLightAxis2.lightSwitch()



def main():
    # create the 2 traffic_light axis 
    tl_y = TrafficLightAxis(TRAFFIC_LIGHT_Y_ID, FIRST_ROAD_IN_Y_ID, SECOND_ROAD_IN_Y_ID)
    tl_x = TrafficLightAxis(TRAFFIC_LIGHT_X_ID, FIRST_ROAD_IN_X_ID, SECOND_ROAD_IN_X_ID)

    # set one traffic light as GREEN
    tl_y.light_status = 'GREEN'

    # for every timeslot_id...
    for i in range(FIRST_TIMESLOT_ID, LAST_TIMESLOT_ID + 1):
        timeslot_remaining_time = TIMESLOT_DURATION
        # reset traffic lights' data and params for new timeslot
        resetDataForTimeslot(tl_y, tl_x)
        setTLParamsForTimeslot(tl_y, tl_x, i)

        # if incoming vehicles from every direction are too few, write 0 ("flashing lights") as the green light's duration value in the db
        if (tl_y.car_input1 / MIN_UNIT_OF_TIME * TIME_THRESHOLD_FOR_FLASHING_LIGHTS) < MIN_VEHICLE_INPUT_PER_FLASHING_LIGHTS_THRESHOLD \
        and (tl_y.car_input2 / MIN_UNIT_OF_TIME * TIME_THRESHOLD_FOR_FLASHING_LIGHTS) < MIN_VEHICLE_INPUT_PER_FLASHING_LIGHTS_THRESHOLD \
        and (tl_x.car_input1 / MIN_UNIT_OF_TIME * TIME_THRESHOLD_FOR_FLASHING_LIGHTS) < MIN_VEHICLE_INPUT_PER_FLASHING_LIGHTS_THRESHOLD \
        and (tl_x.car_input2 / MIN_UNIT_OF_TIME * TIME_THRESHOLD_FOR_FLASHING_LIGHTS) < MIN_VEHICLE_INPUT_PER_FLASHING_LIGHTS_THRESHOLD:
            print("setting flashing lights for timeslot " + str(i))
            setFlashingTrafficLights(tl_y, tl_x, i)
            continue
        
        while timeslot_remaining_time > 0:
            green_remaining_time = GREEN_LIGHT_STANDARD_DURATION
            green_elapsed_time = 0
            min_pop_for_policy_check = MINIMUM_POPULATION_FOR_POLICY_APPLICATION
            diff_thres_for_policy_check = DIFFERENCE_THRESHOLD_FOR_POLICY_APPLICATION

            while green_remaining_time > 0:
                if tl_x.light_status == 'RED':
                    green_remaining_time = trafficLightPolicy(tl_x, tl_y, green_remaining_time, diff_thres_for_policy_check, min_pop_for_policy_check)
                    trafficLightGreenLifeCycle(tl_y, tl_x, green_remaining_time, green_elapsed_time)
                    if green_remaining_time < MIN_UNIT_OF_TIME:
                        green_elapsed_time += green_remaining_time
                        green_remaining_time -= green_remaining_time
                    else:
                        green_elapsed_time += MIN_UNIT_OF_TIME
                        green_remaining_time -= MIN_UNIT_OF_TIME                    
                elif tl_y.light_status == 'RED':
                    green_remaining_time = trafficLightPolicy(tl_y, tl_x, green_remaining_time, diff_thres_for_policy_check, min_pop_for_policy_check)
                    trafficLightGreenLifeCycle(tl_x, tl_y, green_remaining_time, green_elapsed_time)
                    if green_remaining_time < MIN_UNIT_OF_TIME:
                        green_elapsed_time += green_remaining_time
                        green_remaining_time -= green_remaining_time
                    else:
                        green_elapsed_time += MIN_UNIT_OF_TIME
                        green_remaining_time -= MIN_UNIT_OF_TIME

            timeslot_remaining_time -= green_elapsed_time
        
        # calculate the average green light duration for both traffic lights and write them on the db
        tl_y.avg_green_duration = round(tl_y.sum_of_green_duration / tl_y.num_of_green)
        writeTrafficLightPolicy(tl_y, PROJECT_TO_QUERY, i)
        tl_x.avg_green_duration = round(tl_x.sum_of_green_duration / tl_x.num_of_green)
        writeTrafficLightPolicy(tl_x, PROJECT_TO_QUERY, i)
                        

                    





        
    







        
               


main()
