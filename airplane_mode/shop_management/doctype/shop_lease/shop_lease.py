import frappe
from frappe.model.document import Document

class ShopLease(Document):
    def validate(self):
        if not self.rent_amount:
            default_rent = frappe.db.get_single_value("Shop Settings", "default_rent_amount")
            if default_rent:
                self.rent_amount = default_rent