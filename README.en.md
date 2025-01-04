# Frog

[简体中文](README.md) | English

A simple personal blog based on Flask. Write Markdown documents in a text editor, and Frog will automatically parse the directory structure and generate blog pages from the Markdown documents.

Supports categories, tags, comments, search, and RSS.

> [!WARNING]
> This project is currently under development. Only basic features have been completed, and many features are yet to be perfected.

![demo1](imgs/demo1.png)

![demo2](imgs/demo2.png)

## Running

```bash
> git clone https://github.com/GitZhiQing/Frog.git
> cd Frog
> uv sync # Install dependencies with uv
> flask initdb # Initialize the database
> flask run
```

> The GitHub webhook-based automatic document update feature is not yet completed. Therefore, you need to manually place your documents in the

docs

directory.

## Progress

- [x] Categories
- [x] Tags
- [x] Comments
- [ ] Search
- [ ] RSS
- [ ] GitHub Webhook Automatic Document Update

## Acknowledgements

The overall style is inspired by the WordPress [Twenty Twelve](https://wordpress.org/themes/twentytwelve/) theme.

Fonts:

- Chinese: [Noto Sans SC](https://fonts.google.com/specimen/Noto+Sans+SC)
- English: [Roboto](https://fonts.google.com/specimen/Roboto)
- Monospace: [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono)
