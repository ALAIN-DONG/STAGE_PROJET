import pyb
from ucollections import OrderedDict
import utime
import math

def MovingAvg(size=10):
    values = [0.]*size
    pos = 0
    new_val = 0.0
    while True:
        mean = 0.0
        for v in values:
            mean = mean + v
        mean = mean / size
        new_val =  yield(mean)
        values[pos] = new_val
        pos = (pos+1)%size

def Derivative():
    prev_val = 0.0
    derivative = 0.0
    while True:
        new_val =  yield(derivative)
        derivative = new_val-prev_val
        prev_val = new_val


def adc_gen_burst(pin,delay=None):
    buf = bytearray(500)                # create a buffer of 100 bytes
    sample = 0
    start = utime.ticks_ms()
    tim = pyb.Timer(4, freq=100) 
    adc = pyb.ADC(pin)
    while True:
        adc.read_timed(buf, tim)
        for val in buf:                     # loop over all values
            value = adc.read()
            hist = OrderedDict()
            hist['#'] = sample
            hist['adc'] = value
            hist['ms']= utime.ticks_diff(utime.ticks_ms(),start)
            yield (sample,value,hist)
            sample += 1

def adc_gen(pin,delay=None):
    sample = 0
    adc = pyb.ADC(pin)
    ms_time = utime.ticks_ms()
    while True:
        if (delay is None) or (utime.ticks_diff(utime.ticks_ms(),ms_time) > delay):
            ms_time = utime.ticks_ms()
            value = adc.read()
            hist = OrderedDict()
            hist['#'] = sample
            hist['adc'] = value
            yield (sample,value,hist)
            sample += 1

