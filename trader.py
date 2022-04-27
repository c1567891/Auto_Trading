if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
	parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
	parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
	args = parser.parse_args()

	from turtle import shape
	import numpy as np
	from pandas import read_csv
	from keras.models import Sequential
	from keras.layers import Dense
	from keras.layers import LSTM
	from sklearn.preprocessing import MinMaxScaler
	from sklearn.metrics import mean_squared_error

	def createXY(dataset):
		dataX, dataY = [], []
		for i in range(len(dataset)-2):
			a = dataset[i:(i+1), 0]
			dataX.append(a)
			dataY.append(dataset[i + 1, 0])
		return np.array(dataX), np.array(dataY)

	# 載入訓練資料集
	train = read_csv(args.training, usecols=[0])
	train = train.values
	train = train.astype('float32')
	print(train.shape)
	# Normalize 資料
	scaler = MinMaxScaler(feature_range=(0, 1))
	train = scaler.fit_transform(train)
	# 載入測試資料集
	test = read_csv(args.testing, usecols=[0])
	test = test.values
	test = test.astype('float32')
	# Normalize 資料
	scaler = MinMaxScaler(feature_range=(0, 1))
	test = scaler.fit_transform(test)

	trainX, trainY = createXY(train)

	trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
	test = np.reshape(test, (test.shape[0], 1, test.shape[1]))

	# 建立及訓練 LSTM 模型
	model = Sequential()
	model.add(LSTM(4, input_shape=(1, 1)))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(trainX, trainY, epochs=10, verbose=2)
	# 存放答案
	ans=np.zeros(19)
	# 用來記錄目前股票狀態
	slot=0
	for i in range(len(ans)):
		if i == 0:
			testPredict = model.predict(test[i])
			testPredict=scaler.inverse_transform(testPredict)
			test[i]=scaler.inverse_transform(test[i])
			buy=test[i]-1
			sell=test[i]+1
			#預測價錢比今天開盤價低1元就買入
			if(testPredict<buy):
				ans[i]=1
				slot=1
			#預測價錢比今天開盤價高1元就賣空
			elif(testPredict>sell):
				ans[i]=-1
				slot=-1
			else:
				ans[i]=0
				slot=0
		else:
			testPredict = model.predict(test[i])
			testPredict=scaler.inverse_transform(testPredict)
			test[i]=scaler.inverse_transform(test[i])
			buy=test[i]-1
			sell=test[i]+1
			if(testPredict<buy):
				#若之前已買過股票則繼續持有該股票
				if(slot==1):
					ans[i]=0
				else:
					ans[i]=1
					slot=slot+1
			elif(testPredict>sell):
				if(slot==-1):
					#若之前已經賣空則繼續等待時機
					ans[i]=0
				else:
					ans[i]=-1
					slot=slot-1
			else:
				ans[i]=0
	import csv
	# 寫入答案
	with open(args.output, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for i in range(19):
			writer.writerow([int(ans[i])])