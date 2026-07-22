from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from domain.position import Position
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine
from engines.trade_factory import TradeFactory
from services.paper_trading_service import PaperTradingService
from shared.enums import TradeStatus
from tests.test_trade_factory import create_trade


def create_trade():

    market = Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="5m",
        timestamp=datetime.now(),
        open=24990,
        high=25010,
        low=24980,
        close=25000,
        volume=100000,
    )

    indicators = IndicatorSet(
        ema_high=24950,
        ema_low=24850,
        vwap=24900,
        rsi=60,
        volume_average=100000,
    )

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision=decision,
        trades_today=0,
        daily_loss=0,
    )

    return TradeFactory().create(
        risk=risk,
        entry_price=Decimal("25000"),
        stop_loss=Decimal("24950"),
    )


def test_execute_trade():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    assert position.quantity == 65
    assert position.average_price == Decimal("25000")
    assert position.last_traded_price == Decimal("25000")
    assert position.status == TradeStatus.OPEN


def test_update_price():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    updated = service.update_price(
        position,
        Decimal("25025"),
    )

    assert updated.last_traded_price == Decimal("25025")


def test_close_position():

    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    closed = service.close(
        position,
        Decimal("25100"),
    )

    assert closed.status == TradeStatus.CLOSED


def test_close_sets_closed_at():
    service = PaperTradingService()

    position = Position(
        position_id="POS001",
        order=None,
        quantity=1,
        average_price=Decimal("100"),
        last_traded_price=Decimal("100"),
        status=TradeStatus.OPEN,
        opened_at=datetime.now(),
        closed_at=None,
    )

    closed = service.close(
        position,
        Decimal("110"),
    )

    assert closed.closed_at is not None


def test_update_price_preserves_position_id():
    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    updated = service.update_price(
        position,
        Decimal("25050"),
    )

    assert updated.position_id == position.position_id
    assert updated.average_price == position.average_price
    assert updated.quantity == position.quantity
    assert updated.opened_at == position.opened_at


def test_close_preserves_position_data():
    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    closed = service.close(
        position,
        Decimal("25100"),
    )

    assert closed.position_id == position.position_id
    assert closed.quantity == position.quantity
    assert closed.average_price == position.average_price
    assert closed.opened_at == position.opened_at
    assert closed.last_traded_price == Decimal("25100")


def test_paper_trade_lifecycle():
    trade = create_trade()

    service = PaperTradingService()

    position = service.execute(trade)

    position = service.update_price(
        position,
        Decimal("25050"),
    )

    position = service.close(
        position,
        Decimal("25100"),
    )

    assert position.status == TradeStatus.CLOSED
    assert position.last_traded_price == Decimal("25100")
    assert position.closed_at is not None


def test_position_lifecycle():
    service = PaperTradingService()

    trade = create_trade()

    position = service.execute(trade)

    assert position.status == TradeStatus.OPEN

    position = service.update_price(position, 25100)

    assert position.last_traded_price == 25100
    assert position.status == TradeStatus.OPEN

    position = service.close(position, 25200)

    assert position.status == TradeStatus.CLOSED
    assert position.last_traded_price == 25200
    assert position.closed_at is not None


from tests.test_trade_factory import create_trade


def test_update_price_preserves_position_identity():
    service = PaperTradingService()

    trade = create_trade()
    position = service.execute(trade)

    updated = service.update_price(position, 25150)

    assert updated.position_id == position.position_id
    assert updated.quantity == position.quantity
    assert updated.average_price == position.average_price
    assert updated.opened_at == position.opened_at
    assert updated.last_traded_price == 25150


from tests.test_trade_factory import create_trade


def test_close_preserves_position_identity():
    service = PaperTradingService()

    trade = create_trade()
    position = service.execute(trade)

    closed = service.close(position, 25200)

    assert closed.position_id == position.position_id
    assert closed.quantity == position.quantity
    assert closed.average_price == position.average_price
    assert closed.opened_at == position.opened_at
    assert closed.last_traded_price == 25200
    assert closed.closed_at is not None


from shared.enums import TradeStatus
from tests.test_trade_factory import create_trade


def test_execute_initializes_position_correctly():
    service = PaperTradingService()

    trade = create_trade()

    position = service.execute(trade)

    assert position.quantity == trade.quantity
    assert position.average_price == trade.entry_price
    assert position.last_traded_price == trade.entry_price
    assert position.status == TradeStatus.OPEN
    assert position.opened_at is not None


from tests.test_trade_factory import create_trade


def test_update_price_keeps_position_open():
    service = PaperTradingService()

    trade = create_trade()
    position = service.execute(trade)

    updated = service.update_price(position, 25125)

    assert updated.closed_at is None
    assert updated.status == position.status
    assert updated.last_traded_price == 25125


from tests.test_trade_factory import create_trade


def test_close_preserves_average_price():
    service = PaperTradingService()

    trade = create_trade()
    position = service.execute(trade)

    closed = service.close(position, 25250)

    assert closed.average_price == position.average_price
    assert closed.quantity == position.quantity
    assert closed.position_id == position.position_id
    assert closed.status == position.status.CLOSED
