/** @odoo-module */

const showNotification = (notificationService, typ, msg) => {
    notificationService.add(msg, {
        title: "Notification",
        type: typ, //info, warning, danger, success
    })
}

export default showNotification;