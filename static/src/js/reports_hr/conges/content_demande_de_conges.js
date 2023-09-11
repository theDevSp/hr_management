/** @odoo-module */

export function content_demande_de_conges(data,pageNumber, totalPages) {

    const finalContent = {

        info: {
            title: `Demande de Congés : ${data.Conges_Employe_Name} du ${data.Conges_Date_Start} au ${data.Conges_Date_End}`,
            author: "BIOUI TRAVAUX",
            subject: `Demande De Congés`
        },

        content: [

            {
                margin: [0, 0, 0, 0],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*', '*'],
                    headerRows: 1,
                    body: [
                        [{
                            text: 'DEMANDE DE CONGÉS',
                            bold: true,
                            fontSize: 12,
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 10],
                            border: [0, true, 0, true],
                            colSpan: 3,
                            alignment: 'center',
                        },
                        {
                            text: ''
                        },
                        {
                            text: ''
                        }
                        ]
                    ]
                },
            },
            {
                margin: [0, 8, 0, 0],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: [300, '*', '*'],
                    headerRows: 1,
                    body: [
                        [{
                            text: 'INTÉRESSÉ(E) :',
                            bold: true,
                            fontSize: 11,
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 7],
                            alignment: 'center',
                            colSpan: 3
                        },
                        {
                            text: ''
                        },
                        {
                            text: ''
                        }
                        ],
                        [
                            {
                                text: 'NOM ET PÉRNOM :',
                                margin: [215, 8, 0, 0],
                                fontSize: 8,
                                border: [1, true, 0, 0]
                            },
                            {
                                text: data.Conges_Employe_Name,
                                fontSize: 8,
                                border: [0, 0, 1, 0],
                                alignment: 'left',
                                colSpan: 2,
                                margin: [-15, 8, 0, 3],
                            },
                            {
                                text: ''
                            }
                        ],
                        [
                            {
                                text: 'CIN :',
                                margin: [215, 2, 0, 3],
                                fontSize: 8,
                                border: [1, 0, 0, 0],
                            },
                            {
                                text: data.Conges_Employe_CIN,
                                fontSize: 8,
                                border: [0, 0, 1, 0],
                                alignment: 'left',
                                colSpan: 2,
                                margin: [-15, 2, 0, 3],
                            },
                            {
                                text: ''
                            }
                        ],
                        [
                            {
                                text: 'CHANTIER :',
                                margin: [215, 2, 0, 3],
                                fontSize: 8,
                                border: [1, 0, 0, 0],
                            },
                            {
                                text: data.Conges_Employe_Chantier,
                                fontSize: 8,
                                border: [0, 0, 1, 0],
                                alignment: 'left',
                                colSpan: 2,
                                margin: [-15, 2, 0, 3],
                            },
                            {
                                text: ''
                            }
                        ],
                        [
                            {
                                text: 'FONCTION :',
                                margin: [215, 2, 0, 8],
                                fontSize: 8,
                                border: [1, 0, 0, true],
                            },
                            {
                                text: data.Conges_Employe_Fonction,
                                fontSize: 8,
                                border: [0, 0, 1, 1],
                                alignment: 'left',
                                colSpan: 2,
                                margin: [-15, 2, 0, 3],
                            },
                            {
                                text: ''
                            }
                        ]
                    ]
                },
            },
            {
                margin: [0, 8, 0, 0],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*'],
                    headerRows: 1,
                    body: [
                        [{
                            text: 'DÉTAILS DE CONGÉS :',
                            bold: true,
                            fontSize: 11,
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 5],
                            border: [0, true, 0, 1],
                            alignment: 'center',
                            colSpan: 2
                        },
                        {
                            text: '',
                            fontSize: 10,
                            fillColor: '#04aa6d',
                            border: [0, true, 0, true],
                            color: 'white',
                        }
                        ],
                        [
                            {
                                colSpan: 2,
                                margin: [10, 10],
                                border: [1, true, 1, 1],
                                alignment: 'center',
                                text: [
                                    {
                                        text: 'MOTIF DE CONGÉS : ',
                                        fontSize: 8
                                    },
                                    {
                                        text: data.Conges_Motif.toUpperCase()                                        ,
                                        fontSize: 8,
                                    }
                                ]
                            },
                            {
                                text: '',

                            }
                        ]
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
                    widths: ['*', '*', '*'],
                    body: [
                        [{
                            text: 'DATE DEBUT :',
                            margin: [8, 5],
                            bold: true,
                            fontSize: 10,
                            fillColor: '#04aa6d',
                            color: 'white',
                            alignment: 'center'
                        },
                        {
                            text: 'DATE FIN :',
                            fontSize: 10,
                            bold: true,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 5],
                        },
                        {
                            text: 'NBR JOURS :',
                            fontSize: 10,
                            bold: true,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [8, 5],
                        }
                        ],
                        [
                            {
                                text: data.Conges_Date_Start                                ,
                                margin: [5, 10],
                                fontSize: 10,
                                alignment: 'center',
                            },
                            {
                                text: data.Conges_Date_End,
                                fontSize: 10,
                                margin: [5, 10],
                                alignment: 'center'
                            },
                            {
                                text: data.Conges_Nbr_Jours,
                                fontSize: 10,
                                alignment: 'center',
                                margin: [5, 10],
                            }
                        ]
                    ]
                },

            },
            {
                margin: [0, 20, 0, 0],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*'],
                    body: [
                        [{
                            margin: [8, 8],
                            text: 'Signatures :',
                            bold: true,
                            fontSize: 11,
                            fillColor: '#04aa6d',
                            color: 'white',
                            border: [1, true, 0, true],
                            alignment: 'center'
                        }
                        ]
                    ]
                },

            }


        ],
        footer: [
            {
                margin: [12, 0, 12, 0],
                layout: {
                    hLineColor: 'gray',
                    vLineColor: 'gray'
                },
                table: {
                    widths: ['*', '*', '*', '*'],
                    heights: [10, 10],
                    headerRows: 1,
                    body: [
                        [{
                            text: 'Intéressé(e)',
                            bold: true,
                            fontSize: 10,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [0, 5]
                        },
                        {
                            text: 'Pointeur',
                            fontSize: 9,
                            bold: true,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [0, 5]
                        },
                        {
                            text: 'Chef de Projet',
                            fontSize: 9,
                            bold: true,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [0, 5]
                        },
                        {
                            text: 'Directeur Technique',
                            fontSize: 9,
                            bold: true,
                            alignment: 'center',
                            fillColor: '#04aa6d',
                            color: 'white',
                            margin: [0, 5]
                        },
                        ],
                        [{
                            text: '',
                            fontSize: 9,
                            bold: true,
                            margin: [0, 40],
                            //padding: [0, 20]
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
            },
            {
                margin: [12, 5, 12, 0],
                alignment: 'justify',
                columns: [
                    {
                        text: `Imprimer le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' })}`,
                        fontSize: 7,
                        alignment: 'right',
                        bold: true,
                    }
                ]
            }

        ]
    };

    return finalContent


}