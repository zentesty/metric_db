
from datetime import datetime, timedelta

from metrics.test_run import TestRun, TypeEnum
import random


if __name__ == '__main__':
    type = ['TIMER', 'QA', 'TIMER', 'DEV', 'TIMER']
    scenario = ['no_urcaps', 'gripper', 'Wrist_Camera', 'Force_Copilot', 'Grippers|Wrist_Camera|Force_Copilot']

    for idx in range(25):

        for scenarioIdx in range(5):


            datets = datetime.now() - timedelta(days=(idx - 1))
            test = TestRun(build_number=str(10000 + idx), type=TypeEnum.DEV, scenario=scenario[scenarioIdx],
                           group=type[random.randint(0, 4)], dt_stamp=datets)

            # Add tested products
            test.add_product(name="URCapA", version="1.0.0.1 alpha", description="Dev version with mem leak fix")
            test.add_product(name="URCapB", version="2.2.0.0", description="production version of may 2 2019")

            for metricIdx in range(12):
                # Java
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='java', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='java', index=metricIdx,
                                dimensions={'type':'average_all'})

                #driverSensorUR
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='driverSensorUR', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='driverSensorUR', index=metricIdx,
                                dimensions={'type':'average_all'})

                #URControl
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='URControl', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='URControl', index=metricIdx,
                                dimensions={'type':'average_all'})

                #drivergripper
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='drivergripper', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='drivergripper', index=metricIdx,
                                dimensions={'type':'average_all'})

                #xmlrpcserver
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='xmlrpcserver', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='xmlrpcserver', index=metricIdx,
                                dimensions={'type':'average_all'})

                #visionserver
                test.add_metric(name="pcpu", description="", value=(random.random() * 100),qualifier="%",
                                target='visionserver', index=metricIdx,
                                dimensions={'type':'average_all'})
                test.add_metric(name="pmem", description="", value=random.random() * 100, qualifier="MB",
                                target='visionserver', index=metricIdx,
                                dimensions={'type':'average_all'})

            # Commit to the database
            test.commit()
