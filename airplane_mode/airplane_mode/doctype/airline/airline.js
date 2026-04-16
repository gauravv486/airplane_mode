// frappe.ui.form.on listens to events on the Airline form
frappe.ui.form.on('Airline', {

    // 'refresh' fires every time the form loads or reloads
    refresh(frm) {

        // Only add the web link if the website field is NOT empty
        if (frm.doc.website) {

            // frm.add_web_link(url, label)
            // Adds a clickable link in the form's sidebar
            frm.add_web_link(frm.doc.website, "Visit Website");
        }
    }
});