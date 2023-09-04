/** @odoo-module */

import { content_report_pointage_one_salarie } from "./content_report_pointage_one_salarie";
import { portrait_header } from "@reports_templates/js/headers";

export async function content_report_pointage_many_salarie(data) {
  const overlay = document.createElement("div");
  overlay.className = "overlay";

  const spinner = document.createElement("div");
  spinner.id = "spinner";
  spinner.className = "spinner";

  document.body.appendChild(overlay);
  document.body.appendChild(spinner);

  try {
    overlay.style.display = "block";
    spinner.style.display = "block";

    const pageDefinitions = [];

    const pdfMetaData = {
      title: `RAPPORT DES POINTAGES`,
      author: "BIOUI TRAVAUX",
      subject: `RAPPORT POINTAGES`,
      keywords: `Générer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`
    };

    await Promise.all(data.map(async (salarie, index) => {
      const pdfContent = await content_report_pointage_one_salarie(
        salarie,
        index + 1,
        data.length
      );
      pageDefinitions.push(pdfContent);

      if (index !== data.length - 1) {
        pageDefinitions.push({ text: "", pageBreak: "after" });
      }
    }));

    var combinedDocDefinition = {
      pageMargins: [12, 110, 10, 8],
      info: pdfMetaData,
      header: portrait_header(),
      pageSize: "A4",
      pageOrientation: "portrait",
      content: pageDefinitions,
    };

    const pdfDocGenerator = pdfMake.createPdf(combinedDocDefinition);
    const dataUrl = await pdfDocGenerator.getDataUrl();
    const targetElement = document.querySelector("#iframeContainer");
    targetElement.setAttribute("src", dataUrl);
    showModal();
  } catch (error) {
    console.error("Error:", error);
  } finally {
    overlay.style.display = "none";
    spinner.style.display = "none";
    document.body.removeChild(overlay);
    document.body.removeChild(spinner);
  }

  function showModal() {
    document.querySelector("#iframemodal").style.display = "block";
    document.querySelector("#modalClose").addEventListener('click', () => {
      document.querySelector("#iframemodal").style.display = "none";
      const targetElement = document.querySelector("#iframeContainer");
      targetElement.removeAttribute("src");
    });
  }
}


