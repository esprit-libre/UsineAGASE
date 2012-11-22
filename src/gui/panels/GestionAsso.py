#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sun Nov 21 17:24:59 2010

import wx

from gui.panels.GestionAdhesionTypes import GestionAdhesionTypes
from gui.panels.GestionAdherents import GestionAdherents
from gui.panels.GestionCotisationTypes import GestionCotisationTypes
from gui.panels.GestionExercices import GestionExercices
from gui.panels.InfosAsso import InfosAsso

###########################################################################
## Class GestionAsso
###########################################################################


class GestionAsso(wx.Panel):
    def __init__(self, parent):
        # begin wxGlade: panel_GestionAsso.__init__
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_p4 = wx.Panel(self.notebook, -1)
        self.notebook_p3 = wx.Panel(self.notebook, -1)
        self.notebook_p2 = wx.Panel(self.notebook, -1)
        self.notebook_p1 = wx.Panel(self.notebook, -1)

        self.sizer_types_a_staticbox = wx.StaticBox(self.notebook_p4, -1, u"Types d'adh�sion")
        self.label_description_type_adhesion = wx.StaticText(self.notebook_p4, -1, u"Ce sont les diff�rentes formules disponibles pour adh�rer � l'association.")
        self.sizer_types_c_staticbox = wx.StaticBox(self.notebook_p4, -1, "Types de cotisation")
        self.label_description_type_cotisation = wx.StaticText(self.notebook_p4, -1, u"Ce sont les diff�rents tarifs disponibles pour la cotisation mensuelle au GASE.")
        self.sizer_staticbox = wx.StaticBox(self, -1, "Gestion de l'association")

        self.panel_infos_asso = InfosAsso(self.notebook_p1)
        self.panel_gestion_exercices = GestionExercices(self.notebook_p2)
        self.panel_gestion_adherents = GestionAdherents(self.notebook_p3)
        self.panel_gestion_types_cotisation = GestionCotisationTypes(self.notebook_p4)
        self.panel_gestion_types_adhesion = GestionAdhesionTypes(self.notebook_p4)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        self.sizer_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        # begin wxGlade: panel_GestionAsso.__do_layout
        sizer = wx.StaticBoxSizer(self.sizer_staticbox, wx.HORIZONTAL)
        sizer_p4 = wx.BoxSizer(wx.VERTICAL)
        sizer_types_c = wx.StaticBoxSizer(self.sizer_types_c_staticbox, wx.VERTICAL)
        sizer_types_a = wx.StaticBoxSizer(self.sizer_types_a_staticbox, wx.VERTICAL)
        sizer_p3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_p2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_p1 = wx.BoxSizer(wx.VERTICAL)

        sizer_p1.Add(self.panel_infos_asso, 1, wx.ALL, 5)
        self.notebook_p1.SetSizer(sizer_p1)

        sizer_p2.Add(self.panel_gestion_exercices, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p2.SetSizer(sizer_p2)

        sizer_p3.Add(self.panel_gestion_adherents, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p3.SetSizer(sizer_p3)

        sizer_types_a.Add(self.label_description_type_adhesion, 0, wx.ALL|wx.EXPAND, 10)
        sizer_types_a.Add(self.panel_gestion_types_adhesion, 1, wx.ALL, 5)
        sizer_p4.Add(sizer_types_a, 1, wx.ALL|wx.EXPAND, 5)

        sizer_types_c.Add(self.label_description_type_cotisation, 0, wx.ALL|wx.EXPAND, 10)
        sizer_types_c.Add(self.panel_gestion_types_cotisation, 1, wx.ALL, 5)
        sizer_p4.Add(sizer_types_c, 1, wx.ALL|wx.EXPAND, 5)

        self.notebook_p4.SetSizer(sizer_p4)

        self.notebook.AddPage(self.notebook_p1, u"Param�tres de l'association")
        self.notebook.AddPage(self.notebook_p2, "Exercices comptables")
        self.notebook.AddPage(self.notebook_p3, u"Adh�rents")
        self.notebook.AddPage(self.notebook_p4, u"Types de cotisation et d'adh�sion")
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
