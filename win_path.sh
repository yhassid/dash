get_win_path() {
  if command -v cygpath >/dev/null 2>&1; then
    # Cygwin: use cygpath to convert any path
    cygpath -w "$(pwd)"
  elif [[ "$PWD" =~ ^/([a-zA-Z])(/.*)? ]]; then
    # Git Bash: convert /c/... to C:/...
    drive_letter="${BASH_REMATCH[1]}"
    path_part="${BASH_REMATCH[2]}"
    echo "${drive_letter^^}:${path_part//\//\\/}"
  else
    # For paths like /usr/bin or /tmp in Git Bash, try using realpath with fallback
    if command -v realpath >/dev/null 2>&1; then
      win_path=$(realpath -m "$PWD")
      echo "$win_path"
    else
      echo "Unsupported path format in this environment: $PWD" >&2
      return 1
    fi
  fi
}