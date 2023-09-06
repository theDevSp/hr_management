/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

import { content_report_pointage_many_salarie } from "./content_report_pointage_many_salarie";

class PointageListController extends ListController {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    this.overlay = document.createElement("div");
    this.spinner = document.createElement("div");
    this.overlay.className = "overlay";
    this.spinner.id = "spinner";
    this.spinner.className = "spinner";
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


export const PointageListView = {
  ...listView,
  Controller: PointageListController,
  buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_pointage_list", PointageListView);
