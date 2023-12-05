/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, onWillRender, useState } from "@odoo/owl"

import { useService } from "@web/core/utils/hooks";

import { blockUI, unblockUI } from "web.framework";

import { Dashform } from "./DashboardForm/dashboardForm"
import { EquipeCard } from "./EquipeCard/dashboardEquipeCard"

import showNotification from "@configuration_module/js/utils/showNotification";

export class HrMainDashboard extends Component {
    setup() {

        this.notification = useService("notification")

        this.state = useState({
            isFirstLoad: true,
            data: null
        })

    }

    async generateDashboard(periodeID, chantierID, employeType, quinzine, equipe) {

        blockUI();

        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/dashboard/', {
            chantier_id: chantierID,
            period_id: periodeID,
            periodicite: quinzine,
            equipe: equipe,
            /*chantier_id: 432,
            period_id: 142,
            periodicite: 'quinzaine12',
            equipe: '',*/
        })

        switch (res.code) {
            case 200:
                this.state.data = res.data;
                this.state.isFirstLoad = false;
                showNotification(this.notification, "success", 'Chargement réussi !');
                unblockUI();
                break;

            case 202:
                showNotification(this.notification, "warning", 'Pas de données à afficher pour ce critère.');
                unblockUI();
                break;

            case 504:
                console.error(res.error)
                showNotification(this.notification, "danger", res.message);
                unblockUI();
                break;

            default:
                unblockUI();
                break;
        }
    }

    resetView() {
        this.state.isFirstLoad = true;
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = { EquipeCard, Dashform }


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)