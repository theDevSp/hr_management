/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

const { loadJS, loadCSS } = require('@web/core/assets');

const { onWillStart, useRef } = owl



import { content_report_pointage_many_salarie } from "./content_report_pointage_many_salarie";

class PointageListController extends ListController {
  setup() {
    super.setup();

    this.rpc = useService("rpc");
    this.notification = useService("notification");

    this.modal = useRef("modalPrint")
    this.modalClose = useRef("modalClose")

    onWillStart(async () => {
      this.overlay = document.createElement("div");
      this.spinner = document.createElement("div");
      this.overlay.className = "overlay";
      this.spinner.id = "spinner";
      this.spinner.className = "spinner";

      await loadJS("/reports_templates/static/src/lib/selectize/selectize.min.js")
      await loadCSS("/reports_templates/static/src/lib/selectize/selectize.default.min.scss")

      await loadCSS("/reports_templates/static/src/lib/datepicker/datepicker.min.scss")
      await loadJS("/reports_templates/static/src/lib/datepicker/bootstrap-datepicker.min.js")
    })


  }

  async print(url) {
    try {
      this.showOverlayAndSpinner();

      const reportIds = this.model.root.selection.map((rec) => rec.resId);

      if (reportIds.length === 0) {
        console.error("Error in selection");
      } else {
        const data = await this.getData(reportIds);
        this.processData(data);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      this.hideOverlayAndSpinner();
    }
  }

  async modalPrint(data) {
    showModal(this.modal.el);

    const allChantiers = await this.rpc(`/hr_management/pointage/get_all_chantiers`);
    const allEquipes = await this.rpc(`/hr_management/pointage/get_all_Equipes`);

    $("#datepicker").datepicker({
      format: "mm-yyyy",
      startView: "months",
      minViewMode: "months"
    });

    $('#select-chantier').selectize({
      maxItems: 1,
      minItems: 1,
      valueField: 'id',
      labelField: 'name',
      searchField: 'name',
      options: allChantiers,
      create: false
    });

    $('#select-quinzine').selectize({
      maxItems: 1,
      minItems: 1,
      valueField: 'id',
      labelField: 'title',
      searchField: 'title',
      options: [],
      create: false
    });

    $('#select-type').selectize({
      maxItems: 1,
      minItems: 1,
      valueField: 'id',
      labelField: 'title',
      searchField: 'title',
      options: [
        { id: 'o', title: 'Ouvrier' },
        { id: 's', title: 'Salarié' },
      ],
      create: false,
      onChange: (selectedValue) => {
        const selectQuinzine = $('#select-quinzine')[0].selectize;

        if (selectedValue === 'o') {

          selectQuinzine.clearOptions();

          const existingOption = selectQuinzine.options['q12'];
          if (existingOption) {
            delete selectQuinzine.options['q12'];
          }

          selectQuinzine.addOption([
            { id: 'q1', title: 'Quinzaine1' },
            { id: 'q2', title: 'Quinzaine2' }
          ]);
          selectQuinzine.refreshOptions();
          selectQuinzine.clear();
          selectQuinzine.enable();
        } else if (selectedValue === 's') {

          selectQuinzine.clearOptions();
          selectQuinzine.addOption([
            { id: 'q12', title: 'Quinzaine12' },
          ]);
          selectQuinzine.refreshOptions();
          selectQuinzine.clear();
          selectQuinzine.setValue('q12');
          selectQuinzine.disable();
        }
      }
    });

    $('#select-equipe').selectize({
      maxItems: 1,
      minItems: 1,
      valueField: 'id',
      labelField: 'name',
      searchField: 'name',
      options: allEquipes,
      create: false
    });

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

  async getData(ids) {
    const data = await Promise.all(
      ids.map(async (id) => {
        const res = await this.rpc(`/hr_management/get_report_pointage_salarie_ouvrier/${id}`);
        return res ? res : null;
      })
    );
    return data.filter((item) => item !== null);
  }

  processData(data) {
    const sal = [];
    const ouv = [];

    data.forEach((subArray) => {
      subArray.forEach((arr) => {
        if (arr.typeEmployee === "s") {
          sal.push(arr);
        } else if (arr.typeEmployee === "o") {
          ouv.push(arr);
        }
      });
    });

    if (sal.length > 0 && ouv.length > 0) {
      this.showNotification("Merci de sélectionner un seul type d'employé (Salarié).", "Erreur de sélection multiple !", "danger");
    } else if (ouv.length > 0) {
      this.showNotification("Merci de sélectionner uniquement le type d'employé (salarié).", "Erreur de sélection multiple !", "warning");
    } else if (sal.length > 0) {
      return content_report_pointage_many_salarie(sal);
    }
  }

  showNotification(message, title, type) {
    this.notification.add(message, {
      title,
      type,
      sticky: true,
    });
  }
}

const showModal = (el) => {
  el.style.display = "block"
  const modalClose1 = document.querySelector("#modalClose1");
  const modalClose2 = document.querySelector("#modalClose2");
  modalClose1.addEventListener('click', () => {
    el.style.display = "none";
  });
  modalClose2.addEventListener('click', () => {
    el.style.display = "none";
  });
}


export const PointageListView = {
  ...listView,
  Controller: PointageListController,
  buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_pointage_list", PointageListView);
