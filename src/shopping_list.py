import os
class Product:
    def __init__(self, name, category, weight, hardness):
        self.name = name
        self.category = category
        self.weight = weight
        self.hardness = hardness

    def __repr__(self):
        return f"{self.name} (category: {self.category}, w: {self.weight}, h: {self.hardness})"


class ShoppingList:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)
        self.create_product_indizes_dict()
    
    def create_product_indizes_dict(self):
        # Create a mapping from shopping list item names to their indices in the matrices.
        # 0 -> start
        # 1 -> first product
        # len(shopping_list) -> last product
        # len(shopping_list) + 1 -> end
        product_indizes = {prod.name: idx + 1 for idx, prod in enumerate(self.products)}
        self.product_indizes = product_indizes

    @classmethod
    def from_dict(cls, product_dict):
        """Erstellt ein ShoppingList-Objekt aus einem Dictionary."""
        shopping_list = cls()
        for name, props in product_dict.items():
            shopping_list.add_product(
                Product(
                    name=name,
                    category=props["category"],
                    weight=props["weight"],
                    hardness=props["hardness"]
                )
            )
        shopping_list.create_product_indizes_dict()
        return shopping_list

    def save_to_file(self, filename):
        """Speichert die ShoppingList in eine .txt Datei."""
        # Default folder name
        default_dir = "shopping-lists"
        # If no subdirectory is specified → prepend default_dir
        if "/" not in filename and "\\" not in filename:
            filename = os.path.join(default_dir, filename)
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            for p in self.products:
                f.write(f"{p.name},{p.category},{p.weight},{p.hardness}\n")

    @classmethod
    def load_from_file(cls, filename):
        """Lädt eine ShoppingList aus einer .txt Datei."""
        shopping_list = cls()
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == "":
                    continue
                name, category, weight, hardness = line.strip().split(",")
                shopping_list.add_product(Product(
                    name=name,
                    category=category,
                    weight=int(weight),
                    hardness=int(hardness)
                ))
        shopping_list.create_product_indizes_dict()
        return shopping_list

    def __len__(self):
        return len(self.products)

    def __repr__(self):
        return "\n".join([repr(p) for p in self.products])