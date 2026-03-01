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
        return shopping_list

    def save_to_file(self, filename):
        """Speichert die ShoppingList in eine .txt Datei."""
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
        return shopping_list

    def __len__(self):
        return len(self.products)

    def __repr__(self):
        return "\n".join([repr(p) for p in self.products])