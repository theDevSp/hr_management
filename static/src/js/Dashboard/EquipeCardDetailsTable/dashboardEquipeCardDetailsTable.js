/** @odoo-module */

const { Component } = owl

import { EquipeCardDetailsTableLigne } from "./EquipeCardTableLigne/dashboardEquipeTableLigne"

export class EquipeCardDetailsTable extends Component {}

EquipeCardDetailsTable.template = "owl.EquipeCardDetailsTable"
EquipeCardDetailsTable.components = {EquipeCardDetailsTableLigne}