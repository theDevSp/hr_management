/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, useSubEnv, onWillRender, useEffect, useState, useRef, onMounted } from "@odoo/owl"


import { Dashform } from "./DashboardForm/dashboardForm"
import { EquipeCard } from "./EquipeCard/dashboardEquipeCard"


export class HrMainDashboard extends Component {
    setup() {

        this.state = useState({
            isFirstLoad: true,
            data: null
        })

        onWillRender(async () => {

        })
    }

    async generateDashboard(periodeID,chantierID,employeType,quinzine,equipe) {

        var framework = require('web.framework');
        framework.blockUI();

        console.log("Data: ",periodeID,chantierID,employeType,quinzine)

        const rpc = this.env.services.rpc
        const data = await rpc('/hr_management/dashboard/', {
            chantier_id: chantierID,
            period_id: periodeID,
            periodicite: quinzine,
            equipe: equipe,
        })

        this.state.data = data
        this.state.isFirstLoad = false

        framework.unblockUI();
    }

    test() {
        console.log("bind")
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = { EquipeCard, Dashform }


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)