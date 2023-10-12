/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

const { loadJS, loadCSS } = require('@web/core/assets');

const { onWillStart, useRef } = owl

import { portrait_header } from "@reports_templates/js/headers";
import { transfert_pdf_content } from "./content_transfert_pdf";


class TransfertListController extends ListController {
    setup() {
        super.setup();

        this.rpc = useService("rpc");
        this.notification = useService("notification");

        this.modal = useRef("modalPrint")
        this.modalClose = useRef("modalClose")

        console.warn("this is a transfert component")

    }

    async printTransferts(data) {

        var framework = require('web.framework');
        framework.blockUI();

        const allData = [];
        const contents = []

        try {
            const transfers = await Promise.all(data.map(async (id) => {
                const res = await this.rpc(`/hr_management/get_transfert/${id.resId}`);
                return res;
            }));

            allData.push(...transfers);

        } catch (error) {
            return alert('Une erreur est survenue, veuillez réessayer !');
        }

        if (allData) {
            allData.map((transfert, index) => {
                contents.push(transfert_pdf_content(transfert));
                if (index !== allData.length - 1) {
                    contents.push({ text: "", pageBreak: "after" });
                }
            });
        } else {
            framework.blockUI();
            return alert('Une erreur est survenue, veuillez réessayer !');
        }

        if (contents) {
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
                    title: `Transfert de ${allData.length} employées entre chantiers.`,
                    author: "BIOUI TRAVAUX",
                    subject: `Transferts`
                },
                pageMargins: [12, 120, 12, 246],
                header: portrait_header(),
                pageSize: "A4",
                pageOrientation: "portrait",
                content: contents,
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

            const pdf = await pdfMake.createPdf(pdfDefinition);
            const blob = await pdf.getBlob();
            const url = URL.createObjectURL(blob);

            const viewer = window.open(url, '_blank');
            viewer.onload = () => {
                framework.unblockUI();
                URL.revokeObjectURL(url);
            };
        }
        else {
            framework.blockUI();
            return alert('Une erreur est survenue, veuillez réessayer !');
        }
    }


}

export const TransfertListView = {
    ...listView,
    Controller: TransfertListController,
    buttonTemplate: "owl.PdfTransfertListView.Buttons",
};

registry.category("views").add("transfert_many_report", TransfertListView);