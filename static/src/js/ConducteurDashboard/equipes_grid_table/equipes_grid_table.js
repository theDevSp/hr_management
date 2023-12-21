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
                if (this.props) {
                    this.state.data = this.props.data;
                    this.state.id = this.props.id;
                    this.state.type = this.props.type;
                    this.id = `${this.props.type}${this.props.id}`;
                    this.gridTable = document.getElementById(this.id);
                    this.doTable();
                }

            },
            () => [this.props]
        )

        onWillUnmount(() => {
            if (this.grid) {
                this.grid.destroy()
            }
        })

        onMounted(() => {
            this.id = `${this.props.type}${this.props.id}`;
            this.gridTable = document.getElementById(this.id);
            if (this.props) {
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
            resizable: true,
            pagination: {
                limit: 7
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
                { name: 'Nom et Prénom', sort: true, },
                { name: 'CIN', sort: false, },
                { name: 'Poste', sort: false },
                { name: 'Total des Heures', sort: false, },
                { name: 'Total À Payer', sort: false },
            ],
            data: [
                ...this.props.data.map(ligne => [
                    ligne.employe_name,
                    ligne.employe_cin.replace(" ", ""),
                    ligne.employe_poste,
                    ligne.employe_total_heure,
                    this.props.format(ligne.employe_total_a_payer)
                ])

            ]
        }).render(this.gridTable);

    }

}

EquipeGridTable.template = "owl.ConducteurEquipeGridTable"