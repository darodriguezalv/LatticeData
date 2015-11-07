# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LatticeData
                                 A QGIS plugin
 This plugin procces lattice data
                             -------------------
        begin                : 2015-10-07
        copyright            : (C) 2015 by Andrea Castillo, Juan Carrillo, Diego Rodriguez
        email                : darodriguezalv@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LatticeData class from file LatticeData.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .LaticeData import LatticeData
    return LatticeData(iface)
