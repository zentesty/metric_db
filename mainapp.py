
from metrics.test_run import TestRun, TypeEnum



if __name__ == '__main__':
    test = TestRun(build_number="10001", type=TypeEnum.DEV, scenario="SCE001")
    test.add_product(name="URCapA", version="1.0.0.1 alpha", description="Dev version with mem leak fix")
    test.add_product(name="URCapB", version="2.2.0.0", description="production version of may 2 2019")
    test.add_metric(name="CPU Idle", description="", value=82.11, qualifier="sec",
                    dimensions={'index':'1', 'process':'java', 'type':'average_all'})
    test.add_metric(name="CPU Idle", description="", value=65.77, qualifier="sec",
                    dimensions={'index':'2', 'process':'java', 'type':'average_all'})
    test.add_metric(name="CPU Idle", description="", value=58.42, qualifier="sec",
                    dimensions={'index':'3', 'process':'java', 'type':'average_all'})
    test.add_metric(name="CPU Idle", description="", value=58.10, qualifier="sec",
                    dimensions={'index':'4', 'process':'java', 'type':'average_all'})

    test.commit()
