/** @odoo-module */

const { Component, onWillStart, onMounted } = owl
const { loadJS, loadCSS } = require('@web/core/assets');

import { useService } from "@web/core/utils/hooks"

import showNotification from "../Utils/showNotification";

export class Dashform extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = this.env.services.notification;

        onWillStart(async () => {
            await loadJS("/reports_templates/static/src/lib/selectize/selectize.min.js")
            await loadCSS("/reports_templates/static/src/lib/selectize/selectize.default.min.css")
        })

        onMounted(async () => {
            this.formData()
        })
    }

    async formData() {

        this.allChantiers = await this.rpc(`/hr_management/pointage/get_all_chantiers`);
        this.allEquipes = await this.rpc(`/hr_management/pointage/get_all_Equipes`);
        this.periods = await this.rpc(`/hr_management/pointage/get_all_periods`);

        $("#select-period").selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'code',
            searchField: 'code',
            options: this.periods,
            create: false,
            optionGroupRegister: function (optgroup) {
                var capitalised = optgroup.charAt(0).toUpperCase() + optgroup.substring(1);
                var group = {
                    label: 'Année : ' + capitalised
                };

                group[this.settings.optgroupValueField] = optgroup;

                return group;
            },
            optgroupField: 'year',
        });

        $('#select-chantier').selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'name',
            searchField: 'name',
            options: this.allChantiers,
            create: false
        });

        $('#select-quinzine').selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'title',
            searchField: 'title',
            options: [],
            create: false
        });

        $('#select-equipe').selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'name',
            searchField: 'name',
            options: this.allEquipes,
            create: false
        });

        $('#select-type').selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'title',
            searchField: 'title',
            options: [
                { id: 'o', title: 'Ouvrier' },
                { id: 's', title: 'Salarié' },
            ],
            create: false,
            onChange: (selectedValue) => {
                const selectQuinzine = $('#select-quinzine')[0].selectize;

                if (selectedValue === 'o') {

                    selectQuinzine.clearOptions();

                    const existingOption = selectQuinzine.options['quinzaine12'];
                    if (existingOption) {
                        delete selectQuinzine.options['quinzaine12'];
                    }

                    selectQuinzine.addOption([
                        { id: 'quinzaine1', title: 'Quinzaine1' },
                        { id: 'quinzaine2', title: 'Quinzaine2' }
                    ]);
                    selectQuinzine.refreshOptions();
                    selectQuinzine.clear();
                    selectQuinzine.enable();
                } else if (selectedValue === 's') {

                    selectQuinzine.clearOptions();
                    selectQuinzine.addOption([
                        { id: 'quinzaine12', title: 'Quinzaine12' },
                    ]);
                    selectQuinzine.refreshOptions();
                    selectQuinzine.clear();
                    selectQuinzine.setValue('quinzaine12');
                    selectQuinzine.disable();
                }
            }
        });
    }

    verify() {

        const fields = [
            { element: $('#select-period'), message: 'Période' },
            { element: $('#select-type'), message: 'Type de l\'employé' },
            { element: $('#select-quinzine'), message: 'Quinzine' },
            { element: $('#select-chantier'), message: 'Chantier' },
        ];

        let allFieldsNotEmpty = true;

        for (const field of fields) {
            if (field.element.val() === '') {
                showNotification(this.notification, 'danger', `Le champ ${field.message} est requis.`);
                allFieldsNotEmpty = false;
                return;
            }
        }

        if (allFieldsNotEmpty) {
            const periodeID = $('#select-period').val();
            const chantierID = $('#select-chantier').val();
            const employeType = $('#select-type').val();
            const quinzine = $('#select-quinzine').val();
            const equipe = $('#select-equipe').val();
            this.props.onClickFrom(periodeID, chantierID, employeType, quinzine, equipe);
        }
    }

    clear() {
        $('#select-period')[0].selectize.clear();
        $('#select-chantier')[0].selectize.clear();
        $('#select-quinzine')[0].selectize.clear();
        $('#select-type')[0].selectize.clear();
        $('#select-equipe')[0].selectize.clear();
        this.props.updateView()
    }
}

Dashform.template = "owl.dashboardForm"