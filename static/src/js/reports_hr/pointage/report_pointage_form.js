/** @odoo-module */
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import { content_report_pointage_one_salarie } from "./content_report_pointage_one_salarie";
import { content_report_pointage_one_ouvrier } from "./content_report_pointage_one_ouvrier";
import { useService } from "@web/core/utils/hooks";
import { portrait_header } from "@reports_templates/js/headers";

class PointageFormController extends FormController {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.overlay = document.createElement("div");
    this.spinner = document.createElement("div");
    this.overlay.className = "overlay";
    this.spinner.id = "spinner";
    this.spinner.className = "spinner";
  }

  async print(url) {
    try {
      this.showOverlayAndSpinner();

      const res = await this.rpc(`/hr_management/get_report_pointage_salarie_ouvrier/${this.model.root.data.id}`);
      const data = res[0];
      const len = res.length;

      const pdfMetaData = {
        title: `RAPPORT POINTAGE N°: ${data.report_num}-${data.cin}-${data.nometpnom}-${data.month}`,
        author: "BIOUI TRAVAUX",
        subject: `RAPPORT POINTAGE N°: ${data.report_num}`,
        fileName: `RAPPORT POINTAGE N°: ${data.report_num}`,
      };

      const pdfDefinition = {
        info: pdfMetaData,
        pageMargins: [12, 115, 10, 8],
        header: portrait_header(),
        pageSize: "A4",
        pageOrientation: "portrait",
        content: data.typeEmployee === 's' ?
          content_report_pointage_one_salarie(data, len, len) :
          content_report_pointage_one_ouvrier(data, len, len),
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

PointageFormController.template = "owl.ReportPointageFormView";

export const PointageFormView = {
  ...formView,
  Controller: PointageFormController,
};

registry.category("views").add("report_pointage_one_salarie", PointageFormView);
