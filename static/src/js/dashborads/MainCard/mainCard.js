/** @odoo-module */

import { SousCard } from "../SousCard/sousCards"
import { TableCard } from "../TableCard/tableCard"

const { Component } = owl

export class MainCard extends Component {}

MainCard.template = "owl.MainCard"
MainCard.components = {SousCard,TableCard}