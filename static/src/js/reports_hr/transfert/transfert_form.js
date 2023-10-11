/** @odoo-module */

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

const { useRef } = owl

import { portrait_header } from "@reports_templates/js/headers";
import { transfert_pdf_content } from "./content_transfert_pdf";

class TransfertFormController extends FormController {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.modal = useRef("iframemodal")
        this.modalIframe = useRef("iframeContainer")

        console.warn("this is a transfert component Form")
    }

    async print(data) {

        var framework = require('web.framework');

        this.rpc(`/hr_management/get_transfert/${data.id}`)
            .then(response => {
                framework.blockUI();
                const content = transfert_pdf_content(response)
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
                        title: `Transfert Numéro : ${data.name}`,
                        author: "BIOUI TRAVAUX",
                        subject: `Transfert`
                    },
                    pageMargins: [12, 120, 12, 246],
                    header: portrait_header(),
                    pageSize: "A4",
                    pageOrientation: "portrait",
                    content: content,
                    footer: function (currentPage, pageCount) {
                        return [

                            {
                                margin: [12, 5, 12, 0],
                                layout: {
                                    hLineColor: 'gray',
                                    vLineColor: 'gray'
                                },
                                table: {
                                    widths: ['*', '*', '*'],
                                    headerRows: 1,
                                    body: [
                                        [{
                                            text: 'Intéressé(e)',
                                            bold: true,
                                            fontSize: 11,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        },
                                        {
                                            text: 'Pointeur Chantier de Départ',
                                            bold: true,
                                            fontSize: 11,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]

                                        },
                                        {
                                            text: 'Pointeur Chantier de Destination',
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
                                            margin: [0, 35],
                                        },
                                        {
                                            text: '',
                                            fontSize: 9,
                                            bold: true
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
                                margin: [125, 5, 12, 0],
                                layout: {
                                    hLineColor: 'gray',
                                    vLineColor: 'gray'
                                },
                                alignment: 'center',
                                table: {
                                    widths: [350],
                                    headerRows: 1,
                                    body: [
                                        [{
                                            text: 'Visa Responsable du Site',
                                            bold: true,
                                            fontSize: 11,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5],
                                        }],
                                        [{
                                            text: '',
                                            margin: [0, 35],
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

                const pdfDocGenerator = pdfMake.createPdf(pdfDefinition);
                pdfDocGenerator.getDataUrl()
                    .then((result) => {
                        this.modalIframe.el.src = result
                        showModal(this.modal.el)
                        framework.unblockUI();
                    }).catch((error) => {
                        console.error("error:", error);
                    });

            })
            .catch(error => {
                console.error("Error while making RPC:", error);
            });
    }
}

const showModal = (el) => {
    el.style.display = "block"
    const modalClose = document.querySelector("#modalClose");
    modalClose.addEventListener('click', () => {
        el.style.display = "none";
    });
}

const hideModal = (el) => {
    el.style.display = "none"
}

TransfertFormController.template = "owl.FormTransfertView";

export const TransfertFormView = {
    ...formView,
    Controller: TransfertFormController,
};

registry.category("views").add("transfert_single_report", TransfertFormView);
