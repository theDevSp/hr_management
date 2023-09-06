/** @odoo-module */

export function content_report_pointage_one_ouvrier(data, pageNumber, totalPages) {

    const pdfInformation = [
        [

            {
                rowSpan: 3,
                text: [
                    'RAPPORT POINTAGE N°:\n',
                    {
                        text: data.report_num,
                        bold: true,
                        fontSize: 12,

                    }
                ],
                alignment: 'center',
                color: 'white',
                border: [true, true, true, true],
                fillColor: '#04aa6d',
                margin: [0, 10, 0, 0],
                fontSize: 10
            },
            {
                text: ''
            },
            {
                text: 'Nom et Prénom:',
                margin: [30, 8, 0, 0],
                border: [1, true, false, false],
                fontSize: 8,
                fillColor: "#f1f2f3"

            },
            {
                text: data.nometpnom,
                border: [false, true, 1, false],
                margin: [0, 8, 0, 0],
                bold: true,
                fontSize: 9,
                fillColor: "#f1f2f3"
            }
        ],
        ['', {
            text: ''
        },
            {
                text: 'CIN:',
                margin: [30, 0, 0, 0],
                border: [1, false, false, false],
                fontSize: 8,
                fillColor: "#f1f2f3"
            },
            {
                text: data.cin,
                border: [false, false, 1, false],
                bold: true,
                fontSize: 9,
                fillColor: "#f1f2f3"
            }
        ],
        ['', {
            text: ''
        }, {
                text: 'Fonction:',
                margin: [30, 0, 0, 0],
                border: [1, false, false, false],
                fontSize: 8,
                fillColor: "#f1f2f3"
            },
            {
                text: data.fonction,
                border: [false, false, 1, false],
                bold: true,
                fontSize: 9,
                fillColor: "#f1f2f3"
            }
        ],
        [{
            rowSpan: 3,
            text: [
                'MOIS: ',
                {
                    text: data.month,
                    bold: true,
                    fontSize: 12
                }
            ],
            alignment: 'center',
            border: [true, true, true, true],
            margin: [0, 18, 0, 0],
            fontSize: 11
        },
        {
            text: ''
        },
        {
            text: 'Dernier Chantier:',
            border: [1, false, false, false],
            margin: [30, 0, 0, 0],
            fontSize: 8,
            fillColor: "#f1f2f3"
        },
        {
            text: data.dChantier,
            border: [false, false, 1, false],
            bold: true,
            fontSize: 9,
            fillColor: "#f1f2f3"
        }
        ],
        ['', {
            text: ''
        }, {
                text: 'Dernière Equipe:',
                border: [1, false, false, false],
                margin: [30, 0, 0, 0],
                fontSize: 8,
                fillColor: "#f1f2f3"

            },
            {
                text: data.dEquipe,
                border: [false, false, 1, false],
                bold: true,
                fontSize: 9,
                fillColor: "#f1f2f3"
            }
        ],
        ['', {
            text: ''
        }, {
                text: 'Dernier Engin:',
                margin: [30, 0, 0, 8],
                border: [1, false, false, 1],
                fontSize: 8,
                fillColor: "#f1f2f3"

            },
            {
                text: data.dEngin,
                border: [false, false, 1, 1],
                bold: true,
                fontSize: 9,
                margin: [0, 0, 0, 8],
                fillColor: "#f1f2f3"
            }
        ]]

    const tableHeader = [{
        text: 'Jours',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    },
    {
        text: 'TH',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    },
    {
        text: 'Observation',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    },
    {
        text: 'Code',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    },
    {
        text: 'Equipe',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    },
    {
        text: 'Chantier',
        bold: true,
        alignment: 'center',
        fillColor: '#04aa6d',
        color: 'white',
        fontSize: 9
    }
    ]

    const tableRow = data.dates.map(obj => {
        const back = obj.jour.includes('Dim') ? '#dddddd' : null
        const row = [
            {
                text: obj.jour,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: obj.th,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: obj.observation,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: obj.chantier,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: obj.code,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: obj.equipe,
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            }
        ];

        return row;
    });

    const footerTable = {
        margin: [0, 20, 2, 0],
        layout: {
            hLineColor: 'gray',
            vLineColor: 'gray'
        },
        table: {
            widths: [100, '*', '*', '*'],
            heights: [10, 85],
            headerRows: 1,
            body: [
                [{
                    text: 'Total Heures',
                    bold: true,
                    fontSize: 10,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                },
                {
                    text: 'Visa Responsable',
                    fontSize: 9,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                },
                {
                    text: 'Visa Conducteur / Chef Chantier',
                    fontSize: 9,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                },
                {
                    text: 'Visa Pointeur',
                    fontSize: 9,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                },
                ],
                [{
                    text: data.totalheure,
                    fontSize: 19,
                    bold: true,
                    alignment: 'center',
                    margin: [0, 30],
                    //padding: [0, 20]conso
                },
                {
                    text: '',
                    fontSize: 9,
                    bold: true
                },
                {
                    text: '',
                    fontSize: 9,
                    bold: true
                },
                {
                    text: '',
                    fontSize: 9,
                    bold: true
                }
                ]
            ]
        }
    }

    const def = {

        content: [{
            table: {
                widths: [150, 0, 90, 293],
                body: pdfInformation
            },
            layout: {
                defaultBorder: false,
                hLineColor: 'gray',
                vLineColor: 'gray'
            }
        },

        {
            margin: [0, 15, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [26, 15, 330, 35, 44, 65],
                body: [
                    tableHeader,
                    ...tableRow.map((array) => array)
                ]
            }
        },

        footerTable,
        {
            alignment: 'justify',
            margin: [10, 185],
                columns: [
                {
                    text: `Page ${pageNumber} of ${totalPages}`,
                    fontSize: 7,
                    alignment: 'right',
                    bold: true,
                    margin: [0, 2, 2, 0]
                },
                {
                    text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
                    fontSize: 7,
                    margin: [0, 2, 2, 0],
                    alignment: 'right',
                    bold: true,
                }
            ]
        }


        ]
    }

    return def.content
}