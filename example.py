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
import QNotifications

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"

import sys

class Example(QtCore.QObject):
	""" Example showing off the notifications """
	notify = QtCore.pyqtSignal(str,str,int)

	def __init__(self):
		super(Example,self).__init__()
		self.display_widget = self.__setup_widget()
		self.notification_area = self.__setup_notification_area(self.display_widget)
		self.display_widget.show()

	def __setup_widget(self):
		display_widget = QtWidgets.QWidget()
		display_widget.setGeometry(100,100,800,600)
		display_widget.setLayout(QtWidgets.QVBoxLayout())

		inputLayout = QtWidgets.QFormLayout()
		inputLayout.setFieldGrowthPolicy(inputLayout.ExpandingFieldsGrow)

		# Notification message
		message_label = QtWidgets.QLabel("Send notification: ", display_widget)
		self.message_textbox = QtWidgets.QLineEdit(display_widget)
		# Notification type
		type_label = QtWidgets.QLabel("Notification type: ", display_widget)
		self.type_dropdown = QtWidgets.QComboBox(display_widget)
		self.type_dropdown.addItems(["primary", "success", "info", "warning", "danger"])
		
		# Notification duration
		duration_label = QtWidgets.QLabel("Display duration: (ms)", display_widget)
		self.message_duration = QtWidgets.QSpinBox(display_widget)
		self.message_duration.setRange(500, 5000)
		self.message_duration.setValue(2000)
		self.message_duration.setSingleStep(50)
		# Entry effect
		entryeffect_label = QtWidgets.QLabel("Entry effect: ", display_widget)
		self.entry_dropdown = QtWidgets.QComboBox(display_widget)
		self.entry_dropdown.addItems(["None","fadeIn"])
		self.entry_dropdown.currentTextChanged.connect(self.__process_combo_change)
		# Entry effect duration
		self.entryduration_label = QtWidgets.QLabel("Effect duration: (ms)", display_widget)
		self.entryduration = QtWidgets.QSpinBox(display_widget)
		self.entryduration.setRange(100, 1000)
		self.entryduration.setSingleStep(50)
		# Exit effect 
		exiteffect_label = QtWidgets.QLabel("Exit effect: ", display_widget)
		self.exit_dropdown = QtWidgets.QComboBox(display_widget)
		self.exit_dropdown.addItems(["None","fadeOut"])
		self.exit_dropdown.currentTextChanged.connect(self.__process_combo_change)
		# Exit effect duration
		self.exitduration_label = QtWidgets.QLabel("Effect duration: (ms)", display_widget)
		self.exitduration = QtWidgets.QSpinBox(display_widget)
		self.exitduration.setRange(100, 1000)
		self.exitduration.setSingleStep(50)
		# Send button
		send_button = QtWidgets.QPushButton("Send", display_widget)

		inputLayout.addRow(message_label, self.message_textbox)
		inputLayout.addRow(type_label, self.type_dropdown)
		inputLayout.addRow(duration_label, self.message_duration)
		inputLayout.addRow(entryeffect_label, self.entry_dropdown)
		inputLayout.addRow(self.entryduration_label, self.entryduration)
		inputLayout.addRow(exiteffect_label, self.exit_dropdown)
		inputLayout.addRow(self.exitduration_label, self.exitduration)
		inputLayout.addRow(QtWidgets.QWidget(), send_button)

		self.entryduration_label.setDisabled(True)
		self.entryduration.setDisabled(True)
		self.exitduration_label.setDisabled(True)
		self.exitduration.setDisabled(True)

		display_widget.layout().addWidget(QtWidgets.QLabel("<h1>Example</h2>",
			display_widget))
		display_widget.layout().addLayout(inputLayout)

		self.message_textbox.returnPressed.connect(send_button.click)
		send_button.clicked.connect(self.__submit_message)
		return display_widget

	def __setup_notification_area(self, targetWidget):
		notification_area = QNotifications.QNotificationArea(targetWidget)
		self.notify.connect(notification_area.display)
		return notification_area

	def __process_combo_change(self, val):
		new_selection = val
		if self.sender() == self.entry_dropdown:
			if val == "None":
				self.entryduration_label.setDisabled(True)
				self.entryduration.setDisabled(True)
			else:
				self.entryduration_label.setDisabled(False)
				self.entryduration.setDisabled(False)
		elif self.sender() == self.exit_dropdown:
			if val == "None":
				self.exitduration_label.setDisabled(True)
				self.exitduration.setDisabled(True)
			else:
				self.exitduration_label.setDisabled(False)
				self.exitduration.setDisabled(False)

	def __submit_message(self):
		textvalue = self.message_textbox.text().strip()
		typevalue = self.type_dropdown.currentText()
		if textvalue:
			duration = self.message_duration.value()
			entry_effect = self.entry_dropdown.currentText()
			exit_effect = self.exit_dropdown.currentText()
			if entry_effect != "None":
				self.notification_area.setEntryEffect(entry_effect, 
					self.entryduration.value())
			else:
				self.notification_area.setEntryEffect(None)
			if exit_effect != "None":
				self.notification_area.setExitEffect(exit_effect,
					self.exitduration.value())
			else:
				self.notification_area.setExitEffect(None)
			self.notify.emit(textvalue, typevalue, duration)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	print(QtCore.QT_VERSION_STR)

	# Enable High DPI display with PyQt5
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

	example = Example()

	exitcode = app.exec_()
	print("App exiting with code {}".format(exitcode))
	del(example)
	sys.exit(exitcode)




