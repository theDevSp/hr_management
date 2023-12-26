/** @odoo-module */

const { Component, onWillStart, onMounted, useState } = owl
const { loadJS, loadCSS } = require('@web/core/assets');

import { Quinzaine } from "@hr_management/js/components/quinzaine/quinzaine";
import { Periode } from "@account_fiscal_year_period/js/components/periodes/periodes";
import { Chantiers } from "@construction_site_management/js/components/Chantiers/chantiers";
import { Equipes } from "@construction_site_management/js/components/Equipes/equipes";

import { useService } from "@web/core/utils/hooks"

import showNotification from "@configuration_module/js/utils/showNotification";

export class Dashform extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = this.env.services.notification;

        this.state = useState({
            isDisabled: true,
            quinz: [],
            periodeID: '',
            chantierID: '',
            equipeID: ''
        });

        onWillStart(async () => {
            await loadJS("/configuration_module/static/src/libraries/selectize/selectize.min.js")
            await loadCSS("/configuration_module/static/src/libraries/selectize/selectize.default.min.css")
        })
    }

    setState(key, val) {
        this.state[key] = val;
    }

    setQuinz(val) {
        this.setState('quinz', val);
    }

    setPeriodeID(val) {
        this.setState('periodeID', val);
    }

    setChantierID(val) {
        this.setState('chantierID', val);
    }

    setEquipeID(val) {
        this.setState('equipeID', val);
    }

    verify() {

        const state = this.state
        const fields = [
            { element: state.periodeID, message: 'Période' },
            { element: state.quinz[1], message: 'Type de l\'employé' },
            { element: state.quinz[0], message: 'Quinzine' },
            { element: state.chantierID, message: 'Chantier' },
        ];

        let allFieldsNotEmpty = true;

        for (const field of fields) {
            if (field.element === '') {
                showNotification(this.notification, 'danger', `Le champ ${field.message} est requis.`);
                allFieldsNotEmpty = false;
                return;
            }
        }

        if (allFieldsNotEmpty) {
            const periodeID = state.periodeID;
            const chantierID = state.chantierID;
            const employeType = state.quinz[1];
            const quinzine = state.quinz[0];
            const equipe = state.equipeID;
            this.props.onClickFrom(periodeID, chantierID, employeType, quinzine, equipe);
            this.setState('isDisabled', false);
        }
    }

    clear() {
        $('#select-period')[0].selectize.clear();
        $('#select-chantier')[0].selectize.clear();
        $('#select-quinzine')[0].selectize.clear();
        $('#select-type')[0].selectize.clear();
        $('#select-equipe')[0].selectize.clear();

        this.setState('quinz', '');
        this.setState('periodeID', '');
        this.setState('chantierID', '');
        this.setState('equipeID', '');

        this.setState('isDisabled', true);
        this.props.updateView()
    }
}

Dashform.template = "owl.dashboardForm"
Dashform.components = { Chantiers, Equipes, Periode, Quinzaine }
