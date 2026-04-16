import frappe

def get_context(context):
    context.no_cache = 1
    context.shop = None

    shop_name = frappe.form_dict.get("shop")

    if shop_name:
        try:
            context.shop = frappe.get_doc("Shop", shop_name)
        except frappe.DoesNotExistError:
            context.shop = None

    return context