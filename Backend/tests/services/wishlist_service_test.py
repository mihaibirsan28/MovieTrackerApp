# test_wishlist_service.py
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from services.wishlist_service import WishlistService
from models import Wishlist


class TestWishlistService:
    def setup_method(self):
        self.db_mock = Mock()
        self.wishlist_service = WishlistService(self.db_mock)
        self.user_id = 1
        self.imdb_movie_id = "tt1234567"
        self.wishlist_id = 100

    def test_create_wishlist_item_success(self):
        self.wishlist_service.create_wishlist_item(self.user_id, self.imdb_movie_id)
        self.db_mock.add.assert_called()
        self.db_mock.commit.assert_called()

    def test_create_wishlist_item_duplicate(self):
        mock_error = IntegrityError("mock statement", {}, "mock orig")

        # Set the side effect of db.add to the mock error
        self.db_mock.add.side_effect = mock_error

        with pytest.raises(HTTPException) as excinfo:
            self.wishlist_service.create_wishlist_item(self.user_id, self.imdb_movie_id)

        assert excinfo.value.status_code == 400

    def test_get_wishlist_item_success(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = Wishlist(id=self.wishlist_id, user_id=self.user_id)
        result = self.wishlist_service.get_wishlist_item(self.wishlist_id, self.user_id)
        assert result.id == self.wishlist_id

    def test_get_wishlist_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.wishlist_service.get_wishlist_item(self.wishlist_id, self.user_id)
        assert excinfo.value.status_code == 404

    def test_update_wishlist_item_success(self):
        wishlist_item_mock = Wishlist(id=self.wishlist_id, user_id=self.user_id, imdb_movie_id="old_id")
        self.db_mock.query.return_value.filter.return_value.first.return_value = wishlist_item_mock

        result = self.wishlist_service.update_wishlist_item(self.wishlist_id, self.user_id, "new_id")
        assert result.imdb_movie_id == "new_id"
        self.db_mock.commit.assert_called()

    def test_update_wishlist_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.wishlist_service.update_wishlist_item(self.wishlist_id, self.user_id, "new_id")
        assert excinfo.value.status_code == 404

    def test_delete_wishlist_item_success(self):
        wishlist_item_mock = Wishlist(id=self.wishlist_id, user_id=self.user_id)
        self.db_mock.query.return_value.filter.return_value.first.return_value = wishlist_item_mock

        result = self.wishlist_service.delete_wishlist_item(self.wishlist_id, self.user_id)
        assert result == wishlist_item_mock
        self.db_mock.delete.assert_called_with(wishlist_item_mock)
        self.db_mock.commit.assert_called()

    def test_delete_wishlist_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.wishlist_service.delete_wishlist_item(self.wishlist_id, self.user_id)
        assert excinfo.value.status_code == 404

    def test_get_all_wishlists(self):
        wishlists_mock = [Wishlist(id=101, user_id=self.user_id), Wishlist(id=102, user_id=self.user_id)]
        self.db_mock.query.return_value.filter.return_value.all.return_value = wishlists_mock

        result = self.wishlist_service.get_all_wishlists(self.user_id)
        assert len(result) == len(wishlists_mock)
        for item in result:
            assert item.user_id == self.user_id
