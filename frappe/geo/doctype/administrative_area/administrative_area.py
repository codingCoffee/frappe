# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.utils.nestedset import NestedSet

class AdministrativeArea(NestedSet):
	def autoname(self):
		self.name = self.title.lower()
		if frappe.db.exists("Administrative Area", self.name):
			if frappe.db.get_value("Administrative Area", self.name, "parent_administrative_area") == self.parent_administrative_area:
				frappe.throw("The following Administrative Area already exists")
			else:
				doc = frappe.get_doc("Administrative Area", self.name)
				frappe.rename_doc("Administrative Area", doc.name, "{}-{}".format(doc.name, doc.parent_administrative_area), ignore_permissions = True)
				self.name = "{}-{}".format(self.name, self.parent_administrative_area)
	
	def on_update(self):
		super(AdministrativeArea, self).on_update()
		self.validate_one_root()

def on_doctype_update():
	frappe.db.add_index("Administrative Area", ["lft", "rgt"])