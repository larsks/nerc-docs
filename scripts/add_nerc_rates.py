import sys
import argparse
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
    "BM GPUH100",
]

SU_RESOURCETYPE_LIST = ["vCPUs", "vGPUs", "RAM"]


def get_current_month():
    return datetime.now().strftime("%Y-%m")


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("--output", "-o")
    p.add_argument("input")

    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    env = Environment(loader=FileSystemLoader("."))
    rates_info = load_from_url()

    su_info_dict = {}
    for su_type in SU_TYPE_LIST:
        su_info_dict[su_type] = {}
        su_info_dict[su_type]["rate"] = Decimal(
            rates_info.get_value_at(f"{su_type} SU Rate", get_current_month())
        )
        for su_resourcetype in SU_RESOURCETYPE_LIST:
            su_info_dict[su_type][su_resourcetype] = rates_info.get_value_at(
                f"{su_resourcetype} in {su_type} SU", get_current_month()
            )

    template = env.get_template(args.input)
    output = template.render(su_info_dict=su_info_dict)
    with open(args.output, "w") if args.output else sys.stdout as f:
        f.write(output)
