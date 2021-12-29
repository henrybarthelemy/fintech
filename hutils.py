## Calculating sucess of a strategy
def calc_sucess(pclist, strategyname, stockname):
    gains = 0
    ng = 0 #number of gains
    losses = 0
    nl = 0 #number of losses
    totalR = 1

    for i in pclist:
        if(i>0):
            gains += i
            ng += 1
        else:
            losses += i
            nl += 1 
        totalR = totalR * ((i / 100) + 1)

    totalR = round((totalR - 1) * 100, 2)

    if(ng > 0):
        avgGain = gains / ng
        maxR = str(max(pclist))
    else:
        avgGain = 0
        maxR = "undefined"

    if(nl > 0):
        avgLoss = losses / nl
        maxL = str(min(pclist))
        ratio=str(-(avgGain / avgLoss))
    else:
        avgLoss = 0
        maxL = "undefined"
        ratio = "infinite"

    if(ng > 0 or nl > 0):
        battingAverage = ng / (ng + nl)
    else:
        battingAverage = 0

    #Console Printing Output Summary
    print("----- ANALYSIS OF " + strategyname + " -----")
    print("Statistics results for " + stockname + " going back to " + str(df.index[0]) + ", Sample size: " + str(ng + nl)) 
    print("Batting Average: " + str(battingAverage))
    print("Gain/Loss ratio: " + str(ratio))
    print("Average Gain: " + str(avgGain))
    print("Average Loss: " + str(avgLoss))
    print("Max Return: " + str(maxR))
    print("Max Loss: " + str(maxL))
    print("Total returns over " + str(ng + nl) + " trades: " + str(totalR) + "%")
    print()