/** @odoo-module */

export async function content_recap(data) {

    const content = [
       
        {
            alignment: 'justify',
            columns: [
                {
                    margin: [0, -20, 0, 5],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: ['*','*'],
                        body: [
                            [
                                {
                                    text: 'RECAP DES ÉTATS DE PAIEMENT',
                                    bold: true,
                                    fontSize: 12,
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
            alignment: 'justify',
            columns: [
                {
                    margin: [0, 0, 0, 0],
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: ['*','*','*'],
                        body: [
                            [
                                {
                                    text: `MOIS: ${data.recap_period} (${data.recap_quinzaine})`,
                                    bold: true,
                                    fontSize: 8,
                                    //fillColor: '#04aa6d',
                                    color: 'black',
                                    margin: [8, 5],
                                    alignment: 'center',
                                   // colSpan: 2
                                },
                                 {
                                    text: 'REF: '+data.recap_name,
                                    bold: true,
                                    fontSize: 8,
                                   // fillColor: '#04aa6d',
                                    color: 'black',
                                    margin: [8, 5],
                                    alignment: 'center',
                                   // colSpan: 2
                                },
                                 {
                                    text: 'CLASSIFICATION: '+data.recap_type_emp,
                                    bold: true,
                                    fontSize: 8,
                                   // fillColor: '#04aa6d',
                                    color: 'black',
                                    margin: [8, 5],
                                    alignment: 'center',
                                   // colSpan: 2
                                },
                            ],
                            
                        ]
                    }
                },
            ],
        },
        {
            columns:[
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
                        widths: [211,70,25,50,50,50,50],
                        dontBreakRows: true,
                        body: 
                        [
                            [
                                {
                                    text: 'CHANTIERS',
                                    bold: true,
                                    fontSize: 8,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'REFERENCE',
                                    bold: true,
                                    fontSize: 8,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'EFF',
                                    bold: true,
                                    fontSize: 8,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'VIREMENT',
                                    bold: true,
                                    fontSize: 8,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'CCP',
                                    bold: true,
                                    fontSize: 8,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'VERSEMENT',
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
                               
                            ],
                          
                            [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '1.260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ], 
                            [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                           
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                            [
                                {
                                    text: 'CH-00423 - RENFORCEMENT DE LA RP 6030 PK 1+700 AU PK 20+000',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: 'TY/2023/06/108',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 1.4],
                                    alignment: 'center'
                                },
                                {
                                    text: '20',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '289.777,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '126.367,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '72.384,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 0.1],
                                    alignment: 'center'
                                },
                                {
                                    text: '260.541,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0,0.1],
                                    alignment: 'center'
                                },

                            ],
                             [
                                {
                                    text: 'TOTAL',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                    colSpan: 2,
                                },
                                {
                                    text: '',
                                },
                                {
                                    text: '340',
                                    bold: true,
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '4.926,209',
                                    bold: true,
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '2.148,239',
                                    bold: true,
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '1.230,528',
                                    bold: true,
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '21.429.197,0',
                                    bold: true,
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                               
                            ],
                        ]
                    }
                }
                
                
            ]
        },
        
        {
            columns:[
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
                        widths: ['*','*','*'],
                        dontBreakRows: true,
                        body: 
                        [
                            [
                                {
                                    text: 'TYPE',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: 'MONTANT',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: 'RÉFÉRENCE OV',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                               
                            ],
                            [
                                {
                                    text: 'VIREMENT',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '95.706,0',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '........................................',
                                    fontSize: 10,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                               
                            ],
                            [
                                {
                                    text: 'VERSEMENT',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '451.123',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '........................................',
                                    fontSize: 10,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                               
                            ],
                            [
                                {
                                    text: 'TOTAL',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '546,829',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: '',
                                    bold: true,
                                    fontSize: 10,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                               
                            ],
                        ]
                    }
                }
                
                
            ]
        },
        
    ]




    return content
}

function limitText(text, maxLength) {
    if (text.length <= maxLength) {
        return text.replace(/\n/g, " ");
    } else {
        return text.slice(0, maxLength - 3).replace(/\n/g, " ") + '...';
    }
}