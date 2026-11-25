from __future__ import annotations

from typing import Any

from bcsfe import core


class PropertySet:
    """Represents a set of properties in an English property file."""

    def __init__(self, property: str):
        """Initializes a new instance of the PropertySet class.

        Args:
            property (str): Name of the property file.
        """
        self.property = property
        self.path = LocalManager.get_locale_folder().add(property + ".properties")
        self.properties: dict[str, tuple[str, str]] = {}
        self.parse()

    def parse(self):
        """Parses the property file.

        Raises:
            KeyError: If a key is already defined in the property file.
        """
        lines = self.path.read().to_str().splitlines()
        i = 0
        in_multi_line = False
        multi_line_text = ""
        multi_line_key = ""

        while i < len(lines):
            line = lines[i]
            finish_multiline = False
            if (in_multi_line and not line.startswith(">")) or (
                in_multi_line and i == len(lines) - 1
            ):
                in_multi_line = False
                finish_multiline = True
                if multi_line_key in self.properties:
                    raise KeyError(
                        f"Key {multi_line_key} already exists in property file"
                    )
                if line.startswith(">"):
                    multi_line_text += line[1:]
                else:
                    multi_line_text = multi_line_text[:-1]  # remove extra newline
                self.properties[multi_line_key] = (multi_line_text, self.property)
                multi_line_text = ""
                multi_line_key = ""
            if line.startswith("#") or not line:
                i += 1
                continue
            if line.startswith(">") and in_multi_line:
                multi_line_text += line[1:] + "\n"

            parts = line.split("=")
            if line.strip().endswith("="):
                in_multi_line = True
                multi_line_key = parts[0]

            if not in_multi_line and not finish_multiline:
                key = parts[0]
                value = "=".join(parts[1:])
                if key in self.properties:
                    raise KeyError(f"Key {key} already exists in property file")
                self.properties[key] = (value, self.property)

            i += 1

    def get_key(self, key: str) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        return (
            self.properties.get(key, key)[0].replace("\\n", "\n").replace("\\t", "\t")
        )


