import json
import threading
import time
from simple_chalk import chalk, yellow, green, blue, bold



# Threading class
class myThread(threading.Thread):

    def __init__(self, func, threadArgs):
        threading.Thread.__init__(self)
        self._target = func
        self._args = threadArgs
        self.elapsedTime = 0

    def run(self):
        self.elapsedTime = self._target(*self._args, **self._kwargs)


# Decorator for recording time
def timerWrapper(functionToTime):
    def wrappedFunction(*args, **kwargs):
        startTime = time.time()
        functionToTime(*args, **kwargs)
        endTime = time.time()
        return endTime-startTime
    return wrappedFunction

# IOPS functions
@timerWrapper
def intOpsAdd(ops):
    for i in range(ops):
        i + 2

@timerWrapper
def intOpsSub(ops):
    for i in range(ops):
        i - 2

@timerWrapper
def intOpsMul(ops):
    for i in range(ops):
        i * 2

@timerWrapper
def intOpsDiv(ops):
    for i in range(ops):
        i // 2

# FLOPS functions
@timerWrapper
def fpOpsAdd(ops):
    for i in range(ops):
        i + 1.5

@timerWrapper
def fpOpsSub(ops):
    for i in range(ops):
        i - 1.5

@timerWrapper
def fpOpsMul(ops):
    for i in range(ops):
        i * 1.5

@timerWrapper
def fpOpsDiv(ops):
    for i in range(1,ops):
        i / 1.5

# Run all tests specified in main()
def runAllTests(inputs, numThreadsList, testFunctions):
    
    unthreadedReturn = {}
    threadedReturn = {}

    # Unthreaded

    # For all arithmetic functions
    for funcInd in range(len(testFunctions)):
        unthreadedReturn[funcInd] = []
        # For all number of operations
        for i in range (len(inputs)):
            ops = inputs[i]
            unthreadedReturn[funcInd].append(testFunctions[funcInd](ops))

    # Threaded

    # Run tests for range of number of threads
    for numThreads in numThreadsList:
        
        threadedReturn[numThreads] = {}

        # Run tests for all FLOPS and IOPS functions
        for funcInd in range(len(testFunctions)):
            threadedReturn[numThreads][funcInd] = {}

            # Run tests for range of number of operations
            for ops in inputs:
                threadedReturn[numThreads][funcInd][ops] = []
                threadList = []

                # Assign each thread a chunk of the workload/operations
                for i in range(1,numThreads+1):
                    tempThread = myThread(testFunctions[funcInd], [int(ops/numThreads)])
                    threadList.append(tempThread)
                    tempThread.start()

                # Wait for all threads to finish and record the elapsed time
                for i in threadList:
                    i.join()
                    threadedReturn[numThreads][funcInd][ops].append(i.elapsedTime)

    return (unthreadedReturn, threadedReturn)


