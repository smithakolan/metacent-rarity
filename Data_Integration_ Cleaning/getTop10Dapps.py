#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""

import top10Dapps
import json


def main():
    with open("dapps.json") as json_file:
        dapp_list = json.load(json_file)

    selected_dapps = []
    for dapp in dapp_list:
        slug = dapp['slug']
        if slug in top10Dapps.top_10_dapps:
            print(slug)
            selected_dapps.append(dapp)

    chosen_dapps = []
    for sdapp in selected_dapps:
        sdapp_traits = sdapp['traits']
        trait_counts = {}

        for key, value in sdapp_traits.items():
            value_dict = value
            value_list = value_dict.values()
            trait_counts[key] = sum(value_list)

        sdapp['trait_count'] = trait_counts
        chosen_dapps.append(sdapp)

    with open("top_dapps.json", "w") as f:
        json.dump(chosen_dapps, f)


if __name__ == '__main__':
    main()
