/** @odoo-module */

import { Component, useSubEnv, useEffect, useState, useRef } from "@odoo/owl"
import { loadCSS, loadJS } from "@web/core/assets";
const { onWillStart, onMounted, onWillUnmount } = owl;

import { EquipeCardDetailsTableLigne } from "./EquipeCardTableLigne/dashboardEquipeTableLigne"

export class EquipeCardDetailsTable extends Component {
    setup() {

        this.data = JSON.parse(JSON.stringify(this.props.tabledetails.payroll_details))

        onWillStart(async () => {
            await loadCSS("/hr_management/static/src/js/Dashboard/Utils/DataTables/jquery.dataTables.min.css");
            await loadJS("/hr_management/static/src/js/Dashboard/Utils/DataTables/jquery.dataTables.min.js");
            
            // static css
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCardDetailsTable/EquipeCardDetailsTable.css");
        })

        onMounted(() => {
            $(`#${this.props.tabledetails.id}`).DataTable({
                lengthChange: false,
                lengthMenu: [[5], [5]],
                language: {
                    url: "https://cdn.datatables.net/plug-ins/1.10.25/i18n/French.json",
                    searchPlaceholder: "Rechercher..."
                },
            });
        });

    }
}

EquipeCardDetailsTable.template = "owl.EquipeCardDetailsTable"
EquipeCardDetailsTable.components = { EquipeCardDetailsTableLigne }