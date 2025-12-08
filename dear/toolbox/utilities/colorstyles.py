import dearpygui.dearpygui as dpg
from toolbox.utilities.DataClass import Color,Style



def colorstyles(target_tag:str,color:Color = Color(),style:Style = Style()) -> None:
    
    # colStyle_tag = f"{target_tag}_colStyle"
    with dpg.theme() as default:
        with dpg.theme_component(dpg.mvAll):
          
            for target,value in color.get_values():
                dpg.add_theme_color(target,value)
    
            for target,value in style.get_values():
                try:
                    dpg.add_theme_style(target,value)
                except:
                    dpg.add_theme_style(target,value[0],value[1])
        

    dpg.bind_item_theme(target_tag,default)

def fontstyle() -> None:
    with dpg.font_registry():
        #bold
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 12, tag = 'small_x_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 14, tag = 'small_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 27, tag = 'medium_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf',30, tag = 'large_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 35, tag = 'large_x_bold')

        #normal
        dpg.add_font('toolbox/font/Helvetica.ttf', 12, tag = 'small_x')
        dpg.add_font('toolbox/font/Helvetica.ttf', 14, tag = 'small')
        dpg.add_font('toolbox/font/Helvetica.ttf', 27, tag = 'medium')
        dpg.add_font('toolbox/font/Helvetica.ttf',30, tag = 'large')
        dpg.add_font('toolbox/font/Helvetica.ttf', 35, tag = 'large_x')

        #combo
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 15, tag = 'combo_font')
