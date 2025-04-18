from django.db import models
from translations.models import Translation
from slugify import slugify


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nombre de la empresa"
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )
    logo = models.ImageField(
        upload_to="logos/", null=True, blank=True, verbose_name="Logo (opcional)"
    )

    class Meta:
        verbose_name_plural = "Empresas"
        verbose_name = "Empresa"

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la ubicación",
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Ubicaciones"
        verbose_name = "Ubicación"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve location name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: Location name in the correct language
        """
        return getattr(self.name, language)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la categoría",
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve category name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: Category name in the correct language
        """
        return getattr(self.name, language)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Nombre de la etiqueta",
    )

    class Meta:
        verbose_name_plural = "Etiquetas"
        verbose_name = "Etiqueta"

    def __str__(self):
        return str(self.name.key)

    def get_name(self, language: str) -> str:
        """Retrieve tag name in the correct language

        Args:
            language (str): Language to retrieve the name in

        Returns:
            str: tag name in the correct language
        """
        return getattr(self.name, language)


class ShortDescription(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.OneToOneField(
        Translation, on_delete=models.CASCADE, verbose_name="Descripción corta"
    )
    details = models.TextField(
        null=True, blank=True, verbose_name="Detalles adicionales"
    )

    class Meta:
        verbose_name_plural = "Descripciones cortas"
        verbose_name = "Descripción corta"

    def __str__(self):
        return self.description.key

    def get_description(self, language: str) -> str:
        """Retrieve short description in the correct language

        Args:
            language (str): Language to retrieve the short description in

        Returns:
            str: Short description in the correct language
        """

        return getattr(self.description, language)


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name="Nombre del vendedor")
    last_name = models.CharField(max_length=255, verbose_name="Apellido del vendedor")
    phone = models.CharField(
        unique=True,
        max_length=255,
        verbose_name="Teléfono del vendedor",
        null=True,
        blank=True,
    )
    has_whatsapp = models.BooleanField(default=False, verbose_name="Tiene WhatsApp")
    email = models.EmailField(
        unique=True, verbose_name="Correo electrónico del vendedor"
    )

    class Meta:
        verbose_name_plural = "Vendedores"
        verbose_name = "Vendedor"

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="Nombre del desarrollo o propiedad", unique=True
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="Slug",
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Empresa"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, verbose_name="Ubicación"
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, verbose_name="Vendedor"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoría"
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="Etiquetas", blank=True, related_name="properties"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    meters = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Metros cuadrados"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si se mostrará en la página",
    )
    featured = models.BooleanField(
        default=False,
        verbose_name="Destacado",
        help_text="Indica si se mostrará en la sección de destacados",
    )
    short_description = models.ForeignKey(
        ShortDescription,
        on_delete=models.CASCADE,
        verbose_name="Descripción corta",
        help_text="Descripción corta de la propiedad o desarrollo",
    )
    google_maps_src = models.TextField(
        null=True,
        blank=True,
        verbose_name="src de Google Maps",
        help_text="Puedes insertar el iframe completo",
    )
    description_es = models.TextField(verbose_name="Descripción en español")
    description_en = models.TextField(verbose_name="Descripción en inglés")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Propiedades"
        verbose_name = "Propiedad"

    def __str__(self):
        return f"{self.name} - {self.location}"

    def save(self, *args, **kwargs):
        """Custom save method"""

        # Generate slug
        self.slug = slugify(self.name)

        # get src from google maps iframe
        if self.google_maps_src:

            if "src=" in self.google_maps_src:
                src_index = self.google_maps_src.index("src=")
                src = self.google_maps_src[src_index:]
                src = src.split('"')[1]
                self.google_maps_src = src

            # Validate if the links its from google maps
            elif "google.com/maps" not in self.google_maps_src:
                self.google_maps_src = None
                raise ValueError(
                    "El Src de Google Maps debe ser un iframe de Google Maps o Src"
                )

        # Call parent save method
        super().save(*args, **kwargs)

    def get_description(self, language: str) -> str:
        """Retrieve description in the correct language

        Args:
            language (str): Language to retrieve the description in

        Returns:
            str: Description in the correct language
        """

        return getattr(self, f"description_{language}")

    def get_price_str(self) -> str:
        """Retrieve price as a string

        Returns:
            str: Price as a 1,000.00 string
        """
        return f"{self.price:,.2f}"


class PropertyImage(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name="Propiedad"
    )
    image = models.ImageField(upload_to="property-images/", verbose_name="Imagen")
    alt_text = models.OneToOneField(
        Translation,
        on_delete=models.CASCADE,
        verbose_name="Texto alternativo",
        help_text="Texto que se mostrará si la imagen no carga (recomendado para SEO)",
    )
    show_gallery = models.BooleanField(default=True, verbose_name="Mostrar en galería")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name_plural = "Imágenes"
        verbose_name = "Imagen"

    def __str__(self):
        return f"{self.property} - {self.alt_text.key}"

    def get_alt_text(self, language: str) -> str:
        """Retrieve alt text in the correct language

        Args:
            language (str): Language to retrieve the alt text in

        Returns:
            str: Alt text in the correct language
        """
        return getattr(self.alt_text, language)
