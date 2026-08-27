def print_final_report(results):
    """Print the final provisioning report and summary counters."""
    results.sort(
        key=lambda item: item["ExcelRow"]
    )

    successful = sum(
        1
        for item in results
        if item["Status"] == "Successful"
    )

    partial = sum(
        1
        for item in results
        if item["Status"] == "Partial"
    )

    failed = sum(
        1
        for item in results
        if item["Status"] == "Failed"
    )

    skipped = sum(
        1
        for item in results
        if item["Status"] == "Skipped"
    )

    already_exists = sum(
        1
        for item in results
        if item.get("Foreman")
        == "Already Exists"
    )

    width = 162

    print("\n" + "=" * width)
    print("FINAL PROVISIONING REPORT")
    print("=" * width)

    print(
        "{:<7} | {:<20} | {:<25} | "
        "{:<10} | {:<14} | {:<10} | "
        "{:<10} | {:<9} | {}".format(
            "ROW",
            "TYPE",
            "LOGICAL NAME",
            "STATUS",
            "FOREMAN",
            "DNS",
            "ANSIBLE",
            "TIME",
            "DETAILS",
        )
    )

    print("-" * width)

    for result in results:
        print(
            "{:<7} | {:<20} | {:<25} | "
            "{:<10} | {:<14} | {:<10} | "
            "{:<10} | {:<9.2f} | {}".format(
                result["ExcelRow"],
                str(
                    result["EquipmentType"]
                )[:20],
                str(
                    result["LogicalName"]
                )[:25],
                result["Status"],
                result.get(
                    "Foreman",
                    "N/A",
                ),
                result.get(
                    "DNS",
                    "N/A",
                ),
                result.get(
                    "Ansible",
                    "N/A",
                ),
                result["TimeSeconds"],
                result["Details"],
            )
        )

    print("=" * width)

    print(
        "TOTAL: {} | SUCCESSFUL: {} | "
        "ALREADY EXISTS: {} | PARTIAL: {} | "
        "FAILED: {} | SKIPPED: {}".format(
            len(results),
            successful,
            already_exists,
            partial,
            failed,
            skipped,
        )
    )

    print("=" * width + "\n")