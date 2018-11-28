# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Njoy_Cad
                                 A QGIS plugin
 cad fr
                             -------------------
        begin                : 2018-11-26
        copyright            : (C) 2018 by MIGLIORATI Bastien
        email                : s
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
    """Load Njoy_Cad class from file Njoy_Cad.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .NjoyCad import Njoy_Cad
    return Njoy_Cad(iface)
