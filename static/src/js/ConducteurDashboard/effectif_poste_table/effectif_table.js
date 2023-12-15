/** @odoo-module */

import { registry } from "@web/core/registry"
const { Component, onMounted, useState, onWillStart, useEffect, useRef, markup, onWillUnmount } = owl

import { loadCSS, loadJS } from "@web/core/assets";
import { blockUI, unblockUI } from "web.framework";


export class EffectifPosteTable extends Component {
    setup() {

        this.table = useRef("wrapperRef");

        this.state = useState({
            chantierID: this.props.chantier,
            periodeID: this.props.period,
            data: false,
        })

        useEffect(
            () => {
                if (this.props.chantier != '' && this.props.period != '' && this.state.data) {
                    this.state.chantierID = this.props.chantier;
                    this.state.periodeID = this.props.period;
                    this.getPostesData()
                }
            },
            () => [this.props.period, this.props.chantier]
        )

        onWillStart(async () => {
            await loadCSS("/configuration_module/static/src/libraries/GridJS/mermaid.min.css");
            await loadJS("/configuration_module/static/src/libraries/GridJS/gridjs.umd.js");
        })

        onMounted(() => {
            this.getPostesData();
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
            pagination: true,
            data: this.state.data.postesData,
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
                'Postes',
                this.state.data.periode_precedente,
                this.state.data.periode_actuelle,
                {
                    name: '',
                    formatter: (_, row) => gridjs.html(markup(`<span class="text-success">
                                            <i class=""></i>${row.cells[1].data + row.cells[2].data}
                                            </span>`))
                }],

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
        const rpc = this.env.services.rpc
        const res = await rpc('/hr_management/conducteur-dashboard/effectif-postes', {
            chantier_id: this.state.chantierID,
            period_id: this.state.periodeID
        })

        this.state.data = res
        this.mountTable()
    }

}

EffectifPosteTable.template = "owl.ConducteurEffectifPoste"