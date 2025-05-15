import numpy as np

def CalculateVToNCoeffecient(dpg):
    firstMeasure = dpg.get_value("firstTrackItload")
    firstKg = dpg.get_value("firstKgLoad")
    secondMeasure = dpg.get_value("secondTrackItload")
    secondKg = dpg.get_value("secondKgLoad")
    thirdMeasure = dpg.get_value("thirdTrackItload")
    thirdKg = dpg.get_value("thirdKgLoad")
    fourthMeasure = dpg.get_value("fourthTrackItload")
    fourthKg = dpg.get_value("fourthKgLoad")
    fifthMeasure = dpg.get_value("fifthTrackItload")
    fifthhKg = dpg.get_value("fifthKgLoad")

    NprKg = 9.82
    firstN = firstKg * NprKg 
    secondN = secondKg * NprKg
    thirdN = thirdKg * NprKg
    fourthN = fourthKg * NprKg
    fifthN = fifthhKg * NprKg

    measures = np.array([firstMeasure,secondMeasure,thirdMeasure,fourthMeasure,fifthMeasure])
    newtons = np.array([firstN,secondN,thirdN,fourthN,fifthN])

    regressionModel = np.polyfit(measures, newtons,1)

    vToNCoef = regressionModel[0]
    dpg.set_value("vToNCoefficient", vToNCoef)