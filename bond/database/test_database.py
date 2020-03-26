from bond.database import BondDatabase


def test_database_get_and_set():
    for i in range(5):
        BondDatabase.set("test", i)
        assert BondDatabase().get("test") == i
