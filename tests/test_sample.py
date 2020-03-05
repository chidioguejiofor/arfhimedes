from api.models import User

class TestSample:
    def test_basic_setup_works(self):
        assert 1 == 1

    def test_can_make_db_calls(self, init_db):
        assert User.query.count() == 0