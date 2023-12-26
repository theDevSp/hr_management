/** @odoo-module */

import { Component, useSubEnv, useEffect, useState, useRef } from "@odoo/owl"
import { loadCSS, loadJS } from "@web/core/assets";
const { onWillStart, onMounted, onWillUnmount } = owl;

import { EquipeCardDetailsTableLigne } from "./EquipeCardTableLigne/dashboardEquipeTableLigne"

export class EquipeCardDetailsTable extends Component {
    setup() {

        onWillStart(async () => {
            await loadCSS("/configuration_module/static/src/libraries/DataTables/jquery.dataTables.min.css");
            await loadJS("/configuration_module/static/src/libraries/DataTables/jquery.dataTables.min.js");

            // static css
            await loadCSS("/hr_management/static/src/css/Dashboard/EquipeCardDetailsTable/EquipeCardDetailsTable.css");
        })

        onMounted(() => {
            $(`#${this.props.tabledetails.id}`).DataTable({
                lengthChange: false,
                lengthMenu: [[5], [5]],
                language: {
                    url: "/configuration_module/static/src/libraries/DataTables/frenchLanguage.json",
                    searchPlaceholder: "Rechercher..."
                },
            });
        });

    }
}

EquipeCardDetailsTable.template = "owl.EquipeCardDetailsTable"
EquipeCardDetailsTable.components = { EquipeCardDetailsTableLigne }
