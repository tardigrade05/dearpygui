import dearpygui.dearpygui as dpg
from toolbox.utilities.helper import max_char,add_comma,realtime_settelement_change,clean_data,total_cashcount
from toolbox.customWidget.customWidgets import LabelInputLabel
from toolbox.models import Settlement_Model
from sqlalchemy import select
from toolbox import session
from pynput.keyboard import Key, Controller

class CashCount:
    def __init__(self):
        self.INPUT_INDENT = 70
        self.TEXT_INPUT_INDENT = 0
        self.WIDTH = 60
        self.UNIQUE = 'cashcount'
        self.keyboard = Controller()
       
        self.cashcount_widgets = [
            ('1000', 'one_thousand'),
            ('500', 'five_hundred'),
            ('200', 'two_hundred'),
            ('100', 'one_hundred'),
            ('50', 'fifty_pesos'),
            ('20','twenty_pesos'),
            ('10','ten_pesos'),
            ('5','five_pesos'),
            ('1', 'one_peso'),
            ('.50','fifty_cent'),
            ('.25','twoFive_cent'),
            ('.10','ten_cent'),
            ('.05','five_cent'),
            ('.01','one_cent')
        ]
        with dpg.group(horizontal = True):
            with dpg.group(pos=(130,35)):
                for label_name,tag in self.cashcount_widgets[0:7]:
                    value_query = session.scalars(select(Settlement_Model).where(Settlement_Model.category == tag)).first()
                    if value_query is not None:
                        default_val = value_query.value
                    else:
                        add_value = Settlement_Model(
                            category = tag,
                            value = ''
                        )
                        session.add(add_value)
                        session.commit()
                        default_val = ''
                   
                    LabelInputLabel(
                    unique= 'cashcount',
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["medium_bold","medium"],
                    input_readonly= False,
                    input_default_value=default_val
                    )

            with dpg.group(pos=(450,35)):
                for label_name,tag in self.cashcount_widgets[7:14]:
                    value_query = session.scalars(select(Settlement_Model).where(Settlement_Model.category == tag)).first()
                    if value_query is not None:
                        default_val = value_query.value
                    else:
                        add_value = Settlement_Model(
                            category = tag,
                            value = ''
                        )
                        session.add(add_value)
                        session.commit()
                        default_val = ''
                        
                    LabelInputLabel(
                    unique= 'cashcount',
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    input_readonly= False,
                    fonts = ["medium_bold","medium"],
                    input_default_value=default_val
                    
                    )

        dpg.add_spacer(height = 3)
        dpg.add_input_text(tag = "total_cashcount", width = 170, indent = 270, decimal = True,default_value = 0)

        dpg.bind_item_font("total_cashcount","medium")

        for label_name,tag in self.cashcount_widgets:
            dpg.configure_item(f'{tag}_cashcount_input',user_data =[tag,label_name],callback=self.press)
        
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Up, callback=self.up)
            dpg.add_key_press_handler(dpg.mvKey_Down, callback=self.down)

    def up(self):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    def down(self):
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
    
    def press(self,sender, app_data,user_data):
        max_char(tag_name=f'{user_data[0]}_cashcount_input',data= app_data,number=2)
        input_val = dpg.get_value(f'{user_data[0]}_cashcount_input')

        try:
            # self.product = ((float(user_data[1])*1000) * float(input_val))/1000
            self.product = clean_data(user_data[1]) * clean_data(input_val)
        except:
            self.product = 0

        target_row = session.scalars(select(Settlement_Model).filter(Settlement_Model.category == user_data[0])).first()
        target_row.value = input_val
        session.commit()


        dpg.configure_item(f'{user_data[0]}_cashcount_product',default_value= add_comma(str(self.product)))
        total_cashcount()
        realtime_settelement_change()

    