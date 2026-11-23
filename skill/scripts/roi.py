#!/usr/bin/env python3
"""AI Adoption ROI Calculator — CLI mirror of ../index.html.

Same constants, same formulas. No network calls. No data leaves this machine.

Usage:
    python3 scripts/roi.py --team 85 --volume 5000 --hourly 145 --spend 2400
    python3 scripts/roi.py --team 85 --volume 5000 --hourly 145 --spend 2400 --json
    python3 scripts/roi.py --example        # anonymized Netflix-scale worked example
"""
from __future__ import annotations

import argparse
import json

ELIGIBLE_SHARE = 0.40          # 40% of requests are AI-eligible
MINUTES_SAVED = 18             # minutes saved per AI-assisted request
SCENARIOS = {"conservative": 0.30, "expected": 0.40, "optimistic": 0.50}
SOFT_CAP_SHARE = 0.05          # recommended soft spend cap: 5% of gross value

# Anonymized Netflix-scale worked example. Illustrative inputs chosen so the
# model reproduces the verified field anchor (~600 hrs/mo). NOT real data, and
# the $ figure computed here is the model's output for one team — not the
# verified $2.5M/yr program outcome (57 productions, ~8 weeks).
EXAMPLE = {"team_size": 85, "volume": 5000, "hourly_cost": 145.0, "spend": 2400.0}


def calculate_roi(team_size: int, volume: float, hourly_cost: float, spend: float) -> dict:
    hours_per_request = MINUTES_SAVED / 60  # 0.30 hr

    def scenario(share: float) -> dict:
        hours = volume * share * hours_per_request
        gross = hours * hourly_cost
        net = gross - spend
        return {"share": share, "hours": hours, "gross": gross,
                "net": net, "yearly": net * 12}

    expected = scenario(SCENARIOS["expected"])
    eligible = volume * SCENARIOS["expected"]
    return {
        "inputs": {"team_size": team_size, "volume": volume,
                   "hourly_cost": hourly_cost, "spend": spend},
        "hours_saved_per_month": expected["hours"],
        "hours_per_person_per_month": expected["hours"] / team_size if team_size else None,
        "eligible_requests_per_month": eligible,
        "gross_value_per_month": expected["gross"],
        "net_value_per_month": expected["net"],
        "recovered_per_year_net": expected["yearly"],
        "roi_multiple_gross": expected["gross"] / spend if spend else None,
        "cost_per_assisted_request": spend / eligible if eligible else None,
        "soft_spend_cap_per_month": expected["gross"] * SOFT_CAP_SHARE,
        "headroom_vs_soft_cap": expected["gross"] * SOFT_CAP_SHARE - spend,
        "scenarios": {name: scenario(share) for name, share in SCENARIOS.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team", type=int, default=25)
    parser.add_argument("--volume", type=float, default=1200)
    parser.add_argument("--hourly", type=float, default=85)
    parser.add_argument("--spend", type=float, default=500)
    parser.add_argument("--example", action="store_true",
                        help="Use the anonymized Netflix-scale worked example inputs")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.example:
        result = calculate_roi(EXAMPLE["team_size"], EXAMPLE["volume"],
                               EXAMPLE["hourly_cost"], EXAMPLE["spend"])
        result["example"] = ("anonymized worked example — illustrative inputs, "
                             "not real data; $ figure is the model's output for "
                             "one team, not the verified $2.5M/yr program outcome")
    else:
        result = calculate_roi(args.team, args.volume, args.hourly, args.spend)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    r = result
    print("AI Adoption ROI — planning estimate (not a promise of savings)")
    print(f"  Hours saved:            {r['hours_saved_per_month']:,.0f} / mo"
          + (f" ({r['hours_per_person_per_month']:.1f} hrs/person/mo)" if r['hours_per_person_per_month'] is not None else ""))
    print(f"  Gross value:            ${r['gross_value_per_month']:,.0f} / mo")
    print(f"  Net value:              ${r['net_value_per_month']:,.0f} / mo")
    print(f"  $ recovered / yr (net): ${r['recovered_per_year_net']:,.0f}")
    if r['roi_multiple_gross'] is not None:
        import math
        roi_1dp = math.floor(r['roi_multiple_gross'] * 10 + 0.5) / 10  # round-half-up, matches index.html
        print(f"  ROI (gross):            {roi_1dp:.1f}x on AI spend")
    print(f"  Soft spend cap:         ${r['soft_spend_cap_per_month']:,.0f} / mo"
          f" (headroom ${r['headroom_vs_soft_cap']:,.0f})")
    print("  Scenarios (net $/yr):   " + " · ".join(
        f"{name} ${s['yearly']:,.0f}" for name, s in r['scenarios'].items()))
    if result.get("example"):
        print(f"\n  Note: {result['example']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
