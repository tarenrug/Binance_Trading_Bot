def SMACalc(values,length,switch=0):
    if switch==0: #If you want it to take SMA at the end of the vector
        if length <= len(values):
            SMA=(sum(values[len(values)-length:]))/float(length)
            return SMA
        else:
            print("Size of vector not long enough for simple moving average calculation")
            return
    elif switch==1: #If you want it to take the SMA at the beginning of the vector
        if length <= len(values):
            SMA=(sum(values[:length]))/float(length)
            return SMA
        else:
            print("Size of vector not long enough for simple moving average calculation")
            return
    else:
        print("Please choose switch number 0 or 1, for SMA calculation.")

if __name__=="__main__":
    print(SMACalc([10,2,3,4,5,6,7,8,9],3,1))