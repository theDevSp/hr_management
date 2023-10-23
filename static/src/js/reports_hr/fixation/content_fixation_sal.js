/** @odoo-module */

export async function content_fixation_sal(data) {

    return [
        {
            alignment: 'justify',

            columns: [
                {
                    margin: [0, 14, 0, 0],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: ['*', '*'],
                        body: [
                            [{
                                text: `FICHE DE FIXATION N° ${data.fixation_num}`,
                                bold: true,
                                fontSize: 13,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center',
                                colSpan: 2,
                                border: [1, 1, 1, 0],
                            }, {
                                text: ''
                            }],
                            [{
                                text: `LE ${(new Date()).toLocaleDateString('en-GB')}`,
                                bold: true,
                                fontSize: 12,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [0, 0, 0, 5],
                                border: [1, 0, 1, 1],
                                alignment: 'center',
                                colSpan: 2
                            }, {
                                text: ''
                            }],
                            [{
                                text: 'NOM ET PRENOM :',
                                fontSize: 9,
                                border: [1, 1, 0, 0],
                                margin: [15, 15, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_name,
                                fontSize: 9,
                                border: [0, 1, 1, 0],
                                margin: [0, 15, 0, 0],
                                bold: true
                            },

                            ],
                            [{
                                text: '№ CIN :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_cin,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 0, 0, 0],
                                bold: true
                            }],
                            [{
                                text: 'N° CNSS :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_cnss,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 0, 0, 0],
                                bold: true
                            },

                            ],
                            [{
                                text: 'FONCTION :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_fonction,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                text: 'PROFILE PAIE :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_profile,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            },

                            ],
                            [{
                                text: "DATE D'EMBAUCHE :",
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_date_embauche,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                text: 'EMBAUCHÉ PAR:',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                                alignment: 'right',
                            }, {
                                text: data.employe_emb_par,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            },

                            ],
                            [{
                                text: 'RECOMMANDÉ PAR:',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [15, 0, 0, 15],
                                alignment: 'right',
                            }, {
                                text: data.employe_rec_par,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                bold: true
                            }],

                        ]
                    }
                },

            ]
        },

        {


            margin: [0, 5, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray',
            },
            table: {
                widths: '*',
                headerRows: 1,
                body: [
                    [{
                        text: 'CHANTIER D\'AFFECTATION',
                        bold: true,
                        fontSize: 13,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 5.5],
                        alignment: 'center'
                    }],
                    [{
                        text: data.employe_chantier,
                        fontSize: 12,
                        border: [1, 1, 1, 1],
                        margin: [0, 20, 0, 20],
                        bold: true,
                        alignment: 'center'
                    }]

                ]
            }






        },
        {

            columns: [
                {
                    margin: [0, 8, 0, 0],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray',
                    },
                    table: {
                        widths: [270],
                        headerRows: 1,
                        body: [
                            [{
                                text: 'SALAIRE PROPOSÉ',
                                bold: true,
                                fontSize: 13,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5.5],
                                alignment: 'center'
                            }],
                            [{
                                text: data.employe_sal_propose == '' ? '' : `${data.employe_sal_propose} DH`,
                                fontSize: 14,
                                border: [1, 1, 1, 0],
                                margin: [0, 20, 0, 0],
                                bold: true,
                                alignment: 'center'
                            }],
                            [{
                                text: data.employe_sal_propose_lettres == '' ? '' : `${data.employe_sal_propose_lettres} DH`,
                                fontSize: 10,
                                border: [1, 0, 1, 1],
                                margin: [2, 2, 0, 20],
                                bold: false,
                                alignment: 'center'
                            }],

                        ]
                    }
                },

                {
                    margin: [0, 8, 0, 0],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [275.5],
                        body: [
                            [{
                                text: 'SALAIRE VALIDÉ',
                                bold: true,
                                fontSize: 13,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5.5],
                                alignment: 'center'
                            }],
                            [{
                                text: data.employe_sal_valider == '' ? '' : `${data.employe_sal_valider} DH`,
                                fontSize: 14,
                                border: [1, 1, 1, 0],
                                margin: [0, 20, 0, 0],
                                bold: true,
                                alignment: 'center'
                            }],
                            [{
                                text: data.employe_sal_valider_lettres == '' ? '' : `${data.employe_sal_valider_lettres} DH`,
                                fontSize: 10,
                                border: [1, 0, 1, 1],
                                margin: [2, 2, 0, 20],
                                bold: false,
                                alignment: 'center'
                            }],
                        ],

                    }
                }
            ],



        },




    ]

    

}