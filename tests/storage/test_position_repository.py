from services.position_manager import PositionManager
from storage.position_repository import PositionRepository
from tests.services.test_position_manager import create_position


def test_repository_starts_empty():
    repo = PositionRepository()

    assert repo.count() == 0
    assert repo.all() == []


def test_save_and_get():
    repo = PositionRepository()

    position = create_position()

    repo.save(position)

    assert repo.get(position.position_id) is position


def test_exists_after_save():
    repo = PositionRepository()

    position = create_position()

    repo.save(position)

    assert repo.exists(position.position_id) is True


def test_get_unknown_returns_none():
    repo = PositionRepository()

    assert repo.get("UNKNOWN") is None


def test_exists_unknown_returns_false():
    repo = PositionRepository()

    assert repo.exists("UNKNOWN") is False


def test_delete_existing_position():
    repo = PositionRepository()

    position = create_position()

    repo.save(position)
    repo.delete(position.position_id)

    assert repo.get(position.position_id) is None
    assert repo.count() == 0


def test_delete_unknown_position():
    repo = PositionRepository()

    repo.delete("UNKNOWN")

    assert repo.count() == 0


def test_save_overwrites_existing_position():
    repo = PositionRepository()

    first = create_position()

    second = PositionManager.update_price(
        first,
        first.last_traded_price + 1,
    )

    repo.save(first)
    repo.save(second)

    assert repo.count() == 1
    assert repo.get(first.position_id) is second


def test_all_returns_saved_positions():
    repo = PositionRepository()

    p1 = create_position()
    p2 = create_position()

    repo.save(p1)
    repo.save(p2)

    positions = repo.all()

    assert len(positions) == 2
    assert p1 in positions
    assert p2 in positions


def test_clear_repository():
    repo = PositionRepository()

    repo.save(create_position())

    repo.clear()

    assert repo.count() == 0
    assert repo.all() == []


def test_clear_empty_repository():
    repo = PositionRepository()

    repo.clear()

    assert repo.count() == 0
    assert repo.all() == []


def test_count_tracks_repository_size():
    repo = PositionRepository()

    p1 = create_position()
    p2 = create_position()

    repo.save(p1)
    repo.save(p2)

    assert repo.count() == 2

    repo.delete(p1.position_id)

    assert repo.count() == 1

    repo.clear()

    assert repo.count() == 0
