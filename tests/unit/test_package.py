import lachikai


def test_package_has_version() -> None:
    assert lachikai.__version__ == "0.1.0.dev0"
