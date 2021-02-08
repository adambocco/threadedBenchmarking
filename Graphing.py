import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np

from threadedResults import threadedResults

avgs = []
for i in [*threadedResults]: # For all the thread numbers
    plt.xlabel("Threads")
    plt.ylabel("Time")
    plt.title("Average time to complete 1e9 IOPS operations")
    funcResults = []
    for j in [*threadedResults[i]]: # For all the functions
        if int(j) < 4:
            opResults = []
            for k in [*threadedResults[i][j]]: # For all the operations numbers
                opResults.append(sum(threadedResults[i][j][k])/len(threadedResults[i][j][k]))
            funcResults.append(sum(opResults)/len(opResults))
    avgs.append(sum(funcResults)/len(funcResults))

print(avgs)

x = np.array([1,2,4,8])
y = np.array(avgs)

plt.xlabel("Number of Threads")
plt.ylabel("Time")

#create basic scatterplot
plt.plot(x, y, 'o')

#obtain m (slope) and b(intercept) of linear regression line
m, b = np.polyfit(x, y, 1)

#add linear regression line to scatterplot 
plt.plot(x, m*x+b)

plt.show()


# plt.title("Operations vs Time for Multiple Threads (FLOPS)")

# plt.xlabel("Operations")
# plt.ylabel("Time")

# avgs = []
# numOfOperations = 0
# for i in [*threadedResults]: # For all the thread numbers
#     print(i)
#     ops = []
#     avg = []
#     for j in [*threadedResults[i]]: # For all the functions
#         if int(j) > 4:
#             for k in [*threadedResults[i][j]]:
#                 numOfOperations = len(threadedResults[i][j])
                
#                 ops.append(k) if k not in ops else True
#                 avg.append(sum(threadedResults[i][j][k])/len(threadedResults[i][j][k]))
#     newavgs = [0]*len(ops)
#     for t in range(len(avg)):
#         newavgs[t % len(ops)] += avg[t]
#     for o in range(len(newavgs)):
#         newavgs[o] = newavgs[o]/4

#     for v in range(len(ops)):
#         ops[v] = int(ops[v])

    
#     x = np.array(ops)
#     y = np.array(newavgs)

#     #create basic scatterplot
#     plt.plot(x, y, 'o',marker=".", markersize=3)

#     #obtain m (slope) and b(intercept) of linear regression line
#     m, b = np.polyfit(x, y, 1)
#     print("Standard deviation: ", np.std(y))
#     #add linear regression line to scatterplot 
#     plt.plot(x, m*x+b, label=str(i))


# plt.legend(fancybox=True, title="# of Threads")
# plt.show()

