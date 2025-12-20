import dearpygui.dearpygui as dpg
from datetime import date




class DatePicker:
    def __init__(self,tag, title_lbl):
        current_date = date.today()
        unmerge_date = str(current_date).split('-')
        self.default_date = {
            'month_day': int(unmerge_date[2]),
            'month': int(unmerge_date[1])-1,
            'year': int(unmerge_date[0][1:]) + 100,
        }

        self.lbl_tag = f'{tag}_lbl'
        self.input_tag = f'{tag}_input'
        self.btn_tag = f'{tag}_btn' 
        
        with dpg.group(horizontal= True):
            dpg.add_text(tag= self.lbl_tag,default_value= title_lbl)
            dpg.add_input_text(tag= self.input_tag, width=80 , height= 25,multiline=True)
            dpg.add_image_button(texture_tag='calendar_img',background_color = (255,255,255),frame_padding = 0, tag=self.btn_tag, callback=self.show_picker)

    def show_picker(self):
        try:
            dpg.delete_item('date_container')
        except:
            pass
        with dpg.window(tag= 'date_container'):
            dpg.add_date_picker(default_value= self.default_date, callback= self.picked_date)

    def picked_date(self,sender,app_data,user_data):
        print(app_data)
        month = app_data['month'] + 1
        day = app_data['month_day']
        year = app_data['year'] - 100

        date = f'{month}/{day}/{year}'

        dpg.set_value(self.input_tag,date )
        dpg.delete_item('date_container')


if __name__ == '__main__':

    print(date.today())
    
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)
    calendar_w, calendar_h, _, calendar = dpg.load_image("img/calendar.png")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=calendar_w, height=calendar_h, default_value=calendar, tag = 'calendar_img')

    with dpg.window(tag="Primary Window"):
        DatePicker(tag='test',title_lbl='test')
        DatePicker(tag='test1',title_lbl='test1')
        DatePicker(tag='test2',title_lbl='test2')

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()




    