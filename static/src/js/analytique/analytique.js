/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, onWillRender, useState } from "@odoo/owl"

export class HrMainAnalytique extends Component {
    setup() {
    }

    async request1() {
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/analytique_q12/')
        console.log(res)
    }

    async request2() {
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/analytique_q1_q2/')
        console.log(res)
    }
}

HrMainAnalytique.template = "hr_management.main_owl.analytique"

registry.category("actions").add("hr_management.action_main_analytique", HrMainAnalytique)