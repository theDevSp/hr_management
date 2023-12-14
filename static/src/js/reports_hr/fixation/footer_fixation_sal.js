/** @odoo-module */

export function footer_fixation_sal(currentPage, pageCount) {
    return [

        {
            margin: [12, 5, 12, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: ['*', 10, '*', 10, '*'],
                headerRows: 1,
                body: [
                    [{
                        text: 'SERVICE RH',
                        bold: true,
                        fontSize: 10,
                        alignment: 'center',
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5]
                    },
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: 'CONTRÔLE DE GESTION',
                        fontSize: 10,
                        bold: true,
                        alignment: 'center',
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5]
                    },
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: 'RECRUTEUR',
                        fontSize: 10,
                        bold: true,
                        alignment: 'center',
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5]
                    }],
                    [{
                        text: '',
                        margin: [0, 35]
                    }, 
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: ''
                    },
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: ''
                    }]
                ]
            }
        },
        {
            margin: [12, 5, 12, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: ['*', 10, '*'],
                headerRows: 1,
                body: [
                    [{
                        text: 'DIRECTEUR ADMINISTRATIF',
                        bold: true,
                        fontSize: 10,
                        alignment: 'center',
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5]
                    },
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: 'M. LE PDG',
                        fontSize: 10,
                        bold: true,
                        alignment: 'center',
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5]
                    }],
                    [{
                        text: '',
                        margin: [0, 35]
                    }, 
                    {
                        text: '',
                        border:[0]
                    },
                    {
                        text: ''
                    }]
                ]
            }
        },

        {
            margin: [0, 5, 0, 0],
            columns: [{
                text: `${currentPage}/${pageCount}`,
                alignment: 'center',
                fontSize: 7,
                margin: [150, 0, 0, 0]
            }, {
                text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
                fontSize: 7,
                alignment: 'right',
                bold: true,
                margin: [0, 0, 12, 0],
                width: 130
            }]
        }

    ]
}