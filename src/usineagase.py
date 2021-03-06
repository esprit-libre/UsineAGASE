#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Fri Nov 19 17:02:54 2010

import wx

from gui.MainFrame import MainFrame
from datetime import datetime
from peewee import SqliteDatabase
from model.model import Exercice

__author__  = u"Herv� GARNIER"
__name__    = "__main__"
__date__    = "$14 nov. 2010 18:19:52$"

EXERCICE_EN_COURS = None

class UsineAGASE(wx.App):
    def OnInit(self):
        
        wx.InitAllImageHandlers()
        
        F = wx.SplashScreen(wx.Bitmap("../icons/splash.bmp"), wx.SPLASH_TIMEOUT|wx.SPLASH_CENTER_ON_SCREEN, 2000, None, -1)
                
        frame_EcranPrincipal = MainFrame(None, title=u"Usine � GASE", droits=1)
        self.SetTopWindow(frame_EcranPrincipal)
        frame_EcranPrincipal.Show()

        try :
            database = SqliteDatabase('usineagase.sqlite', **{})
            tables_base = database.get_tables()
        except :
            msg = u"Erreur de connection � la base de donn�es"
            dlg = wx.MessageDialog(None, msg, "ERREUR", wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return 0

        tables_obligatoires = [u"achats", u"adherents", u"adhesion_types", u"adhesions", u"cotisations", u"categories", u"credits", u"commandes", u"exercices", u"fournisseurs", u"lignes_achat", u"lignes_commande", u"parametres", u"produits", u"referents", u"tvas"]
        
        
        if set(tables_obligatoires) - set(tables_base) :
            msg = u"Erreur : la base de donn�es n'est pas accessible ou n'est pas conforme."
            dlg = wx.MessageDialog(None, msg, "ERREUR", wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return 0
        else :
            #query = session.query(model.Exercice).filter(model.Exercice.DateDebut<datetime.today()).filter(model.Exercice.DateFin>datetime.today())
            #Exercice.select().where(date_debut<datetime.today())
            
            #if query.count() == 1:
            #    EXERCICE_EN_COURS = query.first()
            
            return 1

usineagase = UsineAGASE(0)
usineagase.MainLoop()
