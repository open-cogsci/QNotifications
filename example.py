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

		message_label = QtWidgets.QLabel("Send notification: ", display_widget)
		self.message_textbox = QtWidgets.QLineEdit(display_widget)
		type_label = QtWidgets.QLabel("Notifcation type: ", display_widget)
		self.type_dropdown = QtWidgets.QComboBox(display_widget)
		self.type_dropdown.addItems(["primary", "success", "info", "warning", "danger"])
		send_button = QtWidgets.QPushButton("Send", display_widget)

		inputLayout.addRow(message_label, self.message_textbox)
		inputLayout.addRow(type_label, self.type_dropdown)
		inputLayout.addRow(QtWidgets.QWidget(), send_button)

		display_widget.layout().addWidget(QtWidgets.QLabel("<h1>Example</h2>",
			display_widget))
		display_widget.layout().addLayout(inputLayout)

		self.message_textbox.returnPressed.connect(send_button.click)
		send_button.clicked.connect(self.__submit_message)
		return display_widget

	def __setup_notification_area(self, targetWidget):
		notification_area = QNotifications.QNotificationArea(targetWidget)
		self.notify.connect(notification_area.display)
		notification_area.setEntryEffect('fadeIn')
		notification_area.setExitEffect('fadeOut')
		return notification_area

	def __submit_message(self):
		textvalue = self.message_textbox.text().strip()
		typevalue = self.type_dropdown.currentText()
		if textvalue:
			self.notify.emit(textvalue, typevalue, 5000)

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




