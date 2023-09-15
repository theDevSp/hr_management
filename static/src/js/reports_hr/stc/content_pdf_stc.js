/** @odoo-module */

export function stc_pdf_content (data) {

    const finalContent = [

        {
            alignment: 'justify',
            columns: [{
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [120, 239, 1],
                        body: [
                            [{
                                text: 'Information sur l\'Employé :',
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
                                    margin: [15, 5, 0, 0],
                                }, {
                                    text: data.stc_employee_nom_prenom,
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
                                margin: [15, 0, 0, 0],
                            }, {
                                text: data.stc_employee_cin,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                margin: [0, 0, 0, 0],
                                bold: true
                            }],
                            [{
                                    text: 'FONCTION :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [15, 0, 0, 0],
                                }, {
                                    text: data.stc_employee_fonction,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    margin: [0, 0, 0, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'SALAIRE :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                            }, {
                                text: `${data.stc_employee_salaire} DH`,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                    text: '№ COMPTE :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [15, 0, 0, 0],
                                }, {
                                    text: data.stc_employee_bank,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'PAIMENT :',
                                fontSize: 9,
                                border: [1, 0, 0, 0],
                                margin: [15, 0, 0, 0],
                            }, {
                                text: data.stc_employee_paiment,
                                fontSize: 9,
                                border: [0, 0, 1, 0],
                                bold: true
                            }],
                            [{
                                    text: 'PÉRIODE TRAVAILLÉE :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [15, 0, 0, 0],
                                }, {
                                    text: data.stc_employee_periode,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                }

                            ],
                            [{
                                    text: 'PAR ORDRE :',
                                    fontSize: 9,
                                    border: [1, 0, 0, 0],
                                    margin: [15, 0, 0, 0],
                                }, {
                                    text: data.stc_par_ordre,
                                    fontSize: 9,
                                    border: [0, 0, 1, 0],
                                    bold: true
                                },

                            ],
                            [{
                                text: 'CHANTIER :',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [15, 0, 0, 5],
                            }, {
                                text: data.stc_employee_chantier,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                bold: true
                            }],

                        ]
                    }
                },
                {
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [173],
                        body: [
                            [{
                                text: data.stc_reference,
                                bold: true,
                                fontSize: 10,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: 'Date : ',
                                    fontSize: 9,
                                    bold: true
                                }, {
                                    text: data.stc_date,
                                    fontSize: 10,
                                    bold: true
                                }],
                                fontSize: 9,
                                alignment: 'center',
                                margin: [8, 20]

                            }],
                            [{
                                text: 'null',
                                fontSize: 7,
                                color: 'white',
                                border: []
                            }],
                            [{
                                text: data.stc_employee_poste,
                                bold: true,
                                fontSize: 10,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 3],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: 'Salarié № : ',
                                    fontSize: 9,
                                    bold: true
                                }, {
                                    text: data.stc_employee_numero,
                                    fontSize: 10,
                                    bold: true
                                }],
                                fontSize: 9,
                                alignment: 'center',
                                margin: [8, 20.3]
                            }]
                        ],

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
                        text: 'Sommes des Additions :',
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
                        text: 'Panier Congés :',
                        fontSize: 9,
                        border: [1, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: `${data.stc_panier_conges_jours} Jr = ${data.stc_panier_conges_dh} DH`,
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }, {
                        text: 'Frais de Dépense :',
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.stc_frais_de_depence === "" ? "-" : `${data.stc_frais_de_depence} DH`,
                        fontSize: 9,
                        border: [0, 1, 1, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'Nombre de Dimanche :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.stc_nbr_dimanche_jours === "" ? "-" : `${data.stc_nbr_dimanche_jours} Jr = ${data.stc_nbr_dimanche_dh} DH`,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'Frais de Route :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.stc_frais_de_route === "" ? "-" : `${data.stc_frais_de_route} DH`,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'Préavis à Ajouter :',
                        fontSize: 9,
                        border: [1, 0, 0, 0],
                        margin: [15, 2, 0, 0]
                    }, {
                        text: data.stc_preavis_ajouter_jours === "" ? "-" : `${data.stc_preavis_ajouter_jours} Jr = ${data.stc_preavis_ajouter_jours} DH`,
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'Prime :',
                        fontSize: 9,
                        border: [0, 0, 0, 0],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.stc_prime === "" ? "-" : `${data.stc_prime} DH`,
                        fontSize: 9,
                        border: [0, 0, 1, 0],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'Licenciement :',
                        fontSize: 9,
                        border: [1, 0, 0, 1],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.stc_liceciment === "" ? "-" : `${data.stc_liceciment} DH`,
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'Reste du Salaire :',
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [15, 2, 0, 0],
                    }, {
                        text: data.stc_rest_salaire === "" ? "-" : `${data.stc_rest_salaire} DH`,
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
                        text: 'Sommes des Déductions :',
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
                        text: 'Préavis à Retenir :',
                        fontSize: 9,
                        border: [1, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.stc_preavis_retenir_jours === "" ? "-" : `${data.stc_preavis_retenir_jours} Jr = ${data.stc_preavis_retenir_dh} DH`,
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }, {
                        text: 'Cotisation CIMR :',
                        fontSize: 9,
                        border: [0, 1, 0, 0],
                        margin: [15, 5, 0, 0],
                    }, {
                        text: data.stc_cotisation_cimr === "" ? "-" : `${data.stc_cotisation_cimr} DH`,
                        fontSize: 9,
                        border: [0, 1, 1, 0],
                        margin: [0, 5, 0, 0],
                        bold: true
                    }],
                    [{
                        text: 'Amende :',
                        fontSize: 9,
                        border: [1, 0, 0, 1],
                        margin: [15, 2, 0,
                            [{
                                text: 'Prélèvement et Crédits :',
                                fontSize: 9,
                                border: [1, 0, 0, 1],
                                margin: [15, 2, 0, 0]
                            }, {
                                text: data.stc_prelevement_credit === "" ? "-" : `${data.stc_prelevement_credit} DH`,
                                fontSize: 9,
                                border: [0, 0, 1, 1],
                                margin: [0, 2, 0, 5],
                                bold: true,
                                colSpan: 3
                            }, {
                                text: ''
                            }, {
                                text: ''
                            }],, 1],
                    }, {
                        text: data.stc_amende === "" ? "-" : `${data.stc_amende} DH`,
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [0, 2, 0, 0],
                        bold: true
                    }, {
                        text: 'Prélèvement et Crédits :',
                        fontSize: 9,
                        border: [0, 0, 0, 1],
                        margin: [15, 2, 0, 1],
                    }, {
                        text: data.stc_prelevement === "" ? "-" : `${data.stc_prelevement} DH`,
                        fontSize: 9,
                        border: [0, 0, 1, 1],
                        margin: [0, 2, 0, 5],
                        bold: true
                    }]

                ]
            }
        },

        {
            margin: [0, 10, 0, 0],
            alignment: 'justify',
            columns: [{
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [120, 239, 1],
                        heights: [20, 55, 44],
                        body: [
                            [{
                                text: 'Notes :',
                                bold: true,
                                fontSize: 11,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center',
                                colSpan: 2
                            }, {
                                text: ''
                            }],
                            [{
                                    text: data.stc_notes,
                                    fontSize: 10,
                                    border: [1, 1, 1, 1],
                                    margin: [15, 5, 15, 0],
                                    colSpan: 2,
                                    rowSpan: 8
                                }, {
                                    text: '',
                                },

                            ],
                            [{
                                text: ''
                            }, {
                                text: ''
                            }],
                            [{
                                    text: ''
                                }, {
                                    text: ''
                                },

                            ],
                            [{
                                text: ''
                            }, {
                                text: ''
                            }],
                            [{
                                    text: ''
                                }, {
                                    text: ''
                                },

                            ],
                            [{
                                text: ''
                            }, {
                                text: ''
                            }],
                            [{
                                    text: ''
                                }, {
                                    text: ''
                                },

                            ],
                            [{
                                text: ''
                            }, {
                                text: ''
                            }]
                        ]
                    }
                },
                {
                    layout: {
                        hLineColor: 'gray',
                        vLineColor: 'gray'
                    },
                    table: {
                        widths: [173],
                        body: [
                            [{
                                text: 'Montant a Payé :',
                                bold: true,
                                fontSize: 11,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 5],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: data.stc_montant_apayer === "" ? "-" : `${data.stc_montant_apayer} (DH)`,
                                    fontSize: 14,
                                    bold: true
                                }],
                                alignment: 'center',
                                margin: [8, 16.3]

                            }],
                            [{
                                text: 'null',
                                fontSize: 2,
                                color: 'white',
                                border: []
                            }],
                            [{
                                text: 'Montant Validé :',
                                bold: true,
                                fontSize: 11,
                                fillColor: '#04aa6d',
                                color: 'white',
                                margin: [8, 3],
                                alignment: 'center'
                            }],
                            [{
                                text: [{
                                    text: data.stc_montant_valider === "" ? "-":`${data.stc_montant_valider} (DH)`,
                                    fontSize: 14,
                                    bold: true
                                }],
                                alignment: 'center',
                                margin: [8, 16.2]
                            }]
                        ],

                    }
                }
            ]
        },


    ]

    return finalContent


}