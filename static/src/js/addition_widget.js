/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { getDefaultConfig } from "@web/views/view"
import { Component, useState, onWillStart, useRef, useSubEnv, useEffect, onWillUpdateProps, onRendered } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AdditionField extends Component {
    setup() {

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        })

        this.state = useState({
            fiche_id: 0,
            employee_id: 0,
            period_id: 0,
            quinzaine: '',
            parent_state: '',
            prime_list: [],
            prime_per_day_list: [],
            is_cal: false
        })
        this.orm = useService("orm")
        this.jourInput = useRef("jour-input")
        this.model = "hr.payslip"
        this.prime_model = "hr.prime"
        this.payement_model = "hr.paiement.ligne"
        this.addition_model = "days.per.addition"
        this.rpc = this.env.services.rpc


        onWillStart(async () => {
            await this.get_prime(this.props.record.data.quinzaine, this.props.record.data.employee_id[0], this.props.record.data.period_id[0], this.props.record.data.id)

        })
        onWillUpdateProps(async (nextProps) => {
            this.get_prime(nextProps.record.data.quinzaine, nextProps.record.data.employee_id[0], nextProps.record.data.period_id[0], nextProps.record.data.id)
            
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

    async get_prime(quinzaine, employee_id, period_id, fiche) {
        const prime_per_day_list = []
        const prime_list = []
        const res = []
        if (quinzaine != 'quinzaine1' & employee_id & period_id) {
            const result = await this.rpc("/hr_management/get_line_paiement/" + employee_id + "/" + period_id)
            result['result'].forEach((element) => {
                if (element.prime.pay_rate === 'j')
                    prime_per_day_list.push(element)
                else
                    prime_list.push(element)
            });

            (async () => {
                prime_list.forEach(element => {
                    res.push(element)
                });
                (await this.get_prime_per_day_list(prime_per_day_list, fiche)).forEach(element => {
                    res.push(element)
                });
                this.state.prime_list = res
            })()
        } else {
            this.state.prime_list = []
        }

    }

    async get_prime_per_day_list(object, fiche) {
        const ids = []
        object.forEach((element) => {
            ids.push(element.prime_id)
        });
        const res = await this.orm.searchRead(this.addition_model, [['prime_id', 'in', ids], ['payroll_id', '=', fiche]], ["prime_id", "jour_prime", "is_cal"])
        object.forEach((element) => {
            res.forEach(days => {
                if (element.prime_id == days.prime_id[0])
                    element.nbr_days = days.jour_prime
                element.is_cal = days.is_cal
            });
        });
        return object
    }

    async valide(prime) {
        const prime_days = document.getElementById('prime-' + prime.prime_id).value
        const res = await this.orm.searchRead(this.addition_model, [['prime_id', '=', prime.prime_id], ['payroll_id', '=', this.props.record.data.id]], ["is_cal"])

        if (_.isEmpty(res))
            await this.orm.create(this.addition_model, [{
                'prime_id': prime.prime_id,
                'payroll_id': this.props.record.data.id,
                'jour_prime': prime_days
            }])
        else
            res.forEach(async element => {
                await this.orm.write(this.addition_model, [element.id], { jour_prime: prime_days })
            })

        await this.get_prime(this.props.record.data.quinzaine, this.props.record.data.employee_id[0], this.props.record.data.period_id[0], this.props.record.data.id)
    }

    get_state_back_color(key) {
        const background = {
            "Non Payé": "bg-danger",
            "Payé": "bg-success",
            "Annulé": "bg-dark",
            "Décalé": "bg-warning",
        }
        return background[key]
    }

    async update_payement(prime) {
        const action = this.env.services.action
        action.doAction({
            type: "ir.actions.act_window",
            name: ("Décaler le paiement de : \"" + prime.prime.label + "  " + prime.period + "\""),
            res_model: "wizard_reporter_dates",
            domain: [],
            context: {
                'line_id': prime.payement_id,
                'current_model': "prime"
            },
            views: [
                [false, "form"],
            ],
            view_type: 'form',
            view_mode: 'form',
            target: "new"
        })
        if (call)
            await this.get_prime(this.props.record.data.quinzaine, this.props.record.data.employee_id[0], this.props.record.data.period_id[0], this.props.record.data.id)
    }

    async calculateSum() {
        let sum = 0;
        if (!this.props.record.data.cal_state)
            this.state.prime_list.forEach(element => {
                if (element.prime.pay_rate === 'm')
                    sum += element.amount
                else
                    sum += (element.amount * element.nbr_days)
            });

        await this.props.update(sum)
    }
}

AdditionField.template = "hr_management.AdditionField";
AdditionField.props = {
    ...standardFieldProps,
};

AdditionField.supportedTypes = ["float"];

registry.category("fields").add("addition_payement", AdditionField);