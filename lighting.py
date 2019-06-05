import pyb
import math
from pyb import Pin, Timer

FLAG_TOGGLE_FOR_STORAGE = False


def init_light():
    leds = [pyb.LED(i) for i in range(1, 5)]
    for l in leds:
        l.off()


def toggle_light_limite_old(num, freq, timelimite):
    """num is the number of the light, must in [0, 1, 2, 3]"""
    '''freq is the frequency in Hz'''
    '''timelimite is the limitation of the execute of this function, in seconds'''
    leds = [pyb.LED(i) for i in range(1, 5)]
    n = 1
    freq = (1000 // freq)
    times = (1000 * timelimite / freq)
    while True:
        leds[num].toggle()
        pyb.delay(freq) # the index must be integer
        n = n + 1
        if n > times:
            break


def turnon_light(num):
    leds = [pyb.LED(i) for i in range(1, 5)]
    leds[num].on()


def turnoff_light(num):
    leds = [pyb.LED(i) for i in range(1, 5)]
    leds[num].off()


def toggle_light_once(num):
    leds = [pyb.LED(i) for i in range(1, 5)]
    leds[num].off()


def toggle_breathing_limite(freq, timelimite):
    presis = 1000  # toggle one time in one second
    freq = freq/2  # freq for function 'sin()', because of 'fabs()'
    t0 = 1 / freq  # period of the 'sin()', the whole time of the 'sin()'
    t00 = t0 / presis  # division of the period, more detailed t00 = 0.002
    for i in range(0, (presis * freq * timelimite)):  # 'presis * freq' is just for one second
        # index = math.floor(math.fabs((255 * math.sin(i/presis*2*math.pi))))
        index = math.floor((255 * math.sin(i / presis * 2 * math.pi)))
        if index <= 0:
            index = 0
        led4 = pyb.LED(4)
        led4.intensity(index)
        pyb.delay(math.floor(t00 * 1000))  # delay of each cycle for t00 milliseconds\

def toggle_breathing(freq):
    """breath forever if don't push the button"""
    presis = 1000  # toggle one time in one second
    freq = freq/2  # freq for function 'sin()', because of 'fabs()'
    t0 = 1 / freq  # period of the 'sin()', the whole time of the 'sin()'
    t00 = t0 / presis  # division of the period, more detailed t00 = 0.002
    i = 0
    led4 = pyb.LED(4)
    while True:
        index = math.floor((255 * math.sin(i / presis * 2 * math.pi)))
        if index <= 0:
            index = 0
        led4.intensity(index)
        pyb.delay(math.floor(t00 * 1000))  # delay of each cycle for t00 milliseconds\
        i += 1

        sw = pyb.Switch()
        if sw.value():
            toggle_light(3,4)
            pyb.delay(1500)
            toggle_light_stop(3)
            break


def Link_LED_Timer(num_LED):
    """link the LEDs and the timers"""
    '''because of the internal structure, some timers are unable to be used'''
    '''so here define:'''
    '''LED1 with Timer1'''
    '''LED2 with Timer4'''
    '''LED3 with Timer9'''
    '''LED4 with Timer10'''
    num_Timer = 1
    if num_LED == 0:
        num_Timer = 1
    elif num_LED == 1:
        num_Timer = 4
    elif num_LED == 2:
        num_Timer = 9
    elif num_LED == 3:
        num_Timer = 10
    else:
        pass
    return num_Timer


def toggle_light(num_light, frequency):
    """toggle the LED given, without limite times"""
    '''num is the number of the light, must in [0, 1, 2, 3]'''
    '''the lights toggle forever acquiescently'''
    '''freq is the frequency in Hz'''
    leds = [pyb.LED(i) for i in range(1, 5)]
    tim = pyb.Timer(Link_LED_Timer(num_light), freq=frequency)
    tim.callback(lambda t: leds[num_light].toggle())


def toggle_light_stop(num_light):
    tim = pyb.Timer(Link_LED_Timer(num_light))
    print("the counter number of the timer", Link_LED_Timer(num_light), " is ", tim.counter())
    tim.deinit()
    leds = [pyb.LED(i) for i in range(1, 5)]
    leds[num_light].off()


# def Light_EnTrainDeEcrire(flag):
#     if flag == False:
#         toggle_light(0, 10)
#
#
# def Light_FinDeEcrire(flag):
#     if flag == True:
#         toggle_light_stop(0)


def Light_EnTrainDeEcrire():
    global FLAG_TOGGLE_FOR_STORAGE
    if FLAG_TOGGLE_FOR_STORAGE is False:
        toggle_light_stop(1)
        toggle_light(0, 10)
    FLAG_TOGGLE_FOR_STORAGE = True


def Light_Pause():
    global FLAG_TOGGLE_FOR_STORAGE
    if FLAG_TOGGLE_FOR_STORAGE is True:
        toggle_light_stop(0)
        toggle_light(1, 10)
    FLAG_TOGGLE_FOR_STORAGE = False


def Light_FinDeEcrire():
    global FLAG_TOGGLE_FOR_STORAGE
    toggle_light_stop(1)
    toggle_light_stop(0)
    FLAG_TOGGLE_FOR_STORAGE = False


def Light_EnRepos():
    toggle_breathing(1)


def Light_Script_Ready():
    flag = True
    while True:
        if flag:
            toggle_light(2, 6)
            flag = False

        sw = pyb.Switch()
        if sw.value():
            toggle_light_stop(2)
            Light_Feedback_Button()
            pyb.delay(200)
            break


def Light_Mian_Start():
    toggle_light(0, 1)
    toggle_light(1, 2)
    toggle_light(2, 3)
    toggle_light(3, 4)
    pyb.delay(2000)
    for i in range(0, 4):
        toggle_light_stop(i)


def Light_Test_Ok(times):
    toggle_light(1, 4)
    pyb.delay(math.floor(1000*times/2))
    toggle_light_stop(1)

def Light_Test_Notok(times):
    toggle_light(0, 4)
    pyb.delay(math.floor(1000*times/2))
    toggle_light_stop(0)


def Light_Feedback_Button():
    sw = pyb.Switch()
    if sw.value():
        toggle_light(2, 20)
        pyb.delay(1000)
        toggle_light_stop(2)




# tim = pyb.Timer(4)
# tim.init(freq=0.5)
# tim.callback(lambda t: pyb.LED(1).toggle())


#### first version of the blue breath light ####
# def toggle_breathing(freq, timelimite):
#     presis = 1000  # toggle one time in one second
#     freq = freq/2  # freq for function 'sin()', because of 'fabs()'
#     t0 = 1 / freq  # period of the 'sin()', the whole time of the 'sin()'
#     t00 = t0 / presis  # division of the period, more detailed t00 = 0.002
#     for i in range(0, (presis * freq * timelimite)):  # 'presis * freq' is just for one second
#         # index = math.floor(math.fabs((255 * math.sin(i/presis*2*math.pi))))
#         index = math.floor((255 * math.sin(i / presis * 2 * math.pi)))
#         if index <= 0:
#             index = 0
#         led4 = pyb.LED(4)
#         led4.intensity(index)
#         pyb.delay(math.floor(t00 * 1000))  # delay of each cycle for t00 milliseconds\
