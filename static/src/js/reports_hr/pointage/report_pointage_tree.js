/** @odoo-module */

/*
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";


const { onWillStart, useRef } = owl

class PointageListController extends ListController {
  setup() {
    super.setup();

  }

  getActionService(){
    const action = this.env.services.action
    action.doAction({
        type: "ir.actions.act_window",
        name: "Action Service",
        res_model: "res.partner",
        domain:[],
        context:{search_default_type_company: 1},
        views:[
            [false, "list"],
            [false, "form"],
            [false, "kanban"],
        ],
        view_mode:"list,form,kanban",
        target: "current"
    })
}

}

export const PointageListView = {
  ...listView,
  Controller: PointageListController,
  buttonTemplate: "owl.hrPointageListView.Buttons",
};

registry.category("views").add("report_pointage_list", PointageListView);
*/