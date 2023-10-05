/** @odoo-module */
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

import { stc_pdf_content } from "./content_pdf_stc";
import { portrait_header } from "@reports_templates/js/headers";

class StcFormController extends FormController {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.overlay = document.createElement("div");
        this.spinner = document.createElement("div");
        this.overlay.className = "overlay";
        this.spinner.id = "spinner";
        this.spinner.className = "spinner";
    }

    async print(data) {
        try {
            this.showOverlayAndSpinner();

            const res = await this.rpc(`/hr_management/get_stc/${data.id}`);
            let res_content = null;

            if (res && res.stc_employee_bank) {
                res_content = stc_pdf_content(res);
            } else {
                return alert('Une erreur est survenue, veuillez réessayer !');
            }

            const pdfDefinition = {
                info: {
                    title: `${res.stc_reference} du ${res.stc_date}`,
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

            const pdfDocGenerator = pdfMake.createPdf(pdfDefinition);
            const dataUrl = await pdfDocGenerator.getDataUrl();
            const targetElement = document.querySelector("#iframeContainer");
            targetElement.setAttribute("src", dataUrl);
            this.showModal();
        } catch (error) {
            console.error("Error:", error);
        } finally {
            this.hideOverlayAndSpinner();
        }
    }

    showOverlayAndSpinner() {
        this.overlay.style.display = "block";
        this.spinner.style.display = "block";
        document.body.appendChild(this.overlay);
        document.body.appendChild(this.spinner);
    }

    hideOverlayAndSpinner() {
        this.overlay.style.display = "none";
        this.spinner.style.display = "none";
        document.body.removeChild(this.overlay);
        document.body.removeChild(this.spinner);
    }

    showModal() {
        const iframeModal = document.querySelector("#iframemodal");
        if (iframeModal) {
            iframeModal.style.display = "block";
            const modalClose = document.querySelector("#modalClose");
            if (modalClose) {
                modalClose.addEventListener('click', () => {
                    iframeModal.style.display = "none";
                    const targetElement = document.querySelector("#iframeContainer");
                    targetElement.removeAttribute("src");
                });
            }
        }
    }
}

StcFormController.template = "owl.StcFormView";

export const StcFormView = {
    ...formView,
    Controller: StcFormController,
};

registry.category("views").add("stc_single_report", StcFormView);
