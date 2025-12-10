import dearpygui.dearpygui as dpg
from toolbox.customWidget.customWidgets import LabelInput
from toolbox.utilities.helper import add_comma,deal_with_decimal,max_char


class Calvat:
    def __init__(self):
        self.FLOATS_VALUES = 1000
        self.INPUT_INDENT = 320
        self.TEXT_INPUT_INDENT = 215
        self.WIDTH = 270

        self.calvat_widgets = [
        ('TOTAL SALES','total_sales'),
        ('LESS: 12% VAT','less_vat'),
        ('NET OF VAT/TOTAL','net_vat'),
        ('LESS:SC/PWD DISC.','less_pwd'),
        ('TOTAL DUE','total_due'),
        ('LESS:WITHHOLDING','less_withholding'),
        ('TOTAL AMOUNT DUE','total_amount_due'),
        ('VATABLE(V)','vatable'),
        ('VAT-EXEMPT(E)','vat_exempt'),
        ('ZERO RATED(Z)','zero_rated'),
        ('VAT(12%)','vat_12'),
        ('TOTAL','total')
        ]

        dpg.add_combo(indent=210,items=["Private","Public"], tag="calvat_category", default_value="Private", width=280, callback= self.pick_calvat_category)
        dpg.bind_item_font("calvat_category","combo_font")

        with dpg.group(pos=[0,80]):
            for label_name,tag in self.calvat_widgets:
    
                LabelInput(
                    unique= 'calvat',
                    label_name = label_name,
                    tag = tag,
                    input_width= self.WIDTH,
                    input_indent = self.INPUT_INDENT,
                    group_indent= self.TEXT_INPUT_INDENT,
                    fonts = ["large_bold","large"],
    
                )
        
        dpg.configure_item('total_sales_calvat_input',callback =self.total_sales_press,readonly = False)

    def pick_calvat_category(self,sender, app_data):
        self.formula()
    def total_sales_press(self,sender, app_data):
        max_char(tag_name='total_sales_calvat_input',data = app_data,number=12)
        self.formula()

    def formula(self):
        value =  dpg.get_value('total_sales_calvat_input')
        
        try:
            CONST_VAT = 1.12*self.FLOATS_VALUES #1120
            SIX_PERCENT = 0.06*self.FLOATS_VALUES #60
            ONE_PERCENT = 0.01*self.FLOATS_VALUES #10
            TOTAL_SALES = float(value)*self.FLOATS_VALUES

            if dpg.get_value("calvat_category") == "Private":
                PERCENT = ONE_PERCENT
            else:
                PERCENT = SIX_PERCENT

            netVal = deal_with_decimal((TOTAL_SALES/CONST_VAT),self.FLOATS_VALUES) #possible 45.809
            lessVat = TOTAL_SALES - netVal
            lessWithHolding = deal_with_decimal((netVal * PERCENT)/(self.FLOATS_VALUES*self.FLOATS_VALUES),self.FLOATS_VALUES)
            totalAmountDue = TOTAL_SALES-lessWithHolding

            self.set_input_values(
                less_vat = str(lessVat/self.FLOATS_VALUES),
                net_vat = str(netVal/self.FLOATS_VALUES),
                total_due = str(value),
                less_withholding=str(lessWithHolding/self.FLOATS_VALUES),
                total_amount_due=str(totalAmountDue/self.FLOATS_VALUES)
                )

        except ValueError:
            self.set_input_values()
    
    def set_input_values(self,less_vat = "",net_vat = "",total_due = "",less_withholding = "",total_amount_due=""):
        self.change_state(state= False)
        dpg.set_value('less_vat_calvat_input',add_comma(less_vat))
        dpg.set_value('net_vat_calvat_input',add_comma(net_vat))
        dpg.set_value('total_due_calvat_input', add_comma(total_due))
        
        dpg.set_value('less_withholding_calvat_input', add_comma(less_withholding))
        dpg.set_value('total_amount_due_calvat_input', add_comma(total_amount_due))
        dpg.set_value('total_calvat_input',  add_comma(total_due))
        self.change_state(state= True)

    def change_state(self, state:bool):
        for _,tag in self.calvat_widgets[1:-1]:
            dpg.configure_item(f'{tag}_calvat_input',readonly = state)

