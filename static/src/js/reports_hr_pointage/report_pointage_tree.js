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

    this.notification = useService("notification")
  }

  async print(url) {

    const reportIds = [];

    this.model.root.selection.map((rec) => {
      reportIds.push(rec.resId);
    });

    if (reportIds.length === 0) {
      console.error("Error in selection");
    } else {
      const data = await this.getData(reportIds);
      data === null ? "" : this.getPDF(data);
    }
  }

  async getData(ids) {
    const data = await Promise.all(
      ids.map(async (id) => {
        const res = await this.rpc(
          "/hr_management/get_report_pointage_salarie_ouvrier/" + id
        );
        return res ? res : null;
      })
    );
    return data
  }

  getPDF(data) {
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
      this.notification.add("Merci de sélectionner un seul type d'employé (Salarié).", {
        title: "Erreur de sélection multiple !",
        type: "danger",
        sticky: true,
      });
    }
    else if (ouv.length > 0) {
      this.notification.add("Merci de sélectionner uniquement le type d'employé (salarié).", {
        title: "Erreur de sélection multiple !",
        type: "warning",
        sticky: true,
      });
    }
    else if (sal.length > 0) {
      return content_report_pointage_many_salarie(sal);

    }
  }
}

export const PointageListView = {
  ...listView,
  Controller: PointageListController,
  buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_pointage_list", PointageListView);
