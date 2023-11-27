/** @odoo-module */

const { Component, onWillStart, onMounted, onWillUnmount } = owl;
import { loadCSS, loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

import { EquipeCardDetails } from "../EquipeCardDetails/dashboardEquipeCardDetails"
import { EquipeCardDetailsTable } from "../EquipeCardDetailsTable/dashboardEquipeCardDetailsTable"
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog"
import { blockUI, unblockUI } from "web.framework";
import showNotification from "../Notification/showNotification";

export class EquipeCard extends Component {
    setup() {
        this.actionService = useService("action")
        this.rpc = useService("rpc")
        this.notification = useService("notification")

        onWillStart(async () => {
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCard/EquipeCard.css");
        })
    }

    updateStatus(state) {
        const rpc = this.env.services.rpc
        const dialog = this.env.services.dialog;
        const notification = this.env.services.notification

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {

                blockUI();
                const payrollIds = this.props.data.payroll_details.map(entry => entry.payroll_id);

                const data = await rpc('/hr_management/dashboard/update_all_fp_status', {
                    ids: payrollIds,
                    status: state
                })

                switch (data.code) {
                    case 200:
                        Object.assign(this.props.data.payroll_details, data.lignes);
                        showNotification(notification,"success", data.message);
                        unblockUI();
                        break;

                    case 202:
                        showNotification(notification,"warning", data.message);
                        unblockUI();
                        break;

                    case 504:
                        console.error(data.error)
                        showNotification(notification,"danger", data.message);
                        unblockUI();
                        break;

                    default:
                        unblockUI();
                        break;
                }

            },
            cancel: () => { }
        });
    }

    showFpsOfEquipe() {

        const equipeID = this.props.data.equipe[0]
        const chantierID = this.props.data.chantierID
        const periodID = this.props.data.periodID
        const quinz = this.props.data.quinz

        this.actionService.doAction({
            name: `Fiche Paies : ${this.props.data.equipe[1].toUpperCase()}`,
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

    async reload() {
        blockUI();
        const equipeID = this.props.data.equipe[0]
        const chantierID = this.props.data.chantierID
        const periodID = this.props.data.periodID
        const quinz = this.props.data.quinz

        const res = await this.rpc('/hr_management/dashboard/', {
            chantier_id: chantierID,
            period_id: periodID,
            periodicite: quinz,
            equipe: equipeID
        })

        switch (res.code) {
            case 200:
                Object.assign(this.props.data, res.data[0]);
                showNotification(this.notification,"success", res.message);
                unblockUI();
                break;

            case 202:
                showNotification(this.notification,"warning", res.message);
                unblockUI();
                break;

            case 504:
                console.error(res.error)
                showNotification(this.notification,"danger", res.message);
                unblockUI();
                break;

            default:
                unblockUI();
                break;
        }
    }

    async deleteTrashReports(){
        const equipeID = this.props.data.equipe[0]
        const chantierID = this.props.data.chantierID
        const periodID = this.props.data.periodID
        const quinz = this.props.data.quinz

        const dialog = this.env.services.dialog;

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {

                blockUI();
                const res = await this.rpc('/hr_management/dashboard/delete_reports', {
                    chantier_id: chantierID,
                    period_id: periodID,
                    periodicite: quinz,
                    equipe: equipeID
                })

                switch (res.code) {
                    case 200:
                        showNotification(this.notification,"success", res.message);
                        unblockUI();
                        break;
        
                    case 202:
                        showNotification(this.notification,"warning", res.message);
                        unblockUI();
                        break;
        
                    case 504:
                        console.error(res.error)
                        showNotification(this.notification,"danger", res.message);
                        unblockUI();
                        break;
        
                    default:
                        unblockUI();
                        break;
                }

            },
            cancel: () => { }
        });

        
    }
}

EquipeCard.template = "owl.EquipeCard"
EquipeCard.components = { EquipeCardDetails, EquipeCardDetailsTable }