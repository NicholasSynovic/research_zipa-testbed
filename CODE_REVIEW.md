# CODE REVIEW

## Table of Contents

- [CODE REVIEW](#code-review)
  - [Table of Contents](#table-of-contents)
  - [Pre-Commit Checks](#pre-commit-checks)
    - [Bandit](#bandit)
    - [Flake 8](#flake-8)
  - [Project Documentation](#project-documentation)
  - [OOP Practices](#oop-practices)
  - [Software Engineering Patterns](#software-engineering-patterns)
  - [Software smells (i.e. spaghetti code, dead code, obfuscation)](#software-smells-ie-spaghetti-code-dead-code-obfuscation)
  - [Optimization](#optimization)

## Pre-Commit Checks

### Bandit

Bandit checks fail.

I recommend adding `# nosec` comments on lines that report errors for easier
refactoring/ identification later

### Flake 8

Most errors have to do with line length being greater than 79 (**E501**). These
can be ignored, assigned to a junior team member to resolve, or skipped with the
`# noqa: E501` comment on relevant lines

**F401** and **F403** (unused imports and using * to import code from modules)
should be resolved

**F405** (undefined functions) should be resolved

**F841** (unused variables) should be resolved

Othere errors revolve around styling. See **E501** recommended solution(s)

## Project Documentation

No `Makefile` or build script present. I suggest one to simplify the steps of
reproducing and testing the software

Diagrams, figures, detailed instructions, or a on how to setup the Zipa Testbed
system devices would be appreciated but not necessary at the moment

## OOP Practices

`eval_fastzip` and `eval_perceptio` have similar method declarations. I suggest
either an ABC (i.e *Evaluation*) that you can then define the minimum necessary
functions, and a *FastZip_Evaluator* and *Perceptio_Evaluator* to implement the
functions

`eval/schurmann` could be rewritten as an *Evaluator* class previously described

`eval/miettinen` could be rewritten as an *Evaluator* class previously described

`eval/miettinen` is very similar to `eval/schurmann`. Possible code duplication

## Software Engineering Patterns

There is duplicated code detected across files. Files often have method
definitions defined in other files. Consider condensing similar functions into a
single, parametric function

Consider abstracting different components of your test bed into well defined
classes. For example:

- An `Evaluator` interface and implementation classes
- A `Protocol` interface and implementation classes

Very little software patterns need to implemented at this time

## Software smells (i.e. spaghetti code, dead code, obfuscation)

Code duplication is prevelant throughout the project at this time. Consolidation
of code will be critical for quickly implementing and testing the system

Very little code documentation is prevelant. I strongly suggest leveraging
ChatGPT to generate code docs quickly. See
[this file](https://github.com/NicholasSynovic/research_ai-usage-in-science/blob/main/src/searchForPapers/main.py)
for example code docs

No type hints for parameters or return types for functions. Non-essential for
the code to run, but absolutely essential in providing context for others to
reuse your code. Leverage `mypy` to identify issues

Very littel dead code present. Leverage `vulture` to identify dead code

Copy-paste code (duplicate code) was identified with `CPD`. Migrate as much of
this code to a individual functions as possible

## Optimization

This will sound counter intuitive, but I suggest taking the week to clean up
your code base to promote reusability and composibility of objects. Individual
functions and scripts work for a single protocol, but it will make it hard to
scale and add additional protocols. Furthermore, if the standard in the field is
to make protocols difficult to reimplement, then you and your team should break
that by making the source code easy to leverage, reuse, and extend

Python is a notorously slow langauge. However, the `pypi` interpreter does offer
some performance benefits (occasionally). It is not a silver bullet however, and
benchmarking is necessary to confirm any improvements

Do not keep data files in source code directories. Move data files to a seperate
`data` directory outside of your source code so that it is both clearly defined
and easy to find

Look into Python project modularization with `poetry` it is the modern way to
create a python project and offers several improvements (typically faster builds
and dependency downloads) and the ability to easily identify dependency
versions, improving reproducibility across systems

Create a single global `.gitignore`. Start with
[GitHub's Python.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
file as it is the standard for open source Python projects
