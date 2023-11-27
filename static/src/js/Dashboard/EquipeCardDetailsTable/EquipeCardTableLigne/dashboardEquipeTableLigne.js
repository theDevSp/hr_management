/** @odoo-module */

import { Component } from "@odoo/owl"
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog"

import { useService } from "@web/core/utils/hooks";

import showNotification from "../../Notification/showNotification";


export class EquipeCardDetailsTableLigne extends Component {

    setup() {
        this.actionService = useService("action")
    }

    updateStatus(state) {
        const rpc = this.env.services.rpc
        const dialog = this.env.services.dialog;
        const notification = this.env.services.notification

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {

                const data = await rpc('/hr_management/dashboard/update_fp_status/', {
                    id: this.props.ligne.payroll_id,
                    status: state
                })

                switch (data.code) {
                    case 200:
                        Object.assign(this.props.ligne, data.ligne);
                        showNotification(notification,"success", data.message);
                        break;

                    case 202:
                        showNotification(notification,"warning", data.message);
                        break;

                    case 504:
                        console.error(data.error)
                        showNotification(notification,"danger", data.message);
                        break;

                    default:
                        break;
                }

            },
            cancel: () => { }
        });
    }

    goToFiche() {
        this.actionService.doAction({
            type: "ir.actions.act_url",
            url: `/web#id=${this.props.ligne.payroll_id}&model=hr.payslip&view_type=form`
        });
    }

}

EquipeCardDetailsTableLigne.template = "owl.EquipeCardDetailsTableLigne"