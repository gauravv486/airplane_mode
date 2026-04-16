import frappe

def get_context(context):
    context.no_cache = 1
    context.shops = frappe.get_all(
        "Shop",
        fields=["name", "shop_name", "shop_number", "airport", "status"]
    )
    return context