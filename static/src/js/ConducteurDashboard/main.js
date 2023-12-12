/** @odoo-module */

import { registry } from "@web/core/registry"

const { Component, onMounted, useState, onWillStart, useRef } = owl
const { loadJS, loadCSS } = require('@web/core/assets');

import { Chantiers } from "@construction_site_management/js/components/Chantiers/chantiers";
import { Periode } from "@account_fiscal_year_period/js/components/periodes/periodes";

import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { EquipeCard } from "./equipes_cards/equipeCard";
import { EffectifPosteTable } from "./effectif_poste_table/effectif_table";

export class ConducteurDashboard extends Component {

    setup() {

        this.state = useState({
            periodeID: 143,
            chantierID: 179,
            chantier: '',
            periode: '',
            pperiode: '',
            totalHeures: {
                labels: ['10/2023', '11/2023'],
                datasets: [
                    {
                        label: 'Hours des Salariés',
                        data: [300, 500],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(153, 102, 255)',
                    },
                    {
                        label: 'Hours des Ouvriers',
                        data: [100, 170],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(255, 205, 86)',
                    }
                ]
            },
            totalEffectifs: {
                labels: ['10/2023', '11/2023'],
                datasets: [
                    {
                        label: 'Total des Salariés',
                        data: [300, 500],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(255, 159, 64)',
                    },
                    {
                        label: 'Total des Ouvriers',
                        data: [100, 170],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(255, 99, 132)',
                    }
                ]
            },
            totalSalaires: {
                labels: ['10/2023', '11/2023'],
                datasets: [
                    {
                        label: 'Total des Salariés',
                        data: [300, 500],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(54, 174, 61)',
                    },
                    {
                        label: 'Total des Ouvriers',
                        data: [100, 170],
                        hoverOffset: 4,
                        backgroundColor: 'rgb(75, 192, 192)',
                    }
                ]
            }
        })

        onWillStart(async () => {
            await loadJS("/configuration_module/static/src/libraries/selectize/selectize.min.js")
            await loadCSS("/configuration_module/static/src/libraries/selectize/selectize.default.min.css")
            await this.getData()
        })

        onMounted(() => {
        })

    }

    setState(key, val) {
        this.state[key] = val;
    }

    setPeriodeID(val) {
        this.setState('periodeID', val);
    }

    setChantierID(val) {
        this.setState('chantierID', val);
    }

    setChantier(val) {
        this.setState('chantier', val);
    }

    setPeriode(val) {
        this.setState('periode', val);
    }

    setPPeriode(val) {
        this.setState('pperiode', val);
    }

    generateRandomRGBA(alpha = 0.9) {
        var red = Math.floor(Math.random() * 256);
        var green = Math.floor(Math.random() * 256);
        var blue = Math.floor(Math.random() * 256);

        var rgbaString = 'rgba(' + red + ', ' + green + ', ' + blue + ', ' + alpha + ')';

        return rgbaString;
    }

    async getData() {
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/conducteur-dashboard/', {
            chantier_id: this.state.chantierID,
            period_id: this.state.periodeID
        })

        console.log(res)

        this.setChantier(res.chantier)
        this.setPeriode(res.current_period)
        this.setPPeriode(res.last_period)

        this.setState('totalEffectifs', {
            labels: [res.last_period, res.current_period],
            datasets: [
                {
                    label: 'Effectif des Salariés',
                    data: [res.salarier_count_last_period, res.salarier_count_current_period],
                    backgroundColor: 'rgb(255, 159, 64)',
                    hoverOffset: 4,
                },
                {
                    label: 'Effectif des Ouvriers',
                    data: [res.ouvrier_count_last_period, res.ouvrier_count_current_period],
                    backgroundColor: 'rgb(255, 99, 132)',
                    hoverOffset: 4
                }
            ]
        });

        this.setState('totalHeures', {
            labels: [res.last_period, res.current_period],
            datasets: [
                {
                    label: 'Total herures des Salariés',
                    data: [res.total_hours_salarier_last_period, res.total_hours_salarier_current_period],
                    backgroundColor: 'rgb(153, 102, 255)',
                    hoverOffset: 4,
                },
                {
                    label: 'Total herures des Ouvriers',
                    data: [res.total_hours_ouvrier_last_period, res.total_hours_ouvrier_current_period],
                    backgroundColor: 'rgb(255, 205, 86)',
                    hoverOffset: 4
                }
            ]
        });

        this.setState('totalSalaires', {
            labels: [res.last_period, res.current_period],
            datasets: [
                {
                    label: 'Total des Salaires des Salariés',
                    data: [res.salarier_amounts_current_period, res.salarier_amounts_last_period],
                    backgroundColor: 'rgb(54, 174, 61)',
                    hoverOffset: 4,
                },
                {
                    label: 'Total des Salaires des Ouvriers',
                    data: [res.ouvrier_amounts_last_period, res.ouvrier_amounts_current_period],
                    backgroundColor: 'rgb(75, 192, 192)',
                    hoverOffset: 4
                }
            ]
        });
    }
}

ConducteurDashboard.template = "owl.ConducteurDashboard"
ConducteurDashboard.components = { Chantiers, Periode, ChartRenderer, EquipeCard, EffectifPosteTable }


registry.category("actions").add("hr_management.action_main_conducteur", ConducteurDashboard)