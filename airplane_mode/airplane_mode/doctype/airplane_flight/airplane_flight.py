import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
    website = frappe._dict(
        template="airplane_mode/doctype/airplane_flight/airplane_flight.html",
        condition_field="is_published",
        page_title_field="name",
    )

    def on_submit(self):
        self.db_set("status", "Completed")

    def on_update(self):
        if not self.has_value_changed("gate_number"):
            return

        frappe.enqueue(
            method="airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gate_numbers",
            queue="default",
            flight=self.name,
            gate_number=self.gate_number,
        )


@frappe.whitelist()
def update_ticket_gate_numbers(flight, gate_number):
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": flight},
        pluck="name"
    )

    for ticket_name in tickets:
        frappe.db.set_value("Airplane Ticket", ticket_name, "gate_number", gate_number)

    frappe.db.commit()