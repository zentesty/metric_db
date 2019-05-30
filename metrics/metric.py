



class Metric:
    def __init__(self, name, description, value, qualifier, dimensions):
        self.name = name
        self.description = description
        self.value = value
        self.qualifier = qualifier
        self.dimensions = dimensions


    def commit(self):
        pass

    class Dimensions:
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def commit(self):
            pass