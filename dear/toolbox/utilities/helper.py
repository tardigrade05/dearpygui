# import pandas as pd
import dearpygui.dearpygui as dpg
import time
from toolbox.utilities.DataClass import Color
from toolbox.utilities.colorstyles import colorstyles


def add_comma(value):
    res = ""
    if value != "":
        try:
            try_split = str(value).split(".")

            if len(try_split[1]) == 1 and try_split[1] == "0":
                res = ('{:,}'.format(int(f"{try_split[0]}")))
            else:
                res = ('{:,}'.format(float(value)))
        
        except IndexError:
            res = ('{:,}'.format(int(value)))

        except ValueError:
            return res
    else:
        return res

    return str(res)


def mod_round(value):
    mod = ""
    prev_round = round(value,2) #4.56

    splitter = str(prev_round).split(".")

    if len(splitter[1]) == 2: #4.56
        mod = f"{splitter[0]}{splitter[1][0]}{splitter[1][1]}0" #4_560
    if len(splitter[1]) == 1: #4.5
        mod = f"{splitter[0]}{splitter[1][0]}00" #4_500

    return int(mod)
       

def deal_with_decimal(value, float_values = 1000):
    total = 0

    try:
        act_val = str(value).split(".")

        if len(act_val[1]) >= 3:
            if int(act_val[1][2])==9:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])}")

            elif int(act_val[1][2])>=5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{int(act_val[1][2])+1}")
               
            elif int(act_val[1][2])<5:
                init_val = float(f"{act_val[0]}.{act_val[1][0]}{act_val[1][1]}{act_val[1][2]}")

            total = mod_round(init_val)

        elif len(act_val[1]) < 3:
            total = int(float((f"{act_val[0]}.{act_val[1]}"))*float_values)

    except Exception as e:
        total = int(value*float_values)
    
    return total

def max_char(tag_name:str,data:str,number:int):
    try:
        if len(data) > number:
            dpg.configure_item(tag_name, readonly = True)
            dpg.set_value(tag_name, data[:number])
            time.sleep(.1)
            dpg.configure_item(tag_name, readonly = False)
    except:
        pass

def clean_data(value):
    try:
        initial = value.replace(',','')
        final = deal_with_decimal(float(initial))/1000
        print(initial)
        return final
    
    except ValueError:
        return 0/1000

    except:
        final = deal_with_decimal(initial)/1000
        print('except')
        return final


