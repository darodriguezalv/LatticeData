# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LatticeData
                                 A QGIS plugin
 This plugin procces lattice data
                              -------------------
        begin                : 2015-10-07
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Andrea Castillo, Juan Carrillo, Diego Rodriguez
        email                : darodriguezalv@gmail.com
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
from PyQt4.QtGui import QAction, QIcon, QMainWindow
from PyQt4 import QtCore
from PyQt4 import QtGui

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from LaticeData_dialog import LatticeDataDialog
import os.path
"""import pysal library for spatial statistics functions"""
try:
    import pysal
    from pysal.weights.util import get_ids, get_points_array_from_shapefile, min_threshold_distance
except:
    QtGui.QMessageBox.warning(None,"Error","Oops! LatticeData Require Pysal.  Try again...")
"""import scipy library for distance function"""
import scipy
"""import numpy library for array function"""
import numpy as np
"""import matplotlib library for scatterplot"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FixedLocator
from qgis.gui import QgsMessageBar, QgsMapLayerComboBox, QgsMapLayerProxyModel
import sys
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject

@pyqtSlot( result = str )


class LatticeData:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
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
            'LatticeData_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = LatticeDataDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Lattice Data')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LatticeData')
        self.toolbar.setObjectName(u'LatticeData')

        """buttons connected with methods"""
        """comboBoxLayer"""

        self.cmbBoxSelectLayer = QgsMapLayerComboBox(self.dlg)
        self.cmbBoxSelectLayer.setFixedWidth(200)
        self.cmbBoxSelectLayer.move(140,20)
        self.cmbBoxSelectLayer.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.cmbBoxSelectLayer.enabledChange(False)
        self.cmbBoxSelectLayer.currentIndexChanged[str].connect(self.changeCurrentIndex)

        """radioButtonSelectMatrix"""

        self.dlg.rdButton_nm.clicked.connect(self.activateNewMatrix)
        self.dlg.rdButton_sm.clicked.connect(self.activateSelectMatrix)

        """radioButtonSelectMatrixWeight"""

        self.dlg.rdButtonContW.clicked.connect(self.radioContW)
        self.dlg.rdButtonDisW.clicked.connect(self.radioDisW)
        self.dlg.rdButtonKNW.clicked.connect(self.radioKNW)

        """sliderdistance"""

        self.dlg.horizontalSlider.setMinimum(0)
        self.dlg.horizontalSlider.setMaximum(100)
        self.dlg.horizontalSlider.setSingleStep(1)
        self.dlg.horizontalSlider.valueChanged[int].connect(self.changeValueSlider)

        """Buttons and connects"""

        self.dlg.btnSave.clicked.connect(self.generate_matrix)

        self.dlg.checkBox.stateChanged.connect(self.activatemoranI)

        self.dlg.cmbBoxSelectField.currentIndexChanged[str].connect(self.moranI)

        self.dlg.btnMoranI.clicked.connect(self.grafico)

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
        return QCoreApplication.translate('LatticeData', message)


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

        icon_path = ':/plugins/LatticeData/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Lattice Data'),
            callback=self.run,
            parent=self.iface.mainWindow())

    """Enable GroupBox and Widgets for select type"""

    def activateNewMatrix(self,enable):
        if enable:
            self.dlg.groupBox_wm.setEnabled(True)
            self.dlg.groupBox_mi.setEnabled(False)
            self.dlg.widget_sm.setEnabled(False)

    """Enable GroupBox and Widgets for select type"""

    def activateSelectMatrix(self,enable):
        if enable:
            self.dlg.groupBox_wm.setEnabled(False)
            self.dlg.groupBox_mi.setEnabled(True)
            self.dlg.widget_sm.setEnabled(True)

    """Enable GroupBox and Widgets for Contiguity Matrix"""

    def radioContW(self,enable):
        if enable:
            self.dlg.widget_cw.setEnabled(True)
            self.dlg.widget_dw.setEnabled(False)
            self.dlg.widget_knn.setEnabled(False)

    """Enable GroupBox and Widgets for distance Matrix"""

    def radioDisW(self,enable):
        if enable:
            self.dlg.widget_cw.setEnabled(False)
            self.dlg.widget_dw.setEnabled(True)
            self.dlg.widget_knn.setEnabled(False)

    """Enable GroupBox and Widgets for k Neighbors Matrix"""

    def radioKNW(self,enable):
        if enable:
            self.dlg.widget_cw.setEnabled(False)
            self.dlg.widget_dw.setEnabled(False)
            self.dlg.widget_knn.setEnabled(True)

    """Generate Matrix for select type and file extension"""

    def generate_matrix(self):

        if self.dlg.txtOutput.text()=='':
            QtGui.QMessageBox.warning(None,"Error","Oops!  Generate weight matrix.  Try again...")

        else:
            filenamein=self.myfile
            filename = self.dlg.txtOutput.text()
            self.filename=filename
            ext=filename[-3:]

            """matrix"""
            if self.dlg.rdButtonContW.isChecked()==True:

                if self.dlg.rdButtonContWQ.isChecked()==True:
                    w = pysal.queen_from_shapefile(filenamein,idVariable=None)
                    if ext=='gal':
                        output_file = pysal.open(filename,'w')
                        output_file.write(w)
                    else:
                        output_file = pysal.open(filename,'w','arcgis_dbf')
                        output_file.write(w, useIdIndex=True)
                    output_file.close()

                if self.dlg.rdButtonContWR.isChecked()==True:
                    w = pysal.rook_from_shapefile(filenamein,idVariable=None)
                    if ext=='gal':
                        output_file = pysal.open(filename,'w')
                        output_file.write(w)
                    else:
                        output_file = pysal.open(filename,'w','arcgis_dbf')
                        output_file.write(w, useIdIndex=True)
                    output_file.close()

                if self.dlg.rdButtonContWB.isChecked()==True:
                    wr = pysal.rook_from_shapefile(filenamein,idVariable=None)
                    wq = pysal.queen_from_shapefile(filenamein,idVariable=None)
                    wb = pysal.w_difference(wq, wr,constrained = False)
                    if ext=='gal':
                        output_file = pysal.open(filename,'w')
                        output_file.write(wb)
                    else:
                        output_file = pysal.open(filename,'w','arcgis_dbf')
                        output_file.write(wb, useIdIndex=True)
                    output_file.close()

            if self.dlg.rdButtonDisW.isChecked()==True:

                w = pysal.threshold_binaryW_from_shapefile(filenamein, float(self.dlg.txtThresh.text()))
                if ext=='gal':
                    output_file = pysal.open(filename,'w')
                    output_file.write(w)
                else:
                    output_file = pysal.open(filename,'w','arcgis_dbf')
                    output_file.write(w, useIdIndex=True)
                output_file.close()

            if self.dlg.rdButtonKNW.isChecked()==True:

                w = pysal.knnW_from_shapefile(filenamein, k=self.dlg.spinBox.value())
                if ext=='gal':
                    output_file = pysal.open(filename,'w')
                    output_file.write(w)
                else:
                    output_file = pysal.open(filename,'w','arcgis_dbf')
                    output_file.write(w, useIdIndex=True)
                output_file.close()

            """end matrix"""

            QtGui.QMessageBox.warning(None,"Complete","Weight matrix is generated")

    """Enable GroupBox and Widgets for calculate MoransI"""

    def activatemoranI(self, enable):

        if enable==2 and self.dlg.txtOutput.text()=='':
            QtGui.QMessageBox.warning(None,"Error","Oops!  Generate weight matrix.  Try again...")
            self.dlg.checkBox.setCheckState(0)
            enable=0
        if enable==2 and self.dlg.txtOutput.text()!='':
            self.dlg.txtSelect.setText(self.dlg.txtOutput.text())
            self.dlg.groupBox_mi.setEnabled(True)
            self.dlg.groupBox_wm.setEnabled(False)
        if enable==0:
            self.dlg.txtMoranI.clear()
            self.dlg.txtMoranIp.clear()
            self.dlg.txtMoranIint.clear()
            self.dlg.groupBox_mi.setEnabled(False)
            self.dlg.groupBox_wm.setEnabled(True)

    """Calculate MoransI for index in comboBox"""

    def moranI(self):

        if (self.dlg.checkBox.checkState()==2 and self.dlg.rdButton_nm.isChecked()==True)or self.dlg.rdButton_sm.isChecked()==True:

            self.w=pysal.open(os.path.join(os.path.dirname(__file__), 'default.gal')).read()
            try:
                self.w = pysal.open(self.dlg.txtSelect.text()).read()

            except IOError, e:
                print e.errno
                print e

            selectedFieldIndex = self.dlg.cmbBoxSelectField.currentIndex()
            field= self.fieldsnumeric[selectedFieldIndex]
            self.fieldName = field.name()

            dbasefile=self.myfile[:-3]+'dbf'
            dbase = pysal.open(dbasefile)
            self.y = np.array(dbase.by_col[self.fieldName], dtype=('<f8'))

            """self.dlg.txtSelectSystemC.setPlainText("")
            for i in self.y:
                self.dlg.txtSelectSystemC.appendPlainText(str(i))"""

            if self.w.n == self.y.size:
                self.mi = pysal.Moran(self.y, self.w, two_tailed=False)

                self.dlg.txtMoranI.setText(str(round(self.mi.I,5)))
                self.dlg.txtMoranIp.setText(str(round(self.mi.p_norm,5)))

                if self.mi.I >0.75 and self.mi.p_norm <0.05:
                    self.dlg.txtMoranIint.setText("I de Moran cercano a 1 y p value significativo (confianza 95%): posible autocorrelacion espacial")
                elif self.mi.I <-0.75 and self.mi.p_norm <0.05:
                    self.dlg.txtMoranIint.setText("I de Moran cercano a -1 y p value significativo (confianza 95%): posible autocorrelacion espacial")
                elif self.mi.I >-0.05 and  self.mi.I <0.05:
                    self.dlg.txtMoranIint.setText("I de Moran cercano a 0: no existe autocorrelacion espacial")
                elif self.mi.p_norm <0.05:
                    self.dlg.txtMoranIint.setText("p value significativo (confianza 95%): posible autocorrelacion espacial debil")
                else:
                    self.dlg.txtMoranIint.setText("p value no significativo (confianza 95%): no existe autocorrelacion espacial")

                """lm = pysal.Moran_Local(y,w)"""
                """self.dlg.txtSelectSystemC2.appendPlainText(str(lm.p_sim))"""
                """self.dlg.txtOutput_2.setText(str(self.w.n)+' - '+str(self.y.size))"""
            else:
                QtGui.QMessageBox.warning(None,"Error","Oops!  matrix has not been generated or not exists.  Generate and try again...")
                self.dlg.checkBox.setCheckState(0)
                self.dlg.txtMoranI.clear()
                self.dlg.txtMoranIp.clear()
                self.dlg.txtMoranIint.clear()
                """self.dlg.txtSelectSystemC.setPlainText("")"""
                self.dlg.groupBox_wm.setEnabled(True)
                self.dlg.groupBox_mi.setEnabled(False)
                self.dlg.widget_sm.setEnabled(False)
                self.dlg.rdButton_sm.setChecked(0)
                self.dlg.rdButton_nm.setChecked(1)

    """ScatterPlot"""

    def grafico(self):

        """Grafico de dispersion"""
        w=self.w
        y=self.y
        ystd=(y-np.mean(y))/np.std(y)
        w.transform = 'r'
        yl = pysal.lag_spatial(w,ystd)

        colors = np.random.rand(100)
        """area = np.pi * (15 * np.random.rand(100))**2 # 0 to 15 point radiuses"""

        fig, ax = plt.subplots()
        m, fit = np.polyfit(ystd, yl, deg=1)
        """ax.plot(self.y, fit[0] * self.y + fit[1], color='blue', alpha=0.4, linewidth=0.3, linestyle='dotted')"""
        ax.scatter(ystd, yl, c=colors, alpha=0.5)
        ax.plot(ystd, m*ystd + fit, color='blue', alpha=0.4, linewidth=0.3)

        fig.suptitle('Moran`s I: '+str(round(self.mi.I,5)))
        plt.xlabel(self.fieldName)
        plt.ylabel('Spatial Lag '+self.fieldName)

        ax.set_yticks([np.mean(yl)],minor=False)
        ax.yaxis.set_major_locator(FixedLocator([round(np.mean(yl),5)]))
        ax.yaxis.grid(True)

        ax.set_xticks([np.mean(ystd), np.amax(ystd)],minor=True)
        ax.xaxis.set_major_locator(FixedLocator([round(np.mean(ystd),5)]))
        ax.xaxis.grid(True)

        """ax.spines['left'].set_position((y,np.mean(y)))"""
        """ax.spines['bottom'].set_position((yl,np.mean(yl)))"""
        """ax.set_yticklabels(['Bill', 'Jim'])"""
        """plt.grid(True)"""
        """fig.savefig('test.jpg')"""
        fig.show()

    """Actions for change Index comboBox Select Layer"""

    def changeCurrentIndex(self):

        self.dlg.groupBox_wm.setEnabled(False)
        self.dlg.groupBox_mi.setEnabled(False)
        self.dlg.widget_sm.setEnabled(False)

        self.dlg.widget_dw.setEnabled(False)
        self.dlg.widget_knn.setEnabled(False)

        self.dlg.buttonGroup_calculate.setExclusive(False)
        self.dlg.rdButton_nm.setChecked(False)
        self.dlg.rdButton_sm.setChecked(False)
        self.dlg.buttonGroup_calculate.setExclusive(True)

        self.dlg.checkBox.setChecked(0)
        self.dlg.txtOutput.clear()
        self.dlg.txtSelect.clear()

        self.dlg.txtMoranI.clear()
        self.dlg.txtMoranIp.clear()
        self.dlg.txtMoranIint.clear()
        """self.dlg.txtSelectSystemC.setPlainText("")"""

        try:
            self.selectedLayer = self.cmbBoxSelectLayer.currentLayer()
            myfilepath=os.path.realpath(self.selectedLayer.dataProvider().dataSourceUri())
            self.myfile=myfilepath[:-10]

            """self.dlg.txtOutput_2.setText(self.myfile)"""

            self.thresh = pysal.min_threshold_dist_from_shapefile(self.myfile)
            array = get_points_array_from_shapefile(self.myfile)
            dist = scipy.spatial.distance.cdist(array,array)
            self.maxthresh=np.amax(dist)
            self.dlg.txtThresh.setText(str(round(self.thresh,5)))

            self.fields = self.selectedLayer.pendingFields()
            self.fieldnames=[]
            self.fieldsnumeric=[]
            for field in self.fields:
                if field.typeName()=='Real' or field.typeName()=='Integer':
                    self.fieldnames.append(field.name())
                    self.fieldsnumeric.append(field)

            self.dlg.cmbBoxSelectField.clear()
            self.dlg.cmbBoxSelectField.addItems(self.fieldnames)
        except:
            QtGui.QMessageBox.warning(None,"Error","There is not layers or it is change.  Try again...")

        self.dlg.cmbBoxSelectField.clear()
        self.dlg.cmbBoxSelectField.addItems(self.fieldnames)

    """Value of slider and connect with minimum and maximum distance between polygons """

    def changeValueSlider(self, value):

        if value == 0:
            self.dlg.txtThresh.setText(str(round(self.thresh,5)))
        elif value > 0 and value < 100:
            distance=((self.thresh)+((self.maxthresh-self.thresh)*(value/100.0)))
            self.dlg.txtThresh.setText(str(round(distance,5)))
        elif value ==100:
            self.dlg.txtThresh.setText(str(round(self.maxthresh,5)))

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Lattice Data'),
                action)
            self.iface.removeToolBarIcon(action)

    """Actions for run plugin"""

    def run(self):
        """Run method that performs all the real work"""
        self.dlg.groupBox_wm.setEnabled(False)
        self.dlg.groupBox_mi.setEnabled(False)
        self.dlg.widget_sm.setEnabled(False)

        self.dlg.widget_dw.setEnabled(False)
        self.dlg.widget_knn.setEnabled(False)

        """rev"""

        try:
            self.selectedLayer = self.cmbBoxSelectLayer.currentLayer()
            myfilepath=os.path.realpath(self.selectedLayer.dataProvider().dataSourceUri())
            self.myfile=myfilepath[:-10]

            """self.dlg.txtOutput_2.setText(self.myfile)"""

            self.thresh = pysal.min_threshold_dist_from_shapefile(self.myfile)
            array = get_points_array_from_shapefile(self.myfile)
            dist = scipy.spatial.distance.cdist(array,array)
            self.maxthresh=np.amax(dist)
            self.dlg.txtThresh.setText(str(round(self.thresh,5)))

            self.fields = self.selectedLayer.pendingFields()
            self.fieldnames=[]
            self.fieldsnumeric=[]
            for field in self.fields:
                if field.typeName()=='Real' or field.typeName()=='Integer':
                    self.fieldnames.append(field.name())
                    self.fieldsnumeric.append(field)

            self.dlg.cmbBoxSelectField.clear()
            self.dlg.cmbBoxSelectField.addItems(self.fieldnames)
        except:
            QtGui.QMessageBox.warning(None,"Error","There is not layers.  Try again...")
            pass
        """rev"""

         # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass




