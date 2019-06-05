
from datetime import datetime, timedelta

from metrics.test_run import TestRun, TypeEnum
import random


if __name__ == '__main__':
    for idx in range(25):

        type = ['TIMER', 'QA', 'TIMER', 'DEV', 'TIMER']

        datets = datetime.now() - timedelta(days=(idx - 1))
        test = TestRun(build_number=str(10000 + idx), type=TypeEnum.DEV, scenario="SCE00" + str(random.randint(1, 8)),
                       group=type[random.randint(0, 4)], dt_stamp=datets)

        # Add tested products
        test.add_product(name="URCapA", version="1.0.0.1 alpha", description="Dev version with mem leak fix")
        test.add_product(name="URCapB", version="2.2.0.0", description="production version of may 2 2019")

        # Add metrics and dimensions
        test.add_metric(name="CPU system", description="", value=(random.random() * 100), qualifier="usage%",
                        dimensions={'index':'1', 'process':'java', 'type':'average_all'})
        test.add_metric(name="Mem Usage", description="", value=random.random() * 100, qualifier="%",
                        dimensions={'index':'2', 'process':'java', 'type':'average_all'})
        test.add_metric(name="Hdd free Space", description="", value=random.random() * 100, qualifier="kb",
                        dimensions={'index':'3', 'process':'java', 'type':'average_all'})
        test.add_metric(name="CPU Idle", description="", value=random.random() * 100, qualifier="usage%",
                        dimensions={'index':'4', 'process':'java', 'type':'average_all'})

        # Commit to the database
        test.commit()
