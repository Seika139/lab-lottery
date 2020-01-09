# lab-lottery
This program will be used for Laboratory Assignment at Tokyo University department of  pharmacy on January 2020 which allows 3rd grade students to enter each laboratory.

# how to use

## データの初期化
```
$ python lab-lottery.py -i
```

## 配属システムの実行

実行する前に、google form の結果を `surveey/first_survey.txt` にコピペ。
```
$ pyhon lab-lottery -c
```

クリップボードにコピーされたデータを `input/student_data.xlsx` に貼り付ける。
これで第一希望の集計が完了するので、次のプログラムを実行できる。

```
$ python lab-lottery.py -e
```
