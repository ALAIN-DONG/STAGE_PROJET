import pyb
import ReadOnlyOneSensor
import lighting
from pyb import Pin

lighting.init_light()

lighting.Light_Mian_Start()
pyb.delay(1000)

ReadOnlyOneSensor.Read_Only_One_Sensor("TOF1", "X11", False)

lighting.Light_EnRepos()

