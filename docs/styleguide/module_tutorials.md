# Anthony's Python Style Guide: Module Tutorials

## Table of Contents

- [1 Background](#1-background)
- [2 Jupyter Notebook](#2-jupyter-notebook)
- [3 Directory Hierarchy](#3-directory-hierarchy)
- [4 Module Tutorial Notebook Structure](#4-module-tutorial-notebook-structure)
  - [4.1 Title and Introduction](#41-title-and-introduction)
  - [4.2 Core Functionality](#42-core-functionality)
  - [4.3 Module Interaction](#43-module-interaction)
  - [4.4 Advanced Features](#44-advanced-features)
  - [4.5 Examples](#45-examples)
  - [4.6 API Highlights](#46-api-highlights)
  - [4.7 Troubleshooting / FAQs](#47-troubleshooting--faqs)
  - [4.8 Conclusion and Next Steps](#48-conclusion-and-next-steps)
- [5 Content Guidelines](#5-content-guidelines)
  - [5.1 Define The Audience and Scope](#51-define-the-audience-and-scope)
  - [5.2 Language](#52-language)
  - [5.3 Logical Flow](#53-logical-flow)
  - [5.4 Markdown Cells](#54-markdown-cells)
  - [5.5 Code Cells](#55-code-cells)
  - [5.6 Self-Contained Examples](#56-self-contained-examples)
  - [5.7 Error Handling Examples](#57-error-handling-examples)
- [6 Formatting and Style](#6-formatting-and-style)
  - [6.1 Headings](#61-headings)
  - [6.2 Code Blocks](#62-code-blocks)
  - [6.3 Emphasis](#63-emphasis)
  - [6.4 Lists](#64-lists)
  - [6.5 Links](#65-links)
- [7 Tips for Module Tutorial Effectiveness](#7-tips-for-module-tutorial-effectiveness)


## 1 Background

A tutorial is a step-by-step guide to a specific topic. It provides a clear and concise explanation of the topic, 
demonstrating the functionality and use cases. It is designed to be self-contained and easy to follow.
However, the purpose of a tutorial is to not only educate users on functionality but also provide inspiration for new 
approaches to solving problems.

This document provides specific guidelines for creating Jupyter Notebook tutorials focused on individual modules.

Unlike package-level tutorials, these module tutorials offer a more targeted approach, helping users understand the 
functionality, features, and use cases of specific modules. The guidelines cover how to define the audience and scope, 
structure the tutorial content, demonstrate module-specific functionality, show interactions with other modules, and 
present practical examples. By following these guidelines, developers can create focused, effective tutorials that help 
users leverage the full potential of individual modules within the larger package ecosystem.


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
- Related tutorials should be grouped together in the same directory
- Filenames should start with descriptive name followed by `_tutorial` (e.g., `name_tutorial.py`).
- Use the format `<component_name>_tutorial.py` for individual component tutorials
- For tutorials that demonstrate multiple components working together, use a descriptive name that indicates the functionality being demonstrated, e.g., `caching_with_sentinel_tutorial.py`
- Use lowercase with underscores for file names (snake_case)

Example:
```
tutorials/
  bases/                          # Tutorials for the bases package
    collections/                  # Tutorials for the bases.collections subpackage
      basedict_tutorial.py
    basecallable_tutorial.py
    sentinelobject_tutorial.py
  ...
  cachingtools/                 # Tutorials for the cachingtools package
    caches/                     # Tutorials for the cachingtools.caches subpackage
    cachingobject_tutorial.py
    ...
```


## 4 Module Tutorial Notebook Structure

Tutorial files should follow a consistent naming convention to make them easily identifiable:

- Use the format `<component_name>_tutorial.py` for individual module tutorials.
- Use lowercase with underscores for file names (snake_case)
- Avoid generic names like `tutorial.py` or `demo.py`

In a tutorial, a clear and logical flow is essential. These sections are recommended:

1. Title and Introduction
2. Core Functionality
3. Module Interactions
4. Advanced Features
5. Examples
6. API Highlights
7. Troubleshooting / FAQs
8. Conclusion and Next Steps


### 4.1 Title and Introduction

The Title and Introduction section sets the stage for the module's tutorial. It should provide users with a clear
understanding of what they will learn and how this module fits into the larger package ecosystem. This section serves as 
the entry point to the tutorial and should be engaging while remaining informative and concise.

- Formatting: Markdown Cell
- Clear Title: "Using the [ModuleName] Module in [PackageName]", "[ModuleName] for [Specific Task]", etc.
- Brief Overview: 
    - Explain the module's primary responsibilities and features.
    - Explain how this module relates to the parent package.
    - Explain what will be covered in this tutorial.
    - Briefly summarize the prerequisites.
- Table of Contents (Optional but Recommended): Markdown links to major sections within this module tutorial.


### 4.2 Core Functionality

The Core Functionality section introduces users to the fundamental features and capabilities of the module. This
section serves as the foundation for understanding how to use the module effectively by demonstrating its primary
functions and basic usage patterns.

- Formatting: Markdown and Code Cells
- Introduce the key functions, classes, and concepts specific to this module.
- Explain the key concepts of the module and how to use them.
- Explain the concepts behind complex functions, methods, and data structure interactions.  
- Provide simple, executable examples for each primary feature of the module.
- Explain each code cell:
    - What the code (from this module) does.
    - Explain the utility of the module and the code.
    - The expected output (and show it by running the cell).
- If the module has a central class, demonstrate its instantiation and methods.


### 4.3 Module Interaction

This section explores how the module interfaces with other components of the package ecosystem. It demonstrates the
module's role in larger workflows and how it can be integrated with other modules to achieve more complex functionality.

- Formatting: Markdown and Code Cells
- If this module is designed to work closely with other modules in the same package, demonstrate these interactions.
- Show how data or objects from this module can be used by, or accept input from, other parts of the package.


### 4.4 Advanced Features

The Advanced Features section delves into more sophisticated aspects of the module, presenting complex functionalities
and specialized use cases. This section is designed for users who have mastered the basics and are ready to explore the
module's full capabilities.

- Formatting: Markdown and Code Cells
- Cover more complex functionalities, configurations, or less common use cases specific to this module.
- Explain each feature in detail.
- Break down examples into understandable steps.


### 4.5 Examples

This section bridges the gap between theory and practice by presenting real-world applications of the module. Through
concrete examples and scenarios, users can better understand how to apply the module's features to solve actual
problems.

- Formatting: Markdown and Code Cells
- Showcase how this specific module solves particular problems or aids in specific tasks.
- Use relatable scenarios or small datasets relevant to the module's purpose.
- This helps users see the module's practical value.


### 4.6 API Highlights

The API Highlights section provides a curated overview of the module's most important API components. It serves as a
quick reference guide to the essential functions, classes, and methods that form the core of the module's interface.

- Formatting: Markdown Cell
- Briefly list key functions/classes within this module and their purpose.
- Link to the relevant section of the full API documentation for this module.


### 4.7 Troubleshooting / FAQs

This section addresses common challenges and questions that users might encounter while working with the module. It
provides solutions, workarounds, and best practices to help users overcome typical obstacles and optimize their use of
the module.

- Formatting: Markdown Cell
- Address common issues or questions specifically related to this module.
- Provide solutions or links to further help.


### 4.8 Conclusion and Next Steps

The Conclusion and Next Steps section wraps up the tutorial and provides guidance for further learning. This section
helps users solidify their understanding and shows them paths for continued exploration of the module and package.

- Formatting: Markdown Cell
- Summarize what was covered about the module.
- Encourage further exploration of the module's capabilities.
- Mention if there are more examples in the examples section of the project.
- Suggest next steps:
  - Trying other features of this module.
  - Exploring related modules in the package.
  - Consulting the full API documentation for the module.


## 5 Content Guidelines

The contents of a tutorial should be accessible, practical, and valuable to users. How the information is presented is 
crucial to ensure that it is easy to follow and understand.

### 5.1 Define The Audience and Scope

**Target Audience:** The target audience will be the main user-base who be reading and using this tutorial.
- Typically, the tutorials' target audience will be those familiar with the Python Standard Library, popular packages,
  and possibly some of the dependencies.
- For modules, it should be assumed that the audience is familiar with the modules in the package and their
  dependencies.
- Depending on the goal of the tutorial, the target audience may be different.
- Tailor the language, complexity of examples, and depth of explanation to the intended audience.

**Module Scope:** The scope clearly defines what this module does and what it *doesn't* do. 
- Consider how does this tutorial fits into the understanding of the broader package.

**Prerequisites:** The requirements in knowledge and resources required to complete the tutorial.
- The concepts of the broader package that are used in the module.
- Any advanced or obscure concepts of the Python Standard Library used in the module.
- The concepts of the dependencies which are used in the module.
- Any resources the user needs to import.


### 5.2 Language

The language used in module tutorials should be clear, accessible, and professional. Effective communication is crucial
for ensuring users can understand and implement the module's functionality. Follow these guidelines to maintain consistent
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
- Ensure top-to-bottom cell execution
- Each section should build upon the previous ones.


### 5.4 Markdown Cells

Markdown cells are essential for providing context, explanations, and documentation within the tutorial. They help break
up code sections, explain concepts, and guide users through the learning process. These cells should be well-formatted
and informative, making the tutorial easy to follow and understand.

- Introduce each code cell or group of related code cells with a Markdown cell.
- Explain the purpose of the code, not just a line-by-line translation.
- Use Markdown formatting (headings, lists, bold, italics, code highlighting) to improve readability.


### 5.5 Code Cells

Code cells are essential for demonstrating the functionality of the module. They provide a clear and concise way to
demonstrate the module's functionality and provide examples of how to use it.

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
  educate the user on how to use key aspects of the module and how they can use it to create new programs, not just 
  test it.  


### 5.7 Error Handling Examples

The Error Handling Examples section demonstrates how to handle common errors and exceptions that users might encounter
while working with the module. This section helps users understand potential pitfalls and how to gracefully handle
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

  
## 7 Tips for Module Tutorial Effectiveness

This section provides practical recommendations for creating impactful and successful module tutorials. These tips help
ensure your tutorial achieves its educational goals while maintaining user engagement.

- **Focus:** Keep the tutorial tightly focused on the functionalities of the specific module. Avoid extensive detours into other modules unless demonstrating direct interaction.
- **Context within Package:** Briefly remind users how this module fits into the overall architecture or purpose of the parent package.
- **Independence:** While part of a package, aim for the module tutorial to be as understandable as possible, even if a user jumps directly to it (though prerequisites should be stated).
- **Test Thoroughly:** Run in a clean kernel. Have someone unfamiliar with the module test it.
- **Keep Updated:** Module APIs can change. Ensure the tutorial reflects the current version of the module.


By adhering to this style guide, you can create clear, focused, and highly effective Jupyter Notebook tutorials for the 
individual modules within your Python packages, empowering users to leverage their full potential.
