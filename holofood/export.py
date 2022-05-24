import csv
from io import StringIO
from typing import MutableMapping

from ninja import NinjaAPI
from ninja.renderers import BaseRenderer

from holofood.api import SampleSlimSchema
from holofood.models import Sample


class CSVRenderer(BaseRenderer):
    media_type = "text/csv"

    @classmethod
    def _flatten_data_generator(cls, dict_field: MutableMapping, parent_path: str = ""):
        for field, fielddata in dict_field.items():
            path = f"{parent_path}__{field}" if parent_path else field
            if isinstance(fielddata, MutableMapping):
                yield from cls._flatten_data(fielddata, path).items()
            else:
                yield path, fielddata

    @classmethod
    def _flatten_data(cls, dict_field: MutableMapping, parent_path: str = ""):
        return dict(cls._flatten_data_generator(dict_field, parent_path))

    def render(self, request, data, *, response_status):
        stream = StringIO()
        csv_data = csv.writer(stream, delimiter="\t")

        for idx, obj in enumerate(data):
            if idx == 0:
                headers = self._flatten_data(obj).keys()
                csv_data.writerow(headers)
            csv_data.writerow(self._flatten_data(obj).values())
        return stream.getvalue()


export_api = NinjaAPI(
    title="HoloFood Data Portal Export API",
    description="Download TSV exports of the HoloFood Data Portal data.",
    urls_namespace="export",
    csrf=True,
    renderer=CSVRenderer(),
)


@export_api.get(
    "/samples",
    response=list[SampleSlimSchema],
    summary="Fetch a list of Samples as a TSV",
    url_name="samples_list",
)
def list_samples(
    request,
):
    return Sample.objects.all()
