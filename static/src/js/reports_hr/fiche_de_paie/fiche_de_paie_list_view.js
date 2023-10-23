/** @odoo-module */

import { registry } from "@web/core/registry"
import { listView } from "@web/views/list/list_view"
import { ListController } from "@web/views/list/list_controller"
import { useService } from "@web/core/utils/hooks"

const { loadJS, loadCSS } = require('@web/core/assets');
const { onWillStart, useRef, onMounted } = owl

import { content_fiche_de_paie } from "./content_fiche_de_paie";
import {header_a3_landscape} from "./header_a3_landscape"

class ficheDePaieListController extends ListController {
    setup() {
        super.setup()

        this.modal = useRef("modalPrint")
        this.modalClose = useRef("modalClose")

        this.http = this.env.services.http
        this.notification = this.env.services.notification;

        onWillStart(async () => {
            await loadJS("/reports_templates/static/src/lib/selectize/selectize.min.js")
            await loadCSS("/reports_templates/static/src/lib/selectize/selectize.default.min.css")
        })

        onMounted(async () => {
            this.allChantiers = await this.rpc(`/hr_management/pointage/get_all_chantiers`);
            this.allEquipes = await this.rpc(`/hr_management/pointage/get_all_Equipes`);
            this.periods = await this.rpc(`/hr_management/pointage/get_all_periods`);
        })
    }


