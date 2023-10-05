/** @odoo-module */

export async function content_report_pointage_salarie(data) {

    const content = [


        {
            table: {
                widths: [150, 0, 90, 293],
                body: [
                    [

                        {
                            rowSpan: 3,
                            text: [
                                'RAPPORT POINTAGE N°:\n',
                                {
                                    text: data.report_Num,
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
                            text: data.employe_name,
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
                            text: data.employe_cin,
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
                            text: data.employe_fonction,
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
                                text: data.employe_month,
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
                        text: data.employe_chantier,
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
                            text: data.employe_equipe,
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
                            text: data.employe_engin,
                            border: [false, false, 1, 1],
                            bold: true,
                            fontSize: 9,
                            margin: [0, 0, 0, 8],
                            fillColor: "#f1f2f3"
                        }
                    ]
                ]
            },
            layout: {
                defaultBorder: false,
                hLineColor: 'gray',
                vLineColor: 'gray'
            }
        },
        {
            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [26, 15, 330, 35, 44, 65],
                body: [
                    [
                        {
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
                    ],
                    ...data.employe_dates.dates_lines.map((item) => {
                        const back = item.jour.includes('Dim') ? '#dddddd' : null
                        const row = [
                            {
                                "text": item.jour,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            },
                            {
                                "text": item.th,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            },
                            {
                                "text": item.observation,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            },
                            {
                                "text": item.code,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            },
                            {
                                "text": item.equipe,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            },
                            {
                                "text": item.chantier,
                                "alignment": "center",
                                "fillColor": back,
                                "fontSize": 7,
                                "margin": [
                                    0,
                                    0.8
                                ]
                            }
                        ];

                        return row;
                    })

                ]
            }
        }

    ]

    return content
}