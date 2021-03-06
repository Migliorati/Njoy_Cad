# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Njoy_Cad
                                 A QGIS plugin
 cad fr
                              -------------------
        begin                : 2018-11-26
        git sha              : $Format:%H$
        copyright            : (C) 2018 by MIGLIORATI Bastien
        email                : s
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from NjoyCad_dialog import Njoy_CadDialog
import os.path


class Njoy_Cad:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Njoy_Cad_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Njoy_cad')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Njoy_Cad')
        self.toolbar.setObjectName(u'Njoy_Cad')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Njoy_Cad', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Njoy_CadDialog()
		
	self.dlg.pushButtonDownload.clicked.connect(self.downloadCAD)
	
	self.dlg.pushButton_2.clicked.connect(self.LoadCAD)
		
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Njoy_Cad/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Njoy__Cad'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Njoy_cad'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def downloadCAD(self):
		import os
		import os.path
		import webbrowser
		import sys

		insee_value = self.dlg.lineEdit.text()
		departement_value = insee_value[:2]

		url = 'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/' + departement_value + '/' + insee_value + '/cadastre-' + insee_value + '-batiments.json.gz'
		url1 = 'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/geojson/communes/' + departement_value + '/' + insee_value + '/cadastre-' + insee_value + '-parcelles.json.gz'

		
		import subprocess  

		info = subprocess.STARTUPINFO()
		info.dwFlags = 1
		info.wShowWindow = 0
		
		subprocess.Popen("start chrome /new-tab " + url, shell=True, startupinfo=info)
		subprocess.Popen("start chrome /new-tab " + url1, shell=True, startupinfo=info)
		
		import time
		time.sleep(5)
		
    def LoadCAD(self):
		
		import time
		from qgis.core import QgsVectorLayer
		from qgis.core import QgsMapLayerRegistry
		import gzip
		import shutil
		import os
		import os.path	
		import sys
		from PyQt4 import QtCore, QtGui
		from PyQt4.QtCore import *
		from PyQt4.QtGui import *

		
		insee_value = self.dlg.lineEdit.text()
		departement_value = insee_value[:2]	
		
		if self.dlg.checkBox.isChecked() == True:
			
			chemin_dl_parcelles = os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-parcelles.json.gz')
			exists = os.path.isfile(chemin_dl_parcelles)
			if exists:
		
				# file exists
					
				with gzip.open(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-parcelles.json.gz'), 'rb') as f_in:
					with open(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-parcelles.json'), 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)	
						
				time.sleep(5)	
				
				vlayer2 = QgsVectorLayer(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-parcelles.json'),insee_value + '_Parcelles',"ogr")
				QgsMapLayerRegistry.instance().addMapLayer(vlayer2)	
			else :
				QtGui.QMessageBox.critical(None, self.tr("Erreur"), self.tr('Cadastre(Parcelles) absent. Veuillez renseigner votre code insee et cliquer sur telecharger au prealable. Il se peut egalement que le code insee renseigne soit vide ou incorrect.'))
			
		if self.dlg.checkBox_2.isChecked() == True:		
		
			chemin_dl_batiments = os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-batiments.json.gz')
			exists = os.path.isfile(chemin_dl_batiments)
			if exists:
		
				with gzip.open(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-batiments.json.gz'), 'rb') as f_in:
					with open(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-batiments.json'), 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)
							
				time.sleep(5)
				
				vlayer = QgsVectorLayer(os.path.expandvars(r'C:\Users\%USERNAME%\Downloads\cadastre-' + insee_value + '-batiments.json'),insee_value + '_Batiments',"ogr")
				QgsMapLayerRegistry.instance().addMapLayer(vlayer)			

			else :
				QtGui.QMessageBox.critical(None, self.tr("Erreur"), self.tr('Cadastre(Batiments) absent. Veuillez renseigner votre code insee et cliquer sur telecharger au prealable. Il se peut egalement que le code insee renseigne soit vide ou incorrect.'))

				
		if self.dlg.checkBox_3.isChecked() == True:			

			from qgis.core import QgsVectorLayer
			from qgis.core import QgsPoint
			from qgis.core import QgsRasterLayer
			from qgis.core import *
			
			
			#urlWithParams = 'crs=EPSG:2154&format=image/png&layers=VOIE_COMMUNICATION&styles=&url=http://inspire.cadastre.gouv.fr/scpc/f4892f41e4004cc88f/' + insee_value + '.wms?service=WMS&request=GetMap'
			#urlWithParams = 'crs=EPSG:2154&dpiMode=all&format=image/png&layers=VOIE_COMMUNICATION&styles=&url=http://inspire.cadastre.gouv.fr/scpc/f4892f41e4004cc88f/' + insee_value + '.wms&version=1.3&request=Getmap&'
			
			urlWithParams = 'url=http://inspire.cadastre.gouv.fr/scpc/f4892f41e4004cc88f/' + insee_value + '.wms?contextualWMSLegend=0&crs=EPSG:2154&dpiMode=7&featureCount=10&format=image/png&layers=VOIE_COMMUNICATION&styles=&maxHeight=1024&maxWidth=1280'
			
			rlayer = QgsRasterLayer(urlWithParams, insee_value + '_Noms-rues', 'wms')
			rlayer.isValid()
			QgsMapLayerRegistry.instance().addMapLayer(rlayer)
			
    def run(self):
        """Run method that performs all the real work"""
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
