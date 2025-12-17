
import dearpygui.dearpygui as dpg
import pandas as pd
from pynput.keyboard import Key, Controller
from toolbox.utilities.helper import add_comma

class SortPrice:
    def __init__(self):
        self.keyboard = Controller()
        self.disabled_branch = []
        self.temp_df = None

        with dpg.theme() as self.table_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(0,0,0,0))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(33, 17, 247))
        
        with dpg.theme() as self.header_col:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding,10,10)
                #dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(33, 17, 247))
        

        self.conversionText = {
        'Item ID':'Item_ID',
        'Item Name':'Item_Name',
        'Total_Qty':'T_Qty',
        'Total_Retail Price':'Retail_Price',
        'Total_Price 4':'Price_4',
        'DAVAO GMALL_Qty':'Gmall_Qty',
        'Joyo Davao SM LANANG_Qty':'SML_Qty',
        'Maxsun Gempesaw Davao_Qty':'Main_Qty',
        'Joyo SM ECOLAND_Qty':'SME_Qty',
        'Davao Lanang Warehouse_Qty':'Warehouse_Qty'
        } 


        self.converDtypes = {
            'Item_ID':'category',
            'Item_Name':'category',
            'T_Qty':'int16',
            'Retail_Price':'int32',
            'Price_4':'int32',
            'Gmall_Qty':'int16',
            'SML_Qty':'int16',
            'Main_Qty':'int16',
            'SME_Qty':'int16',
            'Warehouse_Qty':'int16'
        }

        self.table_col_width= {
            'Item_ID':120,
            'Item_Name':400,
            'T_Qty':30,
            'Retail_Price':50,
            'Price_4':50,
            'Gmall_Qty':30,
            'SML_Qty':30,
            'Main_Qty':30,
            'SME_Qty':30,
            'Warehouse_Qty':30
        }

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Left, callback=self.up)
            dpg.add_key_press_handler(dpg.mvKey_Right, callback=self.down)

        try:
            self.df = pd.read_csv('csv.csv')
            self.temp_df = self.df
        except:
            self.df = None

        with dpg.file_dialog(directory_selector=False, show=False, id="pick_data", width=700 ,height=400, callback = self.extract_data):
            dpg.add_file_extension(".xlsx")

        dpg.add_spacer(height = 10)
        with dpg.group():
            with dpg.group(horizontal = True, tag = 'head_tag'): #Item_ID,Item_Name
                dpg.add_combo(tag = 'category_filter',items =['Item_ID', 'Item_Name'], width = 100, default_value = 'Item_ID')
                dpg.add_input_text(tag = 'search_bar', width = 415, callback = self.search_bar)
                dpg.add_image_button(texture_tag='pick_folder_img', tag = 'pick_file', callback = lambda: dpg.show_item('pick_data'))

                with dpg.group(horizontal = True, tag = 'check_box', parent = 'head_tag'):
                    if self.df is not None:
                        self.checkboxes(self.df.columns.to_list()[5:])
                    else:
                        pass
            dpg.bind_item_font('head_tag', 'small')
            dpg.bind_item_font('category_filter', 'combo_font')

            dpg.add_spacer(height =5)
            
            with dpg.group(tag = 'items_container'):
                with dpg.table(tag = 'item_table',clipper = True,parent  = 'items_container',width=1000,height=550,row_background=True,scrollY = True,resizable = True, header_row = True,freeze_rows = 1):
                    if self.df is not None:
                        self.show_items(self.df)
                    else:
                        pass
                #dpg.bind_item_theme('header_col',self.header_col)
                dpg.bind_item_theme('item_table',self.table_theme)
                dpg.bind_item_font('item_table','small_x')
        
    def search_bar(self,sender,app_data,user_data):
        category_combo = dpg.get_value('category_filter')

        search_df = self.temp_df.loc[self.temp_df[category_combo].str.contains(app_data,case = False)]
        search_df = search_df.reset_index(drop = True)
    

        self.show_items(search_df)

    def extract_data(self, sender,app_data):
        available_cols_rename = {}
        file_path = app_data['file_path_name']
        self.df= pd.read_excel(file_path,skiprows=3,skipfooter=1).fillna(0)
        if 'Total_Price 4' in self.df.columns.to_list():
            if 'Total_Retail Price' not in self.df.columns.to_list():
                self.df['Total_Retail Price'] = self.df['Total_Price 4'].add(self.df['Total_Price 4'].mul(10/100)).round().astype(int)

                column_to_move = self.df.pop('Total_Retail Price')
                self.df.insert(4, 'Total_Retail Price', column_to_move)

            for column in self.df.columns.to_list():
                if column in self.conversionText:
                    available_cols_rename.update({column:self.conversionText[column]})

            self.df = self.df[available_cols_rename.keys()].rename(columns=available_cols_rename, errors = 'raise')

            for column in self.df.columns.to_list():
                self.df[column] = self.df[column].astype(self.converDtypes[column])

            # self.df['Total_Price 4']=self.df['Total_Price 4'].map("{:,}".format)
            # self.df['Total_Retail Price']=self.df['Total_Retail Price'].map("{:,}".format)

            
            self.df.to_csv('csv.csv',index=False)
            self.checkboxes(self.df.columns.to_list()[5:])
            self.show_items(self.df)
            self.disabled_branch = []

        else:
            print('Error Occurs')

    def checkboxes(self, columns = list[str]):
        dpg.delete_item('check_box')
        with dpg.group(horizontal = True, tag = 'check_box', parent = 'head_tag'):
            dpg.add_checkbox(label = 'Zero', tag = 'zero', user_data = 'zero',callback = self.checkbox_clicked)
            for column in columns:
                #column = column.remove('_Qty')
                dpg.add_checkbox(label = column.replace('_Qty',''),tag = column,default_value = True, user_data = column, callback = self.checkbox_clicked)

    def checkbox_clicked(self,sender, app_data, user_data):
        zero_check_val = dpg.get_value('zero')
        category_combo = dpg.get_value('category_filter')
        search_bar = dpg.get_value('search_bar')
        
        if user_data != 'zero':
            if app_data == False:
                self.disabled_branch.append(user_data)
            else:
                self.disabled_branch.remove(user_data)


        self.temp_df = self.df.drop(columns=self.disabled_branch)
        self.temp_df['T_Qty']= self.temp_df.iloc[:,5:].sum(axis = 1)

        if zero_check_val:
            zeros = self.temp_df.query('T_Qty == 0.0 or T_Qty == 0').index.tolist()
            self.temp_df = self.temp_df.drop(index=zeros)

        
        search_df = self.temp_df.loc[self.temp_df[category_combo].str.contains(search_bar,case = False)]
        search_df = search_df.reset_index(drop = True)
    
        self.show_items(search_df)

    def show_items(self,df):
     
        zeros = df.query('T_Qty == 0.0 or T_Qty == 0').index.tolist()
        
        
        dpg.delete_item('item_table',children_only = True)

        for column in df.columns.to_list():
            dpg.add_table_column(label = column, init_width_or_weight = self.table_col_width[column],parent = 'item_table')
        
        for row_item in df.values.tolist():
            with dpg.table_row(parent = 'item_table'):
                for index,column_item in zip(range(0,len(row_item)),row_item):
                    if index == 2 or index == 3 or index == 4:
                        column_item = add_comma(column_item)
                    dpg.add_input_text(default_value=column_item, readonly = True, width = 1000)
    
        for zero in zeros:
            dpg.highlight_table_row('item_table', zero, [255, 0, 0])

    def up(self):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)

    def down(self):
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
