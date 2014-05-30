#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter.messagebox as MB
import tkRAD

class MyMainWindow(tkRAD.RADMainWindow):
    """create MyMainWindow class
    by subclassing tkRAD.RADMainWindow,
    because we want to get a clean and easy workspace"""
    def init_widget(self, **kw):
        # build ^/xml/menu/topmenu.xml
        self.topmenu.xml_build()
        # connect statusbar to control variable
        self.connect_statusbar("show_statusbar")
        # always connect events at last
        self.events.connect(
            "MenuShowListMode",
            self.slot_list_mode_changed
            )
        # init default choice
        self.slot_list_mode_changed()

    def slot_list_mode_changed(self, *args, **kw):
        # get user's choice
        _cvar = self.topmenu.get_stringvar("menu_show_list")
        # got control var and valued?
        if _cvar and _cvar.get():
            # show messagebox
            MB.showinfo(
                "info",
                "choice value: '{}'".format(_cvar.get()),
            )

if __name__ == '__main__':
    MyMainWindow().run()
