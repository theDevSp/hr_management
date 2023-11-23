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

    async generateDashboard() {

        const rpc = this.env.services.rpc
        const data = await rpc('/hr_management/dashboard/', {
            chantier_id: 432,
            period_id: 142,
            periodicite: 'quinzaine12',
            equipe: 3,
        })
        console.log(data)
        console.log(this.state.data)
        this.state.data = data
        console.log(this.state.data)
        this.state.isFirstLoad = false
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = { EquipeCard, Dashform }


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)