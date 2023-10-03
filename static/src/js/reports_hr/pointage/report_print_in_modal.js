/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

const { loadJS, loadCSS } = require('@web/core/assets');
const { onWillStart, useRef } = owl

import { portrait_header } from "@reports_templates/js/headers";
import { horizontal_header } from "@reports_templates/js/horizontal_header"

import { content_report_pointage_salarie } from "./content_report_pointage_salarie";
import { content_report_pointage_ouvrier } from "./content_report_pointage_ouvrier";

class PointageListController extends ListController {
    content_report_pointage_salarie
    setup() {
        super.setup();

        this.rpc = useService("rpc");

        this.modal = useRef("modalPrint")
        this.modalClose = useRef("modalClose")

        this.modalIframe = useRef("iframemodalPrint")

        this.http = this.env.services.http
        this.notification = this.env.services.notification;

        onWillStart(async () => {
            await loadJS("/reports_templates/static/src/lib/selectize/selectize.min.js")
            await loadCSS("/reports_templates/static/src/lib/selectize/selectize.default.min.scss")

            await loadCSS("/reports_templates/static/src/lib/datepicker/datepicker.min.scss")
            await loadJS("/reports_templates/static/src/lib/datepicker/bootstrap-datepicker.min.js")
        })
    }

    async modalPrint(data) {
        showModal(this.modal.el);

        const allChantiers = await this.rpc(`/hr_management/pointage/get_all_chantiers`);
        const allEquipes = await this.rpc(`/hr_management/pointage/get_all_Equipes`);
        const periods = await this.rpc(`/hr_management/pointage/get_all_periods`);

        $("#select-period").selectize({
            maxItems: 1,
            minItems: 1,
            valueField: 'id',
            labelField: 'code',
            searchField: 'code',
            options: periods,
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
            options: allChantiers,
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
            options: allEquipes,
            create: false
        });

        $('#myForm').on('submit', (event) => {
            event.preventDefault();

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
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then((data) => {
                        clearSelectizeInputs();
                        framework.unblockUI();

                        if (data.status === 204) {
                            this.showNotification("Aucune donnée disponible !", "warning");
                            return;
                        }
                        else {
                            data.json().then(async res => {

                                const pdfContent = []

                                res.forEach(async (emp, index) => {
                                    const finalemp = emp
                                    content_report_pointage_salarie(finalemp).then(content => {
                                        pdfContent.push(content)
                                        if (index !== res.length - 1) {
                                            pdfContent.push({ text: "", pageBreak: "after" });
                                        }
                                    })

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

                                pdfMake.createPdf(pdfDefinition).open();

                                //const pdfDocGenerator = pdfMake.createPdf(pdfDefinition);
                                //const dataUrl = await pdfDocGenerator.getDataUrl();
                                //const targetElement = document.querySelector("#iframeContainerModal");
                                //targetElement.setAttribute("src", await pdfDocGenerator.getDataUrl());
                                //showModalIframe(this.modalIframe.el);

                            });
                        }
                    })
                    .catch((error) => {
                        console.log("error")
                        framework.unblockUI();
                        this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                    });

            }
            else if ($('#select-type').val() === 'o') {

                fetch(
                    "./hr_management/get_report_pointage_ouvrier/",
                    {
                        method: "POST",
                        body: JSON.stringify({
                            chantier: $('#select-chantier').val(),
                            quinzine: $('#select-quinzine').val(),
                            typeemp: $('#select-type').val(),
                            equipe: $('#select-equipe').val(),
                            date: $('#select-period').val()
                        }),
                        headers: {
                            "Content-type": "application/json; charset=UTF-8"
                        }
                    }
                )
                    .then(resp => resp.json())
                    .then(data => {

                        clearSelectizeInputs();
                        framework.unblockUI();

                        if (data.status === 204) {
                            this.showNotification("Aucune donnée disponible !", "warning");
                            return;
                        }
                        else {

                            const pdfContent = []

                            data.lines.forEach((emp, index) => {
                                content_report_pointage_ouvrier(emp, data.chantier, data.quinzine, data.periode,data.nbrj_mois).then(content => {
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

                            return pdfMake.createPdf(pdfDefinition).open();

                        }

                    })
                    .catch(error => {
                        console.log("error")
                        framework.unblockUI();
                        this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                    });

                /*fetch("./hr_management/get_report_pointage_ouvrier/", {
                    method: "POST",
                    body: JSON.stringify({
                        chantier: $('#select-chantier').val(),
                        quinzine: $('#select-quinzine').val(),
                        typeemp: $('#select-type').val(),
                        equipe: $('#select-equipe').val(),
                        date: $('#select-period').val()
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then((data) => {
                        clearSelectizeInputs();
                        framework.unblockUI();

                        if (data.status === 204) {
                            this.showNotification("Aucune donnée disponible !", "warning");
                            return;
                        }
                        else {
                            data.json().then(async res => {

                                for (const emp of res) {
                                    console.log(emp);
                                    // content_report_pointage_salarie(emp);
                                }

                                const pdfContent = []

                                return

                                res.forEach(async (emp, index) => {
                                    const finalemp = emp
                                    content_report_pointage_salarie(finalemp).then(content => {
                                        pdfContent.push(content)
                                        if (index !== res.length - 1) {
                                            pdfContent.push({ text: "", pageBreak: "after" });
                                        }
                                    })

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

                                pdfMake.createPdf(pdfDefinition).open();

                            });
                        }
                    })
                    .catch((error) => {
                        console.log("error")
                        framework.unblockUI();
                        this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
                    });*/
            }
        });
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

const showModalIframe = (el) => {
    el.style.display = "block"
    const modalClose1 = document.querySelector("#modalIframeClose");
    modalClose1.addEventListener('click', () => {
        el.style.display = "none";
    });
}

const hideModalIframe = (el) => {
    el.style.display = "none"
}


export const PointageListView = {
    ...listView,
    Controller: PointageListController,
    buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_print_in_modal", PointageListView);
