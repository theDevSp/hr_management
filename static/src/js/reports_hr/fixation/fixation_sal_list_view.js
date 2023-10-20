/** @odoo-module */

import { registry } from "@web/core/registry"
import { listView } from "@web/views/list/list_view"
import { ListController } from "@web/views/list/list_controller"
import { useService } from "@web/core/utils/hooks"

import { portrait_header } from "@reports_templates/js/headers";
import { content_fixation_sal } from "./content_fixation_sal"
import { footer_fixation_sal } from "./footer_fixation_sal";

class fixationSalListController extends ListController {
    setup() {
        super.setup()
    }

    async printAllFixationSal(selection) {
        var framework = require('web.framework');
        framework.blockUI();
        try {

            const stcIds = selection.map((rec) => rec.resId);

            if (stcIds.length === 0) {
                alert("Error in selection");
                framework.unblockUI();
                return;
            }

            const allData = [];
            const contents = []

            try {
                const stcs = await Promise.all(stcIds.map(async (id) => {
                    const res = await this.rpc(`/hr_management/get_fixation_salaire_details/${id}`);
                    return res;
                }));

                allData.push(...stcs);
            } catch (error) {
                framework.unblockUI();
                this.showNotification('Une erreur est survenue, veuillez réessayer !','danger');
            }


            if (allData) {
                allData.map(async (fix, index) => {
                    contents.push(await content_fixation_sal(fix[0]));
                    if (index !== allData.length - 1) {
                        contents.push({ text: "", pageBreak: "after" });
                    }
                });
            } else {
                framework.unblockUI();
                return this.showNotification('Une erreur est survenue, veuillez réessayer !','danger');
            }

            if (contents) {
                const pdfDefinition = {
                    info: {
                        title: `${allData.length} FICHE DE FIXATION SALAIRE`,
                        author: "BIOUI TRAVAUX",
                        subject: `FICHE DE FIXATION SALAIRE`
                    },
                    pageMargins: [12, 120, 12, 240],
                    header: portrait_header(),
                    pageSize: "A4",
                    pageOrientation: "portrait",
                    content: contents,
                    footer: function (currentPage, pageCount) {
                        return footer_fixation_sal(currentPage, pageCount)
                    }
                };

                const pdf = await pdfMake.createPdf(pdfDefinition);
                const blob = await pdf.getBlob();
                const url = URL.createObjectURL(blob);

                const viewer = window.open(url, '_blank');
                viewer.onload = () => {
                    framework.unblockUI();
                    const checkWindowInterval = setInterval(() => {
                        if (viewer.closed) {
                            clearInterval(checkWindowInterval);
                            URL.revokeObjectURL(url);
                        }
                    }, 1000);

                };
            }
            else {
                framework.unblockUI();
                return this.showNotification('Aucune donnée disponible, veuillez réessayer !', 'warning');
            }

        } catch (error) {
            framework.unblockUI();
            this.showNotification('Une erreur est survenue, veuillez réessayer !','danger');
            console.error("Error:", error);
        } finally {
            framework.unblockUI();
        }
    }

    showNotification(message, typeNotification) {
        this.notification.add(message, {
            title: "Odoo Notification Service",
            type: typeNotification, // info, warning, danger, success
        });
    }

}

export const fixationSalListView = {
    ...listView,
    Controller: fixationSalListController,
    buttonTemplate: "owl.fixationSalListView.Buttons",
}

registry.category("views").add("fixation_sal_list_view", fixationSalListView)