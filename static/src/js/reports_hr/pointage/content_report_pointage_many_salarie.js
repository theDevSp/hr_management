/** @odoo-module */

import { content_report_pointage_one_salarie } from "./content_report_pointage_one_salarie";
import { portrait_header } from "@reports_templates/js/headers";

export async function content_report_pointage_many_salarie(data) {
  const overlay = createOverlay();
  const spinner = createSpinner();

  try {
    showLoading(overlay, spinner);

    const pageDefinitions = await generatePageDefinitions(data);

    const combinedDocDefinition = {
      pageMargins: [12, 110, 10, 8],
      info: createPdfMetaData(),
      header: portrait_header(),
      pageSize: "A4",
      pageOrientation: "portrait",
      content: pageDefinitions,
    };

    const dataUrl = await generatePdfDataUrl(combinedDocDefinition);
    displayPdfInModal(dataUrl);
  } catch (error) {
    console.error("Error:", error);
  } finally {
    hideLoading(overlay, spinner);
  }

  function createOverlay() {
    const overlay = document.createElement("div");
    overlay.className = "overlay";
    document.body.appendChild(overlay);
    return overlay;
  }

  function createSpinner() {
    const spinner = document.createElement("div");
    spinner.id = "spinner";
    spinner.className = "spinner";
    document.body.appendChild(spinner);
    return spinner;
  }

  function createPdfMetaData() {
    return {
      title: `RAPPORT DES POINTAGES`,
      author: "BIOUI TRAVAUX",
      subject: `RAPPORT POINTAGES`,
      keywords: `Générer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`
    };
  }

  async function generatePageDefinitions(data) {
    const pageDefinitions = [];
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
    return pageDefinitions;
  }

  async function generatePdfDataUrl(combinedDocDefinition) {
    const pdfDocGenerator = pdfMake.createPdf(combinedDocDefinition);
    return await pdfDocGenerator.getDataUrl();
  }

  function displayPdfInModal(dataUrl) {
    const targetElement = document.querySelector("#iframeContainer");
    targetElement.setAttribute("src", dataUrl);
    showModal();
  }

  function showModal() {
    document.querySelector("#iframemodal").style.display = "block";
    document.querySelector("#modalClose").addEventListener('click', () => {
      document.querySelector("#iframemodal").style.display = "none";
      const targetElement = document.querySelector("#iframeContainer");
      targetElement.removeAttribute("src");
    });
  }

  function showLoading(overlay, spinner) {
    overlay.style.display = "block";
    spinner.style.display = "block";
  }

  function hideLoading(overlay, spinner) {
    overlay.style.display = "none";
    spinner.style.display = "none";
    document.body.removeChild(overlay);
    document.body.removeChild(spinner);
  }
}



