/** @odoo-module */
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

import { portrait_header } from "@reports_templates/js/headers";
import { content_demande_de_conges } from "./content_demande_de_conges";

class CongesListController extends ListController {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
    }

    async printConges(url) {

        var framework = require('web.framework');
        framework.blockUI();

        try {

            const congesIds = this.model.root.selection.map((rec) => rec.resId);

            if (congesIds.length === 0) {
                alert("Error in selection");
                framework.unblockUI();
                return;
            }


            const allData = [];
            const contents = []

            try {
                const conges = await Promise.all(congesIds.map(async (id) => {
                    const res = await this.rpc(`/hr_management/get_conges_details/${id}`);
                    return res;
                }));

                allData.push(...conges);

            } catch (error) {
                framework.unblockUI();
                return alert('Une erreur est survenue, veuillez réessayer !');
            }

            if (allData) {
                allData.map((conge, index) => {
                    contents.push(content_demande_de_conges(conge[0]));
                    if (index !== allData.length - 1) {
                        contents.push({ text: "", pageBreak: "after" });
                    }
                });
            } else {
                framework.unblockUI();
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
                        title: `Demandes des Congés de ${allData.length} employeurs.`,
                        author: "BIOUI TRAVAUX",
                        subject: `Demandes des Congés.`
                    },
                    pageMargins: [12, 120, 12, 180],
                    header: portrait_header(),
                    pageSize: "A4",
                    pageOrientation: "portrait",
                    content: contents,
                    footer: function (currentPage, pageCount, pageSize) {

                        return [
                            {
                                margin: [12, 0, 12, 0],
                                layout: {
                                    hLineColor: 'gray',
                                    vLineColor: 'gray'
                                },
                                table: {
                                    widths: ['*'],
                                    body: [
                                        [{
                                            margin: [8, 8],
                                            text: 'Signatures :',
                                            bold: true,
                                            fontSize: 11,
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            border: [1, true, 0, true],
                                            alignment: 'center'
                                        }
                                        ]
                                    ]
                                },

                            },
                            {
                                margin: [12, 5, 12, 0],
                                layout: {
                                    hLineColor: 'gray',
                                    vLineColor: 'gray'
                                },
                                table: {
                                    widths: ['*', '*', '*', '*'],
                                    heights: [10, 10],
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
                                        },
                                        {
                                            text: 'Pointeur',
                                            fontSize: 9,
                                            bold: true,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        },
                                        {
                                            text: 'Chef de Projet',
                                            fontSize: 9,
                                            bold: true,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        },
                                        {
                                            text: 'Directeur Technique',
                                            fontSize: 9,
                                            bold: true,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        },
                                        ],
                                        [{
                                            text: '',
                                            fontSize: 9,
                                            bold: true,
                                            margin: [0, 40],
                                            //padding: [0, 20]
                                        },
                                        {
                                            text: '',
                                            fontSize: 9,
                                            bold: true
                                        },
                                        {
                                            text: '',
                                            fontSize: 9,
                                            bold: true
                                        },
                                        {
                                            text: '',
                                            fontSize: 9,
                                            bold: true
                                        }
                                        ]
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
                    const checkWindowInterval = setInterval(() => {
                        if (viewer.closed) {
                            clearInterval(checkWindowInterval);
                            URL.revokeObjectURL(url);
                        }
                    }, 1000);

                };
            }
            else {
                framework.unblockUI();
                return alert('Une erreur est survenue, veuillez réessayer !');
            }
        } catch (error) {
            console.error("Error:", error);
            framework.unblockUI();
            alert('Une erreur est survenue, veuillez réessayer !');
        } finally {

        }
    }
}

export const CongesListView = {
    ...listView,
    Controller: CongesListController,
    buttonTemplate: "owl.PdfCongesListView.Buttons",
};

registry.category("views").add("pdf_many_demande_de_conges", CongesListView);