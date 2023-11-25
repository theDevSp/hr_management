/** @odoo-module */

const { Component, onWillStart, onMounted, onWillUnmount } = owl;
import { loadCSS, loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

import { EquipeCardDetails } from "../EquipeCardDetails/dashboardEquipeCardDetails"
import { EquipeCardDetailsTable } from "../EquipeCardDetailsTable/dashboardEquipeCardDetailsTable"
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog"

import NOTIFICATION_MESSAGES from "../Notification/NotificationMessages";

export class EquipeCard extends Component {
    setup() {
        this.actionService = useService("action")

        onWillStart(async () => {
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCard/EquipeCard.css");
        })
    }

    showFpsOfEquipe() {

        const equipeID = this.props.data.equipe[0]
        const chantierID = this.props.data.chantierID
        const periodID = this.props.data.periodID
        const quinz = this.props.data.quinz

        this.actionService.doAction({
            name: `${this.props.data.equipe[1].toUpperCase()}`,
            res_model: "hr.payslip",
            target: "new",
            type: "ir.actions.act_window",
            views: [[false, "list"]],
            domain: [
                ['period_id', '=', periodID],
                ['chantier_id', '=', chantierID],
                ['quinzaine', '=', quinz],
                ['emplacement_chantier_id', '=', equipeID],
            ],
        });
    }

    async allFpOnPaye() {

        var framework = require('web.framework');


        const rpc = this.env.services.rpc
        const dialog = this.env.services.dialog;

        const lignes = this.props.data.payroll_details

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {

                framework.blockUI();

                let check = false

                try {
                    var newData = await Promise.all(
                        lignes.map(async ligne => {
                            const response = await rpc(`/hr_management/dashboard/update_fp_status_paye/${ligne.payroll_id}`);
                            if (response.code !== 200) {
                                throw new Error('Erreur');
                            } else {
                                check = true
                                return response.ligne;
                            }
                        })
                    );

                } catch (error) {
                    framework.unblockUI();
                    alert(error.message);
                }

                switch (check) {
                    case true:
                        this.props.data.payroll_details = newData
                        this.showNotification("success", NOTIFICATION_MESSAGES.success);
                        framework.unblockUI();
                        break;

                    case false:
                        this.showNotification("danger", NOTIFICATION_MESSAGES.warningError);
                        framework.unblockUI();
                        break;

                    default:
                        framework.unblockUI();
                        break;
                }

            },
            cancel: () => { }
        });

    }

    showNotification(typ, msg) {
        const notification = this.env.services.notification
        notification.add(msg, {
            title: "Notification",
            type: typ, //info, warning, danger, success
        })
    }
}

EquipeCard.template = "owl.EquipeCard"
EquipeCard.components = { EquipeCardDetails, EquipeCardDetailsTable }