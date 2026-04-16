import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
    def get_indicator(self):
        colors = {
            "Booked": "gray",
            "Checked-In": "purple",
            "Boarded": "green"
        }
        return colors.get(self.status, "gray")

    def autoname(self):
        source_code = frappe.db.get_value("Airport", self.source_airport_code, "code")
        dest_code = frappe.db.get_value("Airport", self.destination_airport_code, "code")
        self.name = frappe.model.naming.make_autoname(
            f"{self.flight}-{source_code}-to-{dest_code}-.####"
        )

    def before_save(self):
        total = self.flight_price or 0
        for addon in self.add_ons:
            total += addon.amount or 0
        self.total_amount = total

    def validate(self):
        seen = []
        unique_addons = []
        for addon in self.add_ons:
            if addon.item not in seen:
                seen.append(addon.item)
                unique_addons.append(addon)
        self.add_ons = unique_addons
        self.check_overbooking()

    def check_overbooking(self):
        airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
        capacity = frappe.db.get_value("Airplane", airplane, "capacity") or 0

        booked_tickets = frappe.db.count(
            "Airplane Ticket",
            filters={
                "flight": self.flight,
                "docstatus": ["!=", 2],
                "name": ["!=", self.name]
            }
        )

        if booked_tickets >= capacity:
            frappe.throw(f"This flight is fully booked! Max capacity is {capacity} seats.")

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Cannot submit ticket. Status must be 'Boarded'!")

    def before_insert(self):
        self.seat = self.get_next_seat()

    def get_next_seat(self):
        number = random.randint(1, 100)
        letter = random.choice(["A", "B", "C", "D", "E"])
        return f"{number}{letter}"