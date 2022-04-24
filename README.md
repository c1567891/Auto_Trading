# Auto_Trading

使用training.csv作為訓練資料,並對其Normalize使資料都介於0~1之間

使用testing.csv做為測試資料,同樣對其Normalize使資料都介於0~1之間

建立一個unit為4的一層LSTM,並加入一層的dense layer,且input size為(1,1)表示只看前一天的資訊去預測

訓練LSTM

建立迴圈並將訓練好的LSTM去預測testing資料得到隔天股市開盤價

若隔天股市開盤價低於今日開盤價1元才買入,反之若高於今日開盤價1原則賣空

且過程中用slot紀錄目前持有股價的狀態,確保中途不會有非法行為的發生

最後將答案寫入output

執行時直接 py trader.py即可
