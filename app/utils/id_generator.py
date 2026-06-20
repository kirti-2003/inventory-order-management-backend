import uuid

def generate_company_id():
    return f"COMP_{uuid.uuid4()}"

def generate_product_id():
    return f"PDT_{uuid.uuid4()}"

def generate_customer_id():
    return f"CST_{uuid.uuid4()}"

def generate_order_id():
    return f"ODR_{uuid.uuid4()}"

def generate_order_item_id():
    return f"ODRIM_{uuid.uuid4()}"

def generate_transaction_id():
    return f"TRAN_{uuid.uuid4()}"