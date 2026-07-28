from execution.broker_confirmation import (
    BrokerConfirmationValidator,
)



def test_successful_broker_response_is_confirmed():

    validator = BrokerConfirmationValidator()


    response = {
        "status": "success",
        "orderId": "DHAN123",
    }


    assert (
        validator.is_confirmed(
            response
        )
        is True
    )



def test_missing_response_is_rejected():

    validator = BrokerConfirmationValidator()


    assert (
        validator.is_confirmed(
            None
        )
        is False
    )



def test_missing_order_id_is_rejected():

    validator = BrokerConfirmationValidator()


    response = {
        "status": "success",
    }


    assert (
        validator.is_confirmed(
            response
        )
        is False
    )



def test_failed_status_is_rejected():

    validator = BrokerConfirmationValidator()


    response = {
        "status": "failed",
        "orderId": "DHAN123",
    }


    assert (
        validator.is_confirmed(
            response
        )
        is False
    )



def test_invalid_response_type_is_rejected():

    validator = BrokerConfirmationValidator()


    assert (
        validator.is_confirmed(
            "SUCCESS"
        )
        is False
    )



def test_confirmation_requires_success_status():

    validator = BrokerConfirmationValidator()


    response = {
        "status": "pending",
        "orderId": "DHAN123",
    }


    assert (
        validator.is_confirmed(
            response
        )
        is False
    )
