/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, useSubEnv, onWillRender, useEffect, useState, useRef, onMounted } from "@odoo/owl"


import { Dashform } from "./DashboardForm/dashboardForm"
import { EquipeCard } from "./EquipeCard/dashboardEquipeCard"


export class HrMainDashboard extends Component {
    setup() {

        this.state = useState({
            isFirstLoad: true,
            data: [
                {
                    name: "Dune",
                    id: 1
                },
                {
                    name: "Foundation",
                    id: 2
                },
                {
                    name: "1984",
                    id: 3
                },
                {
                    name: "Brave New World",
                    id: 4
                },
                {
                    name: "Ender's Game",
                    id: 5
                },
                {
                    name: "The Hitchhiker's Guide to the Galaxy",
                    id: 6
                },
                {
                    name: "Neuromancer",
                    id: 7
                },
                {
                    name: "Snow Crash",
                    id: 8
                },
                {
                    name: "The Martian",
                    id: 9
                },
                {
                    name: "Ready Player One",
                    id: 10
                }
            ]
        })

        onWillRender(async () => {

        })
    }

    async generateDashboard() {

        console.log("hhhhhhh")

        const rpc = this.env.services.rpc
        const data = await rpc('/hr_management/dashboard/', {
            chantier_id: 432,
            period_id: 142,
            periodicite: 'quinzaine12',
        })
        console.log(data)
        console.log(this.state.data)
        //this.state.data = data
        console.log(this.state.data)
        this.state.isFirstLoad = false
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = { EquipeCard, Dashform }


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)