    modalPrint() {
        showModal(this.modal.el);

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

        $('#select-equipe').selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'name',
            searchField: 'name',
            options: this.allEquipes,
            create: false
        });
    }

    verify() {
        const fields = [
            { element: $('#select-chantier'), message: 'Chantier' },
            { element: $('#select-type'), message: 'Type de l\'employé' },
            { element: $('#select-period'), message: 'Période' },
            { element: $('#select-quinzine'), message: 'Quinzine' },
        ];

        let allFieldsNotEmpty = true;

        for (const field of fields) {
            if (field.element.val() === '') {
                this.showNotification(`Le champ ${field.message} est requis.`, 'danger');
                allFieldsNotEmpty = false;
                return;
            }
        }

        if (allFieldsNotEmpty) {
            this.getFicheDePaie();
        }
    }

    getFicheDePaie() {
        var framework = require('web.framework');

        framework.blockUI();
        hideModal(this.modal.el);

        if ($('#select-chantier').val() === '' || $('#select-type').val() === '' || $('#select-period').val() === '') {
            console.log('Please fill in all required fields.');
            framework.unblockUI();
            return;
        } else {
            fetch("./hr_management/get_fiche_de_paie_details/", {
                method: "POST",
                body: JSON.stringify({
                    chantier: $('#select-chantier').val(),
                    quinzine: $('#select-quinzine').val(),
                    typeemp: $('#select-type').val(),
                    equipe: $('#select-equipe').val(),
                    date: $('#select-period').val()
                })
            })
                .then(async (response) => {
                    clearSelectizeInputs()
                    if (response.status === 204) {
                        this.showNotification("Aucune donnée disponible !", "warning");
                        clearSelectizeInputs();
                        framework.unblockUI();
                        return;
                    } else {
                        const res = await response.json();
                        const pdfContent = [];

                        await Promise.all(res.payslips.map(async (fiche, index) => {
                            const content = await content_fiche_de_paie(fiche, res.chantier, res.periode, res.quinzine, res.type);
                            pdfContent.push(content);

                            if (index !== res.payslips.length - 1) {
                                pdfContent.push({ text: "", pageBreak: "after" });
                            }
                        }));


                        const pdfDefinition = {
                            compress: false,
                            permissions: {
                                printing: 'highResolution',
                                modifying: false,
                                copying: false,
                                annotating: true,
                                fillingForms: true,
                                contentAccessibility: true,
                                documentAssembly: true
                            },
                            info: {
                                title: "Fiche de Paie",
                                author: "BIOUI TRAVAUX",
                                subject: `Fiche de Paie`
                            },
                            pageMargins: [20, 120, 20, 150],
                            header: header_a3_landscape(),
                            pageSize: "A3",
                            pageOrientation: "landscape",
                            content: pdfContent,
                            footer: function (currentPage, pageCount) {
                                return [

                                    {
                                        margin: [18, 5, 18, 0],
                                        layout: {
                                            hLineColor: 'gray',
                                            vLineColor: 'gray'
                                        },
                                        table: {
                                            widths: [337, 50, 335, 50, 335],
                                            headerRows: 1,
                                            body: [
                                                [{
                                                    text: 'SERVICE RESSOURCE HUMAINE',
                                                    bold: true,
                                                    fontSize: 11,
                                                    alignment: 'center',
                                                    fillColor: '#04aa6d',
                                                    color: 'white',
                                                    margin: [0, 5]
                                                },
                                                {
                                                    text: '',
                                                    border: [0, 0, 0, 0],
                                                },
                                                {
                                                    text: 'CONTRÔLE DE GESTION',
                                                    bold: true,
                                                    fontSize: 11,
                                                    alignment: 'center',
                                                    fillColor: '#04aa6d',
                                                    color: 'white',
                                                    margin: [0, 5]

                                                },
                                                {
                                                    text: '',
                                                    border: [0, 0, 0, 0],
                                                },
                                                {
                                                    text: 'SERVICE CONTRÔLE',
                                                    fontSize: 11,
                                                    bold: true,
                                                    alignment: 'center',
                                                    fillColor: '#04aa6d',
                                                    color: 'white',
                                                    margin: [0, 5],
                                                }
                                                ],
                                                [{
                                                    text: '',
                                                    fontSize: 9,
                                                    bold: true,
                                                    margin: [0, 40],
                                                },
                                                {
                                                    text: '',
                                                    border: [0, 0, 0, 0],
                                                },
                                                {
                                                    text: '',
                                                    fontSize: 9,
                                                    bold: true
                                                },
                                                {
                                                    text: '',
                                                    border: [0, 0, 0, 0],
                                                },
                                                {
                                                    text: '',
                                                    fontSize: 9,
                                                    bold: true,
                                                }
                                                ]
                                            ]
                                        }
                                    },
                                    {
                                        margin: [0, 5, 5, 0],
                                        columns: [{
                                            text: `${currentPage}/${pageCount}`,
                                            alignment: 'center',
                                            fontSize: 7,
                                            margin: [150, 0, 0, 0]
                                        }, {
                                            text: `Imprimé le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
                                            fontSize: 7,
                                            alignment: 'right',
                                            bold: true,
                                            margin: [0, 0, 12, 0],
                                            width: 130
                                        }]
                                    }

                                ]
                            }
                        };


                        const pdf = await pdfMake.createPdf(pdfDefinition);
                        const blob = await pdf.getBlob();
                        const url = URL.createObjectURL(blob);

                        const viewer = window.open(url, '_blank');
                        viewer.onload = () => {
                            framework.unblockUI();
                            const checkWindowInterval = setInterval(() => {
                                if (viewer.closed) {
                                    clearInterval(checkWindowInterval);
                                    URL.revokeObjectURL(url);
                                }
                            }, 1000);

                        };
                    }

                })
                .catch(error => {
                    clearSelectizeInputs()
                    console.log(error);
                    framework.unblockUI();
                    this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                });
        }

    }

    showNotification(message, typeNotification) {
        this.notification.add(message, {
            title: "Odoo Notification Service",
            type: typeNotification, // info, warning, danger, success
        });
    }

}

const clearSelectizeInputs = () => {
    $('#select-chantier')[0].selectize.clear();
    $('#select-quinzine')[0].selectize.clear();
    $('#select-type')[0].selectize.clear();
    $('#select-equipe')[0].selectize.clear();
}

const showModal = (el) => {
    el.style.display = "block"
    const modalClose1 = document.querySelector("#modalClose1");
    const modalClose2 = document.querySelector("#modalClose2");
    modalClose1.addEventListener('click', () => {
        el.style.display = "none";
    });
    modalClose2.addEventListener('click', () => {
        el.style.display = "none";
    });
}

const hideModal = (el) => {
    el.style.display = "none"
}

export const ficheDePaieListView = {
    ...listView,
    Controller: ficheDePaieListController,
    buttonTemplate: "owl.ficheDePaieListView.Buttons",
}

registry.category("views").add("fichepaie_report", ficheDePaieListView)