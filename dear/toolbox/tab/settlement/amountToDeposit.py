import dearpygui.dearpygui as dpg
from toolbox.customWidget.customWidgets import LabelInput
from toolbox.utilities.helper import realtime_settelement_change
from toolbox.utilities.colorstyles import colorstyles
from toolbox.utilities.DataClass import Color,Style

class AmountToDeposit:
    def __init__(self):
        self.INPUT_INDENT = 205# + 215
        self.WIDTH = 160
        self.TEXT_INPUT_INDENT = 0
        self.UNIQUE = 'amount_to_deposit'

        self.amountToDeposit_widgets = [
            ('TOTAL SALES','total_sales_atd'),
            ('CARD','card_atd'),
            ('HOME CREDIT','homeCredit_atd'),
            ('PAYTS RA!','normal_atd'),
            ('BILLEASE','billease_atd'),
            ('FORM 2307','form_atd'),
            ('BANK TRANS','bankTrans_atd'),
            ('EXPENSES','expenses_atd')
        ]

        dpg.add_spacer(height = 5)
        with dpg.group(horizontal = True):
            with dpg.group():
                for label_name,tag in self.amountToDeposit_widgets[0:4]:
                    
                    LabelInput(
                    unique= self.UNIQUE,
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["medium_bold","medium"],
                    default_input_val='0'
                    )

            with dpg.group():
                for label_name,tag in self.amountToDeposit_widgets[4:8]:
                    LabelInput(
                    unique= self.UNIQUE,
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["medium_bold","medium"],
                    default_input_val='0'
                    )

        dpg.add_spacer(height = 10)

        LabelInput(
            unique= self.UNIQUE,
            label_name = "AMOUNT TO DEPOSIT",
            tag = f'{self.UNIQUE}_atd',
            input_width= self.WIDTH+156,
            input_indent =  self.INPUT_INDENT+215,
            group_indent= 0,
            fonts = ["large_x_bold","large_x_bold"],
            default_input_val='0'
            )
        
        dpg.configure_item('total_sales_atd_amount_to_deposit_input', readonly = False,callback = self.press, decimal = True)
        colorstyles(target_tag='amount_to_deposit_atd_amount_to_deposit_input',color=Color(text=(60, 133, 250),frame=(255,255,255),border=(60, 133, 250)),style=Style(border_size=3))
    
    def press(self,sender,appdata):
        realtime_settelement_change()
