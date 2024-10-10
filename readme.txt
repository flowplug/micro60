1. Change crypfig.ini so curp is current
1.5 Set write_adaboost to n
2. Set live to n
3. put correct date ranges for training and validation.
4. Run market_model.py to create pickle files.
5. Run simp_train.py, which calls strun_train.py
to create training and validation csv files.
6.in /orange, first start procbuy.py, then procsell.py

