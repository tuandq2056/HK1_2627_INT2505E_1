def v1_create_order(body):
    return {
        "order_id": "ord_v1_1001",
        "version": "v1",
        "account_id": body.get("account_id"),
        "status": "created_via_v1",
    }


def v2_create_order(body):
    return {
        "order_id": "ord_v2_2002",
        "version": "v2",
        "account_id": body.get("account_id"),
        "status": "created_via_v2",
        "features": ["express_delivery", "fraud_protection"],
    }
