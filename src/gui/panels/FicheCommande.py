#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import wx.lib.agw.genericmessagedialog as GMD

from lib.objectlistview import ObjectListView, ColumnDefn, Filter
from textwrap import fill

from classes.Validators import GenericTextValidator, VALIDATE_INT

from model.model import Commande, LigneCommande, Produit, DATABASE
from datetime import date, datetime

###########################################################################
## Class FicheCommande
###########################################################################


class FicheCommande(wx.Panel):
    def __init__(self, parent, commande=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if commande == None:
            commande = Commande.create()

        self.commande = commande

        self.sizer_commande_staticbox = wx.StaticBox(self, -1, "Commande")
        self.sizer_fournisseur_produits_staticbox = wx.StaticBox(self, -1, "Liste des produits")
        self.label_titre_commande = wx.StaticText(self, -1, "Commande pour ")
        self.bouton_infos_fournisseur = wx.Button(self, -1, "Afficher les infos du fournisseur")
        self.label_date_commande = wx.StaticText(self, -1, "Date de la commande :")
        self.datepicker_date_commande = wx.DatePickerCtrl(self, -1)
        self.label_FiltreRecherche = wx.StaticText(self, -1, "Recherche sur le nom :")
        self.text_ctrl_FiltreRecherche = wx.TextCtrl(self, -1, "")
        self.liste_produits = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.label_total = wx.StaticText(self, -1, "Total de la commande :")
        self.label_total_valeur = wx.StaticText(self, -1, u"0.00 �", style=wx.ALIGN_RIGHT)
        self.liste_lignes_commande = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.bouton_Sauvegarder = wx.Button(self, -1, "Enregistrer la commande")

        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE", minimumWidth=100),
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn("Prix TTC", "right", -1, "prix_achat_TTC", stringConverter=u"%.2f �", minimumWidth=100),
            ColumnDefn("Conditionnement", "left", -1, "conditionnement_format", isSpaceFilling=True, minimumWidth=200)
        ])
        self.liste_produits.SetEmptyListMsg("Ce fournisseur n'a aucun produit")
        self.liste_produits.AutoSizeColumns()

        self.liste_lignes_commande.SetColumns([
            ColumnDefn("Ref Fournisseur", "left", -1, "produit.ref_fournisseur", minimumWidth=120),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn(u"Quantit�", "left", -1, "quantite_commandee_conditionnement", minimumWidth=150),
            ColumnDefn("Total TTC", "right", -1, "prix_total_commande_ttc", stringConverter=u"%s �", isSpaceFilling=True, minimumWidth=100)
        ])
        self.liste_lignes_commande.AutoSizeColumns()

        self.liste_lignes_commande.SetEmptyListMsg("La commande ne contient aucun produit")

        self.__set_properties()
        self.__set_values()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnInfosFournisseur, self.bouton_infos_fournisseur)
        self.Bind(wx.EVT_BUTTON, self.OnSauvegarder, self.bouton_Sauvegarder)
        self.Bind(wx.EVT_TEXT, self.OnFilter, self.text_ctrl_FiltreRecherche)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnAjoutProduit, self.liste_produits)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModifProduit, self.liste_lignes_commande)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: NouvelleCommande.__set_properties
        self.label_titre_commande.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_fournisseur_produits_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_commande_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.text_ctrl_FiltreRecherche.SetMinSize((200, -1))
        # end wxGlade

    def __set_values(self):
        if self.commande.fournisseur:
            self.SetFournisseur(self.commande.fournisseur)
            
            date = wx.DateTime()
            date.Set(self.commande.date_commande.day, self.commande.date_commande.month-1, self.commande.date_commande.year)
            self.datepicker_date_commande.SetValue(date)

            self.liste_lignes_commande.SetObjects([lc for lc in self.commande.lignes_commande])
            self.label_total_valeur.SetLabel(u"%.2f �" % self.commande.total_commande_TTC())

    def __do_layout(self):
        # begin wxGlade: NouvelleCommande.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entete = wx.BoxSizer(wx.HORIZONTAL)
        sizer_date_commande= wx.BoxSizer(wx.HORIZONTAL)
        sizer_commande = wx.StaticBoxSizer(self.sizer_commande_staticbox, wx.VERTICAL)
        sizer_fournisseur_produits = wx.StaticBoxSizer(self.sizer_fournisseur_produits_staticbox, wx.HORIZONTAL)
        sizer_ligne_total = wx.BoxSizer(wx.HORIZONTAL)
        sizer_liste_produits = wx.BoxSizer(wx.VERTICAL)
        sizer_fitre_recherche = wx.BoxSizer(wx.HORIZONTAL)

        sizer_entete.Add(self.label_titre_commande, 1, wx.EXPAND, 0)
        sizer_entete.Add(self.bouton_infos_fournisseur, 0, wx.EXPAND, 0)
        sizer.Add(sizer_entete, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        sizer_date_commande.Add(self.label_date_commande, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_date_commande.Add(self.datepicker_date_commande, 0, 0, 0)
        sizer.Add(sizer_date_commande, 0, wx.EXPAND, 0)

        sizer_fitre_recherche.Add(self.label_FiltreRecherche, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_fitre_recherche.Add(self.text_ctrl_FiltreRecherche, 0, 0, 0)
        sizer_liste_produits.Add(sizer_fitre_recherche, 0, wx.BOTTOM|wx.EXPAND, 6)
        sizer_liste_produits.Add(self.liste_produits, 1, wx.EXPAND, 0)
        sizer_fournisseur_produits.Add(sizer_liste_produits, 1, wx.EXPAND, 0)
        sizer.Add(sizer_fournisseur_produits, 1, wx.TOP|wx.EXPAND, 10)

        sizer_ligne_total.Add(self.label_total, 0, wx.EXPAND|wx.RIGHT, 20)
        sizer_ligne_total.Add(self.label_total_valeur, 0, wx.ALIGN_RIGHT, 0)

        sizer_commande.Add(sizer_ligne_total, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 6)
        sizer_commande.Add(self.liste_lignes_commande, 1, wx.EXPAND, 0)
        sizer.Add(sizer_commande, 1, wx.EXPAND, 0)

        sizer_boutons.Add(self.bouton_Sauvegarder, 0, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 6)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __update_total(self):
        self.label_total_valeur.SetLabel(u"%.2f �" % self.commande.total_commande_TTC())
        self.Layout()

    def SetFournisseur(self, fournisseur):
        self.commande.fournisseur = fournisseur

        self.label_titre_commande.SetLabel("Commande pour " + self.commande.fournisseur.nom)

        try:
            produits = Produit.select().where((Produit.fournisseur == fournisseur) &
                                              (Produit.retrait == False))
            self.liste_produits.SetObjects([p for p in produits])
            self.liste_produits.AutoSizeColumns()

        except BaseException as ex:
            print ex

        self.Layout()

    def OnFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_produits, text=self.text_ctrl_FiltreRecherche.GetValue())
        self.liste_produits.SetFilter(filtre_texte)
        self.liste_produits.RepopulateList()

    def OnInfosFournisseur(self, event):  # wxGlade: NouvelleCommande.<event_handler>
        message = ""
        message += self.commande.fournisseur.nom + "\n\n"
        message += self.commande.fournisseur.adresse +"\n"
        message += self.commande.fournisseur.code_postal + " " + \
                   self.commande.fournisseur.ville + "\n\n"
        message += u"Tel fixe : " + self.commande.fournisseur.telephone_fixe + "\n"
        message += u"Tel portable : " + self.commande.fournisseur.telephone_portable + "\n"
        message += u"Email : " + self.commande.fournisseur.email + "\n\n"
        message += u"Nom du contact : " + self.commande.fournisseur.nom_contact + "\n\n"
        message += "Remarques : \n\n"

        message += fill(self.commande.fournisseur.remarques, 50)

        dlg = GMD.GenericMessageDialog(self, message, self.commande.fournisseur.nom,
                                       wx.OK|wx.ICON_INFORMATION)

        dlg.Fit()
        dlg.ShowModal()
        dlg.Destroy()

    def OnAjoutProduit(self, event):
        deja_ajoute = False
        produit_selectionne = self.liste_produits.GetSelectedObject()

        for lc_liste in self.liste_lignes_commande.GetObjects():
            if lc_liste.produit.get_id() == produit_selectionne.get_id():
                deja_ajoute = True
                break

        if deja_ajoute == False:
            lc = LigneCommande(commande=self.commande, produit=produit_selectionne)
            
            dlg = DialogChoixQuantite(lc)

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.GetQuantite() != 0:
                    lc.quantite_commandee = dlg.GetQuantite()
                    lc.save()
                    self.liste_lignes_commande.AddObject(lc)
                    self.liste_lignes_commande.AutoSizeColumns()

                    #Mise � jour du total de la commande
                    self.__update_total()

            dlg.Destroy()

    def OnModifProduit(self, event):
        lc_selectionnee = self.liste_lignes_commande.GetSelectedObject()

        dlg = DialogChoixQuantite(lc_selectionnee)

        id_resultat = dlg.ShowModal()

        if id_resultat == wx.ID_OK and dlg.GetQuantite() != 0:
            lc_selectionnee.quantite_commandee = dlg.GetQuantite()
            lc_selectionnee.save()
            self.liste_lignes_commande.RefreshObject(lc_selectionnee)
            self.liste_lignes_commande.AutoSizeColumns()
        elif id_resultat == wx.ID_DELETE or dlg.GetQuantite() == 0:
            self.liste_lignes_commande.RemoveObject(lc_selectionnee)
            self.liste_lignes_commande.RefreshObject(lc_selectionnee)
            lc_selectionnee.delete_instance()
            self.liste_lignes_commande.AutoSizeColumns()

        #Mise � jour du total de la commande
        self.__update_total()

        dlg.Destroy()

    def OnSauvegarder(self, event):
        try:
            date_commande = self.datepicker_date_commande.GetValue()
            print datetime(date_commande.GetYear(), date_commande.GetMonth()+1, date_commande.GetDay())

            self.commande.date_commande = datetime(date_commande.GetYear(), date_commande.GetMonth()+1, date_commande.GetDay())
            
            self.commande.save()
            DATABASE.commit()
            wx.MessageBox(u"La commande a �t� enregistr�e", "Notification")
        except BaseException as ex:
            wx.MessageBox(u"Probl�me lors de l'enregistrement : %s" % ex, "Erreur")

    def OnDestroy(self, event):
        if self.commande.fournisseur != None:
            dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder la commande ?",
                                   caption=u"Sauvegarde de la commande", style=wx.YES_NO|wx.ICON_QUESTION)

            if dlg.ShowModal() == wx.ID_YES:
                self.OnSauvegarder(None)
            else:
                DATABASE.rollback()

            dlg.Destroy()

        event.Skip()


###########################################################################
## Class ChoixQuantite
###########################################################################


class DialogChoixQuantite(wx.Dialog):
    def __init__(self, ligne_commande):
        wx.Dialog.__init__(self, None, -1, u"Quantit�", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.ligne_commande = ligne_commande

        self.label_type_conditionnement = wx.StaticText(self, -1, "Label type")
        self.label_quantite = wx.StaticText(self, -1, u"Quantit� :")
        self.text_quantite = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER, validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_unite = wx.StaticText(self, -1, "Label unite")
        self.bouton_ok = wx.Button(self, wx.ID_OK, "")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "")

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnregistrer, self.text_quantite)

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        self.text_quantite.SetMinSize((80, -1))
        self.text_quantite.SetFocus()
        if self.ligne_commande.produit.vrac:
            self.label_type_conditionnement.Hide()
        
    def __set_valeurs(self):
        if self.ligne_commande.produit.vrac:
            self.label_unite.SetLabel(self.ligne_commande.produit.conditionnement_format(majuscule=False))
            self.text_quantite.SetValue(str(self.ligne_commande.quantite_commandee / self.ligne_commande.produit.poids_volume))
        else:
            self.label_type_conditionnement.SetLabel(self.ligne_commande.produit.conditionnement_format())
            self.label_unite.SetLabel(u"unit�(s)")
            self.text_quantite.SetValue(str(self.ligne_commande.quantite_commandee))
            
        if self.ligne_commande.quantite_commandee > 0:
            self.bouton_annuler.SetLabel("Supprimer")
            self.bouton_annuler.SetId(wx.ID_DELETE)
            self.bouton_annuler.Bind(wx.EVT_BUTTON, self.OnSupprimer)

    def __do_layout(self):
        sizer_choix = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choix.Add(self.label_quantite, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_choix.Add(self.text_quantite, 0, wx.LEFT|wx.RIGHT, 6)
        sizer_choix.Add(self.label_unite, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_type_conditionnement, 0, wx.ALIGN_CENTER|wx.TOP, 5)
        sizer.Add(sizer_choix, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer_boutons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def GetQuantite(self):
        return int(self.text_quantite.GetValue())

    def OnEnregistrer(self, event):
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def OnSupprimer(self, event):
        self.EndModal(wx.ID_DELETE)
