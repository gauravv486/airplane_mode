frappe.ui.form.on('Shop', {
    setup(frm) {
        frm.set_query('shop_type', () => {
            return {
                filters: {
                    enabled: 1
                }
            };
        });
    }
});