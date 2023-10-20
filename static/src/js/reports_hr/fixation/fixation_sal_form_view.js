/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import { useService } from "@web/core/utils/hooks"

import { portrait_header } from "@reports_templates/js/headers";
import { content_fixation_sal } from "./content_fixation_sal"

import { footer_fixation_sal } from "./footer_fixation_sal";

class fixationSalFormController extends FormController {
    setup() {
        super.setup()
        this.rpc = useService("rpc");
    }

    async printfixation(id) {
        var framework = require('web.framework');
        framework.blockUI();
        try {
            const res = await this.rpc(`/hr_management/get_fixation_salaire_details/${id}`);
            let res_content = null;

            if (res) {
                res_content = await content_fixation_sal(res[0]);
            } else {
                framework.blockUI();
                return this.showNotification('Une erreur est survenue, veuillez réessayer !', "warning");
            }

            if (res_content) {
                const pdfDefinition = {
                    info: {
                        title: `FICHE DE FIXATION SALAIRE N° ${res[0].fixation_num}`,
                        author: "BIOUI TRAVAUX",
                        subject: `FICHE DE FIXATION SALAIRE `
                    },
                    pageMargins: [12, 120, 12, 240],
                    compress: false,
                    permissions: {
                        printing: 'highResolution', //'lowResolution'
                        modifying: false,
                        copying: false,
                        annotating: false,
                        fillingForms: true,
                        contentAccessibility: true,
                        documentAssembly: true
                    },
                    header: portrait_header(),
                    pageSize: "A4",
                    pageOrientation: "portrait",
                    content: res_content,
                    footer: function (currentPage, pageCount) {
                        return footer_fixation_sal(currentPage, pageCount)
                    }
                };

                const pdfDocGenerator = pdfMake.createPdf(pdfDefinition);
                const dataUrl = await pdfDocGenerator.getDataUrl();
                const targetElement = document.querySelector("#iframeContainer");
                targetElement.setAttribute("src", dataUrl);
                this.showModal();
            } else {
                framework.blockUI();
                return this.showNotification('Une erreur est survenue, veuillez réessayer !', "danger");
            }

        } catch (error) {
            console.error("Error:", error);
            this.showNotification("Une erreur s'est produite. Veuillez réessayer.", "danger");
            framework.unblockUI();
        } finally {
            framework.unblockUI();
        }
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


    showNotification(message, typeNotification) {
        this.notification.add(message, {
            title: "Odoo Notification Service",
            type: typeNotification, // info, warning, danger, success
        });
    }


}

fixationSalFormController.template = "owl.fixationSalFormView"

export const fixationSalFormView = {
    ...formView,
    Controller: fixationSalFormController,
}

registry.category("views").add("fixation_sal_form_view", fixationSalFormView)