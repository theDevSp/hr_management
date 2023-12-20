/** @odoo-module */

const { Component, onMounted, useState, useEffect, onWillUnmount } = owl

export class EquipeGridTable extends Component {
    setup() {

        this.state = useState({
            data: this.props.data,
            type: this.props.type,
            id: this.props.id
        })

        useEffect(
            () => {
                if (this.props.id && this.props.type && this.props.data) {
                    this.state.data = this.props.data;
                    this.state.id = this.props.id;
                    this.state.type = this.props.type;
                    this.id = `${this.props.type}${this.props.id}`;
                    this.gridTable = document.getElementById(this.id);
                    this.doTable();
                }

            },
            () => [this.props.id, this.props.type, this.props.data]
        )

        onWillUnmount(() => {
            if (this.grid) {
                this.grid.destroy()
            }
        })

        onMounted(() => {
            this.id = `${this.props.type}${this.props.id}`;
            this.gridTable = document.getElementById(this.id);
            if (this.props.id && this.props.type && this.props.data) {
                this.doTable();
            }
        })


    }

    doTable() {

        if (this.grid) {
            this.grid.destroy()
        }

        if (this.gridTable) {
            this.gridTable.innerHTML = ''
        }

        this.grid = new gridjs.Grid({
            sort: true,
            pagination: {
                limit: 3
            },
            language: {
                'search': {
                    'placeholder': 'Recherche...'
                },
                'pagination': {
                    'previous': 'Précédent',
                    'next': 'Suivant',
                    'showing': 'Affichage de',
                    'results': () => 'enregistrements'
                }
            },
            style: {
                container: {
                    border: '2px solid rgb(0,145,132,0.2)',
                    'border-radius': '16px 16px'
                },
                th: {
                    'background-color': 'rgb(0,145,132,0.1)',
                    'font-weight': 'bold'
                },
                td: {
                }
            },
            columns: [
                { name: 'Nom et Prénom', sort: true, width: '25%' },
                { name: 'CIN', sort: true, width: '15%' },
                { name: 'Poste', sort: true },
                { name: 'Total des Heures', sort: false, width: '10%' },
                { name: 'Total À Payer', sort: false },
            ],
            data: [
                ...this.props.data.map(ligne => [
                    ligne.employe_name,
                    ligne.employe_cin.replace(" ", ""),
                    ligne.employe_poste,
                    ligne.employe_total_heure,
                    ligne.employe_total_a_payer.toFixed(2)
                ])

            ]
        }).render(this.gridTable);

    }

}

EquipeGridTable.template = "owl.ConducteurEquipeGridTable"