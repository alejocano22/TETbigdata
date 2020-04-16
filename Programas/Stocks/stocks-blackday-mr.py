from mrjob.job import MRJob
from mrjob.step import MRStep


class BlackDay(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        data = [price, date]
        yield company, data

    def reducer(self, company, values):
        data = list(values)
        min_value = data[0]
        for value in data:
            if float(value[0]) < float(min_value[0]):
                min_value = value
        yield min_value[1], 1

    def day_reducer(self, day, value):
        yield None, (day, sum(value))

    def black_mapper(self, _, values):
        data = list(values)
        max_value = data[0]
        for i in range(len(data)):
            if int(data[i][1]) > int(max_value[1]):
                max_value = data[i]
        yield ("Black Day", max_value[1]), max_value[0]

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.day_reducer),
            MRStep(reducer=self.black_mapper)
        ]


if __name__ == '__main__':
    BlackDay.run()
