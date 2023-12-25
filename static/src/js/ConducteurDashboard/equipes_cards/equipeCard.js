/** @odoo-module */

import { registry } from "@web/core/registry"
const { Component, onMounted, useState, onWillStart, useEffect, useRef, markup, onWillUnmount } = owl

import { EquipeGridTable } from "../equipes_grid_table/equipes_grid_table"

export class EquipeCard extends Component {
    setup() {

        this.state = useState({
            chantierID: this.props.chantier,
            periodeID: this.props.period,
            data: this.props.data
        })

        onMounted(async () => {

        })

        useEffect(
            () => {
                if (this.props) {
                    this.state.chantierID = this.props.chantier;
                    this.state.periodeID = this.props.period;
                    this.state.data = this.props.data;
                }
            },
            () => [this.props]
        )
    }

    formatNumber(number) {
        return Math.round(number).toLocaleString().replace(/,/g, ' ');
    }

}

EquipeCard.template = "owl.ConducteurEquipeCard"
EquipeCard.components = { EquipeGridTable }