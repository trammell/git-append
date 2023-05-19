# `git-append`

A tool for appending files in git.

## Usage

To append file `foo` to file `bar`:






### Note on `.direnv` Configuration

To use the automatic `direnv` config for `poetry`:

```bash
layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
    log_error 'No pyproject.toml found. Use `poetry new` or `poetry init` to create one first.'
    exit 2
  fi

  # create venv if it doesn't exist
  poetry run true

  export VIRTUAL_ENV=$(poetry env info --path)
  export POETRY_ACTIVE=1
  PATH_add "$VIRTUAL_ENV/bin"
}

```

