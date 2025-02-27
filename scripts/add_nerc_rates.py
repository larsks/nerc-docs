import os
from datetime import datetime
from decimal import Decimal

from jinja2 import Environment, FileSystemLoader

from nerc_rates import load_from_url, load_from_file

SU_TYPE_LIST = [
    "CPU",
    "GPUA100",
    "GPUA100SXM4",
    "GPUV100",
    "GPUK80",
    "GPUH100",
    "BM FC430",
    "BM FC830",
    "BM GPUA100SXM4",
    "BM GPUH100"
]

SU_RESOURCETYPE_LIST = [
    "vCPUs",
    "vGPUs",
    "RAM"]

TEMPLATE_FILE_LIST = [
    "docs/get-started/cost-billing/how-pricing-works.md",
    "docs/get-started/cost-billing/pricing-for-bare-metal-machines.md"
]


def get_current_month():
    return datetime.now().strftime("%Y-%m")


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('docs'))
    rates_info = load_from_url()

    su_info_dict = {}
    for su_type in SU_TYPE_LIST:
        su_info_dict[su_type] = {}
        su_info_dict[su_type]["rate"] = Decimal(rates_info.get_value_at(f"{su_type} SU Rate", get_current_month()))
        for su_resourcetype in SU_RESOURCETYPE_LIST:
            su_info_dict[su_type][su_resourcetype] = rates_info.get_value_at(f"{su_resourcetype} in {su_type} SU", get_current_month())

    for template_file in TEMPLATE_FILE_LIST:
        template = env.get_template(template_file.split(os.sep, 1)[-1])
        output = template.render(su_info_dict=su_info_dict)
        with open(template_file, "w") as f:
            f.write(output)
