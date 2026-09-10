# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from langchain_core.tools import tool 
from app.database import db

# =========================================================================================
#                                        Tools Statements
# =========================================================================================

@tool 
def get_invoices_by_customer_sorted_by_date(customer_id : str) -> list[dict]:
    """
        Look up all invoices for a customer, sorted by invoice data(newest first).
    """
    return db.run(
        f"SELECT * FROM Invoice WHERE CustomerId = {customer_id} ORDER BY InvoiceDate DESC;"
    )


@tool 
def get_invoices_sorted_by_unit_price(customer_id : str) -> list[dict]:
    """
        Look up all invoices for a customer, sorted by unit price (highest first)
    """
    query = f"""
        SELECT Invoice.* , InvoiceLine.UnitPrice
        FROM Invoice
        JOIN InvoiceLine On Invoice.InvoiceId = InvoiceLine.InvoiceId
        WHERE Invoice.CustomerId = {customer_id}
        ORDER BY InvoiceLine.UnitPrice DESC;
    """
    return db.run(query)

@tool
def get_employee_by_invoice_and_customer(invoice_id : str , customer_id : str) -> dict:
    """
        Return the support employee associated with a given invoice + customer.
    """
    query = f"""
        SELECT Employee.FirstName, Employee.Title, Employee.Email
        FROM Employee
        JOIN Customer ON Customer.SupportRepId = Employee.EmployeeId
        JOIN Invoice ON Invoice.CustomerId = Customer.CustomerId
        WHERE Invoice.InvoiceId = ({invoice_id}) AND Invoice.CustomerId = ({customer_id})
    """
    employee_info = db.run(query , include_columns=True)

    if not employee_info:
        return f"No employee found for invoice ID {invoice_id} and customer identifier {customer_id}."
    return employee_info


invoice_tools = [
    get_invoices_by_customer_sorted_by_date,
    get_invoices_sorted_by_unit_price,
    get_employee_by_invoice_and_customer
]