def avg_filter(g,size=10):
    values = [0.] * size
    pos = 0
    for sample,new_val,hist in g:
        mean = 0.0
        for v in values:
            mean = mean + v
        mean = mean / size
        hist['avg'] = mean
        yield (sample,mean,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def thresh_filter(g,threshold=.5,greater_than=True):
    for sample,new_val,hist in g:
        if greater_than:
            t = new_val>threshold
        else:
            t = new_val<threshold
        hist['thresh'] = t
        yield (sample,t,hist)
        
def norm_filter(g,size=10):
    values = [0.] * size
    pos = 0
    trig = 0
    for sample,new_val,hist in g:
        min_val = new_val
        max_val = new_val
        for v in values:
            if v>max_val:
                max_val = v
            if v<min_val:
                min_val = v

        norm = (new_val-min_val)/(max_val-min_val+1)
        hist['norm'] = norm
        hist['max'] = max_val
        hist['min'] = min_val
        yield (sample,norm,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def hysteresis_filter(g,size=10,th_high=.9,th_low=.5):
    values = [0.] * size
    pos = 0
    trig = 0
    for sample,new_val,hist in g:
        min_val = new_val
        max_val = new_val
        for v in values:
            if v>max_val:
                max_val = v
            if v<min_val:
                min_val = v

        norm = (new_val-min_val)/(max_val-min_val+1)
        if trig:
            if norm<=th_low:
                trig = 0
        else:
            if norm>=th_high:
                trig = 1
        hist['trig'] = trig
        hist['norm'] = norm
        hist['max'] = max_val
        hist['min'] = min_val
        yield (sample,trig,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def mean_filter(g,size=10):
    values = [0.] * size
    pos = 0
    for sample,new_val,hist in g:
        mean = 0
        for v in values:
            mean += v
        mean /= size
        hist['mean'] = mean
        yield (sample,mean,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def mean_std_filter(g,size=10):
    values = [0.] * size
    pos = 0
    for sample,new_val,hist in g:
        mean = 0
        for v in values:
            mean += v
        mean /= size
        hist['mean'] = mean
        std = 0
        for v in values:            
            std += (v-mean)*(v-mean)
        std /= size
        hist['std'] = math.sqrt(std)
        yield (sample,mean,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def median_filter(g,size=10):
    values = [0.] * size
    med_pos = int(size / 2)
    pos = 0
    for sample,new_val,hist in g:
        median = sorted(values)[med_pos]
        hist['med'] = median
        yield (sample,median,hist)
        values[pos] = new_val
        pos = (pos + 1) % size

def diff_filter(g,size=10):
    values = [0.] * size
    pos = 0
    for sample,new_val,hist in g:
        diff = values[-1]-values[0]
        hist['diff'] = diff
        yield (sample,diff,hist)
        values[pos] = new_val
        pos = (pos + 1) % size


def detrend_filter(g,size=10):
    values = [0.] * size
    pos = 0
    for sample,new_val,hist in g:
        mean = 0.0
        for v in values:
            mean = mean + v
        mean = mean / size
        hist['detrend'] = new_val-mean
        yield (sample,new_val-mean,hist)
        values[pos] = new_val
        pos = (pos + 1) % size


def butterworth_filter(g):
    values = [0.,.0]
    for sample,new_val,hist in g:
        values[0] = values[1]
        values[1] = (2.452372752527856026e-1 * new_val) + (0.50952544949442879485 * values[0])
        bwth = values[0] + values[1]
        hist['bwth'] = bwth
        yield (sample,bwth,hist)
        

def bpm_filter(g, size=10):
    values = [utime.ticks_us()] * size
    pos = 0
    current = False
    delta = 0
    for sample, new_val, hist in g:
        if not current and new_val:  # rising edge
            current = True
            t = utime.ticks_us()
            values[pos] = t
            next_pos = (pos + 1) % size
            delta = utime.ticks_diff(t,values[next_pos])
            pos = next_pos
        else:
            if not new_val:  # faling edge 
                current = False

        hist['bpm'] = 60e6 * size / (delta + 1)
        yield (sample, delta, hist)



def derivative_filter(g):
    prev_val = 0.0
    derivative = 0.0
    for sample,new_val,hist in g:
        hist['deriv'] = derivative
        yield sample,derivative,hist
        derivative = new_val-prev_val
        prev_val = new_val

def decimate_filter(g,dec=2):
    count = 0
    for sample,new_val,hist in g:
        if count == 0:
            hist['dec'] = new_val
            yield sample,new_val,hist
        count = (count + 1) % dec

def hold_filter(g,size):
    count = 0
    prev_val = 0
    for sample,new_val,hist in g:
        if count == 0:
            hist['hold'] = new_val
            yield sample,new_val,hist
            prev_val = new_val
        else:
            hist['hold'] = prev_val
            yield sample,prev_val,hist
        count = (count + 1) % size

def freq_filter(g):
    freq = 0
    prev_us = utime.ticks_us()
    for sample, new_val, hist in g:
        delta = utime.ticks_diff(utime.ticks_us(),prev_us)
        prev_us = utime.ticks_us()
        hist['us'] = delta
        yield sample,delta, hist

def resample_filter(g,ticks_us):
    prev_us = utime.ticks_us()
    for sample, new_val, hist in g:
        delta = utime.ticks_diff(utime.ticks_us(), prev_us)
        if delta >= ticks_us:
            prev_us = utime.ticks_us()
            hist['resample'] = delta
            yield sample, delta, hist

def example():
    g = adc_gen(10)
    for s,v,h in resample_filter(freq_filter(avg_filter(median_filter(g,10),10)),1000000):
        print(h)

def example_old():
    m1 = MovingAvg(100)
    next(m1)

    m2 = MovingAvg(100)
    next(m2)

    d1 = Derivative()
    next(d1)

    adc = pyb.ADC(pyb.Pin.board.X19)
    while True:
        v = adc.read()
        v1 = m1.send(v)
        v2 = m2.send(v1)
        v3 = d1.send(v1)
        print('%4d %6.1f %6.1f %6.1f'%(v,v1,v2,v3))

