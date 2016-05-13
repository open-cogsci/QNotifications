# -*- coding: utf-8 -*-
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

class QNotificationArea(QtWidgets.QWidget):
	""" Notification area to show notifications in. Will be projected on top of
	another QWidget which should be passed as an argument to this class. """

	default_notification_styles = u"""
	QNotification {
		font-size: 16px;
		padding: 0px;
		margin: 0px;
		border-radius: 6px;
	}

	QNotification #message{
		color: #FFFFFF;
		padding: 0px;
		margin: 0px;
		width: 100%;
	}

	QNotification #closeButton{
		color: #FFFFFF;
		padding: 0px;
		margin: 0px;
	}

	QNotification#primary {
		background-color: #337ab7;
		border-color: #2e6da4;
	}

	QNotification#success {
		background-color: #5cb85c;
		border-color: #4cae4c;
	}

	QNotification#info {
		background-color: #5bc0de;
		border-color: #46b8da;
	}

	QNotification#warning {
		background-color: #f0ad4e;
		border-color: #eea236;
	}

	QNotification#danger {
		background-color: #d9534f;
    	border-color: #d43f3a;
	}
	"""

	### OpenSesame events
	def __init__(self, targetWidget, *args, **kwargs):
		"""Constructor

		Parameters
		----------
		targetWidget : QtWidgets.QWidget
			The widget to project the notifications on
		useGlobalCSS : bool (default: False)
			Flag which indicates whether global style sheets should be used
			(which have been set at app-level). If False, the default style sheets
			stored at self.default_notification_styles will be loaded.

		Raises
		------
		TypeError : if targetWidget is not an object that inherits QWidget
		"""

		if not isinstance(targetWidget, QtWidgets.QWidget):
			raise TypeError('targetWidget is not a QWidget (or child of it')


		useGlobalCSS = kwargs.pop(u'useGlobalCSS', False)
		super(QNotificationArea, self).__init__(*args, **kwargs)
		
		if not useGlobalCSS:
			self.setStyleSheet(self.default_notification_styles)
		
		self.setParent(targetWidget)
		self.targetWidget = targetWidget
		self.setContentsMargins(0,0,0,0)
		
		notification_area_layout = QtWidgets.QVBoxLayout()
		self.setLayout(notification_area_layout)

		# Init effects to None
		self.entryEffect = None
		self.entryEffectDuration = None
		self.exitEffect = None
		self.exitEffectDuration = None

		# Store original target classes resizeEvent to be called in our own
		# function
		self.target_resize_event = targetWidget.resizeEvent
		# Overwrite resizeEvent function of targetWidget to capture it ourself
		# (parent's resizeEvent will be called in our function too)
		self.targetWidget.resizeEvent = self.resizeEvent
		self.hide()

	def __delete_notification(self, notification=None):
		""" Closes and destroys the supplied notification. """
		notification.close()
		self.layout().removeWidget(notification)
		self.adjustSize()
		# Hide notification area if it doesn't contain any items
		if self.layout().count() == 0:
			self.hide()

	# Public functions
	def setEntryEffect(self, effect, duration=250):
		""" Sets the effect with which the notifications are to appear. 
	
		Parameters
		----------
		effect : {'fadeIn', None}
			The effect which should be used (for now only 'fadeIn' is available)
			if None is passed for this argument, no effect will be used and the
			notifcations will just appear directly.
		duration : int (default: 250 ms)
			The duration of the effect in milliseconds

		Raises
		------
		TypeError
			If the object passed for duration is not an int
		ValueError
			When duration is less than 0, or effect has an invalid value
		"""

		if not effect in [u'fadeIn', None]:
			raise ValueError(u'Invalid entry effect')
		if not isinstance(duration, int):
			raise TypeError(u'Duration should be an int')
		if duration < 0:
			raise ValueError(u'Duration should be larger than 0')

		self.entryEffect = effect
		self.entryEffectDuration = duration

	def setExitEffect(self, effect, duration=500):
		""" Sets the effect with which the notifications are to disappear. 
	
		Parameters
		----------
		effect : {'fadeOut', None}
			the effect which should be used (for now only 'fadeOut' is available)
			if None is passed for this argument, no effect will be used and the
			notifcations will just appear directly.
		duration : int (default: 1000 ms)
			The duration of the effect in milliseconds

		Raises
		------
		TypeError
			If the object passed for duration is not an int
		ValueError
			When duration is less than 0, or effect has an invalid value
		"""

		if not effect in [u'fadeOut', None]:
			raise ValueError(u'Invalid exit effect')
		if not isinstance(duration, int):
			raise TypeError(u'Duration should be an int')
		if duration < 0:
			raise ValueError(u'Duration should be larger than 0')

		self.exitEffect = effect
		self.exitEffectDuration = duration

	# Events
	@QtCore.pyqtSlot('QString', 'QString', int)
	def display(self, message, category, timeout=5000):
		""" Displays a notification. 
	
		Parameters
		----------
		message : str
			The message to display
		category : {'primary', 'success', 'info', 'warning', 'danger'}
			The type of notification that should be shown. Adheres to bootstrap
			standards which are primary, success, info, warning and danger
		timeout : int (default: 5000)
			The duration for which the notification should be shown. If None then
			the notification will be shown indefinitely

		Raises
		------
		ValueError
			if the category is other than one of the expected values.
		"""

		self.show()
		notification = QNotification(message, category, self)
		notification.closeClicked.connect(self.remove)
		self.layout().addWidget(notification)
		# Check for entry effects
		if not self.entryEffect is None:
			if self.entryEffect == u"fadeIn":
				notification.fadeIn(self.entryEffectDuration)
		else:
			notification.display()

		self.adjustSize()
		if not timeout is None and timeout > 0:
			QtCore.QTimer.singleShot(timeout, 
				lambda : self.remove(notification))

	@QtCore.pyqtSlot()
	def remove(self, notification = None):
		""" Removes a notification.
	
		Parameters
		----------
		notification : QNotification (default: None)
			The notification to remove. This function also serves as a PyQt slot
			for signals emitted from a QNotification. In this case, the QNotification
			object is retrieved by using self.sender()

		Raises
		------
		ValueError
			If notification is not None or a QNotification
		"""
		# This function also functions as a pyqt slot. In that case, no
		# notification argument is passed, but this is set as self.sender()
		if notification is None:
			try:
				notification = self.sender()
			except:
				raise ValueError(u'QNotification object needs to be passed '
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
		if self.exitEffect == u'fadeOut':
			notification.fadeOut(self.__delete_notification, self.exitEffectDuration)
		else:
			self.__delete_notification(notification)

	# Internal Qt functions
	def resizeEvent(self, event):
		""" Internal QT function (do not call directly). """
		self.target_resize_event(event)
		newsize = event.size()		
		self.setFixedWidth(newsize.width())
		self.adjustSize()

	def paintEvent(self, pe):
		""" Redefinition of paintEvent. 
		Makes class QNotificationArea available in style sheets. 
		Internal QT function (do not call directly) """
		o = QtWidgets.QStyleOption()
		o.initFrom(self)
		p = QtGui.QPainter(self)
		self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, o, p, self)
	
	