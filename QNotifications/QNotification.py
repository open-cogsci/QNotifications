# -*- coding: utf-8 -*-
# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from qtpy import QtWidgets, QtGui, QtCore
from QNotifications.abstractions import *

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

class MessageLabel(QtWidgets.QLabel):
	""" Subclass of QLabel, which reimplements the resizeEvent() function. This
	is necessary because otherwise the notifications take up too much vertical
	space when texts they display become longer. This is because normally the height 
	of a notification is calculated as the minimum height necessary for the text 
	when the widget is horizontally resized to its minimum. """

	def resizeEvent(self, event):
		super(MessageLabel, self).resizeEvent(event)
		if ( self.wordWrap() and \
			self.sizePolicy().verticalPolicy() == QtWidgets.QSizePolicy.Minimum ):
			self.setMaximumHeight( self.heightForWidth( self.width() ) )

class QNotification(QtWidgets.QWidget):
	""" Class representing a single notification """

	closeClicked = QtCore.pyqtSignal()
	""" PyQt signal for click on the notification's close button. """

	def __init__(self, message, category, *args, **kwargs):
		"""Constructor

		Parameters
		----------
		message : str
			The message to show
		category : {'primary', 'success', 'info', 'warning', 'danger'}
			The type of notification. Adheres to bootstrap standard 
			classes which are {primary, success, info, warning, danger}
		"""
		super(QNotification, self).__init__(*args, **kwargs)
		# Store instance variables
		self.message = message
		self.category = category

		# Set Object name for reference
		self.setObjectName(category)
		self.setLayout(QtWidgets.QHBoxLayout())
		self.setContentsMargins(0,0,0,0)
		# self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, 
		# 	QtWidgets.QSizePolicy.Fixed)

		# Create a message area
		#contents = QtWidgets.QWidget(self)
		messageArea = QtWidgets.QHBoxLayout()
		messageArea.setContentsMargins(0,0,0,0)

		# Create the layout
		self.message_display = MessageLabel()
		self.message_display.setObjectName("message")
		self.message_display.setSizePolicy(QtWidgets.QSizePolicy.Minimum, 
			QtWidgets.QSizePolicy.Minimum)
		self.message_display.setWordWrap(True)

		# Create a button that can close notifications
		close_button = QtWidgets.QPushButton(u"\u2715")
		close_button.setObjectName("closeButton")
		close_button.setFixedWidth(20)
		close_button.setFlat(True)
		close_button.clicked.connect(self.closeClicked)

		# Add everything together
		messageArea.addWidget(self.message_display)
		# messageArea.addStretch(1)
		messageArea.addWidget(close_button)
		self.layout().addLayout(messageArea)

		# Initialize some variables
		# self.setStyle(category)
		self.setVisible(False)

		# Flag that is set if notification is being removed. This can be used to
		# make sure that even though the notification has not been really removed
		# yet (because it is for example in an fade out animation), it is in the 
		# process of being removed
		self.isBeingRemoved = False

		self.__init_graphic_effects()

	def __init_graphic_effects(self):
		""" Initializes graphic effects. """
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

	def display(self):
		""" Displays the notification. """
		self.message_display.setText(self.message)
		self.show()

	def close(self):
		""" Closes the notification. """
		super(QNotification,self).close()
		self.deleteLater()

	def fadeIn(self, duration):
		""" Fades in the notification.
	
		Parameters
		----------
		duration : int
			The desired duration of the animation

		Raises
		------
		TypeError
			if duration is not an integer
		"""

		if type(duration) != int:
			raise TypeError("duration should be an integer")
		self.setGraphicsEffect(self.opacityEffect)
		self.fadeInAnimation.setDuration(duration)
		self.display()
		self.fadeInAnimation.start()

	def fadeOut(self, finishedCallback, duration):
		""" Fades out the notification. 
	
		Parameters
		----------
		finishedCallback : callable
			The function to call after the animation has finished (to for instance
			clean up the notification)
		duration : int
			The desired duration of the animation

		Raises
		------
		TypeError
			if the wrong datatype is specified for any of the parameters.
		"""

		if not callable(finishedCallback):
			raise TypeError("finishedCallback should be a callable")
		if type(duration) != int:
			raise TypeError("duration should be an integer")

		self.setGraphicsEffect(self.opacityEffect)
		self.fadeOutAnimation.setDuration(duration)
		self.fadeOutAnimation.finished.connect(lambda: finishedCallback(self))
		self.isBeingRemoved = True
		self.fadeOutAnimation.start()

	def paintEvent(self, pe):
		""" redefinition of paintEvent, do not call directly. 
		Makes class QNotification available in style sheets. Interal Qt function. 
		Should not be called directly. """
		o = QtWidgets.QStyleOption()
		o.initFrom(self)
		p = QtGui.QPainter(self)
		self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, o, p, self)

	### Property attributes
	@property
	def message(self):
		""" The currently set message to display. """
		return self._message

	@message.setter
	def message(self, value):
		""" Sets the message to display. """
		self._message = value

	@property
	def category(self):
		""" The currently set category of this notification. """
		return self._category

	@category.setter
	def category(self, value):
		""" Sets the category of this notification. 

		Parameters
		----------
		value : {'primary','success','info','warning','danger'}
			The category specification

		Raises
		------
		ValueError
			if the category is other than one of the expected values.
		"""

		allowed_values = ['primary','success','info','warning','danger']
		if not value in allowed_values:
			raise ValueError(u'{} not a valid value. '
				'Should be one of').format(value, allowed_values)
		self._category = value

