

from datetime import datetime, timedelta

from metrics.test_run import TestRun, TypeEnum
import random
import math


if __name__ == '__main__':
    type = ['TIMER', 'QA', 'TIMER', 'DEV', 'TIMER']
    scenario = ['no_urcaps', 'gripper', 'Wrist_Camera', 'Force_Copilot', 'Grippers|Wrist_Camera|Force_Copilot']

    NBR_DAYS = 25
    MAX_RANGE = 12
    target_handicap = {"java":0.82,"driverSensorUR":0.21, "URControl":0.55, "drivergripper":0.34,
                             "xmlrpcserver":0.12, "visionserver":0.26}


    for idx in range(NBR_DAYS):
        for scenarioIdx in range(5):
            datets = datetime.now() - timedelta(days=(idx - 1))
            test = TestRun(build_number=str(10000 + (MAX_RANGE - idx)), type=TypeEnum.DEV, scenario=scenario[scenarioIdx],
                           group=type[random.randint(0, 4)], dt_stamp=datets)

            # Add tested products
            test.add_product(name="URCAP-Gripper", version="1.0.0.1 alpha", description="Dev version with mem leak fix")
            test.add_product(name="URCAP-Force_Copilot", version="2.2.0.0", description="production version of may 2 2019")
            test.add_product(name="URCAP-Wrist_Camera", version="1.8.0.0", description="")

            rand_factor = random.random()

            for targetIdx in range(MAX_RANGE):
                if targetIdx is 1:
                    total_space = 1844
                    used_space = 1500 + (250 * rand_factor)
                    avail_space = max(total_space - used_space - (total_space * 0.05), 0)
                    test.add_metric(name="hdd_space", description="", value=1844, qualifier="MB", target='total', index=targetIdx)
                    test.add_metric(name="hdd_space", description="", value=used_space, qualifier="MB", target='used', index=targetIdx)
                    test.add_metric(name="hdd_space", description="", value=avail_space, qualifier="MB", target='available', index=targetIdx)
                    test.add_metric(name="hdd_space", description="", value=210, qualifier="MB", target='Gripper', index=targetIdx)
                    test.add_metric(name="hdd_space", description="", value=180, qualifier="MB", target='Force_Copilote', index=targetIdx)
                    test.add_metric(name="hdd_space", description="", value=261, qualifier="MB", target='Wrist_Camera', index=targetIdx)

                val_cpu = (MAX_RANGE - math.sqrt(targetIdx)) * rand_factor
                # Java
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['java'], qualifier="%",
                                target='java', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='java', index=targetIdx,
                                dimensions={'type':'average_all'})

                #driverSensorUR
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['driverSensorUR'], qualifier="%",
                                target='driverSensorUR', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='driverSensorUR', index=targetIdx,
                                dimensions={'type':'average_all'})

                #URControl
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['URControl'], qualifier="%",
                                target='URControl', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='URControl', index=targetIdx,
                                dimensions={'type':'average_all'})

                #drivergripper
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['drivergripper'], qualifier="%",
                                target='drivergripper', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='drivergripper', index=targetIdx,
                                dimensions={'type':'average_all'})

                #xmlrpcserver
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['xmlrpcserver'], qualifier="%",
                                target='xmlrpcserver', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='xmlrpcserver', index=targetIdx,
                                dimensions={'type':'average_all'})

                #visionserver
                test.add_metric(name="pcpu", description="", value=val_cpu* target_handicap['visionserver'], qualifier="%",
                                target='visionserver', index=targetIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='visionserver', index=targetIdx,
                                dimensions={'type':'average_all'})

            # Commit to the database
            test.commit()
