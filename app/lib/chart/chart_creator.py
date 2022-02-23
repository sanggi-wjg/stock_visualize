from matplotlib import pyplot as plt
from pandas import DataFrame

plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams["figure.figsize"] = (60, 20)
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['font.size'] = 45
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 2


class ChartCreator:

    def __init__(self, start_date: str, end_date: str, chart_term: int = 10):
        self.start_date = start_date
        self.end_date = end_date
        self.chart_term = chart_term

    def create(self, df: DataFrame, label: str, file_save: bool = False):
        """
        TODO
            1. file_save
                1-1 파일 저장하는 util 만들어야 하고
                1-2 경로 같은 건 constants 파일로 한 곳에 지정하면 될 듯?
                    거기다가 DB 설정도 같이
            2.
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        ax1.set_ylabel(label)
        line1 = ax1.plot(df, color = 'blue', label = "Price")

        plt.show()
        plt.close(fig)
