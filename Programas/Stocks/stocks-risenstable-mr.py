from mrjob.job import MRJob
from operator import itemgetter


class RisenStable(MRJob):

    def mapper(self, _, line):
        company, price, date = line.split(',')
        data = [price, date]
        yield company, data

    def reducer(self, company, values):
        data = list(values)
        data = sorted(data, key=itemgetter(1))
        for i in range(len(data)-1):
            if float(data[i+1][0]) < float(data[i][0]):
                return
        yield company, "Raise or stable all time."


if __name__ == '__main__':
    RisenStable.run()
