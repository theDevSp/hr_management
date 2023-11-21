/** @odoo-module */

const { Component } = owl

export class EquipeCardDetailsTableLigne extends Component {
    setup(){
        console.log('table ligne',this.props.lignes)
        this.props.lignes.map(e => console.log)
    }
    
}

EquipeCardDetailsTableLigne.template = "owl.EquipeCardDetailsTableLigne"