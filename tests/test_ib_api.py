import pytest


def test_create_order(ibapi_instance):
    order = ibapi_instance.create_order("STP", 100, 50.0, "OrderRef123")
    assert order.action == "BUY"
    assert order.totalQuantity == 100
    assert order.orderType == "STP"
    assert order.auxPrice == 50.0
    assert order.orderId == ibapi_instance.nextorderId - 1
    assert order.orderRef == "OrderRef123"
    assert not order.transmit


def test_create_stop_loss(ibapi_instance):
    parent_order = ibapi_instance.create_order("LIMIT", 100, 50.0, "ParentOrderRef")
    stop_order = ibapi_instance.create_stop_loss(parent_order, 50, 45.0, "StopOrderRef")
    assert stop_order.action == "SELL"
    assert stop_order.totalQuantity == 50
    assert stop_order.orderType == "STP"
    assert stop_order.auxPrice == 45.0
    assert stop_order.tif == "GTC"
    assert stop_order.orderId == ibapi_instance.nextorderId - 1
    assert stop_order.orderRef == "StopOrderRef"
    assert stop_order.parentId == parent_order.orderId
    assert stop_order.transmit
