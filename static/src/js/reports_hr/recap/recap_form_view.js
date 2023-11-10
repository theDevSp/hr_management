/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import { useService } from "@web/core/utils/hooks"

import { portrait_header } from "@reports_templates/js/headers";
import { content_recap } from "./content_recap";

class RecapFormController extends FormController {
    setup() {
        super.setup()
        console.log("This is res partner form controller")
        this.action = useService("action")
    }

    async printRecap(id) {
        var framework = require('web.framework');
        framework.blockUI();

        const rpc = this.env.services.rpc

        const res = await rpc(`/hr_management/get_recap_details/${id}`);
        const data = res

        console.log(res)
        console.log(data)

        const contents = await content_recap()

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
                    title: `RECAP.`,
                    author: "BIOUI TRAVAUX",
                    subject: `Demandes des Congés.`
                },
                pageMargins: [12, 120, 13, 115],
                header: portrait_header(),
                pageSize: "A4",
                pageOrientation: "portrait",
                content: contents,
                footer: function (currentPage, pageCount, pageSize) {

                    return [

                        {
                            margin: [12, 5, 13, 0],
                            layout: {
                                hLineColor: 'gray',
                                vLineColor: 'gray'
                            },
                            table: {
                                widths: ['*', '*', '*'],
                                headerRows: 1,
                                body: [
                                    [{
                                        text: 'SERVICE RESSOURCES HUMAINES',
                                        bold: true,
                                        fontSize: 10,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'CONTRÔLE DE GESTION',
                                        fontSize: 9,
                                        bold: true,
                                        alignment: 'center',
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5]
                                    }, {
                                        text: 'SERVICE CONTRÔLE',
                                        fontSize: 9,
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
                                        margin: [0, 25],
                                    }, {
                                        text: '',
                                        fontSize: 9,
                                        bold: true
                                    }, {
                                        text: '',
                                        fontSize: 9,
                                        bold: true
                                    },]
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
    }
}

RecapFormController.template = "owl.RecapFormView"

export const recapFormView = {
    ...formView,
    Controller: RecapFormController,
}

registry.category("views").add("recap_form_view", recapFormView)