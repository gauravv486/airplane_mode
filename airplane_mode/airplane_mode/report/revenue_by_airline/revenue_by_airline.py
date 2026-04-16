import frappe

def execute(filters=None):
    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # Get all airlines
    airlines = frappe.get_all("Airline", fields=["name"])

    # Get submitted tickets grouped by airplane's airline
    tickets = frappe.get_all("Airplane Ticket",
        filters={"docstatus": 1},
        fields=["airplane", "total_amount"]
    )

    # Map airplane → airline
    airline_revenue = {a["name"]: 0 for a in airlines}

    for ticket in tickets:
        airline = frappe.db.get_value("Airplane", ticket["airplane"], "airline")
        if airline in airline_revenue:
            airline_revenue[airline] += ticket["total_amount"] or 0

    data = [{"airline": k, "revenue": v} for k, v in airline_revenue.items()]
    data.sort(key=lambda x: x["revenue"], reverse=True)

    # Summary
    total = sum(row["revenue"] for row in data)
    summary = [{"label": "Total Revenue", "datatype": "Currency", "value": total}]

    # Chart
    chart = {
        "type": "donut",
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{"values": [row["revenue"] for row in data]}]
        }
    }

    return columns, data, chart, summary