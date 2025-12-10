import dearpygui.dearpygui as dpg
import math
# from toolbox.utilities.color_styles import Color,Style
from toolbox.customWidget.customWidgets import LabelInput
from toolbox.utilities.helper import add_comma,deal_with_decimal,max_char

class Homecredit:
    def __init__(self):
        self.FLOATS_VALUES = 1000
        self.INPUT_INDENT = 325
        self.TEXT_INPUT_INDENT = 215
        self.WIDTH = 270
        self.UNIQUE = 'calHomecredit'

        self.calHomecredit_widgets = [
            ('INITIAL PRICE','initial'),
            ('6 MONTHS INT.','six_months'),
            ('9 MONTHS INT.','nine_months'),
            ('12/15/18 MONTHS INT.','twelve_above_months')
        ]

        # with dpg.group(pos=[0,80]):
        #     for title,title_tag in calHomecredit_widgets:
        #         input_color = Color(
        #             text=(255,255,255),
        #             border = (255,255,255),
        #             borderShadow= (255,255,255)
        #         )
        #         input_style = Style(
        #             border_size= 0,
        #             frame_round= 10,
        #             frame_padding= (5,5)
        #         )
        #         TextInput(
        #             title = title,
        #             title_tag = title_tag,
        #             title_width = self.WIDTH,
        #             input_width= self.WIDTH,
        #             input_indent = self.INPUT_INDENT,
        #             group_indent= self.TEXT_INPUT_INDENT,
        #             fonts = ["large_bold","large"],
        #             unique= self.UNIQUE,
        #             title_color =input_color,
        #             title_style =input_style,
        #             input_color =input_color,
        #             input_style = input_style
        #         )

        # dpg.configure_item(f'initial_{self.UNIQUE}_field',callback =self.initial_press,readonly = False)



        with dpg.group(pos=[0,80]):
            for label_name,tag in self.calHomecredit_widgets:
    
                LabelInput(
                    unique= self.UNIQUE,
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["large_bold","large"],
    
                )
                
        dpg.configure_item('initial_calHomecredit_input',callback =self.initial_press,readonly = False)

    def initial_press(self,sender,app_data):
        max_char(tag_name='initial_calHomecredit_input',data=app_data,number=12)
        try:
            new_val = float(dpg.get_value(f'initial_{self.UNIQUE}_input'))
        except:
            new_val = 0
        
        self.formula(new_val)

    def formula(self,value):
        six_months = 0.06
        nine_months = 0.08
        twelve_above_months = 0.13

        six_total = math.ceil(value + (value*six_months))
        nine_total = math.ceil(value + (value*nine_months))
        twelve_above_total = math.ceil(value + (value*twelve_above_months))

        self.change_state(False)

        dpg.set_value(f'six_months_{self.UNIQUE}_input',add_comma(six_total))
        dpg.set_value(f'nine_months_{self.UNIQUE}_input',add_comma(nine_total))
        dpg.set_value(f'twelve_above_months_{self.UNIQUE}_input',add_comma(twelve_above_total))

        self.change_state(True)

    def change_state(self, state:bool):
        for _,tag in self.calHomecredit_widgets[1:-1]:
            dpg.configure_item(f'{tag}_{self.UNIQUE}_input',readonly = state)
