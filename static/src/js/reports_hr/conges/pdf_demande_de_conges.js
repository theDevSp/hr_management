/** @odoo-module */
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";

import { content_demande_de_conges } from "./content_demande_de_conges"
import { portrait_header } from "@reports_templates/js/headers";

class CongesFormController extends FormController {
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

      const res = await this.rpc(`/hr_management/get_conges_details/${url.id}`);
      const data = res[0];

      const res_data = content_demande_de_conges(data)

      const pdfDefinition = {
        info: res_data.info,
        pageMargins: [12, 120, 12, 345],
        header: portrait_header(),
        pageSize: "A4",
        pageOrientation: "portrait",
        content: res_data.content,
        footer: res_data.footer
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


CongesFormController.template = "owl.PdfCongesFormView";

export const CongesFormView = {
  ...formView,
  Controller: CongesFormController,
};

registry.category("views").add("pdf_one_demande_de_conges", CongesFormView);