def realtime_settelement_change():
    amountToDeposit_widgets = [
        ('TOTAL SALES','total_sales_atd_amount_to_deposit_input'),
        ('CARD','card_atd_amount_to_deposit_input'),
        ('HOME CREDIT','homeCredit_atd_amount_to_deposit_input'),
        ('NORMAL','normal_atd_amount_to_deposit_input'),
        ('BILLEASE','billease_atd_amount_to_deposit_input'),
        ('FORM 2307','form_atd_amount_to_deposit_input'),
        ('BANK TRANS','bankTrans_atd_amount_to_deposit_input'),
        ('EXPENSES','expenses_atd_amount_to_deposit_input')
    ]
    for _,tag in amountToDeposit_widgets:
        dpg.configure_item(tag,readonly = False)

    total_cashcount = clean_data(dpg.get_value('total_cashcount'))
    total_sales = clean_data(dpg.get_value('total_sales_atd_amount_to_deposit_input'))
    total_card = clean_data(dpg.get_value('card_atd_amount_to_deposit_input'))
    total_homecredit = clean_data(dpg.get_value('homeCredit_atd_amount_to_deposit_input'))
    total_billease = clean_data(dpg.get_value('billease_atd_amount_to_deposit_input'))
    total_form = clean_data(dpg.get_value('form_atd_amount_to_deposit_input'))
    total_bank = clean_data(dpg.get_value('bankTrans_atd_amount_to_deposit_input'))
    total_expenses = clean_data(dpg.get_value('expenses_atd_amount_to_deposit_input'))

    total_subtract = total_card + total_homecredit + total_billease + total_form +total_bank + total_expenses
    amountToDeposit = total_sales - total_subtract
    over_or_lacking = total_cashcount - amountToDeposit

    if over_or_lacking>0:
        dpg.set_value('normal_atd_amount_to_deposit_lbl', value = 'OVER KA BOI!')
        colorstyles(target_tag='normal_atd_amount_to_deposit_input',color= Color(text=(0,255,0)))
    elif over_or_lacking<0:
        over_or_lacking = abs(over_or_lacking)
        dpg.set_value('normal_atd_amount_to_deposit_lbl', value = 'YATI LACKING!')
        colorstyles(target_tag='normal_atd_amount_to_deposit_input',color= Color(text=(255,0,0)))
    elif over_or_lacking == 0:
        dpg.set_value('normal_atd_amount_to_deposit_lbl', value = 'PAYTS RA!')
        colorstyles(target_tag='normal_atd_amount_to_deposit_input',color= Color(text=(255,255,255)))

    dpg.set_value('normal_atd_amount_to_deposit_input',add_comma(over_or_lacking))
    dpg.set_value('amount_to_deposit_atd_amount_to_deposit_input',add_comma(amountToDeposit))

    for _,tag in amountToDeposit_widgets:
        dpg.configure_item(tag,readonly = True)
    dpg.configure_item('total_sales_atd_amount_to_deposit_input',readonly = False)


# max_chars = 12
# try:
#     if len(app_data) > max_chars:
#         dpg.configure_item('total_sales_calvat_input', readonly = True)
#         dpg.set_value('total_sales_calvat_input', app_data[:max_chars])
#         time.sleep(.1)
#         dpg.configure_item('total_sales_calvat_input', readonly = False)
# except:
#     pass

# def set_atd_input():
#     print("set_atd_input __START")
#     df = pd.read_feather('SETTLEMENT.feather')
#     cashcount_total = float(dpg.get_value('total_cashcount').replace(',',''))
#     try:
#         sales_total =float(dpg.get_value('total_sales_atd_amountDeposit_field'))
#     except:
#         print("Except")
#         sales_total = 0.0

#     card_total = df.query('Category == "card"')['Values'].sum()
#     homecredit_total = df.query('Category == "homecredit"')['Values'].sum()
#     billease_total = df.query('Category == "billease"')['Values'].sum()
#     form_total = df.query('Category == "form"')['Values'].sum()
#     bankTrans_total = df.query('Category == "bankTrans"')['Values'].sum()
#     expenses_total = df.query('Category == "expenses"')['Values'].sum()
#     table_total = df['Values'].sum()

#     amout_to_deposit = sales_total - table_total
#     over_lacking = cashcount_total - amout_to_deposit

#     dpg.set_value("card_atd_amountDeposit_field", add_comma(deal_with_decimal(card_total)/1000))
#     dpg.set_value("homeCredit_atd_amountDeposit_field", add_comma(deal_with_decimal(homecredit_total)/1000))
#     dpg.set_value("billease_atd_amountDeposit_field", add_comma(deal_with_decimal(billease_total)/1000))
#     dpg.set_value("form_atd_amountDeposit_field", add_comma(deal_with_decimal(form_total)/1000))
#     dpg.set_value("bankTrans_atd_amountDeposit_field", add_comma(deal_with_decimal(bankTrans_total)/1000))
#     dpg.set_value("expenses_atd_amountDeposit_field", add_comma(deal_with_decimal(expenses_total)/1000))

#     dpg.set_value("normal_atd_amountDeposit_field", add_comma(deal_with_decimal(over_lacking)/1000))
#     dpg.set_value("amount_to_deposit_atd_amountDeposit_field", add_comma(deal_with_decimal(amout_to_deposit)/1000))
    
#     print("set_atd_input __END")