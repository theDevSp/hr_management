/** @odoo-module */

export async function content_fiche_de_paie(data, chantier, period, quinz, type) {

    const data_header = {
        "period": period,
        "quinzine": quinz,
        "chantier": chantier,
        "equipe": data.equipe,
        "type": type
    }

    return [
        {

            columns: [
                {
                    margin: [0, 2],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [270],
                        heights: [0, 52],
                        headerRows: 1,
                        body: [
                            [{
                                text: 'Période',
                                bold: true,
                                fontSize: 12,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 4],
                                alignment: 'center'
                            }],
                            [{
                                text: data_header.period,
                                fontSize: 14,
                                border: [1, 1, 1, 0],
                                margin: [0, 16, 0, 0],
                                bold: true,
                                alignment: 'center'
                            }],
                            [{
                                text: data_header.quinzine,
                                fontSize: 14,
                                border: [1, 0, 1, 1],
                                margin: [2, -12, 0, 8],
                                bold: false,
                                alignment: 'center',
                            }]

                        ]
                    }
                },

                {
                    margin: [0, 2],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray',

                    },
                    table: {
                        widths: [270],
                        heights: [0, 50],

                        body: [
                            [{
                                text: 'Chantier',
                                bold: true,
                                fontSize: 12,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 4],
                                alignment: 'center',

                            }],
                            [{
                                text: [{
                                    text: data_header.chantier,
                                    fontSize: 10,
                                    bold: true,
                                }],
                                fontSize: 10,
                                alignment: 'center',
                                margin: [9, 12, 9, 22.4],
                            }],

                        ],

                    }
                },

                {
                    margin: [0, 2],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [270],
                        heights: [0, 69.5],
                        body: [
                            [{
                                text: 'Équipe',
                                bold: true,
                                fontSize: 12,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [10, 4],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: data_header.equipe,
                                    fontSize: 12,
                                    bold: true
                                }],
                                fontSize: 12,
                                alignment: 'center',
                                margin: [8, 20, 8, 2]

                            }],

                        ],

                    }
                },

                {
                    margin: [0, 2],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: '*',
                        heights: [0, 69.5],
                        body: [
                            [{
                                text: 'Type',
                                bold: true,
                                fontSize: 12,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [10, 4],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: data_header.type,
                                    fontSize: 12,
                                    bold: true
                                }],
                                fontSize: 12,
                                alignment: 'center',
                                margin: [8, 20]

                            }],

                        ],

                    }
                }
            ],



        },
        {
            alignment: 'justify',
            columns: [
                {
                    margin: [0, 8, 0, 0],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: ['*', '*'],
                        body: [
                            [
                                {
                                    text: 'ÉTAT DE PAIEMENT DES SALAIRES',
                                    bold: true,
                                    fontSize: 13,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [8, 5],
                                    alignment: 'center',
                                    colSpan: 2
                                },
                            ],

                        ]
                    }
                },
            ]
        },

        {
            columns: [
                {
                    margin: [0, 4, 0, 0],
                    layout:
                    {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table:
                    {
                        headerRows: 1,
                        widths: [120, 50, 80, 50, 45, 35, 50, 60, 50, 40, 30, 30, 39, 30, 30, 35, 30, 35, '*'],
                        dontBreakRows: true,
                        body:
                            [
                                [
                                    {
                                        text: 'NOM ET PRÉNOM',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'CIN',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'FONCTION',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'CODE ENGIN',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'DATE EMBAUCHE',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'PANIER C.P',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'PROFIL DE PAIE',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'BANQUE',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'SALAIRE DE BASE',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'JOURS HEURES',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'S.J',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'C.P',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'TOTAL',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'DED',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'COT',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'SAD',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'PRIME + FTOR',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'NAP',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                    {
                                        text: 'OBSERVATIONS',
                                        bold: true,
                                        fontSize: 8,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 5],
                                        alignment: 'center',
                                    },
                                ],
                                ...data.data.map((tab) =>
                                    [
                                        {
                                            text: tab.employe_name,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_cin,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_fonction,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_code_engin,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_date_embauche,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_panier_cp,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_profile_de_paie,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_bank,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_salaire_de_base,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_jours_heure,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_salaire_jour,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_cp,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_total,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_deduction,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_cotisation,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_sad,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_prime_ftor,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },
                                        {
                                            text: tab.employe_nap,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        },

                                        {
                                            text: tab.observation,
                                            fontSize: 8,
                                            color: 'black',
                                            margin: [0, 4],
                                            alignment: 'center'
                                        }
                                    ]
                                ),
                                [
                                    {
                                        text: 'TOTAL GÉNÉRAL',
                                        bold: true,
                                        fontSize: 12,
                                        fillColor: '#04aa6d',
                                        color: 'white',
                                        margin: [0, 2],
                                        alignment: 'center',
                                        colSpan: 12,
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_total,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_deduction,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_cotisation,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_sad,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_addition,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },
                                    {
                                        text: data.total_employe_nap,
                                        fontSize: 10,
                                        color: 'black',
                                        bold: true,
                                        margin: [0, 2],
                                        alignment: 'center'
                                    },

                                    {
                                        text: '',
                                        fontSize: 8,
                                        color: 'black',
                                        margin: [0, 2],
                                        alignment: 'center',
                                        border: [1, 1, 0, 0],
                                    }
                                ],

                            ]
                    }
                }


            ]
        },

    ]

}