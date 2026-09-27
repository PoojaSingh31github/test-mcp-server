"""MCP Prompts providing structured AI generation templates."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.mcpserver import MCPServer


def _validate_non_empty_string(value: str, param_name: str) -> str:
    """Validate that the given parameter is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"Parameter '{param_name}' must be a string, got {type(value).__name__}.")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"Parameter '{param_name}' cannot be empty or whitespace-only.")
    return cleaned


def prompt_summarize_text(text: str) -> str:
    """Generate a prompt instructing an LLM to summarize text.

    Args:
        text: The source text to summarize.

    Returns:
        Structured LLM prompt.
    """
    valid_text = _validate_non_empty_string(text, "text")
    return (
        "You are an expert editor and summarizer. Please provide a clear, concise, and structured summary "
        "of the following text. Highlight the key takeaways, main arguments, and actionable points.\n\n"
        f"--- TEXT TO SUMMARIZE ---\n{valid_text}\n-------------------------\n\n"
        "Provide your summary in Markdown with bullet points where appropriate."
    )


def prompt_translate_text(text: str, language: str) -> str:
    """Generate a prompt instructing an LLM to translate text.

    Args:
        text: The text to translate.
        language: The target language.

    Returns:
        Structured LLM prompt.
    """
    valid_text = _validate_non_empty_string(text, "text")
    valid_lang = _validate_non_empty_string(language, "language")
    return (
        f"You are a professional multilingual translator. Please translate the following text into {valid_lang}.\n"
        "Ensure natural phrasing, cultural accuracy, and appropriate tone while strictly preserving the original meaning.\n\n"
        f"--- ORIGINAL TEXT ---\n{valid_text}\n---------------------\n\n"
        f"Target Language: {valid_lang}\n"
        "Output only the translated text followed by a brief translation note if any idioms were adapted."
    )


def prompt_explain_code(code: str) -> str:
    """Generate a beginner-friendly code explanation prompt.

    Args:
        code: The code snippet to explain.

    Returns:
        Structured LLM prompt.
    """
    valid_code = _validate_non_empty_string(code, "code")
    return (
        "You are a friendly and patient programming instructor. Please explain the following code in a clear, "
        "beginner-friendly manner.\n\n"
        "Breakdown requirements:\n"
        "1. High-Level Summary: What does this code do in simple terms?\n"
        "2. Step-by-Step Walkthrough: Explain each significant block/line.\n"
        "3. Key Concepts: Highlight programming concepts, libraries, or algorithms used.\n"
        "4. Example Execution: Trace the execution with sample inputs and outputs.\n\n"
        f"```\n{valid_code}\n```"
    )


def prompt_review_code(code: str) -> str:
    """Generate a comprehensive code-review prompt.

    Args:
        code: The code snippet to review.

    Returns:
        Structured LLM prompt covering bugs, security, performance, maintainability, and quality.
    """
    valid_code = _validate_non_empty_string(code, "code")
    return (
        "You are a Principal Software Engineer performing a rigorous code review. "
        "Review the following code snippet thoroughly across these dimensions:\n\n"
        "1. Bugs & Logic Errors: Identify defects, boundary issues, or off-by-one errors.\n"
        "2. Potential Issues: Edge cases, unexpected null/empty handling, concurrency risks.\n"
        "3. Security: Injection risks, data exposure, insecure practices, unsafe deserialization.\n"
        "4. Performance & Efficiency: Time/space complexity, resource leaks, optimization opportunities.\n"
        "5. Maintainability & Readability: Clean code principles, naming conventions, docstrings.\n"
        "6. Actionable Recommendations: Provide refactored code snippets with improvements.\n\n"
        f"```\n{valid_code}\n```"
    )


def prompt_generate_email(purpose: str, recipient: str, details: str) -> str:
    """Generate a professional email-writing prompt.

    Args:
        purpose: The objective of the email.
        recipient: The intended recipient (name or role).
        details: Specific points or context to include.

    Returns:
        Structured LLM prompt.
    """
    valid_purpose = _validate_non_empty_string(purpose, "purpose")
    valid_recipient = _validate_non_empty_string(recipient, "recipient")
    valid_details = _validate_non_empty_string(details, "details")
    return (
        "You are an executive communications specialist. Draft a polished, professional email based on the following details:\n\n"
        f"- Recipient: {valid_recipient}\n"
        f"- Purpose: {valid_purpose}\n"
        f"- Context & Details:\n{valid_details}\n\n"
        "Structure the output with:\n"
        "- Subject Line (compelling, concise)\n"
        "- Salutation\n"
        "- Well-organized body paragraphs\n"
        "- Clear Call to Action (CTA)\n"
        "- Professional sign-off"
    )


def prompt_generate_blog(topic: str) -> str:
    """Generate a prompt for creating a structured blog article.

    Args:
        topic: The topic of the blog post.

    Returns:
        Structured LLM prompt.
    """
    valid_topic = _validate_non_empty_string(topic, "topic")
    return (
        f"You are an expert technical content writer and SEO copywriter. Write a comprehensive, high-quality blog article on the topic: '{valid_topic}'.\n\n"
        "Include the following structure:\n"
        "1. Engaging Title (optimized for curiosity and SEO)\n"
        "2. Introduction with a strong hook, problem statement, and roadmap\n"
        "3. Body Sections with descriptive H2 and H3 headings, practical examples, and clear explanations\n"
        "4. Key Takeaways or Best Practices summary box\n"
        "5. Conclusion with thought-provoking summary and Call-to-Action (CTA)\n\n"
        "Format entirely in Markdown."
    )


