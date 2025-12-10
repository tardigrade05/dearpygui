import dearpygui.dearpygui as dpg
from toolbox.models import Settlement_Model
from toolbox import session
from sqlalchemy import select
from toolbox.utilities.helper import clean_data,add_comma,realtime_settelement_change
from toolbox.utilities.colorstyles import colorstyles
from toolbox.utilities.DataClass import Color
# import pandas as pd
# from dataclasses import dataclass
# from toolbox.utilities.helper import set_atd_input

class TableTab:
    def __init__(self,tag:str, total_tag:str, unique:str):
        
        self.tag = tag
        self.category = f"{tag}_{unique}"
        self.category_input = f'{self.category}_inputVal'
        self.category_table = f'{self.category}_table'
        self.main_container = f'{self.category}_main_container'
        self.selected = []
        self.btn_w,self.btn_h =(24,24)
        

        with dpg.group(tag = self.main_container):
            dpg.add_spacer(height = 10)
    
            with dpg.group(horizontal = True):
                dpg.add_input_text(tag = self.category_input, hint = 'Type here...', width = 130,height = 30,decimal = True,callback= self.add_value,on_enter = True)
    
                dpg.add_image_button(texture_tag = 'add_img',label = 'Add', tag = f'{self.category}_add', callback = self.add_value)
                dpg.add_image_button(texture_tag = 'delete_all_img', label = 'Delete All', tag = f'{self.category}_deleteAll', callback = self.delete_all)
                dpg.add_image_button(texture_tag = 'edit_img', label = 'Edit',show = False, tag = f'{self.category}_edit', callback = self.edit_value)
                dpg.add_image_button(texture_tag = 'delete_img', label = 'Delete',show = False, tag = f'{self.category}_delete', callback = self.delete_value)
                dpg.add_image_button(texture_tag = 'default_img', label = 'Default',show= False, tag = f'{self.category}_default', callback = self.default_btn)
                dpg.add_spacer(height = 40)

                self.show_values()
       
        colorstyles(self.category_input)
        colorstyles(f'{self.category}_add', color = Color( button_hovered = (122, 154, 247))) #
        colorstyles(f'{self.category}_deleteAll', color = Color( button_hovered = (244, 122, 122)))
        colorstyles(f'{self.category}_edit', color = Color( button_hovered = (122, 154, 247)))
        colorstyles(f'{self.category}_delete', color = Color( button_hovered = (244, 122, 122)))
        colorstyles(f'{self.category}_default', color = Color( button_hovered = (5, 245, 85)))

        dpg.bind_item_font(self.category_input,'medium_y')

    def add_value(self):
        new_value = dpg.get_value(self.category_input)
        add_value = Settlement_Model(
            category = self.category,
            value = new_value
        )
        session.add(add_value)
        session.commit()

        self.show_values()

        dpg.set_value(self.category_input,'')
        self.selected = []
        dpg.focus_item(self.category_input)

    def show_values(self):
        total = 0
        try:
            category_values = session.scalars(select(Settlement_Model).where(Settlement_Model.category == self.category)).all()
        except:
            category_values = []

# header_row=False, no_host_extendX=True, delay_search=True,
# borders_innerH=True, borders_outerH=True, borders_innerV=True,
# borders_outerV=True, context_menu_in_body=True, row_background=True,
# policy=dpg.mvTable_SizingFixedFit, height=150

        dpg.delete_item(self.category_table)
        with dpg.table(tag = self.category_table,parent  = self.main_container,row_background=True, header_row=False,height=485,scrollY = True):
            dpg.add_table_column(label = '')
        
            for value in category_values:
                with dpg.table_row():
                    total = total + clean_data(value.value)
                    dpg.add_selectable(label = add_comma(value.value), tag = f'{value.category}_{value.id}', callback = self.select, user_data = (value.id,value.value))
                    dpg.bind_item_font(f'{value.category}_{value.id}','medium_y')
     
        dpg.set_value(f'{self.tag}_atd_amount_to_deposit_input', add_comma(total))
        realtime_settelement_change()
        

    def delete_all(self):
        session.query(Settlement_Model).filter(Settlement_Model.category == self.category).delete()
        session.commit()
        self.show_values()
        self.selected = []

    def delete_value(self):
        for id,_ in self.selected:
            session.query(Settlement_Model).filter(Settlement_Model.id == id).delete()
        
        session.commit()
        self.selected = []
        dpg.set_value(self.category_input,'')
        self.show_values()
        self.default_btn()

    def edit_value(self):
        updated_value = dpg.get_value(self.category_input)
        target_row = session.scalars(select(Settlement_Model).filter(Settlement_Model.id == self.selected[-1][0])).first()
        target_row.value = updated_value

        session.commit()
        self.selected = []

        self.show_values()
        self.default_btn()
    
    def default_btn(self):
        self.hidden_btn(add=True,delete_all=True,edit=False,delete=False,default=False)
        for id,_ in self.selected:
            dpg.configure_item(item = f"{self.category}_{id}", default_value = False)
        self.selected = []
        dpg.set_value(self.category_input,'')

    def hidden_btn(self, add:bool,delete_all:bool,edit:bool,delete:bool,default:bool) -> None:
        dpg.configure_item(f'{self.category}_add' , show = add)
        dpg.configure_item(f'{self.category}_deleteAll', show = delete_all)
        dpg.configure_item(f'{self.category}_edit', show = edit)
        dpg.configure_item(f'{self.category}_delete', show = delete)
        dpg.configure_item(f'{self.category}_default', show = delete)

    def select(self,sender,app_data,user_data):
        
        if user_data in self.selected:
            self.selected.remove(user_data)
        else:
            self.selected.append(user_data)

      
        dpg.set_value(self.category_input,user_data[1])
        self.hidden_btn(add=False,delete_all=False,edit=True,delete=True,default = True)
        if len(self.selected) == 0:
            self.default_btn()
    
    def initial_setup(self):
        exist_df = DataFrame().get_exist_df(self.tag)
        all_counter,self.counter, self.values = DataFrame().get_counter_values(exist_df,self.tag)
        self.show_values(all_counter,self.values)

        self.hidden_btn(add=True,delete_all=True,edit=False,delete=False)
        self.selected = []
        dpg.set_value(self.input,'')

class AtdTables:
    def __init__(self):

        with dpg.tab_bar():
            with dpg.tab(label="Card"):
                TableTab('card','','atd_tables') #f'{tag}_{unique}_input'  

            with dpg.tab(label="Homecredit"):
                TableTab('homeCredit','','atd_tables')

            with dpg.tab(label="Billease"):
                TableTab('billease','','atd_tables')

            with dpg.tab(label="Form 2307"):
                TableTab('form','','atd_tables')
                
            with dpg.tab(label="Bank Transfer"):
                TableTab('bankTrans','','atd_tables')

            with dpg.tab(label="Expenses"):
                TableTab('expenses','','atd_tables')

#   self.amountToDeposit_widgets = [
#             ('TOTAL SALES','total_sales_atd'),  #homeCredit_atd_amount_to_deposit_input
#             ('HOME CREDIT','homeCredit_atd'),
#             ('PAYTS RA!','normal_atd'),
#             ('BILLEASE','billease_atd'),
#             ('FORM 2307','form_atd'),
#             ('BANK TRANS','bankTrans_atd'),
#             ('EXPENSES','expenses_atd')
#         ]