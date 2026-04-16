frappe.ui.form.on('Airplane Ticket', {

    refresh(frm) {

        // Add custom button only when doc is NOT submitted/cancelled
        if (frm.doc.docstatus === 0) {

            frm.add_custom_button('Assign Seat', function () {

                // frappe.prompt shows a dialog with input fields
                frappe.prompt(
                    [
                        {
                            label: 'Seat Number',  // label shown in dialog
                            fieldname: 'seat',      // key to access value
                            fieldtype: 'Data',      // input type
                            reqd: 1                 // make it mandatory
                        }
                    ],
                    function (values) {
                        // values.seat = what user typed

                        // Set the seat field on the form
                        frm.set_value('seat', values.seat);

                        // Save the document immediately
                        frm.save();
                    },
                    'Assign Seat',   // dialog title
                    'Assign'         // submit button label
                );
            });
        }
    }
});