from typing import List

from matplotlib import pyplot as plt
from pandas import DataFrame

from app.lib.chart.chart_utils import plt_colors, financial_crises

plt.rcParams["font.family"] = 'NanumBarunGothic'
plt.rcParams["figure.figsize"] = (70, 20)
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['font.size'] = 40
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 3

COLORS = plt_colors
FINANCIAL_CRISES = financial_crises


def create_chart(dataframes: List[DataFrame], stock_names: List[str], **options):
    """
    :param dataframes
    :param stock_names
    :param **kwargs
        filesave        bool
            : 파일 저장?

        filename        str
            : 파일명

        chart_y_label   str
            : chart 내  y axis label
    TODO
        1. file_save
            1-1 파일 저장하는 util 만들어야 하고
            1-2 경로 같은 건 constants 파일로 한 곳에 지정하면 될 듯?
                거기다가 DB 설정도 같이
        2.
    """
    chart_y_label = options.get("chart_y_label", "Price")

    # create figure
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_ylabel(chart_y_label)

    lines = []

    # draw dataframes to plot
    for i, df in enumerate(dataframes):
        line = ax1.plot(df, color = COLORS(i), label = df)
        lines.append(line)

        # crisis gray 처리
        first, last = str(df.index[0]), str(df.index[-1])
        for crisis in FINANCIAL_CRISES():
            if first <= crisis[0] and crisis[1] <= last:
                ax1.axvspan(crisis[0], crisis[1], color = 'gray', alpha = 0.2)

    # legend 처리
    ax1.legend([x[0] for x in lines], stock_names, loc = 'upper left')

    plt.grid(True, which = 'both', axis = 'x', color = 'gray', alpha = 0.5, linestyle = '--')
    plt.show()
    plt.close(fig)
