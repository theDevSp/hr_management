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
            await loadJS("https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.umd.js");
            await loadCSS("https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css");
        })

        onMounted(() => {

            const grid = new gridjs.Grid({
                columns: [
                    {
                        data: (row) => row.payroll_id,
                        name: 'ID',
                        hidden: true
                    },
                    {
                        data: (row) => row.employee_obj[1],
                        name: 'Employé'
                    },
                    {
                        data: (row) => row.employee_obj[2],
                        name: 'CIN'
                    },
                    {
                        data: (row) => row.employee_obj[3],
                        name: 'Poste Occupé'
                    },
                    {
                        data: (row) => row.net_paye,
                        name: 'net_paye'
                    },
                    {
                        data: (row) => row.status,
                        name: 'Status F.P'
                    },
                    {
                        name: 'Actions',
                        formatter: (cell, row) => {
                            //return gridjs.html(`<button onclick="alert('${row.cells[0].data}','${row.cells[1].data}')">Edit</button>`);
                            return gridjs.html(`<div>
                                <button type="button" class="btn">
                                    <i class="far fa-calendar-check" style="color: #28a745;"></i>
                                </button>
                                <button type="button" class="btn">
                                    <i class="far fa-calendar-times" style="color: #dc3545;"></i>
                                </button>
                                <button type="button" class="btn" onclick="this.show()">
                                    <i class="fas fa-list" style="color: #007bff;"></i>
                                </button>
                            </div>`)
                        }
                    }],
                pagination: {
                    enabled: true,
                    limit: 5, // Number of rows per page
                },
                language: {
                    'search': {
                        'placeholder': '🔍 Rechercher...'
                    },
                    'pagination': {
                        'previous': 'Précédent',
                        'next': 'Suivant',
                        'showing': 'Affichage de',
                        'results': () => 'lignes'
                    }
                },
                search: true,
                data: this.data,
                style: {
                    table: {
                        border: '1px solid #f4f6f3'
                    },
                    th: {
                        'background-color': '#f4f6f3',
                        color: '#000',
                        'border': '1px solid #f4f6f3',
                        'text-align': 'center',

                    },
                    td: {
                        'text-align': 'center'
                    }
                }
            }).render(document.getElementById(this.props.tabledetails.id));
        })


    }

    show(){
        console.log('hiii')
    }
}

EquipeCardDetailsTable.template = "owl.EquipeCardDetailsTable"
EquipeCardDetailsTable.components = { EquipeCardDetailsTableLigne }