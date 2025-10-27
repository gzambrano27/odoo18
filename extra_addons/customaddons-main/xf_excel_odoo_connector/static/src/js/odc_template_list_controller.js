/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

export class ODCTemplateListController extends ListController {
    setup() {
        super.setup();
        this.actionService = useService("action");
    }

    async onClickCreateTemplate() {
        const arch = this.props.archInfo || this.archInfo;
        const columns = arch?.columns || [];
        const resModel = this.props.resModel;
        const modelRoot = this.model.root;
        const fields = modelRoot?.activeFields || {};
        const domain = JSON.stringify(modelRoot?.domain || []);
        const templateFields = [];

        for (const [i, column] of columns.entries()) {
            if (column.type === "field") {
                const field = fields[column.rawAttrs.name];
                if (!field) continue;
                templateFields.push([
                    0,
                    false,
                    {
                        sequence: i + 1,
                        model: resModel,
                        field_name: field.name,
                        name: field.string,
                        export_type: this._getExportType(field),
                    },
                ]);
            }
        }

        await this.actionService.doAction("xf_excel_odoo_connector.odc_template_modal_window", {
            additionalContext: {
                default_name: this.props.action?.displayName || resModel,
                default_model: resModel,
                default_domain: domain,
                default_field_ids: templateFields,
            },
        });
    }

    _getExportType(field) {
        const num = new Set(["integer", "float", "monetary", "boolean"]);
        const date = new Set(["date"]);
        const datetime = new Set(["datetime"]);
        const supported = new Set(field.FieldComponent?.supportedTypes || []);
        if ([...supported].some((x) => num.has(x))) return "number";
        if ([...supported].some((x) => date.has(x))) return "date";
        if ([...supported].some((x) => datetime.has(x))) return "datetime";
        return "text";
    }
}

// Registrar la vista personalizada basada en listView
const odcTemplateListView = {
    ...listView,
    Controller: ODCTemplateListController,
};

registry.category("views").add("odc_template_list_view", odcTemplateListView);
