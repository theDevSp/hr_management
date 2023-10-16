/** @odoo-module */
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

import { portrait_header } from "@reports_templates/js/headers";
import { stc_pdf_content } from "./content_pdf_stc";

class StcListController extends ListController {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
    }

    async print(data) {
        var framework = require('web.framework');
        framework.blockUI();
        try {

            const stcIds = this.model.root.selection.map((rec) => rec.resId);

            if (stcIds.length === 0) {
                alert("Error in selection");
                framework.unblockUI();
                return;
            }

            const allData = [];
            const contents = []

            try {
                const stcs = await Promise.all(stcIds.map(async (id) => {
                    const res = await this.rpc(`/hr_management/get_stc/${id}`);
                    return res;
                }));

                allData.push(...stcs);
            } catch (error) {
                framework.unblockUI();
                alert('Une erreur est survenue, veuillez réessayer !');
            }


            if (allData) {
                allData.map((conge, index) => {
                    contents.push(stc_pdf_content(conge));
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
                    info: {
                        title: `${allData.length} STCs`,
                        author: "BIOUI TRAVAUX",
                        subject: `STC`
                    },
                    pageMargins: [12, 120, 12, 160],
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
                                    widths: ['*', '*', '*', '*'],
                                    headerRows: 1,
                                    body: [
                                        [{
                                            text: 'Ressource Humaines',
                                            bold: true,
                                            fontSize: 10,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        }, {
                                            text: 'Contrôle de Gestion',
                                            fontSize: 10,
                                            bold: true,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        }, {
                                            text: 'Direction',
                                            fontSize: 10,
                                            bold: true,
                                            alignment: 'center',
                                            fillColor: '#04aa6d',
                                            color: 'white',
                                            margin: [0, 5]
                                        }, {
                                            text: 'Juridique',
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
                                            margin: [0, 48],
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

            /*const stcs = [];
            let res_content = [];

            await Promise.all(data.map(async (id) => {
                const res = await this.rpc(`/hr_management/get_stc/${id.resId}`);
                stcs.push(res)
            }));

            if (stcs) {
                stcs.map((stc, index) => {
                    res_content.push(stc_pdf_content(stc));
                    if (index !== stcs.length - 1) {
                        res_content.push({ text: "", pageBreak: "after" });
                    }
                });
            } else {
                framework.unblockUI();
                return alert('Une erreur est survenue, veuillez réessayer !');
            }

            const pdfDefinition = {
                info: {
                    title: `${stcs.length} STCs`,
                    author: "BIOUI TRAVAUX",
                    subject: `STC`
                },
                pageMargins: [12, 120, 12, 160],
                header: portrait_header(),
                pageSize: "A4",
                pageOrientation: "portrait",
                content: res_content,
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
                                        text: 'Ressource Humaines',
                                        bold: true,
                                        fontSize: 10,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Contrôle de Gestion',
                                        fontSize: 10,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Direction',
                                        fontSize: 10,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'Juridique',
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
                                        margin: [0, 48],
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
                const checkWindowInterval = setInterval(() => {
                    if (viewer.closed) {
                        clearInterval(checkWindowInterval);
                        URL.revokeObjectURL(url);
                    }
                }, 1000);

            };*/


        } catch (error) {
            framework.unblockUI();
            alert('Une erreur est survenue, veuillez réessayer !');
            console.error("Error:", error);
        } finally {
            framework.unblockUI();
        }
    }

}

export const StcListView = {
    ...listView,
    Controller: StcListController,
    buttonTemplate: "owl.StcCongesListView.Buttons",
};

registry.category("views").add("stc_many_report", StcListView);