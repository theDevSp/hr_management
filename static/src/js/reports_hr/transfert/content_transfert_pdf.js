/** @odoo-module */

export function transfert_pdf_content(data) {


    return [
        {
            alignment: 'justify',
            columns: [{
                margin: [0, 14, 0, 10],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*'],
                    body: [
                        [{
                            text: `BON DE TRANSFERT :  ${data.transfert_num}`,
                            bold: true,
                            fontSize: 13,
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 5],
                            alignment: 'center',
                            colSpan: 2
                        }, ],

                    ]
                }
            }, ]
        },
        {
            alignment: 'justify',
            columns: [{
                margin: [0, 8, 0, 10],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*'],
                    body: [
                        [{
                                text: 'INTERESSÉ(E)',
                                bold: true,
                                fontSize: 13,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center',
                                colSpan: 2
                            },
                            {
                                text: '',
                            }
                        ],
                        [{
                                text: 'NOM ET PRENOM :',
                                fontSize: 9,
                                border: [1, 1, 0, 0],
                                margin: [15, 8, 0, 0],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_employe_name,
                                fontSize: 9,
                                border: [0, 1, 1, 0],
                                margin: [0, 8, 0, 0],
                                bold: true
                            },
                        ],
                        [{
                                text: '№ CIN :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 6, 0, 0],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_employe_cin,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 6, 0, 0],
                                bold: true
                            }
                        ],
                        [{
                                text: 'Fonction :',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [15, 6, 0, 8],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_employe_fonction,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                margin: [0, 6, 0, 8],
                                bold: true
                            },

                        ],

                    ]
                }
            }, ]
        },
        {
            alignment: 'justify',
            columns: [{
                margin: [0, 8, 0, 10],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*'],
                    body: [
                        [{
                                text: 'DÉTAILS DU TRANSFERT',
                                bold: true,
                                fontSize: 13,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center',
                                colSpan: 2
                            },
                            {
                                text: '',
                            }
                        ],
                        [{
                                text: 'CHANTIER DE DÉPART :',
                                fontSize: 9,
                                border: [1, 1, 0, 0],
                                margin: [15, 8, 0, 0],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_chantier_depart,
                                fontSize: 9,
                                border: [0, 1, 1, 0],
                                margin: [0, 8, 0, 0],
                                bold: true
                            },
                        ],
                        [{
                                text: 'DATE DE DÉPART :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 6, 0, 0],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_date_depart,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 6, 0, 0],
                                bold: true
                            }
                        ],
                        [{
                                text: 'CHANTIER D\'ARRIVÉ :',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [15, 6, 0, 8],
                                alignment: 'right',
                            },
                            {
                                text: data.transfert_chantier_dest,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                margin: [0, 6, 0, 8],
                                bold: true
                            },

                        ],

                    ]
                }
            }, ]
        },
        {
            margin: [0, 8, 0, 0],
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: ['*', '*', '*', '*'],
                headerRows: 1,
                body: [
                    [{
                        text: 'MOYEN DE TRANSPORT',
                        bold: true,
                        fontSize: 13,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 5],
                        alignment: 'center',
                        colSpan: 4
                    }, {
                        text: '',
                    }, {
                        text: '',
                    }, {
                        text: '',
                    }],
                    [{
                            text: 'Véhicule Personnel :',
                            fontSize: 9,
                            border: [1, 1, 0, 0],
                            margin: [25, 8, 0, 0],
                        },
                        {
                            border: [0, 0, 0, 0],
                            margin: [0, 2, 0, 0],
                            table: {
                                body: [
                                    ['....']
                                ]
                            }
                        },
                        {
                            text: 'Matricule :',
                            fontSize: 9,
                            border: [0, 1, 0, 0],
                            margin: [60, 8, 0, 0],
                        },
                        {
                            border: [0, 0, 1, 0],
                            margin: [-15, 2, 0, 8],
                            table: {
                                body: [
                                    ['....................................']
                                ]
                            }
                        },
                    ],
                    [{
                            text: 'Véhicule de Service :',
                            fontSize: 9,
                            border: [1, 0, 0, 0],
                            margin: [25, 8, 0, 0],
                        },
                        {
                            border: [0, 0, 0, 0],
                            margin: [0, 2, 0, 0],
                            table: {
                                body: [
                                    ['....']
                                ]
                            }
                        },
                        {
                            text: 'Matricule :',
                            fontSize: 9,
                            border: [0, 0, 0, 0],
                            margin: [60, 8, 0, 0],
                        },
                        {
                            border: [0, 0, 1, 0],
                            margin: [-15, 2, 0,8],
                            table: {
                                body: [
                                    ['....................................']
                                ]
                            }
                        },
                    ],
                    [{
                            text: 'Trajet :',
                            fontSize: 9,
                            border: [1, 0, 0, 1],
                            margin: [25, 8, 0, 8],
                        },
                        {
                            border: [0, 0, 0, 1],
                            margin: [0, 2, 0, 0],
                            table: {
                                body: [
                                    ['....................................']
                                ]
                            }
                        },
                        {
                            text: 'Gasoil :',
                            fontSize: 9,
                            border: [0, 0, 0, 1],
                            margin: [60, 8, 0, 8],
                        },
                        {
                            border: [0, 0, 1, 1],
                            margin: [-15, 2, 0, 8],
                            table: {
                                body: [
                                    ['....................................']
                                ]
                            }
                        },
                    ],
                ]
            }
        },



    ]




}