/** @odoo-module */

export async function content_fiche_employee(data) {

    return [
        {
            layout: {
                hLineColor: 'gray',
                vLineColor: 'gray'
            },
            table: {
                widths: ['*'],
                body: [
                    [{
                        margin: [8, 4],
                        text: 'Fiche de l\'Employé :',
                        bold: true,
                        fontSize: 14,
                        fillColor: '#04aa6d',
                        color: 'white',
                        border: [1, true, 0, true],
                        alignment: 'center'
                    }]
                ]
            },
        },
        
        {
            alignment: 'justify',
            margin: [0,5,0,0],
            columns: [{
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [250,'*'],
                        body: [
                            [{
                                text: 'INFORMATION SUR L\'EMPLOYÉ :',
                                bold: true,
                                fontSize: 10,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center',
                                colSpan: 2
                            }, {
                                text: ''
                            }],
                            [{
                                    text: 'NOM ET PRÉNOM :',
                                    fontSize: 9,
                                    border: [1, 1, 0, 0],
                                    margin: [120, 5, 0, 0],
                                }, {
                                    text: data.employe_name,
                                    fontSize: 9,
                                    border: [0, 1, 1, 0],
                                    margin: [0, 5, 0, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: '№ CIN :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [120, 0, 0, 0],
                            }, {
                                text: data.employe_cin,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 0, 0, 0],
                                bold: true
                            }],
                            [{
                                    text: 'CNSS :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [120, 0, 0, 0],
                                }, {
                                    text: data.employe_cnss,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    margin: [0, 0, 0, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'DATE DE NAISSANCE :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [120, 0, 0, 0],
                            }, {
                                text: data.employe_date_naissance,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                    text: 'VALIDITÉ CIN :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [120, 0, 0, 0],
                                }, {
                                    text: data.employe_val_cin,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'LIEU DE NAISSANCE :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [120, 0, 0, 0],
                            }, {
                                text: data.employe_lieu_naissance,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                    text: 'GENRE :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [120, 0, 0, 0],
                                }, {
                                    text: data.employe_genre,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                },

                            ],
                            [{
                                    text: 'ÉTAT CIVILE :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [120, 0, 0, 0],
                                }, {
                                    text: data.employe_etat_civil,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'NOMBRE D\'ENFANT :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [120, 0, 0, 0],
                            }, {
                                text: data.employe_nbr_enfant,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                text: 'NUMÉRO DE TÉLÉPHONE :',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [120, 0, 0, 5],
                            }, {
                                text: data.employe_num_tele,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                bold: true
                            }],
                            

                        ]
                    }
                }
            ]
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
                        text: 'CONTRAT :',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 3],
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
                        text: 'TYPE EMPLOYÉ :',
                        fontSize: 9,
                        border: [1, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.employe_type == 's' ? "SALARIE" : data.employe_type == 'o' ? "OUVRIER" : "-",
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }, {
                        text: 'FONCTION :',
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.employe_fonction,
                        fontSize: 9,
                        border: [0, 1, 1, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'TYPE CONTRAT :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_contract_type,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'SALAIRE :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_salaire,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'DATE DÉBUT :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0]
                    }, {
                        text: data.employe_contract_debut,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'DATE FIN :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_contract_fin,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'PROFILE PAIE :',
                        fontSize: 9,
                        border: [1, 0, 0, 1],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_profile_paie,
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'PÉRIODICITÉ :',
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_periodictite,
                        fontSize: 9,
                        border: [0, 0, 1, 1],
                        margin: [0, 2, 0, 5],
                        bold: true
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
                widths: ['*', '*', '*', '*'],
                headerRows: 1,
                body: [
                    [{
                        text: 'AFFECTATION ET QUALIFICATION :',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 3],
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
                        text: 'CHANTIER :',
                        fontSize: 9,
                        border: [1, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.employe_chantier,
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [0, 5, 0, 0],
                        bold: true,
                    }, {
                        text: '',
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: '',
                        fontSize: 9,
                        border: [0, 1, 1, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'EMBAUCHÉ PAR :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_embaucher_par,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'RECOMMANDER PAR :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_recomander_par,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'MOTIF D\'EMBAUCHE: :',
                        fontSize: 9,
                        border: [1, 0, 0, 1],
                        margin: [15, 2, 0, 0]
                    }, {
                        text: data.employe_motif_embauche,
                        fontSize: 9,
                        border: [0, 0, 1, 1],
                        margin: [0, 2, 0, 5],
                        bold: true,
                        colSpan: 3
                    }, {
                        text: ''
                    }, {
                        text: ''
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
                widths: ['*', '*', '*', '*'],
                headerRows: 1,
                body: [
                    [{
                        text: 'INFORMATION BANCAIRE :',
                        bold: true,
                        fontSize: 10,
                        fillColor: '#04aa6d',
                        color: 'white',
                        margin: [8, 3],
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
                        text: 'COMPTE N° :',
                        fontSize: 9,
                        border: [1, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.employe_rib,
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [0, 5, 0, 0],
                        bold: true,
                    }, {
                        text: 'BANQUE :',
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.employe_bank,
                        fontSize: 9,
                        border: [0, 1, 1, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'AGENCE :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_agence,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'VILLE :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_bank_ville,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'MODE PAIEMENT :',
                        fontSize: 9,
                        border: [1, 0, 0, 1],
                        margin: [15, 2, 0,5]
                    }, {
                        text: data.employe_mode_paiment,
                        fontSize: 9,
                        border: [0, 0, 1, 1],
                        margin: [0, 2, 0, 0],
                        bold: true,
                        colSpan: 3
                    }, {
                        text: 'DATE FIN :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.employe_contract_fin,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }]

                ]
            }
        },




    ]

}