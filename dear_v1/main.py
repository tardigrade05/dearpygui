import dearpygui.dearpygui as dpg
from toolbox.utilities.colorstyles import fontstyle,colorstyles,img_stack
import dearpygui.demo as demo
from toolbox.tab.calculator.Calculator import Calculator
from toolbox.tab.settlement.Settlement import Settlement

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title="Toolbox",width=1020,height=650,max_width=1020,max_height=650, resizable= False) #,small_icon="tool-box.ico"

    # demo.show_demo()
    # dpg.show_style_editor()
    fontstyle()
    img_stack()

    with dpg.window(tag="primary_window"):
        with dpg.tab_bar():
            with dpg.tab(tag = 'calculator',label="Calculator"):
                Calculator()

            with dpg.tab(tag = 'settlement',label="Settlement"):
                Settlement()

    tabs = [
        ('calculator','small'),
        ('settlement','small')
    ]

    for tag,font in tabs:
        dpg.bind_item_font(tag,font)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()

    dpg.destroy_context()