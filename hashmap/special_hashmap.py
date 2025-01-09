class SpecialHashMap:
    def __init__(self):
        self.map = {}

    def insert(self, key, value):
        """Добавляет ключ и значение в карту."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        self.map[key] = value

    def get(self, key):
        """Возвращает значение по ключу."""
        if key not in self.map:
            raise KeyError(f"Key '{key}' not found.")
        return self.map[key]

    def delete(self, key):
        """Удаляет ключ и значение из карты."""
        if key not in self.map:
            raise KeyError(f"Key '{key}' not found.")
        del self.map[key]

    def iloc(self, index):
        """Возвращает значение по порядковому индексу ключа."""
        sorted_keys = self.toSortedSet()
        if index < 0 or index >= len(sorted_keys):
            raise IndexError("Index out of range.")
        key = sorted_keys[index]
        return self.map[key]

    def ploc(self, condition):
        """Возвращает подмножество ключей и значений, удовлетворяющих условию."""
        def _apply_condition(key, value, condition):
            operator, threshold = self._parse_condition(condition)
            if operator == ">":
                return value > threshold
            elif operator == ">=":
                return value >= threshold
            elif operator == "<":
                return value < threshold
            elif operator == "<=":
                return value <= threshold
            elif operator == "==":
                return value == threshold
            elif operator == "!=":
                return value != threshold
            else:
                raise ValueError(f"Invalid operator in condition: {operator}")

        result = {}
        for key, value in self.map.items():
            if _apply_condition(key, value, condition):
                result[key] = value
        return result

    def _parse_condition(self, condition):
        """Парсит условие вида '>10', возвращая оператор и значение."""
        operators = [">=", "<=", ">", "<", "==", "!="]
        for operator in operators:
            if condition.startswith(operator):
                try:
                    threshold = float(condition[len(operator):])
                    return operator, threshold
                except ValueError:
                    raise ValueError(f"Invalid threshold value in condition: {condition}")
        raise ValueError(f"Invalid condition format: {condition}")

    def toSortedSet(self):
        """Возвращает отсортированные ключи как Set."""
        def key_sort_function(key):
            try:
                return tuple(map(float, key.split(',')))
            except ValueError:
                return tuple(key.split(','))
        return sorted(self.map.keys(), key=key_sort_function)
