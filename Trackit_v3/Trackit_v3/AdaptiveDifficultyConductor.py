import dearpygui.dearpygui as dpg

def changeDifficulty(dpg):
    if(dpg.get_value("adaptiveDif")):
        level = dpg.get_value("playerLevel")
        minCloseness = dpg.get_value("minCloseness")
        maxCloseness = dpg.get_value("maxCloseness")
        minRandomHeight = dpg.get_value("minRandomHeight")
        maxRandomHeight = dpg.get_value("maxRandomHeight")

        adjustmentFactor = level * 5
        dpg.configure_item("minCloseness", default_value = minCloseness + adjustmentFactor*2)
        dpg.configure_item("maxCloseness", default_value = maxCloseness + adjustmentFactor*2)
        dpg.configure_item("minRandomHeight", default_value = minRandomHeight - (adjustmentFactor/2))
        dpg.configure_item("maxRandomHeight", default_value = maxRandomHeight - adjustmentFactor)

