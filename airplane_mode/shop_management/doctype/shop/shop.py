import frappe
from frappe.model.document import Document

class Shop(Document):
    def on_update(self):
        old_airport = self.get_doc_before_save().airport if self.get_doc_before_save() else None
        update_airport_shop_counts(self.airport)

        if old_airport and old_airport != self.airport:
            update_airport_shop_counts(old_airport)

    def on_trash(self):
        update_airport_shop_counts(self.airport)


def update_airport_shop_counts(airport):
    if not airport:
        return

    total = frappe.db.count("Shop", {"airport": airport})
    occupied = frappe.db.count("Shop", {"airport": airport, "status": "Occupied"})
    available = frappe.db.count("Shop", {"airport": airport, "status": "Available"})

    frappe.db.set_value("Airport", airport, "total_shops", total)
    frappe.db.set_value("Airport", airport, "occupied_shops", occupied)
    frappe.db.set_value("Airport", airport, "available_shops", available)