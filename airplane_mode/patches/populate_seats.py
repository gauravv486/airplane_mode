import frappe
import random


def execute():
    # Get all existing Airplane Ticket names
    tickets = frappe.get_all("Airplane Ticket", fields=["name", "seat"])

    for ticket in tickets:
        # Only populate if seat is empty
        if not ticket.seat:
            number = random.randint(1, 100)
            letter = random.choice(["A", "B", "C", "D", "E"])
            seat = f"{number}{letter}"

            # Write directly to DB without triggering hooks
            frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)

    frappe.db.commit()