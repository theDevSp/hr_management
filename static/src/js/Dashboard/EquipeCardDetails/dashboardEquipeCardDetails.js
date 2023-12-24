/** @odoo-module */

import { loadCSS, loadJS } from "@web/core/assets";
const { Component, onWillStart } = owl;

export class EquipeCardDetails extends Component {
    setup() {
        onWillStart(async () => {
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCardDetails/EquipeCardDetails.css");
        })

    }
}

EquipeCardDetails.template = "owl.EquipeCardDetails"