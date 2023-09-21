/** @odoo-module */

import { registry } from "@web/core/registry"
import { Layout } from "@web/search/layout"
import { ChantierDrop } from "@construction_site_management/js/searchable_dropdown/searchable_dropdown"
import { Dropdown } from "@web/core/dropdown/dropdown"
import { DropdownItem } from "@web/core/dropdown/dropdown_item"
import { getDefaultConfig } from "@web/views/view"
import { useService } from "@web/core/utils/hooks"
import { Component, useSubEnv, onWillStart, useEffect, useState, useRef } from "@odoo/owl"


export class HrMainDashboard extends Component {
    setup() {

        this.rpc = useService("rpc");

        this.display = {
            controlPanel: { "top-right": false, "bottom-right": false }
        }

        this.state = useState({
        })

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        })
        useEffect(() => { 
            
        })
        
        this.test()
        
    }

    async test() {
        const res = await this.rpc(
            `/hr_management/get_dashboard_report_pointage_salarie_ouvrier/2`
          );
          console.log(res)
    }

}

HrMainDashboard.template = "hr_management.main_dashboard"
HrMainDashboard.components = { Layout, Dropdown, DropdownItem, ChantierDrop }

registry.category("actions").add("hr_management.action_main_dashboard", HrMainDashboard)