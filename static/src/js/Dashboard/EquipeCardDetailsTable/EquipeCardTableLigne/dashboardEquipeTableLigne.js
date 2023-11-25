/** @odoo-module */

import { Component, useSubEnv, useEffect, useState, useRef } from "@odoo/owl"
import { loadCSS, loadJS } from "@web/core/assets";
const { onWillStart, onMounted, onWillUnmount } = owl;
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog"

import { useService } from "@web/core/utils/hooks";

import NOTIFICATION_MESSAGES from "../../Notification/NotificationMessages";


export class EquipeCardDetailsTableLigne extends Component {

    setup() {
        this.actionService = useService("action")
    }

    changeStatusToPaye(id) {
        const rpc = this.env.services.rpc
        const dialog = this.env.services.dialog;

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {

                const data = await rpc(`/hr_management/dashboard/update_fp_status_paye/${id}`);

                switch (data.code) {
                    case 200:
                        const ligneToPay = this.props.lignes.find(ligne => {
                            if (ligne.payroll_id === id) {
                                Object.assign(ligne, data.ligne);
                                return true;
                            }
                            return false;
                        });
                        this.showNotification("success", NOTIFICATION_MESSAGES.success);
                        break;

                    case 202:
                        this.showNotification("warning", NOTIFICATION_MESSAGES.warningSuccess);
                        break;

                    case 502:
                        this.showNotification("warning", NOTIFICATION_MESSAGES.warningError);
                        break;

                    default:
                        break;
                }

            },
            cancel: () => { }
        });
    }

    changeStatusToCloture(id) {
        const rpc = this.env.services.rpc
        const dialog = this.env.services.dialog;

        dialog.add(ConfirmationDialog, {
            title: "Confirmation",
            body: "Êtes-vous sûr de vouloir continuer cette action ?",
            confirm: async () => {
                const data = await rpc(`/hr_management/dashboard/update_fp_status_cloture/${id}`);

                switch (data.code) {
                    case 200:
                        const ligneToCloture = this.props.lignes.find(ligne => {
                            if (ligne.payroll_id === id) {
                                Object.assign(ligne, data.ligne);
                                return true;
                            }
                            return false;
                        });
                        this.showNotification("success", NOTIFICATION_MESSAGES.success);
                        break;

                    case 202:
                        this.showNotification("warning", "Statut n'est pas mis à jour avec succès");
                        break;

                    case 502:
                        this.showNotification("warning", "Quelque chose ne va pas, veuillez contacter l'Administrateur du système");
                        break;

                    default:
                        break;
                }

            },
            cancel: () => { }
        });
    }

    goToFiche(id) {

        this.actionService.doAction({
            type: "ir.actions.act_url",
            url: `/web#id=${id}&model=hr.payslip&view_type=form`
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

EquipeCardDetailsTableLigne.template = "owl.EquipeCardDetailsTableLigne"