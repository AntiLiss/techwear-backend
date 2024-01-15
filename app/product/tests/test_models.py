from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from product.models import (
    Category,
    Product,
    generate_product_image_path,
    Property,
)


def create_category(name="sample category"):
    return Category.objects.create(name=name)


def create_property(name="color", value="white"):
    """Create Property instance"""
    return Property.objects.create(name=name, value=value)


def create_product(category, **fields):
    default_fields = {
        "name": "testname",
        "description": "some desc",
        "brand": "test brand",
        "price": Decimal("100.99"),
        "stock": 100,
    }
    default_fields.update(**fields)
    return Product.objects.create(category=category, **default_fields)


class CategoryModelTests(TestCase):
    """Test Category model"""

    def test_create_category(self):
        """Test creating Category instance"""
        category_name = "sample category"
        category = create_category(category_name)

        self.assertEqual(str(category), category_name)


class ProductModelTests(TestCase):
    """Test Product model"""

    def test_create_product(self):
        """Test creating Product instance"""
        category = create_category()
        product_name = "sample product"
        product = create_product(name=product_name, category=category)

        self.assertEqual(str(product), product_name)

    @patch("product.models.uuid4")
    def test_product_image_uuid(self, mock_uuid):
        """Test generating product image path"""
        sample_uuid = "sample-uuid"
        mock_uuid.return_value = sample_uuid
        image_path = generate_product_image_path(None, "example.jpg")

        self.assertEqual(image_path, f"uploads/product/{sample_uuid}.jpg")

    def test_product_prop_name_duplication(self):
        """Test product can't have more than one prop with the same name"""
        category = create_category()
        product = create_product(category=category)
        color_red = create_property("color", "red")
        # Ensure prop name case doesn't matter
        color_blue = create_property("COLOR", "blue")

        # Should raise error cuz product can't have
        # two props with the same name
        with self.assertRaises(ValueError):
            product.properties.add(color_red, color_blue)


class PropertyModelTests(TestCase):
    """Test Property model"""

    def test_create_product_property(self):
        """Test creation of Property model instance"""
        fields = {
            "name": "color",
            "value": "red",
        }
        product_property = create_property(**fields)

        self.assertEqual(
            str(product_property),
            f"{product_property.name} {product_property.value}",
        )

    def test_entry_duplication_error(self):
        """
        Test case-insensitive duplication of properties raises error
        """
        with self.assertRaises(ValueError):
            create_property(name="Fabric", value="Cotton")
            create_property(name="FABRIC", value="COTTON")