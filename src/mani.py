import json
from pathlib import Path

from recommendations.underutilized_vm import analyze_vm


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = BASE_DIR / "tests"


def load_json(file_name):
    file_path = TEST_DATA_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    # Load sample data
    vms = load_json("sample_vms.json")
    metrics = load_json("sample_metrics.json")
    costs = load_json("sample_costs.json")

    # Convert metrics and costs into lookup dictionaries
    metrics_by_vm = {
        item["vm_name"]: item
        for item in metrics
    }

    costs_by_vm = {
        item["vm_name"]: item
        for item in costs
    }

    recommendations = []

    for vm in vms:
        vm_name = vm["name"]

        vm_metrics = metrics_by_vm.get(vm_name)
        vm_cost = costs_by_vm.get(vm_name)

        if not vm_metrics or not vm_cost:
            print(f"Skipping {vm_name}: required data is missing.")
            continue

        result = analyze_vm(
            vm,
            vm_metrics,
            vm_cost
        )

        recommendations.append(result)

    # Display results
    print("\n" + "=" * 70)
    print("AZURE COST OPTIMIZATION - VM ANALYSIS")
    print("=" * 70)

    for result in recommendations:
        print(f"\nVM Name        : {result['vm_name']}")
        print(f"Environment    : {result['environment']}")
        print(f"VM Size        : {result['vm_size']}")
        print(f"Monthly Cost   : ₹{result['monthly_cost']:,.2f}")
        print(f"Average CPU    : {result['average_cpu_percent']:.2f}%")
        print(f"Maximum CPU    : {result['maximum_cpu_percent']:.2f}%")
        print(f"Status         : {result['status']}")

        if result["recommendation"]:
            print(f"Recommendation : {result['recommendation']}")

        print("-" * 70)


if __name__ == "__main__":
    main()