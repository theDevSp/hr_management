/** @odoo-module */
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

import { content_many_demande_de_conges } from "./content_many_demande_de_conges"
import { portrait_header } from "@reports_templates/js/headers";

class CongesListController extends ListController {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.overlay = document.createElement("div");
        this.spinner = document.createElement("div");
        this.overlay.className = "overlay";
        this.spinner.id = "spinner";
        this.spinner.className = "spinner";
    }

    async printConges(url) {
        try {
            this.showOverlayAndSpinner();

            const congesIds = this.model.root.selection.map((rec) => rec.resId);

            if (congesIds.length === 0) {
                console.error("Error in selection");
                return;
            }

            const data = await this.getData(congesIds);
            const pdfDefinitions = await this.getPDFDefinitions(data);

            const pdfDefinition = {
                info: {
                    title: `${this.model.root.selection.length} Demandes de Congés`,
                    author: "BIOUI TRAVAUX",
                    subject: "Demandes De Congés",
                },
                pageMargins: [12, 120, 12, 20],
                header: portrait_header(),
                pageSize: "A4",
                pageOrientation: "portrait",
                content: pdfDefinitions,
                footer: (currentPage, pageCount) => ({
                    text: `${currentPage.toString()} of ${pageCount}`,
                    alignment: "center",
                    fontSize: 7,
                }),
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
                modalClose.addEventListener("click", () => {
                    iframeModal.style.display = "none";
                    const targetElement = document.querySelector("#iframeContainer");
                    targetElement.removeAttribute("src");
                });
            }
        }
    }

    async getData(ids) {
        const data = await Promise.all(
            ids.map(async (id) => {
                const res = await this.rpc(`/hr_management/get_conges_details/${id}`);
                return res ? res[0] : null;
            })
        );
        return data.filter((item) => item !== null);
    }

    async getPDFDefinitions(data) {
        const pageDefinitions = [];
        for (let index = 0; index < data.length; index++) {
            const conge = data[index];
            const pdfContent = content_many_demande_de_conges(conge, index + 1, data.length);
            pageDefinitions.push(pdfContent);
            if (index !== data.length - 1) {
                pageDefinitions.push({ text: "", pageBreak: "after" });
            }
        }
        return pageDefinitions;
    }
}

export const CongesListView = {
    ...listView,
    Controller: CongesListController,
    buttonTemplate: "owl.PdfCongesListView.Buttons",
};

registry.category("views").add("pdf_many_demande_de_conges", CongesListView);