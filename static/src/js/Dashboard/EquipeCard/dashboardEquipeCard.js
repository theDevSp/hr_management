/** @odoo-module */

const { Component } = owl

import { EquipeCardDetails } from "../EquipeCardDetails/dashboardEquipeCardDetails"
import { EquipeCardDetailsTable } from "../EquipeCardDetailsTable/dashboardEquipeCardDetailsTable"

export class EquipeCard extends Component {}

EquipeCard.template = "owl.EquipeCard"
EquipeCard.components = {EquipeCardDetails,EquipeCardDetailsTable}