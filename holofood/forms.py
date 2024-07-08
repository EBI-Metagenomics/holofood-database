from django import forms
from django.forms.widgets import SelectMultiple
from django.utils.html import format_html
from django.utils.encoding import force_str


class CazyCheckboxesWidget(SelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (
            [
                ("GH", "Glycoside Hydrolase"),
                ("CB", "Carbohydrate-Binding"),
                ("PL", "Polysaccharide Lyases"),
                ("CE", "Carbohydrate Esterases"),
                ("AA", "Auxiliary Activities"),
                ("GT", "GlycosylTransferases"),
            ],
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if not isinstance(value, list):
            value = [value]
        for option_value, option_label in self.choices:
            final_attrs = self.build_attrs(self.attrs, attrs)
            final_attrs["type"] = "checkbox"
            final_attrs["name"] = name
            final_attrs["value"] = option_value
            final_attrs["id"] = "id_%s_%s" % (name, option_value)

            if value and force_str(option_value) in value:
                final_attrs["checked"] = "checked"
            else:
                final_attrs.pop("checked", None)

            output.append(
                format_html(
                    '<div class="hf-checkbox">'
                    '<input{} /> <label for="{}">{}</label>'
                    "</div>",
                    format_html(
                        "".join(
                            f' {key}="{value}"' for key, value in final_attrs.items()
                        )
                    ),
                    final_attrs["id"],
                    option_label,
                )
            )

        return format_html("".join(output))


class CazyAnnotationsFilterForm(forms.Form):
    field_order = [
        "accession__icontains",
        "cluster_representative__icontains",
        "taxonomy__icontains",
        "cazy_annotations",
    ]
    cazy_annotations = forms.MultipleChoiceField(
        choices=[
            ("GH", "Glycoside Hydrolase"),
            ("CB", "Carbohydrate-Binding"),
            ("PL", "Polysaccharide Lyases"),
            ("CE", "Carbohydrate Esterases"),
            ("AA", "Auxiliary Activities"),
            ("GT", "GlycosylTransferases"),
        ],
        widget=CazyCheckboxesWidget,
        required=False,
        label="CAZy Annotations present",
        help_text="Annotated on species rep.",
    )
