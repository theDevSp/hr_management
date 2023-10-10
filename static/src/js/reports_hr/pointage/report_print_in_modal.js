/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

const { loadJS, loadCSS } = require('@web/core/assets');
const { onWillStart, useRef, onMounted } = owl

import { portrait_header } from "@reports_templates/js/headers";
import { horizontal_header } from "@reports_templates/js/horizontal_header"

import { content_report_pointage_salarie } from "./content_report_pointage_salarie";
import { content_report_pointage_ouvrier } from "./content_report_pointage_ouvrier";

class PointageListController extends ListController {
    setup() {
        super.setup();

        this.rpc = useService("rpc");

        this.modal = useRef("modalPrint")
        this.modalClose = useRef("modalClose")

        this.http = this.env.services.http
        this.notification = this.env.services.notification;

        onWillStart(async () => {
            await loadJS("/reports_templates/static/src/lib/selectize/selectize.min.js")
            await loadCSS("/reports_templates/static/src/lib/selectize/selectize.default.min.scss")
        })

        onMounted(async () => {
            this.allChantiers = await this.rpc(`/hr_management/pointage/get_all_chantiers`);
            this.allEquipes = await this.rpc(`/hr_management/pointage/get_all_Equipes`);
            this.periods = await this.rpc(`/hr_management/pointage/get_all_periods`);
        })
    }

    async modalPrint() {
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

    test() {
        console.log("modal print")
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
            this.submit();
        }
    }



