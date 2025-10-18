# Contributing to Discord Bot Manager

First off, thank you for considering contributing to Discord Bot Manager! It's people like you that make this tool better for everyone.

## 🌟 Ways to Contribute

There are many ways to contribute to this project:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share your ideas for new functionality
- 📝 **Improve documentation** - Help others understand and use the project
- 🎨 **Design improvements** - Enhance the UI/UX experience
- 💻 **Code contributions** - Add features, fix bugs, or optimize performance
- 🧪 **Write tests** - Improve code quality and reliability
- 🌍 **Translations** - Help make the project multilingual
- 🔧 **DevOps improvements** - Enhance CI/CD, deployment, or development tools
- 🔒 **Security audits** - Help identify and fix security issues

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Git** (latest version)
- **A GitHub account**
- **Code editor** (VS Code, PyCharm, or similar)
- **Basic knowledge** of:
  - Python and async programming
  - Web development (HTML, CSS, JavaScript)
  - Discord bot development
  - Git workflow

### Setting Up Development Environment

1. **Fork the repository**
   - Click the 'Fork' button at the top right of the repository page
   - This creates your personal copy of the project

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/discord-bot-manager.git
   cd discord-bot-manager
   ```

3. **Add the original repository as upstream**
   ```bash
   git remote add upstream https://github.com/headx/discord-bot-manager.git
   ```

4. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

5. **Install development dependencies**
   ```bash
   # Install main dependencies
   pip install -r requirements.txt
   
   # Install development dependencies (uncomment in requirements.txt first)
   # pip install pytest black flake8 mypy
   ```

6. **Set up pre-commit hooks** (recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

7. **Create your feature branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   # or
   git checkout -b fix/bug-description
   ```
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a branch for your feature**
   ```bash
   git checkout -b feature/amazing-feature
   ```

6. **Make your changes**
   - Write your code
   - Test your changes
   - Update documentation if needed

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add some amazing feature"
   ```

8. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

9. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click 'New Pull Request'
   - Select your feature branch
   - Describe your changes
   - Submit the PR

## 📋 Code Style Guidelines

### Python

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes
- Use type hints where appropriate

Example:
```python
def create_bot(name: str, token: str, prefix: str = "!") -> dict:
    """
    Create a new Discord bot instance.
    
    Args:
        name: The name of the bot
        token: Discord bot token
        prefix: Command prefix (default: "!")
        
    Returns:
        dict: Bot configuration dictionary
    """
    return {
        "name": name,
        "token": token,
        "prefix": prefix
    }
```

### JavaScript

- Use 4 spaces for indentation
- Use semicolons
- Use camelCase for variables and functions
- Add JSDoc comments for functions
- Use ES6+ features where appropriate

Example:
```javascript
/**
 * Create a new bot instance
 * @param {string} name - Bot name
 * @param {string} token - Discord token
 * @returns {Object} Bot configuration
 */
function createBot(name, token) {
    return {
        name: name,
        token: token,
        createdAt: new Date()
    };
}
```

### HTML/CSS

- Use semantic HTML5 elements
- Use meaningful class names
- Follow BEM naming convention for CSS
- Keep styles modular and reusable
- Use CSS custom properties for theming

## 🧪 Testing

Before submitting a pull request:

1. **Test your changes manually**
   - Start the server
   - Test all affected features
   - Check for console errors

2. **Test on different browsers** (if UI changes)
   - Chrome/Edge
   - Firefox
   - Safari

3. **Test on different operating systems** (if possible)
   - Windows
   - Linux
   - macOS

4. **Write tests** (planned for future)
   ```python
   # Example test
   def test_create_bot():
       bot = create_bot("TestBot", "token123")
       assert bot["name"] == "TestBot"
       assert bot["token"] == "token123"
   ```

## 📝 Commit Message Guidelines

Write clear and descriptive commit messages:

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

Good ✅:
```
feat: Add dark mode toggle button

- Added toggle button in header
- Implemented dark mode styles
- Saved preference to localStorage

Closes #123
```

Bad ❌:
```
updated stuff
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - How to reproduce the issue
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Screenshots** - If applicable
6. **Environment**:
   - OS: [e.g., Windows 10, Ubuntu 20.04]
   - Python Version: [e.g., 3.9.5]
   - Browser: [e.g., Chrome 96]

Use the bug report template when creating an issue.

## 💡 Suggesting Features

When suggesting features, please include:

1. **Problem Description** - What problem does this solve?
2. **Proposed Solution** - How should it work?
3. **Alternatives** - Other approaches you've considered
4. **Additional Context** - Mockups, examples, etc.

Use the feature request template when creating an issue.

## 📖 Documentation

Good documentation is crucial! When contributing:

- Update README.md if you change functionality
- Add comments to complex code
- Update CHANGELOG.md
- Write clear commit messages
- Add JSDoc/docstrings to functions

## 🎨 UI/UX Guidelines

When making UI changes:

- Maintain consistency with existing design
- Follow the cosmic space theme
- Ensure responsive design (mobile-friendly)
- Test animations and transitions
- Consider accessibility (a11y)
- Maintain high contrast for readability

## ⚖️ Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism
- ✅ Focus on what's best for the community
- ✅ Show empathy towards others

- ❌ No harassment or discrimination
- ❌ No trolling or personal attacks
- ❌ No inappropriate behavior

## 📞 Getting Help

If you need help:

- 📖 Check the [documentation](README.md)
- 🔍 Search [existing issues](https://github.com/yourusername/discord-bot-manager/issues)
- 💬 Ask in the discussions section
- 📧 Contact the maintainers

## 🎯 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** if applicable
3. **Update CHANGELOG.md** with your changes
4. **Ensure code style** follows guidelines
5. **Test thoroughly** before submitting
6. **Write clear PR description**:
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
   - Screenshots (if UI changes)

### PR Review Process

- Maintainers will review your PR
- They may request changes
- Once approved, your PR will be merged
- Your contribution will be credited

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Appreciated by the community! 🎉

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for being awesome! 🌟

---

**Questions?** Feel free to reach out to the maintainers.

**Created with ❤️ by headx & the psychon**
