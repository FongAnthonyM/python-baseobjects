# Anthony's Python Style Guide: Package Tutorials

## Table of Contents

- [1 Background](#1-background)
- [2 Jupyter Notebook](#2-jupyter-notebook)
- [3 Directory Hierarchy](#3-directory-hierarchy)
- [4 Package Tutorial Notebook Structure](#4-package-tutorial-notebook-structure)
  - [4.1 Title and Introduction](#41-title-and-introduction)
  - [4.2 Installation](#42-installation)
  - [4.3 Importing the Package](#43-importing-the-package)
  - [4.4 Core Concepts & Basic Usage](#44-core-concepts--basic-usage)
  - [4.5 Advanced Features](#45-advanced-features)
  - [4.6 Examples](#46-examples)
  - [4.7 API Highlights](#47-api-highlights)
  - [4.8 Troubleshooting / FAQs](#48-troubleshooting--faqs)
  - [4.9 Conclusion and Next Steps](#49-conclusion-and-next-steps)
- [5 Content Guidelines](#5-content-guidelines)
  - [5.1 Define The Audience and Scope](#51-define-the-audience-and-scope)
  - [5.2 Language](#52-language)
  - [5.3 Logical Flow](#53-logical-flow)
  - [5.4 Markdown Cells](#54-markdown-cells)
- [6 Formatting and Style](#6-formatting-and-style)
  - [6.1 Headings](#61-headings)
  - [6.2 Code Blocks](#62-code-blocks)
  - [6.3 Emphasis](#63-emphasis)
  - [6.4 Lists](#64-lists)
  - [6.5 Links](#65-links)
- [7 Tips for Effectiveness](#7-tips-for-effectiveness)


## 1 Background

A tutorial is a step-by-step guide to a specific topic. It provides a clear and concise explanation of the topic, 
demonstrating the functionality and use cases. It is designed to be self-contained and easy to follow.
However, the purpose of a tutorial is to not only educate users on functionality but also provide inspiration for new 
approaches to solving problems.

This document provides comprehensive guidelines for creating effective Jupyter Notebook tutorials for Python packages.

It outlines best practices for structuring tutorials, defining the target audience, presenting code examples, formatting 
content, and leveraging Jupyter Notebook features. These guidelines help developers create clear, accessible, and 
educational tutorials that enable users to quickly understand and effectively use the packages, enhancing the overall 
user experience and adoption of the project's components.


## 2 Jupyter Notebook

Jupyter Notebooks are a powerful tool for creating interactive tutorials. They allow users to combine text, code, and 
visualizations into a single document. They are ideal for educational purposes, as they provide a clear and concise 
explanation of a topic, demonstrating the functionality and use cases.

When creating a tutorial, it is important to consider an report the following:
- **Kernel Choice:** Specify if needed.
- **Magic Commands:** Explain any used.


## 3 Directory Hierarchy

Tutorials should be organized in a directory structure that mirrors the package structure. This makes it easy for users 
to find tutorials relevant to the specific components they're interested in.

- Each major package should have its own directory under the `tutorials/` directory
- Subpackages should have their own subdirectories when they contain multiple components
- Typically, there should be a single tutorial for each major package and subpackage, but there may be exceptions
- Filenames should start with descriptive name followed by `_package_tutorial` (e.g., `name_package_tutorial.py`)
- Use the format `<component_name>_package_tutorial.py` for individual component tutorials
- For tutorials that demonstrate multiple components working together, use a descriptive name that indicates the functionality being demonstrated, e.g., `caching_with_sentinel_tutorial.py`
- Use lowercase with underscores for file names (snake_case)

Example:
```
tutorials/
  bases/                          # Tutorials for the bases package
    collections/                  # Tutorials for the bases.collections subpackage
      collections_package_tutorial.py
    bases_package_tutorial.py
  cachingtools/                 # Tutorials for the cachingtools package
    cachingtools_package_tutorial.py
  baseobjects_package_tutorial.py
```


## 4 Package Tutorial Notebook Structure

A clear and logical flow is essential. These sections are recommended:

1. Title and Introduction
2. Installation
3. Importing the Package
4. Core Concepts & Basic Usage
5. Advanced Features
6. Examples
7. API Highlights
8. Troubleshooting / FAQs


### 4.1 Title and Introduction

The Title and Introduction section sets the stage for the package's tutorial. It should provide users with a clear
understanding of what they will learn and how this package fits into the larger package ecosystem. This section serves as 
the entry point to the tutorial and should be engaging while remaining informative and concise.

- Formatting: Markdown Cell
- Clear Title: "Using [PackageName]", "[PackageName] for [Specific Task]", etc.
- Brief Overview: 
    - Explain the package's primary responsibilities and features.
    - Explain how this package relates to the parent package.
    - Explain what will be covered in this tutorial.
    - Briefly summarize the prerequisites.
- Table of Contents (Optional but Recommended): Markdown links to major sections within this package tutorial.


### 4.2 Installation

The Installation section provides clear instructions for setting up the package in the user's environment. This section
should be straightforward and cover both standard and alternative installation methods, ensuring users can successfully
install the package regardless of their setup.

- Formatting: Markdown and Code Cells
- Instructions: Clear, step-by-step installation instructions using pip or conda.
    ```python
    # !pip install your-package-name
    # or
    # !conda install -c your-channel your-package-name
    ```
- Dependencies: Mention any critical dependencies if they are not automatically handled.
- Verification (Optional):** A small code snippet to verify successful installation.

If the package tutorial is a subpackage, an Installation section is not required.


### 4.3 Importing the Package

The Importing the Package section demonstrates the proper way to import and access the package's functionality. This
section should clearly show users the standard import patterns and any alternative import styles that might be useful for
different use cases. It's essential to explain any naming conventions or common aliases used in the package's ecosystem.

- Formatting: Markdown and Code Cells
- Show the standard way to import the package or its key subpackages.

Example:
```python
import package_name
# or
from package_name import specific_package
# or
import package_name as alias
```


### 4.4 Core Concepts & Basic Usage

The Core Concepts & Basic Usage section introduces users to the fundamental building blocks and primary functionality of
the package. This section forms the foundation of the tutorial, ensuring users understand the essential concepts before
moving on to more advanced features. Here, users learn the basic operations and typical usage patterns that form the
core of working with the package.

- Formatting: Markdown and Code Cells
- Introduce the fundamental concepts and objects of the package.
- Provide simple, executable examples for the most common use cases.
- Explain the basic operations and typical usage patterns.
- Give a brief overview of the key modules in the package and direct users to view the module tutorials rather than 
  going into detail.
- Explain each code cell:
    - What the code does.
    - Why it's done that way.
    - The expected output (and show it, by running the cell).


### 4.5 Advanced Features

The Advanced Features section introduces users to more advanced features of the package. This section provides users
with a deeper understanding of the package's capabilities and provides a deeper understanding of the package's
functionality. It's important to provide users with a deeper understanding of the package's functionality and
capabilities, so they can make informed decisions when using the package.

- Formatting: Markdown and Code Cells
- Introduce more complex functionalities, options, or configurations.
- Break down complex examples into smaller, understandable steps.
- Clearly explain the parameters and their impact.


### 4.6 Examples

The Examples section demonstrates how the package can be used to solve real-world problems. This section provides users 
with a concrete example of how the package can be used to solve a real-world problem. It's important to provide users 
with a concrete example of how the package can be used to solve a real-world problem, so they can make informed 
decisions when using the package.

- Formatting: Markdown and Code Cells
- Showcase how the package can be used to solve real-world problems.
- This section helps users understand the package's value and applicability.
- If possible, use a small, relatable dataset or scenario.


### 4.7 API Highlights

The API Highlights section provides users with a quick overview of the package's API. This section provides users with
a quick overview of the package's API and provides a quick reference for users to quickly access the package's
functionality. It's important to provide users with a quick overview of the package's API and provide a quick reference
for users to quickly access the package's functionality, so they can make informed decisions when using the package.

- Formatting: Markdown Cell
- Briefly mention key functions/classes and their purpose.
- Provide a link to the full API documentation. Avoid replicating the entire API reference here.


### 4.8 Troubleshooting / FAQs

The Troubleshooting / FAQs section provides users with solutions to common issues they might encounter while using the
package. This section provides users with solutions to common issues they might encounter while using the package. It's
important to provide users with solutions to common issues they might encounter while using the package, so they can
make informed decisions when using the package.

- Formatting: Markdown Cell
- Address common issues users might encounter.
- Provide solutions or workarounds.
- Link to issue trackers or support forums.


### 4.9 Conclusion and Next Steps

The Conclusion and Next Steps section wraps up the tutorial and provides guidance for further learning. This section
helps users solidify their understanding and shows them paths for continued exploration of the package.

- Formatting: Markdown Cell
- Summarize what was covered.
- Encourage further exploration.
- Suggest next steps:
    - Trying other features.
    - Reading more advanced tutorials.
    - Consulting the full documentation.
    - Contributing to the package.


## 5 Content Guidelines

The contents of a tutorial should be accessible, practical, and valuable to users. How the information is presented is 
crucial to ensure that it is easy to follow and understand. 


## 5.1 Define The Audience and Scope

**Target Audience:** The target audience will be the main user-base who be reading and using this tutorial.
- Typically, the tutorials' target audience will be those familiar with the Python Standard Library, popular packages,
  and possibly some of the dependencies.
- For packages, it should be assumed that the audience is familiar with the packages in the package and their
  dependencies.
- Depending on the goal of the tutorial, the target audience may be different.
- Tailor the language, complexity of examples, and depth of explanation to the intended audience.

**package Scope:** The scope clearly defines what this package does and what it *doesn't* do. 
- Consider how does this tutorial fits into the understanding of the broader package.

**Prerequisites:** The requirements in knowledge and resources required to complete the tutorial.
- The concepts of the broader package that are used in the package.
- Any advanced or obscure concepts of the Python Standard Library used in the package.
- The concepts of the dependencies which are used in the package.
- Any resources the user needs to import.


### 5.2 Language

The language used in package tutorials should be clear, accessible, and professional. Effective communication is crucial
for ensuring users can understand and implement the package's functionality. Follow these guidelines to maintain consistent
and user-friendly language throughout the tutorial:

- Polite, friendly, and approachable while still being clear, concise, and certain.
- Use simple, direct language. Avoid jargon where possible, or explain it if necessary.
- Keep sentences and paragraphs short.
- Use active voice.


### 5.3 Logical Flow

The logical flow of content is crucial for effective learning. A well-structured tutorial should progress naturally,
building upon previous concepts and maintaining a clear connection between topics.

- Organize topics from simple to complex.
- Ensure a smooth transition between sections.
- Each section should build upon the previous ones.


### 5.4 Markdown Cells

Markdown cells are essential for providing context, explanations, and documentation within the tutorial. They help break
up code sections, explain concepts, and guide users through the learning process. These cells should be well-formatted
and informative, making the tutorial easy to follow and understand.

- Introduce each code cell or group of related code cells with a Markdown cell.
- Explain the purpose of the code, not just a line-by-line translation.
- Use Markdown formatting (headings, lists, bold, italics, code highlighting) to improve readability.


### 5.5 Code Cells

Code cells are essential for demonstrating the functionality of the package. They provide a clear and concise way to
demonstrate the package's functionality and provide examples of how to use it.

- Every code cell must be runnable independently or in sequence.
- Ensure imports and variable initializations are correctly placed.
- Test all code cells thoroughly.
- Display Outputs: Ensure cell outputs are visible and illustrative. 
- For plots, make sure they render correctly in the notebook.


### 5.6 Self-Contained Examples

Self-contained examples are crucial for ensuring that users can run and understand the tutorial without external
dependencies or setup requirements. These examples should be complete, runnable units of code that demonstrate specific
functionality while being independent of external resources. This approach makes the tutorial more accessible and
reduces potential points of failure.

- Avoid reliance on external files or services if possible. If necessary, provide clear instructions on how to 
  obtain/set them up, or include mock data/objects directly in the notebook.
- For data, consider including a small CSV or generating data programmatically.
- If there are unit tests, use them as a reference but do not copy them exactly. The tutorial and examples should 
  educate the user on how to use key aspects of the package and how they can use it to create new programs, not just 
  test it.  


### 5.7 Error Handling Examples

The Error Handling Examples section demonstrates how to handle common errors and exceptions that users might encounter
while working with the package. This section helps users understand potential pitfalls and how to gracefully handle
error conditions, making their code more robust and maintainable. It is optional, but recommended.

- Show how to handle common exceptions or invalid inputs if relevant to the package's usage.


## 6 Formatting and Style

This section provides specific formatting and style guidelines to ensure consistency and readability. These conventions 
help create a professional and easily navigable document.


### 6.1 Headings

- Use `#` for the main title (H1).
- Use `##` for major sections (H2).
- Use `###` for sub-sections (H3), and so on.
- Be consistent with heading levels.


### 6.2 Code Blocks

- In Markdown cells, use backticks for inline code: `my_function()`.
- Use triple backticks for code blocks:
    ```python
    # your python code here
    ```
- Specify the language for syntax highlighting in Markdown code blocks (e.g., ` ```python`).


### 6.3 Emphasis

- Use `**bold**` for strong emphasis (e.g., key terms, warnings).
- Use `*italics*` for mild emphasis or for terms being defined.


### 6.4 Lists

- Use numbered lists for sequential steps.
- Use bulleted lists for non-sequential items or features.


### 6.5 Links

- Use descriptive text for hyperlinks:
    - Good: `[Read the full API documentation](link-to-docs)`
    - Avoid: `Click [here](link-to-docs)`


## 7 Tips for Effectiveness

This section provides practical recommendations for creating impactful and successful package tutorials. These tips help
ensure the tutorial achieves its educational goals while maintaining user engagement.

- **Start Simple:** Assume the user is a beginner with the package.
- **Build Complexity Gradually:** Don't overwhelm users with too much information at once.
- **Encourage Interaction:** Phrase explanations to invite users to try modifying the code.
- **Provide Context:** Explain *why* something is done, not just *how*.
- **Test Thoroughly:**
    - Run the entire notebook from start to finish in a clean kernel.
    - Have someone else go through the tutorial.
- **Keep it Updated:** As the package evolves, update the tutorial to reflect changes.
- **Clear Outputs Before Distribution (Usually):** Unless the outputs are essential for understanding without running (e.g., a complex plot that takes time to generate), it's often best to "Clear All Outputs" before distributing the `.ipynb` file. This reduces file size and allows users to generate outputs themselves. Alternatively, ensure all outputs are clean and directly relevant.

By following this style guide, you can create high-quality Jupyter Notebook tutorials that significantly enhance the user experience for your Python package.