    async submit() {
        var framework = require('web.framework');

        framework.blockUI();
        hideModal(this.modal.el);

        if ($('#select-chantier').val() === '' || $('#select-type').val() === '' || $('#select-period').val() === '') {
            console.log('Please fill in all required fields.');
            framework.unblockUI();
            return;
        }
        else if ($('#select-type').val() === 's') {

            fetch("./hr_management/get_report_pointage/", {
                method: "POST",
                body: JSON.stringify({
                    chantier: $('#select-chantier').val(),
                    quinzine: $('#select-quinzine').val(),
                    typeemp: $('#select-type').val(),
                    equipe: $('#select-equipe').val(),
                    date: $('#select-period').val()
                })
            })
                .then(async (data) => {
                    if (data.status === 204) {
                        this.showNotification("Aucune donnée disponible !", "warning");
                        clearSelectizeInputs();
                        framework.unblockUI();
                        return;
                    } else {
                        clearSelectizeInputs();
                        try {
                            const res = await data.json();
                            const pdfContent = [];

                            await Promise.all(res.map(async (emp, index) => {
                                const content = await content_report_pointage_salarie(emp);
                                pdfContent.push(content);

                                if (index !== res.length - 1) {
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
                                    title: "Rapport", //`${res.length} STCs`,
                                    author: "BIOUI TRAVAUX",
                                    subject: `Report`
                                },
                                pageMargins: [12, 110, 12, 135],
                                header: portrait_header(),
                                pageSize: "A4",
                                pageOrientation: "portrait",
                                content: pdfContent,
                                footer: function (currentPage, pageCount) {

                                    return [

                                        {
                                            margin: [12, 5, 12, 0],
                                            layout: {
                                                hLineColor: 'gray',
                                                vLineColor: 'gray'
                                            },
                                            table: {
                                                widths: ['*', '*', '*', '*'],
                                                headerRows: 1,
                                                body: [
                                                    [{
                                                        text: 'Intéressé(e)',
                                                        bold: true,
                                                        fontSize: 10,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Pointeur',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Chef de Projet',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Directeur Technique',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    },],
                                                    [{
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true,
                                                        margin: [0, 35],
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }]
                                                ]
                                            }
                                        },

                                        {
                                            margin: [0, 5, 0, 0],
                                            columns: [{
                                                text: `${currentPage}/${pageCount}`,
                                                alignment: 'center',
                                                fontSize: 7,
                                                margin: [150, 0, 0, 0]
                                            }, {
                                                text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
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
                                URL.revokeObjectURL(url);
                            };
                        } catch (error) {
                            console.log(error);
                            framework.unblockUI();
                            this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                        }
                    }
                })
                .catch((error) => {
                    console.log(error);
                    framework.unblockUI();
                    this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                });

        }
        else if ($('#select-type').val() === 'o') {

            fetch("./hr_management/get_report_pointage_ouvrier/", {
                method: "POST",
                body: JSON.stringify({
                    chantier: $('#select-chantier').val(),
                    quinzine: $('#select-quinzine').val(),
                    typeemp: $('#select-type').val(),
                    equipe: $('#select-equipe').val(),
                    date: $('#select-period').val()
                })
            })
                .then(async (data) => {
                    if (data.status === 204) {
                        this.showNotification("Aucune donnée disponible !", "warning");
                        clearSelectizeInputs();
                        framework.unblockUI();
                        return;
                    } else {
                        clearSelectizeInputs();
                        try {
                            const res = await data.json();
                            const pdfContent = [];

                            res.lines.forEach((emp, index) => {
                                content_report_pointage_ouvrier(emp, res.chantier, res.quinzine, res.periode, res.nbrj_mois).then(content => {
                                    pdfContent.push(content);
                                    if (index !== res.lines.length - 1) {
                                        pdfContent.push({ text: "", pageBreak: "after" });
                                    }
                                });
                            });

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
                                    title: "Rapport", //`${res.length} STCs`,
                                    author: "BIOUI TRAVAUX",
                                    subject: `Report`
                                },
                                pageSize: 'A4',
                                pageMargins: [13, 110, 13, 135],
                                header: horizontal_header(),
                                pageSize: "A4",
                                pageOrientation: "landscape",
                                content: pdfContent,
                                footer: function (currentPage, pageCount) {

                                    return [

                                        {
                                            margin: [13, 5, 13, 0],
                                            layout: {
                                                hLineColor: 'gray',
                                                vLineColor: 'gray'
                                            },
                                            table: {
                                                widths: ['*', '*', '*', '*'],
                                                headerRows: 1,
                                                body: [
                                                    [{
                                                        text: 'Intéressé(e)',
                                                        bold: true,
                                                        fontSize: 10,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Pointeur',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Chef de Projet',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    }, {
                                                        text: 'Directeur Technique',
                                                        fontSize: 10,
                                                        bold: true,
                                                        alignment: 'center',
                                                        fillColor: '#04aa6d',
                                                        color: 'white',
                                                        margin: [0, 5]
                                                    },],
                                                    [{
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true,
                                                        margin: [0, 35],
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }, {
                                                        text: '',
                                                        fontSize: 9,
                                                        bold: true
                                                    }]
                                                ]
                                            }
                                        },

                                        {
                                            margin: [0, 5, 0, 0],
                                            columns: [{
                                                text: `${currentPage}/${pageCount}`,
                                                alignment: 'center',
                                                fontSize: 7,
                                                margin: [150, 0, 0, 0]
                                            }, {
                                                text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
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
                                URL.revokeObjectURL(url);
                            };

                            /*pdf.getBlob((blob) => {

                                console.log(blob)
                                const url = URL.createObjectURL(blob);
                                const viewer = window.open(url, '_blank');
                                viewer.onload = () => {
                                    URL.revokeObjectURL(url);
                                };
                                framework.unblockUI();
                            });*/

                            /*framework.unblockUI();
                            const pdf = await pdfMake.createPdf(pdfDefinition);
                            return pdf.open()*/


                        } catch (error) {
                            console.log(error);
                            framework.unblockUI();
                            this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                        }
                    }
                })
                .catch((error) => {
                    console.log(error);
                    framework.unblockUI();
                    this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                });

            /*const response = await fetch(
                "",
                {
                    method: "POST",
                    body: JSON.stringify({
                        chantier: $('#select-chantier').val(),
                        quinzine: $('#select-quinzine').val(),
                        typeemp: $('#select-type').val(),
                        equipe: $('#select-equipe').val(),
                        date: $('#select-period').val(),
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8",
                    },
                }
            );

            if (response.status === 204) {
                this.showNotification("Aucune donnée disponible !", "warning");
                clearSelectizeInputs();
                framework.unblockUI();
                return;
            }

            clearSelectizeInputs();
            const data = await response.json();
            const pdfContent = []

            data.lines.forEach((emp, index) => {
                content_report_pointage_ouvrier(emp, data.chantier, data.quinzine, data.periode, data.nbrj_mois).then(content => {
                    pdfContent.push(content);
                    if (index !== data.lines.length - 1) {
                        pdfContent.push({ text: "", pageBreak: "after" });
                    }
                });
            });

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
                    title: "Rapport", //`${res.length} STCs`,
                    author: "BIOUI TRAVAUX",
                    subject: `Report`
                },
                pageSize: 'A4',
                pageMargins: [13, 110, 13, 135],
                header: horizontal_header(),
                pageSize: "A4",
                pageOrientation: "landscape",
                content: pdfContent,
                footer: function (currentPage, pageCount) {

                    return [

                        {
                            margin: [13, 5, 13, 0],
                            layout: {
                                hLineColor: 'gray',
                                vLineColor: 'gray'
                            },
                            table: {
                                widths: ['*', '*', '*', '*'],
                                headerRows: 1,
                                body: [
                                    [{
                                        text: 'Intéressé(e)',
                                        bold: true,
                                        fontSize: 10,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Pointeur',
                                        fontSize: 10,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Chef de Projet',
                                        fontSize: 10,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Directeur Technique',
                                        fontSize: 10,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    },],
                                    [{
                                        text: '',
                                        fontSize: 9,
                                        bold: true,
                                        margin: [0, 35],
                                    }, {
                                        text: '',
                                        fontSize: 9,
                                        bold: true
                                    }, {
                                        text: '',
                                        fontSize: 9,
                                        bold: true
                                    }, {
                                        text: '',
                                        fontSize: 9,
                                        bold: true
                                    }]
                                ]
                            }
                        },

                        {
                            margin: [0, 5, 0, 0],
                            columns: [{
                                text: `${currentPage}/${pageCount}`,
                                alignment: 'center',
                                fontSize: 7,
                                margin: [150, 0, 0, 0]
                            }, {
                                text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
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

            framework.unblockUI();
            const pdf = await pdfMake.createPdf(pdfDefinition);
            return pdf.open()*/
        }
    };

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

export const PointageListView = {
    ...listView,
    Controller: PointageListController,
    buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_print_in_modal", PointageListView);
