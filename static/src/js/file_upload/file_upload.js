/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, onWillStart, onMounted, useRef } from "@odoo/owl"
import { MainFileUpload } from "@configuration_module/components/file_upload/fileupload";
import { FilesView } from "@configuration_module/components/files_view/filesview";

export class HrMainAnalytique extends Component {
    setup() {

    }
}

HrMainAnalytique.template = "hr_management.file_upload"
HrMainAnalytique.components = { MainFileUpload, FilesView }

registry.category("actions").add("hr_management.action_file_upload", HrMainAnalytique)