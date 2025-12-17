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
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 13, tag = 'small_x_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 15, tag = 'small_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 27, tag = 'medium_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf',30, tag = 'large_bold')
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 35, tag = 'large_x_bold')

        #normal
        dpg.add_font('toolbox/font/Helvetica.ttf', 13, tag = 'small_x')
        dpg.add_font('toolbox/font/Helvetica.ttf', 15, tag = 'small')
        dpg.add_font('toolbox/font/Helvetica.ttf', 24, tag = 'medium_y')
        dpg.add_font('toolbox/font/Helvetica.ttf', 27, tag = 'medium')
        dpg.add_font('toolbox/font/Helvetica.ttf',30, tag = 'large')
        dpg.add_font('toolbox/font/Helvetica.ttf', 35, tag = 'large_x')

        #combo
        dpg.add_font('toolbox/font/Helvetica-Bold.ttf', 15, tag = 'combo_font')

def img_stack():
    add_w, add_h, _, add = dpg.load_image("toolbox/images/add.png") # Replace with your image loading logic
    delete_all_w, delete_all_h, _, delete_all = dpg.load_image("toolbox/images/delete_all.png") 
    edit_w, edit_h, _, edit = dpg.load_image("toolbox/images/edit.png") 
    delete_w, delete_h, _, delete = dpg.load_image("toolbox/images/delete.png") 
    default_w, default_h, _, default = dpg.load_image("toolbox/images/default.png") 
    folder_w, folder_h, _, folder = dpg.load_image("toolbox/images/pick_folder.png") 


    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=add_w, height=add_h, default_value=add, tag = 'add_img')
        dpg.add_static_texture(width=delete_all_w, height=delete_all_h, default_value=delete_all,tag = 'delete_all_img')
        dpg.add_static_texture(width=edit_w, height=edit_h, default_value=edit,tag = 'edit_img')
        dpg.add_static_texture(width=delete_w, height=delete_h, default_value=delete,tag = 'delete_img')
        dpg.add_static_texture(width=default_w, height=default_h, default_value=default,tag = 'default_img')
        dpg.add_static_texture(width=folder_w, height=folder_h, default_value=folder,tag = 'pick_folder_img')