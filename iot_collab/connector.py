import pyodbc
from parameters import MOTORBIKE_COUNT_WEIGHT, CAR_COUNT_WEIGHT, TRUCK_COUNT_WEIGHT

server = 'pwsmartcross.database.windows.net'
database = 'smartcross'
username ='its2020'
password = 'Projectwork2020'
driver= '{ODBC Driver 17 for SQL Server}'

#DateCreated DATETIME NOT NULL DEFAULT(GETDATE()) x campo data?

cnxn = pyodbc.connect('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';PWD='+ password)

cursor = cnxn.cursor()
cursor2 = cnxn.cursor()
cursor3 = cnxn.cursor()

def queryForVehicles(project_id, tl_id, road_id, timeslot_id):
    cursor.execute("""SELECT
    id_incrocio
    , id_semaforo
    , id_strada
    , fascia_oraria
    , SUM(conteggio) conteggio
FROM (
    SELECT
        id_incrocio
        , id_semaforo
        , id_strada
        , fascia_oraria
        , data
        , tipologia_veicolo
        , CASE
            WHEN tipologia_veicolo = 'Motociclo' THEN conteggio * """ + str(MOTORBIKE_COUNT_WEIGHT) + """
            WHEN tipologia_veicolo = 'Automobile' THEN conteggio * """ + str(CAR_COUNT_WEIGHT) + """
            WHEN tipologia_veicolo = 'Mezzo pesante' THEN conteggio * """ + str(TRUCK_COUNT_WEIGHT) + """
            END as conteggio
    FROM
        dbo.traffico
    WHERE
        id_incrocio = """ + str(project_id) + """
        AND id_semaforo = """ + str(tl_id) + """
        AND id_strada = """ + str(road_id) + """
        AND fascia_oraria = """ + str(timeslot_id) + """
        AND data = (
                SELECT
                    MAX(data)
                FROM
                    dbo.traffico
                WHERE
                    id_incrocio = """ + str(project_id) + """
                    AND id_semaforo = """ + str(tl_id) + """
                    AND id_strada = """ + str(road_id) + """
                    AND fascia_oraria = """ + str(timeslot_id) + """
            )
) q1
GROUP BY
    id_incrocio
    , id_semaforo
    , id_strada
    , fascia_oraria"""
)
    row = cursor.fetchone()
    return row

def writeTrafficLightPolicy(TrafficLightAxis1, project_id, timeslot_id):
    cursor2.execute("""DELETE FROM dbo.temporizzazione
WHERE
	id_incrocio = """ + str(project_id) + """
	AND id_semaforo = """ + str(TrafficLightAxis1.tl_id) + """
	AND fascia_oraria = """ + str(timeslot_id) + """
""")

    cursor3.execute("""INSERT INTO dbo.temporizzazione (
	id_incrocio
	, id_semaforo
	, fascia_oraria
	, valore_tempo
)
VALUES (
	""" + str(project_id) + """
	, """ +  str(TrafficLightAxis1.tl_id) + """
	, """ +  str(timeslot_id) + """
	, """ + str(TrafficLightAxis1.avg_green_duration) + """
           
)""")
    cnxn.commit()
    
