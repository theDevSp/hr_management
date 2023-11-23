/** @odoo-module */

import { Component, useSubEnv, useEffect, useState, useRef } from "@odoo/owl"
import { loadCSS, loadJS } from "@web/core/assets";
const { onWillStart, onMounted, onWillUnmount } = owl;

import { useService } from "@web/core/utils/hooks";


export class EquipeCardDetailsTableLigne extends Component {

    setup() {
        this.actionService = useService("action")
        this.orm = useService("orm")
    }

    check(id) {
        alert('this is is check function')
    }

    times(id) {
        alert('this is is times function')
    }

    async goToFiche(id) {

        const baseURL = await this.orm.searchRead(
            'ir.config_parameter',
            [
                ['key', '=', 'web.base.url']
            ],
            ['value'],
        );

        console.log(baseURL)

        this.actionService.doAction({ 
            type: "ir.actions.act_url", 
            url: `${baseURL[0].value}/web#id=${id}&model=hr.payslip&view_type=form` });
        /*this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Action Service',
            target: 'new',
            res_id: id,
            res_model: 'hr.payslip',
            views: [[false, 'form']],
            context: {
                'dialog_size': 'large',
            }
        });*/
    }
}

EquipeCardDetailsTableLigne.template = "owl.EquipeCardDetailsTableLigne"