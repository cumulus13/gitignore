# gitignore

A simple script to generate a `.gitignore` file with default entries, additional entries, or templates from gitignore.io.  
It uses [rich](https://github.com/Textualize/rich) for console output and supports reading existing `.gitignore` files.

## Features

- Generate `.gitignore` with default and custom entries
- Fetch templates from [gitignore.io](https://www.toptal.com/developers/gitignore)
- Append or overwrite existing `.gitignore`
- Read and display `.gitignore` with syntax highlighting
- Rich colored output

## Installation

```bash
pip install .
```

## Usage

```bash
gitign [OPTIONS]
gitig [OPTIONS]
gitignore [OPTIONS]
```

### Options

- `-p, --path PATH` : Target directory (default: current)
- `-d, --data ENTRY` : Additional entry (can be repeated)
- `-t, --template TEMPLATE` : Use template from gitignore.io (e.g. python node java)
- `-a, --append` : Append to existing `.gitignore`
- `-f, --force` : Overwrite without prompt
- `-r, --read` : Read and display `.gitignore` file

### Example

```bash
gitign -t python,linux
gitig -d "*.env" -d "*.sqlite3"
gitignore -r
```

## License

MIT License. See [LICENSE](LICENSE).


## Author

[Hadi Cahyadi](mailto:cumulus13@gmail.com)

## Coffee

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)