/** @odoo-module */

import { registry } from "@web/core/registry"

const { Component, onMounted, useState, onWillStart, useEffect } = owl
const { loadJS, loadCSS } = require('@web/core/assets');
import { blockUI, unblockUI } from "web.framework";
import { useService } from "@web/core/utils/hooks";

import { Chantiers } from "@construction_site_management/js/components/Chantiers/chantiers";
import { Periode } from "@account_fiscal_year_period/js/components/periodes/periodes";

import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { EquipeCard } from "./equipes_cards/equipeCard";
import { EffectifPosteTable } from "./effectif_poste_table/effectif_table";
import showNotification from "@configuration_module/js/utils/showNotification";

export class ConducteurDashboard extends Component {

    setup() {

        this.notification = useService("notification")

        this.state = useState({
            periodeID: 143,
            chantierID: 432,
            chantierName: '',
            periodeCode: '',
            prevPeriodeCode: '',
            totalHeures: null,
            totalEffectifs: null,
            totalSalaires: null,
            equipesData: false
        })

        useEffect(
            () => {
                if (this.state.chantierID != '' && this.state.periodeID != '') {
                    this.getData();
                }
            },
            () => [this.state.chantierID, this.state.periodeID]
        )

        onWillStart(async () => {
            await loadJS("/configuration_module/static/src/libraries/selectize/selectize.min.js")
            await loadCSS("/configuration_module/static/src/libraries/selectize/selectize.default.min.css")
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

    setChantierName(val) {
        this.setState('chantierName', val);
    }

    setPeriodeCode(val) {
        this.setState('periodeCode', val);
    }

    setPrevPeriodeCode(val) {
        this.setState('prevPeriodeCode', val);
    }

    async getData() {
        blockUI();
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/conducteur-dashboard/', {
            chantier_id: this.state.chantierID,
            period_id: this.state.periodeID
        })

        switch (res.code) {
            case 200:
                this.setChantierName(res.chantier)
                this.setPeriodeCode(res.periode_courante)
                this.setPrevPeriodeCode(res.periode_precedente)

                this.setState('totalEffectifs', {
                    labels: [res.periode_precedente, res.periode_courante],
                    datasets: [
                        {
                            label: 'Effectif des Salariés',
                            data: [res.count_salaries_derniere_periode, res.count_salaries_periode],
                            backgroundColor: 'rgb(255, 159, 64)',
                            hoverOffset: 4,
                        },
                        {
                            label: 'Effectif des Ouvriers Q1',
                            data: [res.count_ouvriers_q1_derniere_periode, res.count_ouvriers_q1_periode],
                            backgroundColor: 'rgb(255, 29, 132)',
                            hoverOffset: 4
                        },
                        {
                            label: 'Effectif des Ouvriers Q2',
                            data: [res.count_ouvriers_q2_periode, res.count_ouvriers_q2_derniere_periode],
                            backgroundColor: 'rgb(255, 99, 102)',
                            hoverOffset: 4
                        }
                    ]
                });

                this.setState('totalHeures', {
                    labels: [res.periode_precedente, res.periode_courante],
                    datasets: [
                        {
                            label: 'Total herures des Salariés',
                            data: [res.total_heures_derniere_periode_salaries, res.total_heures_periode_salaries],
                            backgroundColor: 'rgb(153, 102, 255)',
                            hoverOffset: 4,
                        },
                        {
                            label: 'Total herures des Ouvriers',
                            data: [res.total_heures_derniere_periode_ouvriers, res.total_heures_periode_ouvriers],
                            backgroundColor: 'rgb(255, 205, 86)',
                            hoverOffset: 4
                        }
                    ]
                });

                this.setState('totalSalaires', {
                    labels: [res.periode_precedente, res.periode_courante],
                    datasets: [
                        {
                            label: 'Total des Salaires des Salariés',
                            data: [res.total_salaires_derniere_periode_salaries, res.total_salaires_periode_salaries],
                            backgroundColor: 'rgb(54, 174, 61)',
                            hoverOffset: 4,
                        },
                        {
                            label: 'Total des Salaires des Ouvriers',
                            data: [res.total_salaires_derniere_periode_ouvriers, res.total_salaires_periode_ouvriers],
                            backgroundColor: 'rgb(75, 192, 192)',
                            hoverOffset: 4
                        }
                    ]
                });

                const equipesData = await rpc('/hr_management/conducteur-dashboard/equipes', {
                    chantier_id: this.state.chantierID,
                    period_id: this.state.periodeID
                })

                if (equipesData.code == 200) {
                    this.setState('equipesData', equipesData)
                    showNotification(this.notification, "success", equipesData.message);
                }
                else {
                    this.setState('equipesData', false)
                    showNotification(this.notification, "warning", 'Pas de données à afficher pour ce critère.');
                }
                unblockUI();
                break;

            case 202:
                showNotification(this.notification, "warning", 'Pas de données à afficher pour ce critère.');
                unblockUI();
                break;

            case 504:
                console.error(res.error)
                showNotification(this.notification, "danger", res.message);
                unblockUI();
                break;

            default:
                unblockUI();
                break;
        }
    }
}

ConducteurDashboard.template = "owl.ConducteurDashboard"
ConducteurDashboard.components = { Chantiers, Periode, ChartRenderer, EquipeCard, EffectifPosteTable }


registry.category("actions").add("hr_management.action_main_conducteur", ConducteurDashboard)