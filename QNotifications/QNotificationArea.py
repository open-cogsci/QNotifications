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

from qtpy import QtWidgets, QtCore, QtGui
from QNotifications.QNotification import QNotification
from QNotifications.abstractions import *

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

import os

class QNotificationArea(QtWidgets.QWidget):

	default_notification_styles = """
	.QNotification #primary {
		color: '#FFFFFF';
		background-color: '#337AB7';
		border-radius: 5px;
		font-size: 15px;
	}

	.QNotification #success {
		color: '#000000';
		background-color: '#DFF0D8';
		border-radius: 5px;
		font-size: 15px;
	}
	"""

	### OpenSesame events
	def __init__(self, targetWidget, *args, **kwargs):
		super(QNotificationArea, self).__init__(*args, **kwargs)
		self.setObjectName("QNotificationArea")
		self.setParent(targetWidget)
		self.targetWidget = targetWidget
		self.setContentsMargins(0, 10, 0, 0)

		# Store original target classes resizeEvent to be called in our own
		# function
		self.old_target_resize_event = targetWidget.resizeEvent
		# Overwrite resizeEvent function of targetWidget to capture it ourself
		# (parent's resizeEvent will be called in our function too)
		self.targetWidget.resizeEvent = self.resizeEvent
		
		# self.notification_area.setStyleSheet("border: 1px solid #F00")
		notification_area_layout = QtWidgets.QVBoxLayout()
		notification_area_layout.setContentsMargins(50,0,50,0)
		self.setLayout(notification_area_layout)
		self.mapTo(targetWidget, QtCore.QPoint(0,0))

		self.entryEffect = None
		self.entryEffectDuration = None

		self.setStyleSheet(self.default_notification_styles)

	def __delete_notification(self, notification=None):
		notification.close()
		self.layout().removeWidget(notification)
		self.adjustSize()

	# Public functions
	
	def setEntryEffect(self, effect, duration=250):
		self.entryEffect = effect
		self.entryEffectDuration = duration

	# Events
	@QtCore.pyqtSlot('QString', 'QString', int)
	def display(self, message, messagetype, timeout=0):
		notification = QNotification(message, messagetype)
		notification.closeClicked.connect(self.remove)
		self.layout().addWidget(notification)
		# Check for entry effects
		if not self.entryEffect is None:
			if self.entryEffect == "fadeIn":
				notification.fadeIn(self.entryEffectDuration)
		else:
			notification.display()

		self.adjustSize()
		if timeout > 0:
			QtCore.QTimer.singleShot(timeout, 
				lambda : self.remove(notification))

	@QtCore.pyqtSlot()
	def remove(self, notification = None):
		# This function also functions as a pyqt slot. In that case, no
		# notification argument is passed, but this is set as self.sender()
		if notification is None:
			try:
				notification = self.sender()
			except:
				raise ValueError('QNotification object needs to be passed '
					'or this function should be used as a slot for a signal'
					' emitted by a QNotification')

		if notification.isBeingRemoved:
			return
		else:
			notification.isBeingRemoved = True

		# Check if notification is still present (and has not manually been
		# closed before this function is called by a timeout)
		if self.layout().indexOf(notification) < 0:
			return

		# Implement animation here
		animation = 'fadeOut'
		if animation == 'fadeOut':
			notification.fadeOut(self.__delete_notification)
		else:
			self.__delete_notification(notification)

		
	def resizeEvent(self, event):
		self.old_target_resize_event(event)
		newsize = event.size()		
		self.setFixedWidth(newsize.width())
	
	