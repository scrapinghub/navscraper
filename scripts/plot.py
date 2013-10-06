"""Script to plot output of the spiders."""
import json
import matplotlib.pyplot as plt
import pandas as pd


def read_items(filename):
    for line in open(filename):
        yield json.loads(line)


def main(filename):
    series = []
    for item in read_items(filename):
        series.append(
            pd.TimeSeries(item['values'], index=item['dates'], name=item['fund_id'])
        )

    df = pd.concat(series, axis=1)
    df.plot()

    plt.show()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print 'Usage: python %s items.jl' % sys.argv[0]
        sys.exit(1)

    main(sys.argv[1])
