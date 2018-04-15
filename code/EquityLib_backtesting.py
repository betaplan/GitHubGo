import os, sys
# sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.abspath(''),"GitHubGo\code"))
sys.path.append(os.path.join(os.path.abspath(''),"GitHubGo\cn_stock_163"))
import EquityLib as el
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Market_test:
    def __init__(self, data_path = 'cn_stock_163'):
        self.folder = data_path
        self.cash = 100
        self.position = []
        self.action = []
        self.MTM = []

    def newPosition(self,action):
        try:
            temp = self.position[len(self.position)-1]
            temp = temp+action
            self.position.append(temp)
        except IndexError:
            self.position.append(action)

    def newAction(self,action):
        self.action.append(action)

    def tradingInfo(self):
        print('here is trading info')

    def newMtm(self,currentMTM):
        self.MTM.append(currentMTM)

    def calculateMtm(self, marketToday):
        MTM = 0
        temp = len(self.position[len(self.position) - 1])
        for _ in range(temp):
            if( _ == 0 ) :
                MTM += self.position[len(self.position) - 1][_]
            elif(self.position[len(self.position) - 1][_] != 0):
                MTM += self.position[len(self.position) - 1][_] * marketToday.iloc[_]
            else:
                MTM = MTM
                #         There is no action on this index
        return MTM


    def strategy(self, marketToday):
        activePosition = np.zeros(len(marketToday))
        try:
            # print(np.log(marketToday.iloc[3] / marketToday.iloc[6]))
            if(np.log(marketToday.iloc[3]/ marketToday.iloc[6])>0.05 and marketToday.iloc[3] != 0):
                activePosition[0] -= 1
                activePosition[3] += 1/marketToday.iloc[3]
            elif(np.log(marketToday.iloc[3]/ marketToday.iloc[6])<-0.05):
                activePosition[0] += self.position[-1][3] * marketToday.iloc[3]
                activePosition[3] = - self.position[-1][3]
        except ZeroDivisionError:
            return activePosition
        return activePosition

    def backTest(self):
        market_data = el.Market()
        # source = '163'
        testing_data = market_data.load_data_test(self.folder)
        testing_data = testing_data.sort_values('日期')
        activePosition = np.zeros(len(testing_data.iloc[0]))
        initialPosition = activePosition
        initialPosition[0] = self.cash
        self.newAction(initialPosition)
        self.newPosition(initialPosition)
        for index, row in testing_data.iterrows():
            if index == len(testing_data.index) - 1:
                print('index is ', index, 'row data is ', row)
            action = self.strategy(row)
            self.newAction(action)
            self.newPosition(action)
            self.newMtm(self.calculateMtm(row))
        self.plotMtmVsBenchmark(testing_data, [0,3])

    def plotMTM(self):
        plt.plot(self.MTM)
        plt.show()

    def plotMtmVsBenchmark(self,testing_data, plotReference):
        plotdata = testing_data.iloc[:,plotReference]
        for index, elem in enumerate(plotReference):
            try:
                plotdata.iloc[:, index] = plotdata.iloc[:, index].div(0.01*plotdata.iloc[0, index])
            except TypeError:
                print('Plot MTM vs benchmark')
        plotdata.loc[:, 'MTM'] = pd.Series(aa.MTM, index=plotdata.index)
        plotdata.set_index('日期', inplace=True)

        plt.figure()
        plotdata.plot()

    def moving_average(x, n, type='simple'):
        """
        compute an n period moving average.
        type is 'simple' | 'exponential'
        """
        x = np.asarray(x)
        if type == 'simple':
            weights = np.ones(n)
        else:
            weights = np.exp(np.linspace(-1., 0., n))
        weights /= weights.sum()
        a = np.convolve(x, weights, mode='full')[:len(x)]
        a[:n] = a[n]
        return a


aa = Market_test()
aa.backTest()