def main():

    # # Specify tests for various numbers of threads
    # testThreads = [i for i in range(1,200)]
    testThreads = [1, 2, 4, 8]


    # Specify tests for various numbers of operations
    # KEEP THE RANGE (1,2) FOR SINGLE VALUE
    # testInputs = [int(i * 1e4) for i in range(1,10)]
    testInputs = [int(i * 1e4) for i in range(1,100)]

    totalOps = sum(testInputs)*4

    # Compile all FLOPS and IOPS functions into list and associated descriptions list
    testFunctions = [intOpsAdd, intOpsSub, intOpsMul, intOpsDiv, fpOpsAdd, fpOpsSub, fpOpsMul, fpOpsDiv]
    testFunctionDescriptions = ["IOPS Add", "IOPS Subtract", "IOPS Multiply", "IOPS Divide", "FLOPS Add", "FLOPS Subtract", "FLOPS Multiply", "FLOPS Divide"]


    # RUN ALL TESTS
    unthreadedResults, threadedResults = runAllTests(testInputs, testThreads, testFunctions)

    iopsUnthreadedAverage = 0
    flopsUnthreadedAverage = 0
    iopsThreadedAverage = {}
    for i in testThreads:
        iopsThreadedAverage[i] = 0
    flopsThreadedAverage = {}
    for i in testThreads:
        flopsThreadedAverage[i] = 0

    # Print unthreaded results to console
    print(chalk.blue.bold("Unthreaded Results:"))
    print(chalk.blue.bold("-------------------------------"))
    for i in range(len(testFunctions)):
        print(chalk.yellow.bold(testFunctionDescriptions[i] + " : "))
        for j in range(len(unthreadedResults[i])):
            if i < 4:
                iopsUnthreadedAverage += (testInputs[j] / unthreadedResults[i][j])
            else:
                flopsUnthreadedAverage += (testInputs[j] / unthreadedResults[i][j])
            print(chalk.yellow(str(testInputs[j]) + " operations took " + str(unthreadedResults[i][j]) + " seconds"))

        print(chalk.blue("-------------------------------"))

    print("\n\n")

    # Print threaded results to the console
    print(chalk.blue.bold("Threaded Results:"))
    print(chalk.blue.bold("-------------------------------"))
    for i in testThreads:
        print(chalk.green.bold(str(i) + " threads: "))
        for j in range(len(testFunctions)):
            print(chalk.yellow.bold(testFunctionDescriptions[j]) + " : ")
            for k in range(len(testInputs)):
                if j < 4:

                    iopsThreadedAverage[i] +=sum(threadedResults[i][j][testInputs[k]])
                else:
                    flopsThreadedAverage[i] += (sum(threadedResults[i][j][testInputs[k]]))
                print(chalk.yellow(str(testInputs[k]) + " operations took " + str(sum(threadedResults[i][j][testInputs[k]])) + " seconds"))
            print()
        print(chalk.blue("-------------------------------"))

    for i in iopsThreadedAverage:
        iopsThreadedAverage[i] = totalOps / iopsThreadedAverage[i]
        flopsThreadedAverage[i] = totalOps / flopsThreadedAverage[i]

    print("\n\n")

    # Print summary of results
    print(chalk.blue.bold("Summary of Results:"))
    print(chalk.blue.bold("-------------------------------"))
    print(chalk.yellow.bold("Unthreaded IOPS: ") + str(iopsUnthreadedAverage))
    print(chalk.yellow.bold("Unthreaded FLOPS: ") + str(flopsUnthreadedAverage))
    print(chalk.yellow.bold("Unthreaded Giga IOPS: ") + str(iopsUnthreadedAverage/1e9))
    print(chalk.yellow.bold("Unthreaded Giga FLOPS: ") + str(flopsUnthreadedAverage/1e9))
    print(chalk.blue("-------------------------------"))

    print(chalk.yellow.bold("Threaded IOPS: "))
    for i in testThreads:
        print(chalk.green(str(i) + " threads: ") + str(iopsThreadedAverage[i]))
        
    print(chalk.yellow.bold("Threaded FLOPS: "))
    for i in testThreads:
        print(chalk.green(str(i) + " threads: ") + str(flopsThreadedAverage[i]))

    print(chalk.yellow.bold("Threaded Giga IOPS: "))
    for i in testThreads:
        print(chalk.green(str(i) + " threads: ") + str(iopsThreadedAverage[i]/1e9))

    print(chalk.yellow.bold("Threaded Giga FLOPS: "))
    for i in testThreads:
        print(chalk.green(str(i) + " threads: ") + str(flopsThreadedAverage[i]/1e9))


    print(chalk.blue("-------------------------------"))


    # Convert results to JSON for formatting
    f = open("threadedResults.py", "w")

    f.write("threadedResults = ")
    f.write(json.dumps(threadedResults, indent = 4) )

    f.write("\niops = ")
    f.write(json.dumps(iopsThreadedAverage, indent = 4) )

    f.write("\nflops = ")
    f.write(json.dumps(flopsThreadedAverage, indent = 4) )
    f.close()


if __name__ == "__main__":
    main()