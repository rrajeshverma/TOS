from deployment.dependency_checker import (
    DependencyChecker,
)



def test_empty_dependencies_are_not_ready():

    checker = DependencyChecker()


    assert (
        checker.is_ready()
        is False
    )



def test_all_dependencies_available():

    checker = DependencyChecker()


    checker.register(
        "python",
        True,
    )

    checker.register(
        "dhan_api",
        True,
    )


    assert (
        checker.is_ready()
        is True
    )



def test_missing_dependency_blocks_ready():

    checker = DependencyChecker()


    checker.register(
        "python",
        True,
    )

    checker.register(
        "config",
        False,
    )


    assert (
        checker.is_ready()
        is False
    )



def test_missing_dependencies_are_reported():

    checker = DependencyChecker()


    checker.register(
        "python",
        True,
    )

    checker.register(
        "broker",
        False,
    )


    assert (
        checker.missing()
        == ["broker"]
    )



def test_multiple_missing_dependencies():

    checker = DependencyChecker()


    checker.register(
        "broker",
        False,
    )

    checker.register(
        "database",
        False,
    )


    assert (
        len(
            checker.missing()
        )
        == 2
    )



def test_reset_clears_dependencies():

    checker = DependencyChecker()


    checker.register(
        "python",
        True,
    )


    checker.reset()


    assert (
        checker.is_ready()
        is False
    )