def prompt_fix_grammar(text: str) -> str:
    """Generate a prompt that fixes grammar while preserving meaning.

    Args:
        text: The text to correct.

    Returns:
        Structured LLM prompt.
    """
    valid_text = _validate_non_empty_string(text, "text")
    return (
        "You are an expert copyeditor. Please review and correct the following text for grammar, spelling, punctuation, syntax, and phrasing.\n"
        "Strict Guidelines:\n"
        "- Preserve the author's original voice, style, and meaning without rewriting unnecessarily.\n"
        "- Present the corrected version cleanly.\n"
        "- List the key corrections made in a concise bullet-point summary.\n\n"
        f"--- ORIGINAL TEXT ---\n{valid_text}\n---------------------"
    )


def prompt_create_test_cases(code: str) -> str:
    """Generate a prompt for generating a complete test suite.

    Args:
        code: The code to test.

    Returns:
        Structured LLM prompt covering happy path, edge cases, invalid inputs, and assertions.
    """
    valid_code = _validate_non_empty_string(code, "code")
    return (
        "You are a Quality Assurance and Software Testing expert. Create a comprehensive, production-grade test suite for the following code.\n\n"
        "Organize the test suite into:\n"
        "1. Happy-Path Tests: Standard inputs with expected successful outcomes.\n"
        "2. Edge-Case Tests: Boundary conditions, empty strings, zero/negative values, large datasets, type limits.\n"
        "3. Invalid-Input & Error-Handling Tests: Malformed inputs, wrong types, raised exceptions.\n"
        "4. Expected Results Table: Clear mapping of Test Name | Input | Expected Output | Assertion Type.\n\n"
        f"```\n{valid_code}\n```"
    )


def prompt_explain_error(error: str) -> str:
    """Generate a prompt explaining an error message and troubleshooting steps.

    Args:
        error: The error message or stack trace.

    Returns:
        Structured LLM prompt.
    """
    valid_error = _validate_non_empty_string(error, "error")
    return (
        "You are a Senior Debugging and Systems Engineer. Analyze the following error message or stack trace:\n\n"
        f"```\n{valid_error}\n```\n\n"
        "Provide a structured diagnostic breakdown:\n"
        "1. Meaning: Explain what this error means in plain English.\n"
        "2. Root Causes: List the most probable causes (configuration, logic, environment, dependencies).\n"
        "3. Step-by-Step Resolution: Provide specific, actionable steps to diagnose and fix the issue.\n"
        "4. Code Fix Examples: Provide before-and-after code snippets illustrating the correction."
    )


def prompt_generate_sql(requirement: str) -> str:
    """Generate a prompt that asks an LLM to produce SQL plus explanation.

    Args:
        requirement: The database query requirement.

    Returns:
        Structured LLM prompt.
    """
    valid_requirement = _validate_non_empty_string(requirement, "requirement")
    return (
        "You are an expert Database Administrator and SQL Specialist. Generate a high-performance SQL query satisfying the following requirement:\n\n"
        f"Requirement: {valid_requirement}\n\n"
        "Please provide:\n"
        "1. The complete SQL query with clean syntax, proper indentation, and standard ANSI SQL conventions.\n"
        "2. Query Breakdown: Explanation of clauses, joins, aggregations, filtering, and indexing considerations.\n"
        "3. Schema Assumptions: Explicitly list any assumed table schemas, column names, data types, and foreign key relationships."
    )


def register_prompts(server: "MCPServer") -> None:
    """Register all 10 MCP prompts on the server instance."""
    server.prompt(
        name="summarize_text",
        description="Generate a prompt instructing an LLM to summarize the supplied text.",
    )(prompt_summarize_text)

    server.prompt(
        name="translate_text",
        description="Generate a prompt instructing an LLM to translate text into a specified language.",
    )(prompt_translate_text)

    server.prompt(
        name="explain_code",
        description="Generate a beginner-friendly code explanation prompt.",
    )(prompt_explain_code)

    server.prompt(
        name="review_code",
        description="Generate a comprehensive code-review prompt covering bugs, security, performance, and quality.",
    )(prompt_review_code)

    server.prompt(
        name="generate_email",
        description="Generate a professional email-writing prompt given purpose, recipient, and details.",
    )(prompt_generate_email)

    server.prompt(
        name="generate_blog",
        description="Generate a prompt for creating a structured, SEO-friendly blog article.",
    )(prompt_generate_blog)

    server.prompt(
        name="fix_grammar",
        description="Generate a prompt that fixes grammar, spelling, and phrasing while preserving original meaning.",
    )(prompt_fix_grammar)

    server.prompt(
        name="create_test_cases",
        description="Generate a prompt for creating comprehensive test suites (happy-path, edge-cases, invalid inputs).",
    )(prompt_create_test_cases)

    server.prompt(
        name="explain_error",
        description="Generate a prompt explaining error messages, probable root causes, and resolution steps.",
    )(prompt_explain_error)

    server.prompt(
        name="generate_sql",
        description="Generate a prompt that asks an LLM to produce SQL plus explanation and schema assumptions.",
    )(prompt_generate_sql)
