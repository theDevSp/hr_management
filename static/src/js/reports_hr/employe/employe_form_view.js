/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import { useService } from "@web/core/utils/hooks"

import { portrait_header } from "@reports_templates/js/headers";
import { content_fiche_employee } from "./content_fiche_employe"

class employeFormController extends FormController {
    setup() {
        super.setup()
        this.action = useService("action")
    }

    async printFiche(id) {
        var framework = require('web.framework');
        framework.blockUI();

        const rpc = this.env.services.rpc

        try {

            const res = await rpc(`/hr_management/get_employe_details/${id}`);
            const data = res[0]
            const content = await content_fiche_employee(data)

            const pdfDefinition = {
                info: {
                    title: `Fiche employee`,
                    author: "BIOUI TRAVAUX",
                    subject: `Fiche employee`
                },
                pageMargins: [12, 120, 12, 25],
                header: portrait_header(),
                pageSize: "A4",
                pageOrientation: "portrait",
                compress: false,
                permissions: {
                    printing: 'highResolution',
                    modifying: false,
                    copying: false,
                    annotating: false,
                    fillingForms: true,
                    contentAccessibility: true,
                    documentAssembly: true
                },
                content: content,
                footer: function (currentPage, pageCount, pageSize) {

                    return [
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
            await this.showModal();

            return
        } catch (error) {
            console.error("Error:", error);
            alert("Une erreur s'est produite. Veuillez réessayer.");
            framework.unblockUI();
        } finally {
            framework.unblockUI();
        }
    }

    async showModal() {
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

employeFormController.template = "owl.employeFormView"

export const employeFormView = {
    ...formView,
    Controller: employeFormController,
}

registry.category("views").add("employe_form_view", employeFormView)