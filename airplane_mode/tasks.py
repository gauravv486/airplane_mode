import frappe
from frappe.utils import today

def send_rent_reminders():
    enabled = frappe.db.get_single_value("Shop Settings", "enable_rent_reminders")
    if not enabled:
        return

    leases = frappe.get_all(
        "Shop Lease",
        fields=["name", "tenant", "shop", "rent_amount", "expiry_date"]
    )

    for lease in leases:
        tenant_email = frappe.db.get_value("Shop Tenant", lease.tenant, "email")
        if tenant_email:
            frappe.sendmail(
                recipients=[tenant_email],
                subject="Monthly Rent Reminder",
                message=f"""
                    Dear Tenant,<br><br>
                    This is a reminder that rent for shop <b>{lease.shop}</b> is due.<br>
                    Amount: <b>{lease.rent_amount}</b><br>
                    Lease: <b>{lease.name}</b><br><br>
                    Regards,<br>
                    Airport Shop Management
                """
            )