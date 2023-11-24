/** @odoo-module */

const { Component,onWillStart, onMounted, onWillUnmount } = owl;
import { loadCSS, loadJS } from "@web/core/assets";

import { EquipeCardDetails } from "../EquipeCardDetails/dashboardEquipeCardDetails"
import { EquipeCardDetailsTable } from "../EquipeCardDetailsTable/dashboardEquipeCardDetailsTable"

export class EquipeCard extends Component {
    setup() {
        onWillStart(async () => {
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCard/EquipeCard.css");
        })
    }
}

EquipeCard.template = "owl.EquipeCard"
EquipeCard.components = {EquipeCardDetails,EquipeCardDetailsTable}