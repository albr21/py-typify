# Contributing

Thanks for considering contributing to **py-typify**! Here’s how you can help:

## How to Contribute
1. **Fork** the repository
2. **Clone** your fork locally
3. Create a **new branch** for your feature or bug fix
4. Make your changes and **write tests** for them
5. Update the **manifest.yaml** to include your changes
5. **Commit** your changes with a descriptive message
6. Push your changes to your fork and create a **pull request**

## Issues
- If you find a bug or need a feature, please open an **issue**.
- Please search the issue tracker to avoid duplicates.

## Code Style
- Follow PEP 8 for Python code style
- Ensure that your code passes existing tests and includes new ones for new features or fixes

## Development Environment
- Use Python 3.8 or higher
- Install dependencies with `pip install -r requirements-dev.txt`

## File Architecture
- The main code is in the `typify` directory
- Tests are in the `test` directory

## Testing
Make sure your changes pass the tests. You can run the tests with:

```bash
pytest --cov="typify" --cov-report=term-missing
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License -- see the [LICENSE](LICENSE) file for details.
