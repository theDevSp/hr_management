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
        this.orm = useService("orm")
        this.payement_model = "hr.paiement.prelevement"

        onWillStart(async ()=>{
            await this.get_prelevement(this.props.record.data.quinzaine,this.props.record.data.employee_id[0],this.props.record.data.period_id[0])
        })
        onWillUpdateProps(async (nextProps) => {
            this.get_prelevement(nextProps.record.data.quinzaine,nextProps.record.data.employee_id[0],nextProps.record.data.period_id[0])
        });

        useEffect(
            () => {

                this.state.fiche_id = this.props.record.data.fiche_id
                this.state.employee_id = this.props.record.data.employee_id
                this.state.period_id = this.props.record.data.period_id
                this.state.quinzaine = this.props.record.data.quinzaine
                this.state.parent_state = this.props.record.data.state
                
            }
        )
    }
    
    async get_prelevement(quinzaine,employee_id,period_id){
        const prelevement_list = []
        const res = []
        try {
            if (employee_id & period_id){
                const result = await this.rpc("/hr_management/get_line_prelevement/"+employee_id+"/"+period_id)
                result['result'].forEach((element) => {
                    prelevement_list.push(element)
                });
                this.state.prelevement_list = prelevement_list
            }else{
                this.state.prelevement_list = []
            }
            return true
        } catch (error) {
            return false
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

    async update_payement(prelevement) {
        const action = this.env.services.action
        action.doAction({
            type: "ir.actions.act_window",
            name: ("Décaler le paiement de : \"" + prelevement.label + "  " + prelevement.period + "\""),
            res_model: "wizard_reporter_dates",
            domain: [],
            context: {
                'line_id': prelevement.payement_id,
                'current_model': "prelevement"
            },
            views: [
                [false, "form"],
            ],
            view_type: 'form',
            view_mode: 'form',
            target: "new"
        })
    }

    async save_note(prelevement){
        const prelevement_note = document.getElementById('note-prelevement-' + prelevement.prelevement_id).value
        await this.orm.write(this.payement_model, [prelevement.payement_id], { observations: prelevement_note })
        
        this.get_prelevement(this.props.record.data.quinzaine,
                this.props.record.data.employee_id[0],
                this.props.record.data.period_id[0]).then((res) => {
            $('#modal-prelevement-' + prelevement.prelevement_id).modal('hide')
            this.showNotification(res) 
        })
    }

    async postepone_action(prelevement){
        const prime_note = document.getElementById('note-prelevement-' + prelevement.prelevement_id).value
        this.rpc('/hr_management/reporter_prelevement/'+prelevement.payement_id+'/'+prime_note).then((res) => {
            if (res.code == 200) {
                this.get_prelevement(this.props.record.data.quinzaine,
                    this.props.record.data.employee_id[0],
                    this.props.record.data.period_id[0],
                    this.props.record.data.id).then((res) => {
                        $('#modal-prelevement-' + prelevement.prelevement_id).modal('hide')
                        this.showNotification(res) 
                    })
            } else {
                this.showNotification(false)
            }
        })
    }

    async cancel_postepone_action(prelevement){
        const prime_note = document.getElementById('note-prelevement-' + prelevement.prelevement_id).value
        this.rpc('/hr_management/cancel_prelevement_gap/'+prelevement.payement_id).then((res) => {
            
            if (res.code == 200) {
                this.get_prelevement(this.props.record.data.quinzaine,
                    this.props.record.data.employee_id[0],
                    this.props.record.data.period_id[0],
                    this.props.record.data.id).then((res) => {
                        $('#modal-prelevement-' + prelevement.prelevement_id).modal('hide')
                        this.showNotification(res) 
                    })
            } else {
                this.showNotification(false,res.code == 303 ? res.msg : false)
            }
        })
    }

    showNotification(result,message="Une erreur est roncontrer durant le traitement veuillez réessayer plustard"){
        const notification = this.env.services.notification
        let msg = ""
        let type = "" 
        result ? msg = "Action réusii" : message
        result ? type = "success" : "danger"
        
        notification.add(msg, {
            title: "Notification",
            type: type, //info, warning, danger, success
            sticky: false,
            className: "p-4",
            buttons: [
                /*{
                    name: "Notification Action",
                    onClick: ()=>{
                        console.log("This is notification action")
                    },
                    primary: true,
                },
                {
                    name: "Show me again",
                    onClick: ()=>{
                        this.showNotification()
                    },
                    primary: false,
                }*/
            ]
        })
    }

    async calculateSum() {
        let sum = 0;
        this.state.period_id.forEach(element => {
            sum += element.amount
        });
        let value = sum 
        await this.props.update(value)
    }

    access_record(prelevement){
        const action = this.env.services.action
        action.doAction({
            type: "ir.actions.act_window",
            name: "Action Service",
            res_model: "hr.prelevement",
            res_id:prelevement.prelevement_id,
            domain:[],
            views:[
                [false, "form"]
            ],
            view_mode:"form",
            target: "current"
        })
    }
}


DeductionField.template = "hr_management.DeductionField";
DeductionField.props = {
    ...standardFieldProps,
};

DeductionField.supportedTypes = ["float"];

registry.category("fields").add("deduction_payement", DeductionField);