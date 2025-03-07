/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadCSS, loadJS } from "@web/core/assets";
import { blockUI, unblockUI } from "web.framework";
const { Component, onMounted, useState, onWillStart, useEffect, useRef, xml, onWillUnmount } = owl
import { useService } from "@web/core/utils/hooks";
import showNotification from "@configuration_module/js/utils/showNotification";

export class EffectifPosteTable extends Component {
    setup() {

        this.notification = useService("notification")
        this.table = useRef("wrapperRef");

        this.state = useState({
            chantierID: false,
            periodeID: false,
            data: false,
        })

        useEffect(
            () => {
                if (this.props) {
                    this.state.chantierID = this.props.chantier;
                    this.state.periodeID = this.props.period;
                    this.getPostesData()
                }
            },
            () => [this.props]
        )

        onWillStart(async () => {
            await loadCSS("/configuration_module/static/src/libraries/GridJS/mermaid.min.css");
            await loadJS("/configuration_module/static/src/libraries/GridJS/gridjs.umd.js");
        })

        onMounted(() => {
        });

        onWillUnmount(() => {
            if (this.grid) {
                this.grid.destroy()
            }
        })

    }

    async mountTable() {
        if (this.grid) {
            this.grid.destroy()
        }

        this.grid = new gridjs.Grid({
            search: true,
            sort: true,
            pagination: {
                limit: 12
            },
            data: this.state.data.postesData,
            data: () => {
                return new Promise(resolve => {
                    setTimeout(() =>
                        resolve(this.state.data.postesData), 500);
                });
            },
            language: {
                'search': {
                    'placeholder': 'Recherche...'
                },
                'pagination': {
                    'previous': 'Précédent',
                    'next': 'Suivant',
                    'showing': 'Affichage de',
                    'results': () => 'enregistrements'
                }
            },
            columns: [
                { id: 'postes', name: 'Postes' },
                { id: 'periode_precedente', name: this.state.data.periode_precedente },
                { id: 'periode_actuelle', name: this.state.data.periode_actuelle },
                {
                    id: 'difference',
                    name: '',
                    sort: false,
                    formatter: (_, row) => {
                        const diff = row.cells[1].data - row.cells[2].data;

                        if (!isNaN(diff) && diff !== 0) {
                            const arrowIcon = diff > 0 ? 'fa-arrow-up' : 'fa-arrow-down';
                            const textColorClass = diff > 0 ? 'text-success' : 'text-danger';

                            return gridjs.html(`<span class="${textColorClass}">
                                        <i class="fas ${arrowIcon}"></i> ${Math.abs(diff)}
                                    </span>`);
                        } else if (diff === 0) {
                            return gridjs.html(`<span class="text-info">
                                        ${diff}
                                    </span>`);
                        }
                    }
                }
            ],
            style: {
                table: {
                },
                th: {
                    'background-color': 'rgb(0,145,132,0.1)',
                    'font-weight': 'bold'
                },
                td: {
                }
            }

        }).render(this.table.el);
    }

    setState(key, val) {
        this.state[key] = val;
    }

    setChantier(val) {
        this.setState('chantier', val);
    }

    setPeriodeID(val) {
        this.setState('periodeID', val);
    }

    setPeriode(val) {
        this.setState('periode', val);
    }

    setLastPeriode(val) {
        this.setState('lastPeriode', val);
    }

    setData(val) {
        this.setState('data', val);
    }

    async getPostesData() {

        if (this.state.chantierID === null || this.state.periodeID === null) {
            return
        }
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/conducteur-dashboard/effectif-postes', {
            chantier_id: this.state.chantierID,
            period_id: this.state.periodeID
        })

        switch (res.code) {
            case 200:
                this.table.el.innerHTML = ''
                this.state.data = res
                this.mountTable()
                showNotification(this.notification, "success", `Effectif des Postes: ${res.message}`);
                break;

            case 202:
                this.table.el.innerHTML = `<strong>Pas de données à afficher pour ce critère.</strong>`
                showNotification(this.notification, "warning", 'Effectif des Postes: Pas de données à afficher pour ce critère.');
                break;

            case 504:
                this.table.el.innerHTML = ''
                showNotification(this.notification, "danger", `Effectif des Postes: ${res.message}`);
                break;

            default:
                break;
        }
    }

}

EffectifPosteTable.template = "owl.ConducteurEffectifPoste"