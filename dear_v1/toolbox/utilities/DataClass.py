import dearpygui.dearpygui as dpg
from dataclasses import dataclass
from typing import Any



@dataclass
class Color:
    text:tuple[int] = (255,255,255)
    frame:tuple[int] = (51, 50, 54)
    button:tuple[int] = (255,255,255)
    button_hovered:tuple[int] = (51, 50, 54)
    border:tuple[int] = (255,255,255)
    borderShadow:tuple[int] = (51, 50, 54)
        
    def get_values(self) -> list[Any]:
        text_color = (dpg.mvThemeCol_Text, self.text)
        frame_color = (dpg.mvThemeCol_FrameBg, self.frame)

        button_color = (dpg.mvThemeCol_Button, self.button)
        button_hovered_color = (dpg.mvThemeCol_ButtonHovered, self.button_hovered)


        border_color = (dpg.mvThemeCol_Border, self.border)
        borderShadow_color = (dpg.mvThemeCol_BorderShadow, self.borderShadow)
       
        return [text_color,frame_color,button_color,button_hovered_color,border_color,borderShadow_color] #,frame_color


@dataclass
class Style:
    border_size:int = 0
    frame_round:int = 5
    frame_padding:tuple[int] = (5,5)

    def get_values(self) -> list[Any]:
        borderSize = (dpg.mvStyleVar_FrameBorderSize, self.border_size)
        frameRound = (dpg.mvStyleVar_FrameRounding, self.frame_round)
        framePadding = (dpg.mvStyleVar_FramePadding, self.frame_padding)

        return [borderSize,frameRound,framePadding]


