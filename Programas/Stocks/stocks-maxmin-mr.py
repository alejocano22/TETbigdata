from mrjob.job import MRJob


class MaxMin(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        data = [price, date]
        yield company, data

    def reducer(self, company, values):
        data = list(values)
        min_value = data[0]
        max_value = min_value
        for value in data:
            if float(value[0]) < float(min_value[0]):
                min_value = value
            if float(value[0]) > float(max_value[0]):
                max_value = value
        yield company, (min_value, max_value)


if __name__ == '__main__':
    MaxMin.run()
