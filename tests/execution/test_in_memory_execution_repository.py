from execution.in_memory_execution_repository import (
    InMemoryExecutionRepository,
)


def test_save_and_load():
    repo = InMemoryExecutionRepository()

    repo.save("1", {"status": "NEW"})

    assert repo.load("1") == {
        "status": "NEW",
    }


def test_exists():
    repo = InMemoryExecutionRepository()

    repo.save("1", {})

    assert repo.exists("1")


def test_not_exists():
    repo = InMemoryExecutionRepository()

    assert not repo.exists("1")


def test_delete():
    repo = InMemoryExecutionRepository()

    repo.save("1", {})

    repo.delete("1")

    assert not repo.exists("1")


def test_delete_unknown():
    repo = InMemoryExecutionRepository()

    repo.delete("1")

    assert not repo.exists("1")


def test_overwrite():
    repo = InMemoryExecutionRepository()

    repo.save("1", {"a": 1})

    repo.save("1", {"a": 2})

    assert repo.load("1") == {
        "a": 2,
    }