class LocalManager:
    """Manages the editor's English UI text."""

    def __init__(self):
        """Initializes a new instance of the LocalManager class."""
        self.path = LocalManager.get_locale_folder()
        self.properties: dict[str, PropertySet] = {}
        self.all_properties: dict[str, tuple[str, str]] = {}
        self.parse()

    def parse(self):
        """Parses all property files in the locale folder recursively."""
        for file in self.path.glob("**/*.properties", recursive=True):
            file_name = file.strip_path_from(self.path).path
            property_set = PropertySet(file_name[:-11])
            self.all_properties.update(property_set.properties)
            self.properties[file_name[:-11]] = property_set

    def get_key(self, key: str, escape: bool = True, **kwargs: Any) -> str:
        """Gets a key from the property file.

        Args:
            key (str): Key to get.

        Returns:
            str: Value of the key.
        """
        try:
            text = self.get_key_recursive(key, kwargs, escape)
        except RecursionError:
            text = key

        for kwarg_key, kwarg_value in kwargs.items():
            value = str(kwarg_value)
            if escape:
                value = LocalManager.escape_string(value)
            text = text.replace("{" + kwarg_key + "}", value)

        if "$(" in text:
            text = self.parse_condition(text, kwargs)

        return text

    def parse_condition(self, text: str, kwargs: dict[str, Any]) -> str:
        counter = 0
        final_text = ""
        in_expression = False
        expression_text = ""
        count_down = 0
        while counter < len(text):
            char = text[counter]
            if counter == len(text) - 1:
                final_text += char
                break
            next_char = text[counter + 1]
            if char == "\\":
                final_text += next_char
                counter += 2
                continue
            if char == "$" and next_char == "(":
                count_down = 0
                in_expression = True
            elif char == "/" and next_char == "$":
                count_down = 2
                in_expression = False
                if len(expression_text) < 3:
                    counter += 1
                    continue
                new_expression_text = expression_text[2:-1]
                expression_text = ""
                parts = new_expression_text.split(":")
                if len(parts) < 2:
                    counter += 1
                    continue
                keyword = parts[0].strip()
                expression = parts[1].strip()
                conditions = expression.split("$,")
                string = ""
                for i, condition in enumerate(conditions):
                    condition = condition.strip()
                    if not condition:
                        continue
                    if i == len(conditions) - 1:
                        string = condition
                        break
                    condition_parts = condition.split("($")
                    if len(condition_parts) < 2:
                        continue
                    logic = condition_parts[0].strip()
                    word = condition_parts[1].strip()
                    if not word:
                        continue
                    word = word[:-1]
                    value = kwargs.get(keyword)
                    if value is None:
                        continue
                    equality = None
                    if logic.startswith("=="):
                        equality = "=="
                    elif logic.startswith("!="):
                        equality = "!="
                    elif logic.startswith(">="):
                        equality = ">="
                    elif logic.startswith("<="):
                        equality = "<="
                    elif logic.startswith(">"):
                        equality = ">"
                    elif logic.startswith("<"):
                        equality = "<"
                    if equality is None:
                        continue
                    logic_parts = logic.split(equality)
                    if len(logic_parts) < 2:
                        continue
                    logic_value = logic_parts[1].strip()

                    if isinstance(value, int):
                        if not logic_value.isdigit():
                            continue
                        logic_value = int(logic_value)

                    if equality == "==":
                        if logic_value == value:
                            string = word
                            break
                    elif equality == "!=":
                        if logic_value != value:
                            string = word
                            break

                    if isinstance(logic_value, int) and not string:
                        if equality == ">":
                            if logic_value > value:
                                string = word
                                break
                        elif equality == ">=":
                            if logic_value >= value:
                                string = word
                                break
                        elif equality == "<":
                            if logic_value < value:
                                string = word
                                break
                        elif equality == "<=":
                            if logic_value <= value:
                                string = word
                                break

                final_text += string

            if in_expression:
                expression_text += char
            else:
                if count_down <= 0:
                    final_text += char
                else:
                    count_down -= 1

            counter += 1

        return final_text

    @staticmethod
    def get_special_chars() -> list[str]:
        return ["<", ">", "/"]

    @staticmethod
    def escape_string(string: str) -> str:
        for char in LocalManager.get_special_chars():
            string = string.replace(char, "\\" + char)
        return string

    def get_key_recursive(
        self,
        key: str,
        kwargs: dict[str, Any],
        escape: bool = True,
        properties: dict[str, tuple[str, str]] | None = None,
    ) -> str:
        if properties is None:
            properties = self.all_properties
        value = properties.get(key, (key, key))
        value = value[0].replace("\\n", "\n").replace("\\t", "\t")
        # replace {{key}} with the value of the key
        if "{{" not in value:
            return value
        char_index = 0
        while char_index < len(value):
            if value[char_index] == "{" and value[char_index + 1] == "{":
                key_name = ""
                char_index += 2
                while value[char_index] != "}":
                    key_name += value[char_index]
                    char_index += 1

                if key_name != key:
                    value = value.replace(
                        "{{" + key_name + "}}",
                        self.get_key(key_name, escape, **kwargs),
                    )
            char_index += 1

        return value

    @staticmethod
    def get_all_aliases(value: str) -> list[str]:
        """Gets all aliases from a string. Aliases are separated by |.

        Args:
            value (str): String to get aliases from.

        Returns:
            list[str]: List of aliases.
        """
        if "|" not in value:
            return [value]
        i = 0
        aliases: list[str] = []
        while i < len(value):
            char = value[i]
            prev_char = value[i - 1] if i > 0 else ""
            if char == "|" and prev_char != "\\":
                aliases.append(value[:i])
                value = value[i + 1 :]
                i = 0
            i += 1

        aliases.append(value)
        return aliases

    @staticmethod
    def get_locales_folder() -> core.Path:
        """Gets the locales folder.

        Returns:
            core.Path: Path to the locales folder.
        """
        return core.Path.get_data_folder().add("locales")

    @staticmethod
    def get_locale_folder() -> core.Path:
        """Gets the folder for the English locale.

        Returns:
            core.Path: Path to the English locale folder.
        """
        return LocalManager.get_locales_folder().add("en")
