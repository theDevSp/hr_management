/** @odoo-module */

import { registry } from "@web/core/registry"
import { getDefaultConfig } from "@web/views/view"
import { useService } from "@web/core/utils/hooks"
import { Component, useSubEnv, onWillStart, useEffect, useState, useRef, onMounted } from "@odoo/owl"

const { loadJS, loadCSS } = require('@web/core/assets');

import { DashboardForm } from "./form/form";
import { MainCard } from "./MainCard/mainCard";

export class HrMainDashboard extends Component {
    setup() {
        
    }

    buildDashboard() {
        console.log(this)
    }

    

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = {DashboardForm,MainCard}


registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)