/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, useSubEnv, onWillStart, useEffect, useState, useRef, onMounted } from "@odoo/owl"


import { Dashform } from "./DashboardForm/dashboardForm"
import { EquipeCard } from "./EquipeCard/dashboardEquipeCard"


export class HrMainDashboard extends Component {
    setup() {
        onMounted(async () => {
            this.generateDashboard()
        })
    }

    async generateDashboard() {
        const rpc = this.env.services.rpc
        const data = await rpc('/hr_management/dashboard/', {
            chantier_id: 432,
            period_id: 142,
            periodicite: 'quinzaine12',
        })
        console.log(data)
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = {EquipeCard,Dashform}


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)