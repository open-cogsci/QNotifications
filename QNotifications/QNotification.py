# -*- coding: utf-8 -*-
"""
@author: Daniel Schreij

This file is part of QNotifications.

QNotifications is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

QNotifications is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GPLv3 License
along with this module.>.
"""

# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from qtpy import QtWidgets, QtCore
from QNotifications.abstractions import *

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

class QNotification(QtWidgets.QWidget):
	""" Class representing a single notification """

	closeClicked = QtCore.pyqtSignal()

	def __init__(self, message, category, *args, **kwargs):
		super(QNotification, self).__init__(*args, **kwargs)
		# Store instance variables
		self.message = message
		self.category = category

		# Set Object name for reference
		self.setObjectName('QNotification')
		self.setFixedHeight(40)
		self.setLayout(QtWidgets.QHBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)

		# Create a message area
		self.messageArea = QtWidgets.QWidget(self)
		self.messageArea.setObjectName(category)
		self.layout().addWidget(self.messageArea)

		# Create the layout
		self.messageArea.setLayout(QtWidgets.QHBoxLayout())
		self.message_display = QtWidgets.QLabel()

		# Create a button that can close notifications
		close_button = QtWidgets.QPushButton("X")
		close_button.setFixedWidth(20)
		close_button.clicked.connect(self.closeClicked)

		# Add everything together
		self.messageArea.layout().addWidget(self.message_display)
		self.messageArea.layout().addStretch(1)
		self.messageArea.layout().addWidget(close_button)

		# Initialize some variables
		self.setStyle(category)
		self.setVisible(False)

		# Flag that is set if notification is being removed. This can be used to
		# make sure that even though the notification has not been really removed
		# yet (because it is for example in an fade out animation), it is in the 
		# process of being removed
		self.isBeingRemoved = False

		self.__init_graphic_effects()

	def __init_graphic_effects(self):
		# Opacityeffect for fade in/out
		self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)

		# Fade in animation
		self.fadeInAnimation = QtCore.QPropertyAnimation(self.opacityEffect, 
			safe_encode("opacity"))
		self.fadeInAnimation.setStartValue(0.0)
		self.fadeInAnimation.setEndValue(1.0)

		# Fade out animation
		self.fadeOutAnimation = QtCore.QPropertyAnimation(self.opacityEffect, 
			safe_encode("opacity"))
		self.fadeOutAnimation.setStartValue(1.0)
		self.fadeOutAnimation.setEndValue(0.0)

	def setStyle(self, category):
		if category == "primary":
			textcolor = "#FFFFFF"
			bgcolor = '#337AB7'
		elif category == "success":
			textcolor = "#000000"
			bgcolor = '#DFF0D8'
		elif category == "info":
			textcolor = "#000000"
			bgcolor = '#D9EDF7'
		elif category == "warning":
			textcolor = "#000000"
			bgcolor = '#FCF8E3'
		elif category == "danger":
			textcolor = "#000000"
			bgcolor = '#F2DEDE'

		self.setStyleSheet(
			"""
			color: {};
			background-color: {};
			border-radius: 5px;
			font-size: 15px;
			""".format(textcolor, bgcolor))

	def display(self):
		self.message_display.setText(self.message)
		self.show()

	def close(self):
		super(QNotification,self).close()
		self.deleteLater()

	def fadeIn(self, duration=100):
		self.setGraphicsEffect(self.opacityEffect)
		self.fadeInAnimation.setDuration(duration)
		self.display()
		self.fadeInAnimation.start()

	def fadeOut(self, finishedCallback, duration=500):
		self.setGraphicsEffect(self.opacityEffect)
		self.fadeOutAnimation.setDuration(duration)
		self.fadeOutAnimation.finished.connect(lambda: finishedCallback(self))
		self.isBeingRemoved = True
		self.fadeOutAnimation.start()

	### Property attributes
	@property
	def message(self):
		return self._message

	@message.setter
	def message(self, value):
		self._message = value

	@property
	def category(self):
	    return self._category

	@category.setter
	def category(self, value):
		allowed_values = ['primary','success','info','warning','danger']
		if not value in allowed_values:
			raise ValueError(_('{} not a valid value. '
				'Should be one of').format(value, allowed_values))
		self._category = value

