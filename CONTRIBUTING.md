# Contributing to Deixis Analysis Pipeline

Thank you for your interest in contributing to the Deixis Analysis Pipeline! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/deixis-analysis-pipeline.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit with clear messages: `git commit -m "Add: description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

1. Follow the installation instructions in README.md
2. Install development dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your API keys
4. Run tests: `pytest` (when available)

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Comment complex logic

## Adding New Features

### New Dilemmas
1. Add to `deixis_analysis_pipeline/input_questions/all_dilemmas_deictic_questions.json`
2. Follow the existing structure with all 9 deictic framings
3. Include ethical dimensions and trade-offs

### New Analysis Modules
1. Create module in appropriate directory
2. Follow existing patterns for integration
3. Update documentation
4. Add tests

### New Deictic Framings
1. Update transformer.py with new framing
2. Add to all existing dilemmas
3. Update analysis scripts to handle new framing
4. Document the linguistic features

## Testing

- Test with small datasets first
- Verify outputs match expected format
- Check for edge cases
- Monitor API costs during testing

## Documentation

- Update README.md for user-facing changes
- Update technical documentation for implementation changes
- Include examples where helpful
- Keep documentation in sync with code

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add a clear PR description explaining:
   - What changes were made
   - Why they were needed
   - How they were tested
4. Link any related issues
5. Be responsive to review feedback

## Reporting Issues

- Use GitHub Issues
- Include:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Python version)
  - Error messages/logs

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

- Open an issue for questions
- Tag with "question" label
- Check existing issues first

Thank you for contributing to advancing research in AI ethics and linguistics!