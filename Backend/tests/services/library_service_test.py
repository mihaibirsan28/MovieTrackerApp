# test_library_service.py
import pytest
from unittest.mock import Mock, create_autospec, MagicMock
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from services.library_service import LibraryService
from models import Library, User

class TestLibraryService:
    def setup_method(self):
        self.db_mock = MagicMock(spec=Session)
        self.library_service = LibraryService(self.db_mock)
        self.user_id = 1
        self.imdb_movie_id = "tt1234567"
        self.library_id = 100

    def test_create_library_item_success(self):
        # Prepare
        self.db_mock.add.return_value = None
        self.db_mock.commit.return_value = None
        self.db_mock.refresh.return_value = None

        # Execute
        result = self.library_service.create_library_item(self.user_id, self.imdb_movie_id)

        # Assert
        added_library_item = self.db_mock.add.call_args[0][0]
        assert added_library_item.user_id == self.user_id
        assert added_library_item.imdb_movie_id == self.imdb_movie_id
        self.db_mock.commit.assert_called_once()

    def test_create_library_item_duplicate(self):
        self.db_mock.add.side_effect = IntegrityError("mock statement", {}, "mock orig")
        with pytest.raises(HTTPException) as excinfo:
            self.library_service.create_library_item(self.user_id, self.imdb_movie_id)
        assert excinfo.value.status_code == 400

    def test_get_library_item_success(self):
        library_item = Library(id=self.library_id, user_id=self.user_id)
        self.db_mock.query.return_value.filter.return_value.first.return_value = library_item
        result = self.library_service.get_library_item(self.library_id, self.user_id)
        assert result == library_item

    def test_get_library_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.library_service.get_library_item(self.library_id, self.user_id)
        assert excinfo.value.status_code == 404

    def test_update_library_item_success(self):
        existing_library_item = Library(id=self.library_id, user_id=self.user_id, imdb_movie_id="old_id")
        self.db_mock.query.return_value.filter.return_value.first.return_value = existing_library_item

        self.library_service.update_library_item(self.library_id, self.user_id, "new_id")
        self.db_mock.commit.assert_called_once()
        assert existing_library_item.imdb_movie_id == "new_id"

    def test_update_library_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.library_service.update_library_item(self.library_id, self.user_id, "new_id")
        assert excinfo.value.status_code == 404

    def test_delete_library_item_success(self):
        library_item_to_delete = Library(id=self.library_id, user_id=self.user_id)
        self.db_mock.query.return_value.filter.return_value.first.return_value = library_item_to_delete

        self.library_service.delete_library_item(self.library_id, self.user_id)
        self.db_mock.delete.assert_called_once_with(library_item_to_delete)
        self.db_mock.commit.assert_called_once()

    def test_delete_library_item_not_found(self):
        self.db_mock.query.return_value.filter.return_value.first.return_value = None
        with pytest.raises(HTTPException) as excinfo:
            self.library_service.delete_library_item(self.library_id, self.user_id)
        assert excinfo.value.status_code == 404

    def test_get_all_libraries(self):
        expected_libraries = [Library(id=1, user_id=self.user_id), Library(id=2, user_id=self.user_id)]
        self.db_mock.query.return_value.filter.return_value.all.return_value = expected_libraries
        result = self.library_service.get_all_libraries(self.user_id)
        assert result == expected_libraries
