/** @odoo-module */

export function content_demande_de_conges(data) {

    const con =  [

        {
            margin: [0, 10, 0, 0],
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
                                    text: data.Conges_Motif.toUpperCase(),
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
                            text: data.Conges_Date_Start,
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

        }
    ]
    
    return con

}