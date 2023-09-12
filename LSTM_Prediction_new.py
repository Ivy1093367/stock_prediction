# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd    
import pandas_datareader as web   
import numpy as np      
import plotly.graph_objects as g   
import matplotlib.pyplot as plt                                   
from datetime import datetime as dt
from sklearn.preprocessing import MinMaxScaler                 
from keras.models import Sequential             
from keras.layers import Dense, Dropout, LSTM 

parameter = ''     # 使用者輸入股票代碼
companyname = ''   # 股票名稱
end_time = ''      # 欲查看時間

# string = "2022/01/01"
def run():
    
    start = dt(2012, 1, 1) # start date of data  回傳最近的交易日
    end = dt(2022, 1, 1)   # end date of data    回傳最近的交易日
    test_end = dt.strptime(end_time, '%Y/%m/%d')

    yf.pdr_override()
    data = web.get_data_yahoo(parameter, start, end)
    # print(data)
    # ['現在時間',  , '最高價' ,   '最低價', ' 開盤價 '   '收盤價 ',  ' 成交量 '  '調整後收盤價 ',]
    # [' Date ' ,   ,' High ',    ' Low ' , ' Open '    'Close ' , 'Volume '   'Adj Close ' ,]

    # 用股票代碼找公司名稱
    # sttock = y.Ticker(parameter)
    # company_name = sttock.info['shortName']
    # print(company_name)

    # stock = yf.download(parameter, start, end)
    stock = yf.download(parameter, period='30d', interval='1d')
    # ['現在時間',    ' 開盤價 ',  '最高價' , '最低價',   '收盤價 ',  "調整後收盤價 ', ' 成交量 ']
    # [' Date ' ,    ' Open ' ,  ' High ',  ' Low ' ,   'Close ' ,  'Adj Close ' , 'Volume ']
    data = data.reset_index()
    data['Volume'] //= 1000  
    stock = stock.reset_index()
    stock['Volume'] //= 1000  
    # stock_data.columns = ['現在時間', '開盤價', '最高價', '最低價', '收盤價', '調整後收盤價', '成交量']
    # stock_data['現在時間'] = p.to_datetime(stock_data['現在時間'].dt.strftime('%Y-%m-%d %H:%M'))

    result = g.Figure()
    result_k = g.Figure()

    result.add_trace(
        g.Bar(
            x = stock['Date'],
            y = stock['Volume'],
            marker_color = '#99ccff'
        )
    )

    result.update_layout(
        title = companyname + ' 成交量',
        hovermode = 'x',
        font = dict(
            size = 20
        )
    )

    result_k.add_trace(
        g.Candlestick(
            x = stock['Date'],
            open = stock['Open'],
            high = stock['High'],
            low = stock['Low'],
            close = stock['Close'],
            increasing_line_color = '#fd5047',
            increasing_fillcolor = '#f29696',
            decreasing_line_color = '#3d9970',
            decreasing_fillcolor = '#91c2b3'
        )
    )

    result_k.update_layout(
        title = companyname + ' K線',
        hovermode = 'x',
        xaxis_rangeslider_visible=False,
        font = dict(
            size = 20
        )
    )

    result.write_image("Vol.png", height=480, width=640)
    result_k.write_image("Candlestick.png", height=480, width=640)

    scaler = MinMaxScaler (feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
    prediction_days = 50
    x_train = []
    y_train = []
    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])  
        y_train.append(scaled_data[x, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Model building.
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))   # the prediction of the next closing value
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=36, batch_size=49)

    ''' Model testing with data already known.'''

    # Test data loading.
    test_start = dt(2022, 1, 1)    # start date of test data
    # test_end = dt.now()            # end date of test data
    # test_data = web.DataReader(company, 'yahoo', test_start, test_end)
    test_data = web.get_data_yahoo(parameter, test_start, test_end)
    actual_prices = test_data['Close'].values
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)  
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    # Making prediction on test data.
    x_test = []
    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)

    '''remake'''
    df = web.get_data_yahoo(parameter, start, test_start)
    # df = web.DataReader(company, 'yahoo', start, test_start)    # The end date "test_start" is the start date of the prediction.
    df1 = df.reset_index()['Close']                             # Use "close" price as before.
    df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))

    test_data1 = df1[len(df1)-len(test_data):len(df1),:1]
    x_input = test_data1[len(test_data1)-prediction_days:].reshape(1, -1)

    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()
    lst_output = []
    i = 0
    period = 40                                         # period in the future
    while (i < period):                                 # A logic. Future predictions based on the data before the end date. It can continously returned the predicted data, and use it to make another predicton.
        if (len(temp_input) > prediction_days):
            x_input = np.array(temp_input[1:])
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, prediction_days, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, prediction_days, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            lst_output.extend(yhat.tolist())
            i=i+1
    lst_output = scaler.inverse_transform(lst_output)
    day_pred = np.arange(0, period)
    plt.plot(day_pred, lst_output, color='blue', label='Predictions for the next ' + str(period) + ' days, based on the past data.')

    '''remake'''

    # Future prediction (tomorrow only).
    real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs + 1), 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)

    # Result ploting.
    plt.plot(actual_prices, color='black', label='Actual ' + parameter + ' Price')
    plt.plot(predicted_prices, color='green', label='Predicted ' + parameter + ' Price (for the next day)')
    plt.title(parameter)
    plt.xlabel('Time')
    plt.legend()
    plt.savefig('close.png')

if __name__ == '__main__':
    run()