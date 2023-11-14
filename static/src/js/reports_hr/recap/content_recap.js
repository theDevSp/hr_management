/** @odoo-module */

export async function content_recap(data) {


    let recap_lines = []

    /*console.log(data.recap_lines[0].recap_mode_payes_total.map(arr => {
        return arr.mode
    }))*/

    data.recap_lines.forEach(line => {
        recap_lines.push([
            createRecapItem(line.recap_chantier),
            createRecapItem(line.recap_equipe),
            createRecapItem(line.recap_nbr_effectif),
            createRecapItem((line.recap_mode_payes_total.find(mod => mod.mode === 'Virement') || {}).total || '0'),
            createRecapItem((line.recap_mode_payes_total.find(mod => mod.mode === 'Versement') || {}).total || '0'),
            createRecapItem((line.recap_mode_payes_total.find(mod => mod.mode === 'Espece') || {}).total || '0'),
            createRecapItem(line.recap_montant_total)
        ]);
    });

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
                        widths: [206,70,28,50,52,50,50],
                        dontBreakRows: true,
                        body: 
                        [
                            [
                                {
                                    text: 'CHANTIERS',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'ÉQUIPES',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'EFF',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'VIREMENT',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'VERSEMENT',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'ESPÈCE',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                                {
                                    text: 'TOTAL',
                                    bold: true,
                                    fontSize: 9,
                                    fillColor: '#04aa6d',
                                    color: 'white',
                                    margin: [0, 5],
                                    alignment: 'center',
                                },
                               
                            ],
                          
                            ...recap_lines, 
                            
                            
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
                                    text: data.recap_total_virement,
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
                                    text: data.recap_total_versement,
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
                                    text: 'ESPÈCE',
                                    fontSize: 8,
                                    color: 'black',
                                    margin: [0, 2],
                                    alignment: 'center',
                                },
                                {
                                    text: data.recap_total_espece,
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
                                    text: data.recap_lines_total,
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
        }
        
    ]




    return content
}

const createRecapItem = (text, fontSize = 8) => ({
    text,
    fontSize,
    color: 'black',
    margin: [0, 2],
    alignment: 'center'
});

function limitText(text, maxLength) {
    if (text.length <= maxLength) {
        return text.replace(/\n/g, " ");
    } else {
        return text.slice(0, maxLength - 3).replace(/\n/g, " ") + '...';
    }
}