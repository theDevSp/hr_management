/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { getDefaultConfig } from "@web/views/view"
import { Component, useState, onWillStart, useRef, useSubEnv, useEffect,onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DeductionField extends Component {
    setup() {
        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        })

        this.state = useState({

            employee_id:0,
            period_id:0,
            quinzaine:'',
            parent_state:'',
            prelevement_list:[],
        })
        this.rpc = this.env.services.rpc

        onWillStart(async ()=>{
            await this.get_prelevement(this.props.record.data.quinzaine,this.props.record.data.employee_id[0],this.props.record.data.period_id[0])
        })
        onWillUpdateProps(async (nextProps) => {
            this.get_prelevement(nextProps.record.data.quinzaine,nextProps.record.data.employee_id[0],nextProps.record.data.period_id[0])
        });
    }
    
    async get_prelevement(quinzaine,employee_id,period_id){
        const prelevement_list = []
        const res = []
        if (quinzaine != 'quinzaine1' & employee_id & period_id){
            const result = await this.rpc("/hr_management/get_line_prelevement/"+employee_id+"/"+period_id)
            result['result'].forEach((element) => {
                prelevement_list.push(element)
            });
            

            this.state.prelevement_list = prelevement_list

        }else{
            this.state.prelevement_list = []
        }
    }

    get_state_back_color(key){
        const background = {
            "Non Payé" : "bg-danger",
            "Payé" : "bg-success",
            "Annulé" : "bg-dark",
            "Décalé" : "bg-warning",
        }
        return background[key]
    }

    async calculateSum() {
        let sum = 0;
        this.state.period_id.forEach(element => {
            sum += element.amount
        });
        let value = sum 
        await this.props.update(value)
    }
}


DeductionField.template = "hr_management.DeductionField";
DeductionField.props = {
    ...standardFieldProps,
};

DeductionField.supportedTypes = ["float"];

registry.category("fields").add("deduction_payement", DeductionField);