# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LatticeDataDialog
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QPixmap

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'LaticeData_dialog_base.ui'))


class LatticeDataDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LatticeDataDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        """inserta"""
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'universidad.gif'))
        self.label.setPixmap(pixmap)
        pixmapsp = QPixmap(os.path.join(os.path.dirname(__file__), 'scatterplot.jpg'))
        self.scatterplot.setPixmap(pixmapsp)
        self.txtOutput.clear()
        self.btnOutput.clicked.connect(self.select_output_file)
        self.btnSelect.clicked.connect(self.select_matrix_file)
        self.btnCancel.clicked.connect(self.btnCancel_clicked)

        self.rdButtonContWQ.setChecked(1)
        self.rdButtonContW.setChecked(1)

        self.horizontalSlider.setValue(0)
        self.spinBox.setValue(1)
        """fin inserta"""

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self, "Select output file ","","GAL File (*.gal);;Dbase (*.dbf)")
        self.txtOutput.setText(filename)

    def select_matrix_file(self):
        matrixfilename = QFileDialog.getOpenFileName(self, "Select matrix file ","", "GAL File (*.gal);;Dbase (*.dbf)")
        self.txtSelect.setText(matrixfilename)

    def btnCancel_clicked(self):
        self.reject()