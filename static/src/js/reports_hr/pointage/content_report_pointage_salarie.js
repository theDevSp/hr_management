/** @odoo-module */

export async function content_report_pointage_salarie(data) {

    const pdfInformation = [
        [

            {
                rowSpan: 3,
                text: [
                    'RAPPORT POINTAGE N°:\n',
                    {
                        text: limitText(data.report_Num, 67),
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
                text: limitText(data.employe_name, 67),
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
                text: limitText(data.employe_cin, 60),
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
                text: limitText(data.employe_fonction, 60),
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
            text: limitText(data.employe_chantier, 60),
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
                text: limitText(data.employe_engin, 60),
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

    const tableRow = data.employe_dates.dates_lines.map(obj => {
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
                text: limitText(obj.observation,78),
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: limitText(obj.code,14),
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: limitText(obj.equipe,11),
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            },
            {
                text: limitText(obj.chantier,20),
                alignment: 'center',
                fillColor: back,
                fontSize: 7,
                margin: [0, 0.8]
            }
        ];

        return row;
    });

    const footerTable = {
        margin: [0, 5, 0, 0],
        layout: {
            hLineColor: 'gray',
            vLineColor: 'gray'
        },
        table: {
            widths: [124, 135, 135, 139],
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
                }, {
                    text: 'Responsable',
                    fontSize: 10,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                }, {
                    text: 'Conducteur/Chef de Projet',
                    fontSize: 10,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                }, {
                    text: 'Pointeur',
                    fontSize: 10,
                    bold: true,
                    alignment: 'center',
                    fillColor: '#04aa6d',
                    color: 'white',
                    margin: [0, 5]
                },],
                [{
                    text: (data && data.employe_totalheure !== '' && data.employe_totaljours !== '') ? `${data.employe_totalheure}H / ${data.employe_totaljours}J` : `0H / 0J`,
                    fontSize: 17,
                    alignment: 'center',
                    bold: true,
                    margin: [0, 30],
                }, {
                    text: '',
                    fontSize: 9,
                    bold: true
                }, {
                    text: '',
                    fontSize: 9,
                    bold: true
                }, {
                    text: '',
                    fontSize: 9,
                    bold: true
                }]
            ]
        }
    }

    const content = [
        {
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
            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: [26, 15, 290, 52, 52, 80],
                body: [
                    tableHeader,
                    ...tableRow.map((array) => array)
                ]
            }
        },

        footerTable

    ]

    /*const content = [


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

    ]*/




    return content
}

function limitText(text, maxLength) {
    if (text.length <= maxLength) {
        return text.replace(/\n/g, " ");
    } else {
        return text.slice(0, maxLength - 3).replace(/\n/g, " ") + '...';
    }
}