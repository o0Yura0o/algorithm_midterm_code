import numpy as np
import time     
import statistics
import matplotlib.pyplot as plt
        
START_WITH = 10 #n從多少開始
ITER_TIMES = 100  #疊代次數(要讓n增加幾次)
INCREASING_INTERVAL = 10  #n每次增加的幅度
#以題目8.a要求設置由上到下為10、100、10
#以題目8.c要求設置由上到下為100、990、10
COUNTIN_SORT_TIME = False #是否計入二元搜尋及費氏搜尋所需預先排序資料的時間

def generateTask(n): #根據n(數組大小)生成不重複之隨機整數清單S以及隨機數x，範圍皆介於0~10*n
  S = np.random.choice(10*n, size=n, replace=False)
  x = np.random.randint(10*n)
  return S, x

def linearSearch(S, x): #線性搜尋演算法，給予清單S及目標x
  for i in range(len(S)):
    if S[i] == x:
      return i
  return -1

def binarySearch(S, x): #二元搜尋演算法，給予清單S及目標x
  if COUNTIN_SORT_TIME:
    S = sorted(S)
  low = 0
  high = len(S)-1
  while low <= high:
    mid = low + (high - low)//2
    if S[mid] == x:
      return mid
    elif S[mid] < x:
      low = mid + 1
    else:
      high = mid - 1
  return -1

def fibonacciSearch(S, x):  #費氏搜尋演算法，給予清單S及目標x
  if COUNTIN_SORT_TIME:
    S = sorted(S)
  size = len(S) 
  start = -1 
  f0 = 0
  f1 = 1
  f2 = 1
  while(f2 < size):
    f0 = f1
    f1 = f2
    f2 = f1 + f0
  while(f2 > 1):
    index = min(start + f0, size - 1)
    if S[index] < x:
      f2 = f1
      f1 = f0
      f0 = f2 - f1
      start = index
    elif S[index] > x:
      f2 = f0
      f1 = f1 - f0
      f0 = f2 - f1
    else:
      return index
  if f1 and S[size - 1] == x:
    return size - 1
  return -1

#準備用以紀錄各演算法在不同n下mean execution time的清單
#i為清單的index，其中 START_WITH + i*INCREASING_INTERVAL 即為位於該index之數據基於的n大小
#數據單位為秒
LS_MET = [0]*ITER_TIMES
BS_MET = [0]*ITER_TIMES
FS_MET = [0]*ITER_TIMES
for i in range(ITER_TIMES): #進行疊代以套用不同n
  n = START_WITH + i*INCREASING_INTERVAL
  #用來記錄各演算法每個的task執行時間
  LS_execution_time = []
  BS_execution_time = []
  FS_execution_time = []
  for t in range(5):  #每個n執行5次task
    S, x = generateTask(n)
    start = time.process_time()
    LS_result = linearSearch(S, x)
    end = time.process_time()
    LS_execution_time.append(end - start)
    if not COUNTIN_SORT_TIME:
      S = sorted(S) #二元搜尋及費氏搜尋需要排列過的資料，因題目無特別要求，故在此預設不計入排序時間，如須計入可透過COUNTIN_SORT_TIME參數調整
    start = time.process_time()
    BS_result = binarySearch(S, x)
    end = time.process_time()
    BS_execution_time.append(end - start)
    start = time.process_time()
    FS_result = fibonacciSearch(S, x)
    end = time.process_time()
    FS_execution_time.append(end - start)
  #將五次成果取平均存入紀錄mean execution time的清單中
  LS_MET[i] = statistics.mean(LS_execution_time)
  BS_MET[i] = statistics.mean(BS_execution_time)
  FS_MET[i] = statistics.mean(FS_execution_time)

#可以透過mean execution time清單存取各個n下的時間記錄，這裡節省版面只列出最後一個(最大的n下的紀錄)
print(LS_MET[-1])
print(BS_MET[-1])
print(FS_MET[-1])

#繪製圖表(折線圖)，紅色為線性搜尋；藍色為二元搜尋；綠色為費氏搜尋
X = [START_WITH+i*INCREASING_INTERVAL for i in range(ITER_TIMES)]
plt.plot(X, LS_MET, color='r', marker='o', linestyle='--', linewidth=2, markersize=3)
plt.plot(X, BS_MET, color='b', marker='o', linestyle='--', linewidth=2, markersize=3)
plt.plot(X, FS_MET, color='g', marker='o', linestyle='--', linewidth=2, markersize=3)
plt.xlabel('the size of n',fontsize=10)
plt.ylabel('time',fontsize=10)
plt.show()
