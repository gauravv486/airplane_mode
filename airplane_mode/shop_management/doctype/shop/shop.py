import frappe
from frappe.website.website_generator import WebsiteGenerator

class Shop(WebsiteGenerator):

    def autoname(self):
        # Optional: use shop_name as document name (cleaner URLs)
        if self.shop_name:
            self.name = self.shop_name

    def before_save(self):
        # Always generate clean route (runs on create + update)
        if self.name:
            slug = frappe.scrub(self.name)   # converts to lowercase + hyphen
            self.route = f"shops/{slug}"

    def on_update(self):
        old_doc = self.get_doc_before_save()

        if old_doc:
            old_airport = old_doc.airport
        else:
            old_airport = None

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