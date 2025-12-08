import dearpygui.dearpygui as dpg
from toolbox.utilities.helper import max_char,add_comma,realtime_settelement_change
from toolbox.customWidget.customWidgets import LabelInputLabel

class CashCount:
    def __init__(self):
        self.INPUT_INDENT = 70
        self.TEXT_INPUT_INDENT = 0
        self.WIDTH = 60
        self.UNIQUE = 'cashcount'
        
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
                   
                   LabelInputLabel(
                    unique= 'cashcount',
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["medium_bold","medium"],
                    input_readonly= False
                    )

            with dpg.group(pos=(450,35)):
                for label_name,tag in self.cashcount_widgets[7:14]:
                    LabelInputLabel(
                    unique= 'cashcount',
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    input_readonly= False,
                    fonts = ["medium_bold","medium"])

        dpg.add_spacer(height = 3)
        dpg.add_input_text(tag = "total_cashcount", width = 170, indent = 270, decimal = True,default_value = 0)

        dpg.bind_item_font("total_cashcount","medium")

        for label_name,tag in self.cashcount_widgets:
            dpg.configure_item(f'{tag}_cashcount_input',user_data =[tag,label_name],callback=self.press)


    def press(self,sender, app_data,user_data):
        max_char(tag_name=f'{user_data[0]}_cashcount_input',data= app_data,number=2)
        input_val = dpg.get_value(f'{user_data[0]}_cashcount_input')

        try:
            self.product = ((float(user_data[1])*1000) * float(input_val))/1000
        except:
            self.product = 0

        dpg.configure_item(f'{user_data[0]}_cashcount_product',default_value= add_comma(str(self.product)))
        # print(user_data)
        self.total_cash()
        realtime_settelement_change()

    def total_cash(self):
        cashcount_data = []
        total = 0
        for _,tag in self.cashcount_widgets:
            try:
                add_val = float(dpg.get_value(f"{tag}_cashcount_product").replace(',',''))
                total = total +add_val
                qty = int(dpg.get_value(f"{tag}_cashcount_field"))

            except:
                add_val = 0.0
                qty = 0
            cashcount_data.append((qty,add_val))

        dpg.set_value('total_cashcount',add_comma(str(total)))