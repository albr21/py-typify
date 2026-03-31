import pytest
from conftest import (
    Address, Person, Company, OptionalNested
)

class TestTypedCompositionSetattr:
    def test_typed_composition_setattr_valid_replace(self):
        addr1 = Address(street="Old", city="Paris", zip_code="75001")
        addr2 = Address(street="New", city="Lyon", zip_code="69001")
        p = Person(name="Alice", age=30, address=addr1)
        p.address = addr2
        assert p.address.city == "Lyon"

    def test_typed_composition_setattr_invalid_replace(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        p = Person(name="Alice", age=30, address=addr)
        with pytest.raises(TypeError, match="'address'"):
            p.address = "not an address"

    def test_typed_composition_setattr_invalid_replace_dict(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        p = Person(name="Alice", age=30, address=addr)
        with pytest.raises(TypeError, match="'address'"):
            p.address = {"street": "New", "city": "Lyon", "zip_code": "69001"}

    def test_typed_composition_setattr_invalid_replace_none(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        p = Person(name="Alice", age=30, address=addr)
        with pytest.raises(TypeError, match="'address'"):
            p.address = None

    def test_typed_composition_setattr_optional_to_none(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        m = OptionalNested(name="Test", address=addr)
        m.address = None
        assert m.address is None

    def test_typed_composition_setattr_optional_to_value(self):
        m = OptionalNested(name="Test")
        addr = Address(street="New", city="Lyon", zip_code="69001")
        m.address = addr
        assert m.address.city == "Lyon"

    def test_typed_composition_setattr_list_of_objects(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        ceo = Person(name="Bob", age=45, address=addr)
        company = Company(name="Acme", ceo=ceo, employees=[])
        new_emp = Person(name="Eve", age=28, address=addr)
        company.employees = [new_emp]
        assert len(company.employees) == 1
        assert company.employees[0].name == "Eve"

    def test_typed_composition_setattr_list_invalid_item(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        ceo = Person(name="Bob", age=45, address=addr)
        company = Company(name="Acme", ceo=ceo, employees=[])
        with pytest.raises(TypeError, match="'employees'"):
            company.employees = [{"name": "Fake"}]

    def test_typed_composition_setattr_preserves_on_error(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        p = Person(name="Alice", age=30, address=addr)
        with pytest.raises(TypeError):
            p.address = 42
        assert p.address.street == "1"
