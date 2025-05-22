to_windows_path() {
  input_path="$1"

  if [[ -z "$input_path" ]]; then
    echo "Usage: to_windows_path <unix_path>" >&2
    return 1
  fi

  if command -v cygpath >/dev/null 2>&1; then
    # Cygwin: reliable conversion
    cygpath -w "$input_path"
  elif [[ "$input_path" =~ ^/([a-zA-Z])(/.*)? ]]; then
    # Git Bash or MSYS2 with /c/... style
    drive_letter="${BASH_REMATCH[1]}"
    path_part="${BASH_REMATCH[2]}"
    echo "${drive_letter^^}:${path_part//\//\\/}"
  else
    # Non-drive-rooted path (e.g., /tmp), try resolving full path
    if command -v realpath >/dev/null 2>&1; then
      abs_path=$(realpath -m "$input_path")
      if [[ "$abs_path" =~ ^/([a-zA-Z])(/.*)? ]]; then
        drive_letter="${BASH_REMATCH[1]}"
        path_part="${BASH_REMATCH[2]}"
        echo "${drive_letter^^}:${path_part//\//\\/}"
      else
        echo "Cannot convert path: $abs_path" >&2
        return 1
      fi
    else
      echo "Unsupported path format and 'realpath' not available." >&2
      return 1
    fi
  fi
}