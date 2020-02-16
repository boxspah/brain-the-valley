def clamp(x,upper,lower):
    if x>upper:
        return upper
    if x<lower:
        return lower
    return x

def scale(x,a,b,c,d):
    return (x-a) * (d-c)/(b-a) + c

def sma(data, window):
    """
    Calculates Simple Moving Average
    http://fxtrade.oanda.com/learn/forex-indicators/simple-moving-average
    """
    if len(data) < window:
        return None
    return [sum(x for x,y in data[-window:])/window, sum(y for x,y in data[-window:])/window]


def ema_filter(curr,prev,weight):
    EWMF = []
    for c,p,w in zip(curr,prev,weight):
        EWMF.append((1-w)*p+w*c)
    return EWMF
# data = [76.09, 69.6, 66.51, 80.28, 70.32, 75.82, 74.24, 72.5, 64.51, 72.61, 71.03, 67.89, 67.1, 72.49, 71.05, 67.28, 73.22, 73.72, 77.05, 74.25, 66.81, 69.8, 66.88, 72.04, 70.71, 72.89, 73, 71.9, 67.29, 71.42, 69.31, 70.63, 77.65, 71.62, 71.28, 68.79, 66.76, 72.83, 70.75, 75.58, 68.63, 74.54, 69.38, 74.73, 70.1, 64.83, 73.31, 67.89, 71.86, 74.27, 72.44, 73.43, 69.07, 68.94, 76.1, 73.24, 70.13, 69.46, 70.42, 76.45, 71.85, 71.72, 73.64, 66.78, 73.3, 74.22, 74.63, 74.31, 72.23, 69.77, 66.87, 67.74, 75.71, 76.85, 76.86, 72.31, 70.86, 71.33, 64.67, 69.85, 69.68, 71.01, 71.38, 71.82, 75.15, 70.45, 73.81]
# prev = data[0]
# for point in data[1:]:
#     print(prev)
#     prev = ema_filter(point, prev, 0.05)
