import subprocess
import sys

def run_step(step_name, script_name):
    print(f"\nRunning {step_name} ({script_name})")
    result = subprocess.run(
        ["python", f"scripts/{script_name}"]
    )
    if result.returncode != 0:
        sys.exit(1)

if __name__ == "__main__":
    run_step("Orders with Items", "orders_with_items.py")
    run_step("Orders + Items + Customers", "ord_itm_cust.py")
    run_step("Add Payments", "ord_pay.py")
    run_step("Add Products", "ord_pay_prod.py")
    run_step("Add Sellers", "ord_prod_sell.py")
    run_step("Cleaning", "clean.py")
    run_step("Transformation", "transform.py")

    print("\nPipeline completed successfully")
