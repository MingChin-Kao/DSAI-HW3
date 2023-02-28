
# You should not modify this part.
import pandas as pd
import datetime

def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return

def secret_trade(date):
    return_data = []
    for i in range(50):
        temp = [date, "sell", 1000000, 1000000]
        return_data.append(temp)
    return return_data

def normal_trade(date):
    return_data = []
    now = pd.to_datetime(date, format="%Y/%m/%d %H:%M:%S")
    for i in range(24):
        if i == 0:
            temp = [datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S'), "sell", 10000, 10000]
        else:
            temp = [datetime.datetime.strftime(now,'%Y-%m-%d %H:%M:%S'), "sell", 0.01, 0.01]
            now = now + datetime.timedelta(hours=1)
            return_data.append(temp)
    return return_data


if __name__ == "__main__":
    args = config()

    data = pd.read_csv(args.generation)
    bidresult_data = pd.read_csv(args.bidresult)
    bidresult_data = bidresult_data.dropna()

    last_day = data["time"][data.shape[0]-1]
    last_day_time = pd.to_datetime(last_day, format="%Y-%m-%d %H:%M:%S")

    predict_date = last_day_time + datetime.timedelta(hours=1)
    # print("predict date is ", predict_date)
    output_date = datetime.datetime.strftime(predict_date,'%Y-%m-%d %H:%M:%S')

    if bidresult_data.empty:
        print("is empty")
        trade_strategy = secret_trade(output_date)
    else:
        print('is not empty')
        trade_strategy = normal_trade(output_date)

    output(args.output, trade_strategy)
    #output(args.output, trade_strategy)
    #data = [[output_date, "buy", 2, 5]]

    # data = [["2018-01-01 00:00:00", "buy", 2.5, 3],
    #         ["2018-01-01 01:00:00", "sell", 3, 5]]
    #
