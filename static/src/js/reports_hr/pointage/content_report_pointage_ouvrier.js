/** @odoo-module */

export async function content_report_pointage_ouvrier(data, chantier, quinz, period, nbr) {

    const data_header = {
        "period": period,
        "quinzine": quinz,
        "chantier": chantier,
        "equipe": data.equipe,
    }

    const widthTable = [40, 120, 60, ...Array(nbr).fill('*'), 35]

    const headerTable = Array.from({ length: nbr }, (_, index) => ({
        text: ((data_header.quinzine === 'quinzaine1') ? index + 1 : index + 16).toString(),
        bold: true,
        fontSize: 10,
        fillColor: '#04aa6d',
        color: 'white',
        margin: [0, 5],
        alignment: 'center'
    }));

    const linges = [];
    const sup_lignes = [];

    data.data.map(arr => {
        const row = [
            {
                text: arr.employe_cin,
                fontSize: 8,
                color: 'black',
                margin: [0, 3],
                alignment: 'center'
            },
            {
                text: arr.employe_name,
                fontSize: 8,
                color: 'black',
                margin: [0, 3],
                alignment: 'center'
            },
            {
                text: arr.employe_fonction,
                fontSize: 8,
                color: 'black',
                margin: [0, 3],
                alignment: 'center'
            },
            ...arr.employe_dates.dates_lines.map(ligne => {
                if (ligne.sup > 0.0) {
                    sup_lignes.push([
                        {
                            text: ligne.date,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 2],
                            alignment: 'center'
                        },
                        {
                            text: arr.employe_cin,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 1.5],
                            alignment: 'center'
                        },
                        {
                            text: arr.employe_name,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 1.5],
                            alignment: 'center'
                        },
                        {
                            text: arr.employe_fonction,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 1.5],
                            alignment: 'center'
                        },
                        {
                            text: ligne.sup,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 1.5],
                            alignment: 'center'
                        },
                        {
                            text: ligne.observation,
                            fontSize: 8,
                            color: 'black',
                            margin: [0, 1.5],
                            alignment: 'center'
                        },

                    ])
                }
                return {
                    text: ligne.th,
                    fontSize: 8,
                    color: 'black',
                    margin: [0, 3],
                    alignment: 'center'
                }
            }),
            {
                text: arr.employe_totalheure,
                fontSize: 8,
                color: 'black',
                margin: [0, 3],
                alignment: 'center'
            },
        ];

        linges.push(row); // Add the row to the linges array
    });


    const content = [{

        columns: [{
            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [260],
                headerRows: 1,
                body: [
                    [{
                        text: 'Période',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 5],
                        alignment: 'center'
                    }],
                    [{
                        text: data_header.period,
                        fontSize: 14,
                        border: [1, 1, 1, 0],
                        margin: [0, 9.7, 0, 0],
                        bold: true,
                        alignment: 'center'
                    }],
                    [{
                        text: data_header.quinzine,
                        fontSize: 11,
                        border: [1, 0, 1, 1],
                        margin: [2, 6, 0, 7],
                        bold: false,
                        alignment: 'center'
                    }],

                ]
            }
        },

        {
            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [260],
                heights: [0, 52],
                body: [
                    [{
                        text: 'Chantier',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 5],
                        alignment: 'center'
                    }],
                    [{

                        bold: true,
                        text: data_header.chantier,
                        fontSize: 9,
                        alignment: 'center',
                        rowSpan: 2,
                        margin: [0, 15]

                    }],
                    [{
                        text: ''
                    }]
                ],

            }
        },

        {
            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [262],
                heights: [0, 51.3],
                body: [
                    [{
                        text: 'Équipe',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [10, 5.3],
                        alignment: 'center'
                    }],
                    [{
                        text: data_header.equipe,
                        bold: true,

                        fontSize: 9,
                        alignment: 'center',
                        margin: [0, 12],
                        rowSpan: 2

                    }],
                    [{
                        text: '',
                    }]
                ],

            }
        }
        ],

    },

    {

        margin: [0, 8, 0, 0],
        layout: {
            hLineColor: 'gray',
            vLineColor: 'gray'
        },
        table: {

            widths: widthTable,
            headerRows: 1,
            dontBreakRows: true,
            body: [
                [
                    {
                        text: 'CIN',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5],
                        alignment: 'center'
                    },
                    {
                        text: 'NOM COMPLET',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5],
                        alignment: 'center'
                    },
                    {
                        text: 'FONCTION',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5],
                        alignment: 'center'
                    },
                    ...headerTable,
                    {
                        text: 'TOTAL',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [0, 5],
                        alignment: 'center'
                    }
                ],
                ...linges.map((array) => array),
            ]
        }
    },
    sup_lignes.length > 0 ? { text: "", pageBreak: "after" } : {},
    sup_lignes.length > 0 ? {

        layout: {
            hLineColor: 'gray',
            vLineColor: 'gray'
        },
        table: {
            headerRows: 1,
            widths: [50, 50, 200, 70, 50, 343],
            dontBreakRows: true,
            body: [
                [{

                    text: 'DATE',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center',
                },
                {
                    text: 'CIN',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center',
                    width: 1050,
                },
                {
                    text: 'NOM COMPLET',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center',
                    width: 1000,
                },
                {
                    text: 'FONCTION',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center'
                },
                {
                    text: 'SUPP',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center'
                },
                {
                    text: 'JUSTIFICATION',
                    bold: true,
                    fontSize: 10,
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5],
                    alignment: 'center'
                },
                ],
                ...sup_lignes.map((array) => array),
            ],
        }

    } : {}


    ]

    return content
}
