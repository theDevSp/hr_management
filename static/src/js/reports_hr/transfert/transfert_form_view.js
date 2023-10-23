/** @odoo-module */

import { registry } from "@web/core/registry"
import { formView } from "@web/views/form/form_view"
import { FormController } from "@web/views/form/form_controller"
import { useService } from "@web/core/utils/hooks"

class transfertFormController extends FormController {
    setup(){
        super.setup()
        console.log("This is transfert form controller")
        this.action = useService("action")
    }
}

transfertFormController.template = "owl.transfertFormView"

export const transfertFormView = {
    ...formView,
    Controller: transfertFormController,
}

registry.category("views").add("transfert_form_view", transfertFormView)