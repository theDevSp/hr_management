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
  }

  async printConges(url) {

    var framework = require('web.framework');
    framework.blockUI();
    

    try {

      const res = await this.rpc(`/hr_management/get_conges_details/${url.id}`);
      const data = res[0];

      const content = await content_demande_de_conges(data)

      const pdfDefinition = {
        info: {
          title: `Demande de Congés : ${data.Conges_Employe_Name}`,
          author: "BIOUI TRAVAUX",
          subject: `Demande De Congés`
        },
        pageMargins: [12, 120, 12, 180],
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

      const pdfDocGenerator = pdfMake.createPdf(pdfDefinition);
      const dataUrl = await pdfDocGenerator.getDataUrl();
      const targetElement = document.querySelector("#iframeContainer");
      targetElement.setAttribute("src", dataUrl);
      await this.showModal();
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


CongesFormController.template = "owl.PdfCongesFormView";

export const CongesFormView = {
  ...formView,
  Controller: CongesFormController,
};

registry.category("views").add("pdf_one_demande_de_conges", CongesFormView);