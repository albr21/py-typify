import pytest
from conftest import (
    Address, Person, Company, Tag, Article, OptionalNested, UnionNested, DeeplyNested
)

class TestTypedCompositionInstantiationValid:
    def test_typed_composition_instantiation_simple_nested(self):
        addr = Address(street="123 Main St", city="Paris", zip_code="75001")
        p = Person(name="Alice", age=30, address=addr)
        assert p.address.city == "Paris"

    def test_typed_composition_instantiation_company_with_employees(self):
        addr = Address(street="1 Rue A", city="Lyon", zip_code="69001")
        ceo = Person(name="Bob", age=45, address=addr)
        emp1 = Person(name="Eve", age=28, address=Address(street="2 Rue B", city="Lyon", zip_code="69002"))
        emp2 = Person(name="Dan", age=35, address=Address(street="3 Rue C", city="Lyon", zip_code="69003"))
        company = Company(name="Acme", ceo=ceo, employees=[emp1, emp2])
        assert company.ceo.name == "Bob"
        assert len(company.employees) == 2
        assert company.employees[0].address.city == "Lyon"

    def test_typed_composition_instantiation_article_with_tags(self):
        addr = Address(street="10 Av X", city="Marseille", zip_code="13001")
        author = Person(name="Claire", age=40, address=addr)
        tags = [Tag(label="python", priority=1), Tag(label="testing", priority=2)]
        article = Article(title="Typify", author=author, tags=tags, metadata={"views": 100})
        assert article.author.name == "Claire"
        assert article.tags[0].label == "python"
        assert article.metadata["views"] == 100

    def test_typed_composition_instantiation_optional_nested_with_value(self):
        addr = Address(street="5 Rue Z", city="Nantes", zip_code="44000")
        m = OptionalNested(name="Test", address=addr)
        assert m.address.city == "Nantes"

    def test_typed_composition_instantiation_optional_nested_none(self):
        m = OptionalNested(name="Test", address=None)
        assert m.address is None

    def test_typed_composition_instantiation_optional_nested_default(self):
        m = OptionalNested(name="Test")
        assert m.address is None

    def test_typed_composition_instantiation_union_nested_person(self):
        addr = Address(street="1 Rue", city="Lille", zip_code="59000")
        person = Person(name="Alice", age=30, address=addr)
        m = UnionNested(owner=person)
        assert m.owner.name == "Alice"

    def test_typed_composition_instantiation_union_nested_company(self):
        addr = Address(street="1 Rue", city="Lille", zip_code="59000")
        ceo = Person(name="Bob", age=50, address=addr)
        company = Company(name="Corp", ceo=ceo, employees=[])
        m = UnionNested(owner=company)
        assert m.owner.name == "Corp"

    def test_typed_composition_instantiation_deeply_nested(self):
        addr = Address(street="HQ", city="Paris", zip_code="75008")
        ceo = Person(name="Marie", age=55, address=addr)
        emp = Person(name="Jean", age=30, address=Address(street="Home", city="Paris", zip_code="75010"))
        company = Company(name="DeepCo", ceo=ceo, employees=[emp])
        deep = DeeplyNested(company=company)
        assert deep.company.ceo.address.city == "Paris"
        assert deep.company.employees[0].name == "Jean"

    def test_typed_composition_instantiation_empty_employees_list(self):
        addr = Address(street="Solo", city="Nice", zip_code="06000")
        ceo = Person(name="Solo", age=40, address=addr)
        company = Company(name="SoloCo", ceo=ceo, employees=[])
        assert company.employees == []

    def test_typed_composition_instantiation_article_empty_tags(self):
        addr = Address(street="1 Rue", city="Paris", zip_code="75001")
        author = Person(name="Max", age=25, address=addr)
        article = Article(title="Empty", author=author, tags=[], metadata={})
        assert article.tags == []

class TestTypedCompositionInvalid:
    def test_typed_composition_instantiation_wrong_nested_type(self):
        with pytest.raises(TypeError, match="'address'"):
            Person(name="Alice", age=30, address={"street": "1", "city": "Paris", "zip_code": "75001"})

    def test_typed_composition_instantiation_wrong_nested_str(self):
        with pytest.raises(TypeError, match="'address'"):
            Person(name="Alice", age=30, address="123 Main St")

    def test_typed_composition_instantiation_wrong_nested_none(self):
        with pytest.raises(TypeError, match="'address'"):
            Person(name="Alice", age=30, address=None)

    def test_typed_composition_instantiation_wrong_ceo_type(self):
        with pytest.raises(TypeError, match="'ceo'"):
            Company(name="Acme", ceo="Bob", employees=[])

    def test_typed_composition_instantiation_wrong_employee_type_in_list(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        ceo = Person(name="Bob", age=45, address=addr)
        with pytest.raises(TypeError, match="'employees'"):
            Company(name="Acme", ceo=ceo, employees=[ceo, "not a person"])

    def test_typed_composition_instantiation_wrong_tag_type_in_list(self):
        addr = Address(street="1", city="Paris", zip_code="75001")
        author = Person(name="Claire", age=40, address=addr)
        with pytest.raises(TypeError, match="'tags'"):
            Article(title="Bad", author=author, tags=[{"label": "x", "priority": 1}], metadata={})

    def test_typed_composition_instantiation_wrong_author_type(self):
        with pytest.raises(TypeError, match="'author'"):
            Article(title="Bad", author="Claire", tags=[], metadata={})

    def test_typed_composition_instantiation_optional_nested_wrong_type(self):
        with pytest.raises(TypeError, match="'address'"):
            OptionalNested(name="Test", address="not an address")

    def test_typed_composition_instantiation_optional_nested_wrong_dict(self):
        with pytest.raises(TypeError, match="'address'"):
            OptionalNested(name="Test", address={"street": "1"})

    def test_typed_composition_instantiation_union_nested_wrong_type(self):
        with pytest.raises(TypeError, match="'owner'"):
            UnionNested(owner="Not a person or company")

    def test_typed_composition_instantiation_union_nested_wrong_dict(self):
        with pytest.raises(TypeError, match="'owner'"):
            UnionNested(owner={"name": "Fake"})

    def test_typed_composition_instantiation_deeply_nested_wrong_type(self):
        with pytest.raises(TypeError, match="'company'"):
            DeeplyNested(company={"name": "Fake"})
