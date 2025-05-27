import sensor, image, time, lcd, gc, cmath
from maix import KPU

from modules import ybserial
import time

serial = ybserial()

lcd.init()                          # Init lcd display

# sensor.reset(dual_buff=True)      # improve fps
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

print("ready load model")

labels = ["red","green","school","walk","one","right","two","freeSpeed","left","limitSpeed","horn"]
anchor = (0.91, 1.16, 0.84, 1.78, 1.16, 1.38, 1.78, 1.31, 1.11, 4.28)

kpu = KPU()
kpu.load_kmodel('/sd/tinybit_AI.kmodel')

kpu.init_yolo2(anchor, anchor_num=(int)(len(anchor)/2), img_w=320, img_h=240, net_w=320 , net_h=240 ,layer_w=10 ,layer_h=8, threshold=0.4, nms_value=0.3, classes=len(labels)) 

msg_ = ""

while(True):
    gc.collect() #清内存

    clock.tick()
    img = sensor.snapshot()

    kpu.run_with_output(img)
    dect = kpu.regionlayer_yolo2()

    fps = clock.fps()

    if len(dect) > 0:
        for l in dect :
            img.draw_rectangle(l[0],l[1],l[2],l[3],color=(0,255,0))
            info = "%s %.3f" % (labels[l[4]], l[5])
            img.draw_string(l[0],l[1],info,color=(255, 255, 0),scale=1.5)
            print(info)
            del info

            #msg_ = labels[l[4]]
            idd = str(l[4]+1) #从1开始

    if len(dect) > 0:
       send_data ="$"+"09"+ idd+','+"#"
       time.sleep_ms(5)
       serial.send(send_data)
    else :
        serial.send("#")

    img.draw_string(0, 0, "%2.1ffps" %(fps),color=(0,60,255),scale=2.0)
    lcd.display(img)
