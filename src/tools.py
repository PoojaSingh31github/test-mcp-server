"""MCP Tools for mathematical operations, unit conversions, and text processing."""

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.mcpserver import MCPServer


def _validate_finite_number(value: float, param_name: str) -> float:
    """Validate that the given value is a finite number."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"Parameter '{param_name}' must be a number, got {type(value).__name__}.")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"Parameter '{param_name}' must be a finite number.")
    return float(value)


def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number.
        b: Second number.

    Returns:
        The sum of a and b (e.g., 10 + 20 -> 30).
    """
    a_val = _validate_finite_number(a, "a")
    b_val = _validate_finite_number(b, "b")
    result = a_val + b_val
    return int(result) if result.is_integer() else result


def subtract_numbers(a: float, b: float) -> float:
    """Subtract the second number from the first number (a - b).

    Args:
        a: Number to subtract from.
        b: Number to subtract.

    Returns:
        The difference of a and b (e.g., 20 - 5 -> 15).
    """
    a_val = _validate_finite_number(a, "a")
    b_val = _validate_finite_number(b, "b")
    result = a_val - b_val
    return int(result) if result.is_integer() else result


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First factor.
        b: Second factor.

    Returns:
        The product of a and b (e.g., 5 * 6 -> 30).
    """
    a_val = _validate_finite_number(a, "a")
    b_val = _validate_finite_number(b, "b")
    result = a_val * b_val
    return int(result) if result.is_integer() else result


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit.

    Formula: (celsius * 9 / 5) + 32

    Args:
        celsius: Temperature in Celsius (must be >= -273.15 C).

    Returns:
        Temperature in Fahrenheit (e.g., 25 C -> 77 F).
    """
    c_val = _validate_finite_number(celsius, "celsius")
    if c_val < -273.15:
        raise ValueError("Temperature in Celsius cannot be below absolute zero (-273.15 C).")
    result = (c_val * 9.0 / 5.0) + 32.0
    return int(result) if result.is_integer() else round(result, 4)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a temperature from Fahrenheit to Celsius.

    Formula: (fahrenheit - 32) * 5 / 9

    Args:
        fahrenheit: Temperature in Fahrenheit (must be >= -459.67 F).

    Returns:
        Temperature in Celsius (e.g., 77 F -> 25 C).
    """
    f_val = _validate_finite_number(fahrenheit, "fahrenheit")
    if f_val < -459.67:
        raise ValueError("Temperature in Fahrenheit cannot be below absolute zero (-459.67 F).")
    result = (f_val - 32.0) * 5.0 / 9.0
    return int(result) if result.is_integer() else round(result, 4)


def km_to_miles(km: float) -> float:
    """Convert a distance from kilometers to miles.

    Args:
        km: Distance in kilometers (must be non-negative).

    Returns:
        Distance in miles (e.g., 10 km -> approximately 6.21371 miles).
    """
    km_val = _validate_finite_number(km, "km")
    if km_val < 0:
        raise ValueError("Distance in kilometers cannot be negative.")
    result = km_val * 0.621371
    return round(result, 5)


def kg_to_pounds(kg: float) -> float:
    """Convert a mass/weight from kilograms to pounds (lbs).

    Args:
        kg: Mass in kilograms (must be non-negative).

    Returns:
        Weight in pounds (e.g., 10 kg -> approximately 22.0462 lb).
    """
    kg_val = _validate_finite_number(kg, "kg")
    if kg_val < 0:
        raise ValueError("Weight in kilograms cannot be negative.")
    result = kg_val * 2.20462
    return round(result, 4)


def uppercase_text(text: str) -> str:
    """Convert input text to uppercase characters.

    Args:
        text: Input string.

    Returns:
        The uppercase string (e.g., 'hello' -> 'HELLO').
    """
    if not isinstance(text, str):
        raise TypeError(f"Parameter 'text' must be a string, got {type(text).__name__}.")
    return text.upper()


def reverse_text(text: str) -> str:
    """Reverse the characters of the input text.

    Args:
        text: Input string.

    Returns:
        The reversed string (e.g., 'hello' -> 'olleh').
    """
    if not isinstance(text, str):
        raise TypeError(f"Parameter 'text' must be a string, got {type(text).__name__}.")
    return text[::-1]


def count_words(text: str) -> int:
    """Count the number of whitespace-delimited words in the input text.

    Args:
        text: Input string.

    Returns:
        The word count as an integer (e.g., 'hello how are you' -> 4).
    """
    if not isinstance(text, str):
        raise TypeError(f"Parameter 'text' must be a string, got {type(text).__name__}.")
    return len(text.split())


def register_tools(server: "MCPServer") -> None:
    """Register all 10 MCP tools on the server instance."""
    server.tool(
        name="add_numbers",
        description="Add two numbers together (a + b).",
    )(add_numbers)

    server.tool(
        name="subtract_numbers",
        description="Subtract the second number from the first number (a - b).",
    )(subtract_numbers)

    server.tool(
        name="multiply_numbers",
        description="Multiply two numbers together (a * b).",
    )(multiply_numbers)

    server.tool(
        name="celsius_to_fahrenheit",
        description="Convert temperature from Celsius to Fahrenheit ((C * 9/5) + 32).",
    )(celsius_to_fahrenheit)

    server.tool(
        name="fahrenheit_to_celsius",
        description="Convert temperature from Fahrenheit to Celsius ((F - 32) * 5/9).",
    )(fahrenheit_to_celsius)

    server.tool(
        name="km_to_miles",
        description="Convert distance from kilometers to miles (1 km ~ 0.621371 miles).",
    )(km_to_miles)

    server.tool(
        name="kg_to_pounds",
        description="Convert weight from kilograms to pounds (1 kg ~ 2.20462 lb).",
    )(kg_to_pounds)

    server.tool(
        name="uppercase_text",
        description="Convert input text to uppercase characters.",
    )(uppercase_text)

    server.tool(
        name="reverse_text",
        description="Reverse the character order of the input text.",
    )(reverse_text)

    server.tool(
        name="count_words",
        description="Count the total number of words in a text string.",
    )(count_words)
