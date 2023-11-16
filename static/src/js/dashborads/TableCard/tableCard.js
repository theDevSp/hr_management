/** @odoo-module */

const { Component } = owl

import { Tableligne } from "./TableLigne/tableLigne"

export class TableCard extends Component {}

TableCard.template = "owl.TableCard"
TableCard.components = {Tableligne}