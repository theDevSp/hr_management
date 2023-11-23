/** @odoo-module */

import { Component, useSubEnv, useEffect, useState, useRef } from "@odoo/owl"
import { loadCSS, loadJS } from "@web/core/assets";
const { onWillStart, onMounted, onWillUnmount } = owl;

import { EquipeCardDetailsTableLigne } from "./EquipeCardTableLigne/dashboardEquipeTableLigne"

export class EquipeCardDetailsTable extends Component {
    setup() {

        console.log(JSON.parse(JSON.stringify(this.props.tabledetails.payroll_details)))

        this.data = JSON.parse(JSON.stringify(this.props.tabledetails.payroll_details))

        onWillStart(async () => {
            await loadCSS("https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css");
            await loadCSS("/hr_management/static/src/js/Dashboard/EquipeCardDetailsTable/dashboardEquipeCardDetailsTable.css");
            await loadJS("https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js");
        })

        onMounted(() => {
            $(`#${this.props.tabledetails.id}`).DataTable({
                lengthChange: false,
                lengthMenu: [[5], [5]],
                language: {
                  url: "https://cdn.datatables.net/plug-ins/1.10.25/i18n/French.json"
                },
              });
        });

    }
}

EquipeCardDetailsTable.template = "owl.EquipeCardDetailsTable"
EquipeCardDetailsTable.components = { EquipeCardDetailsTableLigne }