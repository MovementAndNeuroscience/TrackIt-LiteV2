#CalibrationConductor
#runs the calibration game and stores the calibration value 
import pygame 
from win32api import GetSystemMetrics
import dearpygui.dearpygui as dpg
import VoltageConverter
import daqmxlib

def RunCalibration(dpg, calibrationDataClass):

    pygame.init()
    #Setup calibration space and such 
    gameDisplay = pygame.display.set_mode((GetSystemMetrics(0),GetSystemMetrics(1)))
    pygame.display.set_caption('Calibration')

    bl = (0,0,0)
    w = (255,255,255)
    r = (255,0,0)
    g = (0,255,0)
    b = (0,0,255)

    clock = pygame.time.Clock()
    inputMode = dpg.get_value("device")
    calibrated = False
    calibrationStarted = False
    calibrationCounter = 0
    reader = daqmxlib.Reader()

    font = pygame.font.Font('freesansbold.ttf', 40)
    introText = font.render('Press Return to Start Calibration', True, w)
    text_1 = font.render('1', True, w)
    text_2 = font.render('2', True, w)
    text_3 = font.render('3', True, w)
    text_calibrate = font.render('CALIBRATE!', True, w)
    text_motivation = font.render('FULL THROTTLE!', True, w)
    text_done = font.render('DONE!', True, w)

    textRect = introText.get_rect()
    text_1_Rect = text_1.get_rect()
    text_2_Rect = text_2.get_rect()
    text_3_Rect = text_3.get_rect()
    text_cali_rect = text_calibrate.get_rect()
    text_moti_rect = text_motivation.get_rect()
    text_done_rect = text_done.get_rect()

    textpos = (GetSystemMetrics(0) // 2 ,GetSystemMetrics(1) //20 )
    textRect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2)
    text_1_Rect.center = textpos
    text_2_Rect.center = textpos
    text_3_Rect.center = textpos
    text_cali_rect.center = textpos
    text_moti_rect.center = textpos
    text_done_rect.center = textpos

    def drawPlayer(ypos):
        pygame.draw.circle(gameDisplay, r, (GetSystemMetrics(0)/2, ypos), 5)

    #running calibtation
    while not calibrated:

        if(calibrationStarted == True):
        #resets image
            calibrationCounter += clock.get_time()
            gameDisplay.fill(bl)

            if inputMode == "Mouse":
                mx,my=pygame.mouse.get_pos()
                drawPlayer(my)
                if(my > calibrationDataClass.GetMaxInput()):
                    calibrationDataClass.SetMaxInput(my)
            
            if inputMode == "USB/ADAM":
                ypos=0 #USB/ADAM input goes here 
                drawPlayer(ypos)
                if(ypos > calibrationDataClass.GetMaxInput()):
                    calibrationDataClass.SetMaxInput(ypos)

            if inputMode == "NIDAQ":
                voltage = reader.read()[0]
                print("Voltage : " + str(voltage))
                calibrationDataClass = VoltageConverter.Calibrate_minAndMaxVoltage(voltage, calibrationDataClass)
                ypos=VoltageConverter.get_px_from_voltage(voltage,calibrationDataClass.GetMaxVoltage(), calibrationDataClass.GetMinVoltage())
                #print("ypos : "+ str(ypos))
                drawPlayer(ypos)
                if(ypos > calibrationDataClass.GetMaxInput()):
                    calibrationDataClass.SetMaxInput(ypos)

            if(calibrationCounter < 1000):
                gameDisplay.blit(text_3, text_3_Rect)
            elif(calibrationCounter < 2000):
                gameDisplay.blit(text_2, text_2_Rect)
            elif(calibrationCounter < 3000):
                gameDisplay.blit(text_1, text_1_Rect)
            elif(calibrationCounter < 5000):
                gameDisplay.blit(text_calibrate, text_cali_rect)
            elif(calibrationCounter < 6000):
                gameDisplay.blit(text_motivation, text_moti_rect)
            elif(calibrationCounter < 8000):
                gameDisplay.blit(text_done, text_done_rect)
            elif(calibrationCounter < 8500):
                calibrated = True                     

        else:
            gameDisplay.blit(introText, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calibrated = True
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

                if event.key == pygame.K_RETURN:
                    calibrationStarted = True

        pygame.display.update()
        clock.tick(120)
    pygame.quit()