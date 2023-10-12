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
    this.notification = this.env.services.notification;
  }

  async print(url) {

    var framework = require('web.framework');
    framework.blockUI();

    try {

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
        pageMargins: [12, 110, 12, 27],
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
        header: portrait_header(),
        pageSize: "A4",
        pageOrientation: "portrait",
        content: data.typeEmployee === 's' ?
          await content_report_pointage_one_salarie(data) :
          await content_report_pointage_one_ouvrier(data),
        footer: function (currentPage, pageCount) {
          return [
            {
              margin: [0, 5, 0, 0],
              columns: [{
                text: `${currentPage}/${pageCount}`,
                alignment: 'center',
                fontSize: 7,
                margin: [150, 0, 0, 0]
              }, {
                text: `Imprimé le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
                fontSize: 7,
                alignment: 'right',
                bold: true,
                margin: [0, 0, 13, 0],
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
      console.log(error);
      framework.unblockUI();
      this.showNotification("Erreur d'impression ! Merci de réessayer !", "danger");
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
      title: "Notification Service",
      type: typeNotification, // info, warning, danger, success
    });
  }
}

PointageFormController.template = "owl.ReportPointageFormView";

export const PointageFormView = {
  ...formView,
  Controller: PointageFormController,
};

registry.category("views").add("report_pointage_one_salarie", PointageFormView);
